"""Download map tiles and save them as a georeferenced TIFF."""

import argparse
import io
import math
import os
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import rasterio
from PIL import Image
from rasterio.transform import from_bounds


MAX_LATITUDE = 85.0511287798
TILE_SIZE = 256
DOWNLOAD_RETRIES = 3
DOWNLOAD_TIMEOUT = 20
DEFAULT_WORKERS = min(32, (os.cpu_count() or 1) * 4)

GOOGLE_URL = "https://mts0.googleapis.com/vt?lyrs={style}&x={x}&y={y}&z={z}"
TIANDITU_LAYERS = {
    "m": ("vec", "cva"),
    "s": ("img",),
    "y": ("img", "cia"),
    "t": ("ter",),
    "p": ("ter", "cta"),
    "h": ("cva",),
}
STYLE_NAMES = {
    "m": "map",
    "s": "satellite",
    "y": "satellite with labels",
    "t": "terrain",
    "p": "terrain with labels",
    "h": "labels",
}
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.tianditu.gov.cn/",
}


def coordinates_to_tile(longitude, latitude, zoom):
    """Return the XYZ tile containing a WGS 84 coordinate."""
    latitude = max(-MAX_LATITUDE, min(MAX_LATITUDE, latitude))
    tile_count = 2 ** zoom
    x = math.floor((longitude + 180) / 360 * tile_count)
    latitude_radians = math.radians(latitude)
    y = math.floor(
        (1 - math.asinh(math.tan(latitude_radians)) / math.pi)
        / 2
        * tile_count
    )
    return x, y


def tile_to_coordinates(x, y, zoom):
    """Return the WGS 84 coordinate at the top-left corner of an XYZ tile."""
    tile_count = 2 ** zoom
    longitude = x / tile_count * 360 - 180
    latitude = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / tile_count))))
    return longitude, latitude


def get_tile_grid(left, top, right, bottom, zoom):
    """Return the inclusive tile bounds covering the requested area."""
    first_x, first_y = coordinates_to_tile(left, top, zoom)
    last_x, last_y = coordinates_to_tile(right, bottom, zoom)
    return first_x, first_y, last_x, last_y


def build_google_urls(style, x, y, zoom):
    return (GOOGLE_URL.format(style=style, x=x, y=y, z=zoom),)


def build_tianditu_urls(style, x, y, zoom, token):
    urls = []
    for layer in TIANDITU_LAYERS[style]:
        params = urllib.parse.urlencode({
            "SERVICE": "WMTS",
            "REQUEST": "GetTile",
            "VERSION": "1.0.0",
            "LAYER": layer,
            "STYLE": "default",
            "TILEMATRIXSET": "w",
            "FORMAT": "tiles",
            "TILEMATRIX": zoom,
            "TILEROW": y,
            "TILECOL": x,
            "tk": token,
        })
        node = (x + y) % 8
        urls.append(f"https://t{node}.tianditu.gov.cn/{layer}_w/wmts?{params}")
    return tuple(urls)


def build_tile_urls(server, style, x, y, zoom, token=None):
    """Return one or more source URLs needed to render a tile."""
    if server == "Google":
        return build_google_urls(style, x, y, zoom)
    return build_tianditu_urls(style, x, y, zoom, token)


def fetch_url(url):
    """Download one URL, retrying transient failures."""
    request = urllib.request.Request(url, headers=REQUEST_HEADERS)
    last_error = None

    for _ in range(DOWNLOAD_RETRIES):
        try:
            with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT) as response:
                return response.read()
        except Exception as error:
            last_error = error

    host = urllib.parse.urlsplit(url).netloc
    raise RuntimeError(
        f"Failed to download tile from {host} after {DOWNLOAD_RETRIES} attempts."
    ) from last_error


def download_tile(urls):
    """Download and combine all layers for one tile."""
    layers = [Image.open(io.BytesIO(fetch_url(url))).convert("RGBA") for url in urls]
    tile = layers[0]
    for layer in layers[1:]:
        tile = Image.alpha_composite(tile, layer)
    return tile


def download_tiles(tile_urls, workers=DEFAULT_WORKERS):
    """Download tiles concurrently while preserving their original order."""
    worker_count = min(workers, len(tile_urls))
    print(f"Downloading {len(tile_urls)} tiles with {worker_count} workers...")
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        tiles = list(executor.map(download_tile, tile_urls))
    print("Tiles downloaded")
    return tiles


