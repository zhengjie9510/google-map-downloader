# Google Map Downloader

English | [简体中文](README.md)

![Google Map Downloader](https://geospatialmedia.s3.amazonaws.com/wp-content/uploads/2016/07/google-earth.jpg)

Download Google Maps tiles for a specified geographic extent and zoom level, then merge them into a GeoTIFF with WGS 84 coordinates.

## Features

- Satellite, road, terrain, and label layers
- Google and Google China map services
- Automatic tile merging and geographic metadata
- Multiprocessing and multithreading for faster downloads

## Quick Start

Install [uv](https://docs.astral.sh/uv/), then run the following commands in the project directory:

```shell
uv sync
uv run python downloader_1.2.py
```

The script downloads a small example area and creates `example.tif` in the project directory.

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
| `--server` | Map service: `Google` or `Google China` |

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

## Script Versions

- `downloader_1.2.py`: Recommended. Uses multiprocessing and multithreading.
- `downloader_1.1.py`: Earlier version. Uses multithreading and displays progress.

## Troubleshooting

If you encounter `Bad network link`, check whether your network can reach the map tile service. You can also try another `server` value.

When downloading and using map data, comply with the map provider's terms of service and applicable local laws.
