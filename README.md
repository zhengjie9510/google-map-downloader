# Google Map Downloader

[English](README_EN.md) | 简体中文

![Google Map Downloader](https://geospatialmedia.s3.amazonaws.com/wp-content/uploads/2016/07/google-earth.jpg)

根据经纬度范围和缩放等级下载 Google 地图瓦片，并合成为带有 WGS 84 坐标信息的 GeoTIFF 文件。

## 功能

- 支持卫星图、道路图、地形图和标注图层
- 支持 Google 与 Google China 地图服务
- 自动拼接瓦片并写入地理坐标信息
- 使用多进程和多线程提高下载速度

## 快速开始

安装 [uv](https://docs.astral.sh/uv/) 后，在项目目录运行：

```shell
uv sync
uv run python downloader_1.2.py
```

脚本会下载一个小范围示例，并在项目目录生成 `example.tif`。

## 命令行参数

通过命令行指定下载范围、缩放等级和输出文件：

```shell
uv run python downloader_1.2.py --left 100.361 --top 38.866 --right 100.386 --bottom 38.839 --zoom 13 --output example.tif --style s --server Google
```

参数说明：

| 参数 | 说明 |
| --- | --- |
| `--left`, `--top` | 下载区域左上角的经纬度 |
| `--right`, `--bottom` | 下载区域右下角的经纬度 |
| `--zoom` | 地图缩放等级，等级越高分辨率越高、瓦片越多 |
| `--output` | 输出 GeoTIFF 文件路径 |
| `--style` | 地图样式，见下表 |
| `--server` | 地图服务：`Google` 或 `Google China` |

所有参数都有示例默认值。查看完整帮助：

```shell
uv run python downloader_1.2.py --help
```

地图样式：

| 值 | 样式 |
| --- | --- |
| `m` | 道路图 |
| `s` | 卫星图 |
| `y` | 带标注的卫星图 |
| `t` | 地形图 |
| `p` | 带标注的地形图 |
| `h` | 标注图层 |

## 脚本版本

- `downloader_1.2.py`：推荐使用，多进程与多线程下载。
- `downloader_1.1.py`：早期版本，使用多线程下载并显示进度。

## 常见问题

如果出现 `Bad network link`，通常是当前网络无法访问地图瓦片服务。请先检查网络连接，也可以尝试切换 `server`。

下载和使用地图数据时，请遵守相应地图服务的使用条款以及当地法律法规。