def merge_tiles(tiles, columns, rows):
    """Combine downloaded tiles into one RGB image."""
    result = Image.new("RGB", (columns * TILE_SIZE, rows * TILE_SIZE))
    for index, tile in enumerate(tiles):
        x = index % columns
        y = index // columns
        result.paste(tile.convert("RGB"), (x * TILE_SIZE, y * TILE_SIZE))
    return result


def save_geotiff(image, output_path, tile_grid, zoom):
    """Save an image as a three-band WGS 84 GeoTIFF."""
    first_x, first_y, last_x, last_y = tile_grid
    west, north = tile_to_coordinates(first_x, first_y, zoom)
    east, south = tile_to_coordinates(last_x + 1, last_y + 1, zoom)
    transform = from_bounds(west, south, east, north, image.width, image.height)
    bands = np.asarray(image).transpose(2, 0, 1)

    with rasterio.open(
        output_path,
        "w",
        driver="GTiff",
        width=image.width,
        height=image.height,
        count=3,
        dtype=bands.dtype,
        crs="EPSG:4326",
        transform=transform,
    ) as output:
        output.write(bands)


def validate_options(left, top, right, bottom, zoom, server, token):
    if not -180 <= left < right <= 180:
        raise ValueError("Longitude must satisfy -180 <= left < right <= 180.")
    if not -MAX_LATITUDE <= bottom < top <= MAX_LATITUDE:
        raise ValueError(
            f"Latitude must satisfy {-MAX_LATITUDE} <= bottom < top <= {MAX_LATITUDE}."
        )
    if not 0 <= zoom <= 22:
        raise ValueError("Zoom must be between 0 and 22.")
    if server == "Tianditu" and not token:
        raise ValueError(
            "Tianditu requires --token or the TIANDITU_TOKEN environment variable."
        )
    if server == "Tianditu" and zoom > 18:
        raise ValueError("Tianditu supports zoom levels from 0 to 18.")


def main(left, top, right, bottom, zoom, output_path, style="s", server="Google", token=None):
    """Download a map covering the requested WGS 84 extent."""
    validate_options(left, top, right, bottom, zoom, server, token)
    tile_grid = get_tile_grid(left, top, right, bottom, zoom)
    first_x, first_y, last_x, last_y = tile_grid
    columns = last_x - first_x + 1
    rows = last_y - first_y + 1

    print(f"Area covers {columns} x {rows} tiles")
    tile_urls = [
        build_tile_urls(server, style, x, y, zoom, token)
        for y in range(first_y, last_y + 1)
        for x in range(first_x, last_x + 1)
    ]
    tiles = download_tiles(tile_urls)
    image = merge_tiles(tiles, columns, rows)
    save_geotiff(image, output_path, tile_grid, zoom)
    print(f"Saved {output_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Download map tiles as a GeoTIFF.")
    parser.add_argument("--left", type=float, default=100.361, help="Left longitude.")
    parser.add_argument("--top", type=float, default=38.866, help="Top latitude.")
    parser.add_argument("--right", type=float, default=100.386, help="Right longitude.")
    parser.add_argument("--bottom", type=float, default=38.839, help="Bottom latitude.")
    parser.add_argument("--zoom", type=int, default=13, help="Map zoom level.")
    parser.add_argument("--output", default="example.tif", help="Output GeoTIFF path.")
    parser.add_argument("--style", choices=STYLE_NAMES, default="s", help="Map style: " + ", ".join(f"{key}={value}" for key, value in STYLE_NAMES.items()))
    parser.add_argument("--server", choices=("Google", "Tianditu"), default="Google", help="Map server.")
    parser.add_argument("--token", default=os.getenv("TIANDITU_TOKEN"), help="Tianditu API token.")
    args = parser.parse_args()
    try:
        validate_options(args.left, args.top, args.right, args.bottom, args.zoom, args.server, args.token)
    except ValueError as error:
        parser.error(str(error))
    return args


if __name__ == "__main__":
    args = parse_args()
    started_at = time.time()
    main(args.left, args.top, args.right, args.bottom, args.zoom, args.output, args.style, args.server, args.token)
    print(f"Finished in {time.time() - started_at:.2f} seconds")
