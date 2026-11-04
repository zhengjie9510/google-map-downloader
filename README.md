# Google Map Downloader

[English](README_EN.md) | 简体中文

![Google Map Downloader](https://geospatialmedia.s3.amazonaws.com/wp-content/uploads/2016/07/google-earth.jpg)

支持 Google 和天地图。根据经纬度范围与缩放等级下载地图瓦片，并合成为带有 WGS 84 坐标信息的 GeoTIFF 文件。

## 功能

- 支持卫星图、道路图、地形图和标注图层
- 支持 Google 与天地图服务
- 自动拼接瓦片并写入地理坐标信息
- 并发下载地图瓦片

## 快速开始

安装 [uv](https://docs.astral.sh/uv/) 后，在项目目录运行：

```shell
uv sync
uv run python downloader_1.2.py
```

脚本会下载一个小范围示例，并在项目目录生成 `example.tif`。

使用 Google 前，可以打开 [Google 地图服务测试链接](https://mts0.googleapis.com/vt?lyrs=s&x=1&y=1&z=1)。如果浏览器能显示地图瓦片，说明当前网络可以访问；如果无法打开，请改用天地图。

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
| `--server` | 地图服务：`Google` 或 `Tianditu` |
| `--token` | 天地图 API Token，仅使用天地图时需要 |

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

## 使用天地图

先在[天地图控制台](https://console.tianditu.gov.cn/)申请 Token，然后通过 `--token` 传入：

```shell
uv run python downloader_1.2.py --server Tianditu --token YOUR_TOKEN --style y --zoom 13 --output tianditu.tif
```

天地图最高支持 zoom 18；带标注的样式会自动合成底图和对应的中文注记图层。

## 脚本版本

- `downloader_1.2.py`：推荐使用，代码更简洁，并发下载瓦片。
- `downloader_1.1.py`：使用手动管理的多线程下载并显示进度，同时保留 WGS 84、Web Mercator 和 GCJ-02 坐标转换工具。

## 常见问题

如果出现 `Bad network link`，通常是当前网络无法访问地图瓦片服务。请先检查网络连接，也可以尝试切换 `server`。

下载和使用地图数据时，请遵守相应地图服务的使用条款以及当地法律法规。
