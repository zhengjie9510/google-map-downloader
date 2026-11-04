# Google Map Downloader

English | [简体中文](README.md)

![Google Map Downloader](https://geospatialmedia.s3.amazonaws.com/wp-content/uploads/2016/07/google-earth.jpg)

Supports Google and Tianditu. Download map tiles for a specified geographic extent and zoom level, then merge them into a GeoTIFF with WGS 84 coordinates.

## Features

- Satellite, road, terrain, and label layers
- Google and Tianditu map services
- Automatic tile merging and geographic metadata
- Concurrent tile downloads

## Quick Start

Install [uv](https://docs.astral.sh/uv/), then run the following commands in the project directory:

```shell
uv sync
uv run python downloader_1.2.py
```

The script downloads a small example area and creates `example.tif` in the project directory.

Before using Google, open the [Google map service test](https://mts0.googleapis.com/vt?lyrs=s&x=1&y=1&z=1). If the browser displays a map tile, the service is reachable from your network. Otherwise, use Tianditu instead.

## Command-line Options

Specify the download area, zoom level, and output file on the command line:

```shell
uv run python downloader_1.2.py --left 100.361 --top 38.866 --right 100.386 --bottom 38.839 --zoom 13 --output example.tif --style s --server Google
```

Parameters:

| Parameter | Description |
| --- | --- |
| `--left`, `--top` | Longitude and latitude of the upper-left corner |
| `--right`, `--bottom` | Longitude and latitude of the lower-right corner |
| `--zoom` | Map zoom level; higher levels provide more detail and require more tiles |
| `--output` | Output GeoTIFF path |
| `--style` | Map style; see the table below |
| `--server` | Map service: `Google` or `Tianditu` |
| `--token` | Tianditu API token; required only when using Tianditu |

All options have example defaults. To see the complete help text:

```shell
uv run python downloader_1.2.py --help
```

Map styles:

| Value | Style |
| --- | --- |
| `m` | Road map |
| `s` | Satellite |
| `y` | Satellite with labels |
| `t` | Terrain |
| `p` | Terrain with labels |
| `h` | Labels |

## Using Tianditu

Request a token from the [Tianditu console](https://console.tianditu.gov.cn/), then pass it with `--token`:

```shell
uv run python downloader_1.2.py --server Tianditu --token YOUR_TOKEN --style y --zoom 13 --output tianditu.tif
```

Tianditu supports zoom levels up to 18. Styles with labels automatically combine the base map with the matching Chinese annotation layer.

## Script Versions

- `downloader_1.2.py`: Recommended. Uses a simpler implementation with concurrent downloads.
- `downloader_1.1.py`: Uses manually managed threads with progress output and retains WGS 84, Web Mercator, and GCJ-02 conversion utilities.

## Troubleshooting

If you encounter `Bad network link`, check whether your network can reach the map tile service. You can also try another `server` value.

When downloading and using map data, comply with the map provider's terms of service and applicable local laws.
