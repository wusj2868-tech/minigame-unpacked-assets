# 小游戏拆包资料库

共12款，按游戏独立打包。包括正中靶心、向僵尸开炮、永远的蔚蓝星球、向末日开炮，以及新增的三国：冰河时代、无尽冬日、寻道大千、咸鱼之王、小小蚁国、生存33天、镇邪人、疯狂水世界。

**公开仓库，可直接分享下载链接，无需邀请协作者。** 大文件存放于Releases，配置、报告、工具和校验清单可直接在仓库浏览。

## 分项目下载

12款全部上传完成，整包SHA256已与GitHub服务端摘要逐一核对。下载某一款无需下载其他游戏。

| 项目 | 版本 | 独立ZIP | 大小 | 原始文件与已有解析 |
|---|---|---|---:|---|
| 01 正中靶心 | 34.0 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/01-zhengzhongbaxin-v34.0-20261120.zip) | 389.7 MB | 完整原始条目＋已导出素材/配置 |
| 02 向僵尸开炮 | 1.10 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/02-xiangjiangshikaipao-v1.10-20261120.zip) | 826.5 MB | 完整原始条目＋已导出素材/配置 |
| 03 永远的蔚蓝星球 | 3.0.5 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/03-blueplanet-v3.0.5-20261120.zip) | 1,170.0 MB | 完整原始条目＋已导出素材/配置 |
| 04 向末日开炮（补充） | 1.12 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/04-xiangmorikaipao-v1.12-20261120.zip) | 1,076.2 MB | 完整原始条目＋已导出素材/配置 |
| 05 三国：冰河时代 | 2.1.12.0 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/05-sanguobinghe-v2.1.12.0-20261120.zip) | 410.1 MB | 完整原始条目＋57份已有配置/索引/报告 |
| 06 无尽冬日 | 1.34.19 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/06-whiteout-survival-v1.34.19-20261120.zip) | 829.9 MB | 完整原始条目＋1份已有配置/索引/报告 |
| 07 寻道大千 | 3.2.00 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/07-xundaodaqian-v3.2.00-20261120.zip) | 619.9 MB | 完整原始条目＋7份已有配置/索引/报告 |
| 08 咸鱼之王 | 0.36.0 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/08-xianyuzhiwang-v0.36.0-20261120.zip) | 530.4 MB | 完整原始条目＋7份已有配置/索引/报告 |
| 09 小小蚁国 | 3.0.60 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/09-the-ants-v3.0.60-20261120.zip) | 259.4 MB | 完整原始条目＋23份已有配置/索引/报告 |
| 10 生存33天 | 1.0.26 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/10-survival33-v1.0.26-20261120.zip) | 1,390.2 MB | 完整原始条目＋4份已有配置/索引/报告 |
| 11 镇邪人 | 1.0.3 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/11-zhenxieren-v1.0.3-20261120.zip) | 112.9 MB | 完整原始条目＋1份已有配置/索引/报告 |
| 12 疯狂水世界 | 1.4.4 | [下载](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/12-flotshelter-v1.4.4-20261120.zip) | 587.6 MB | 完整原始条目＋3份已有配置/索引/报告 |

[完整下载页](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/tag/v2026.11.20) · [项目清单与SHA256](catalog/projects.json) · [逐文件清单](catalog/files/)

GitHub自动生成的“Source code”压缩包只包含Git仓库文件。请下载上表的项目ZIP以获得完整原始资源。

## 新增八款的内容说明

05—12号项目均含原APK/XAPK的完整展开条目，保留assets、lib、res、DEX等路径，XAPK内的split APK也已展开。原包从Rice任务记录的同一来源重新下载，SHA256与Rice记录一致。

另附本地已保存的Rice配置、资产索引与身份核验后的报告。这些已有解析成果**不是Rice服务器整个work目录的全量镜像**；文件数量见表，服务端报告中的路径用于溯源，不表示每个路径均已单独导出。

- `01_原始解压/`：完整原始条目，包括未解密的容器，可继续解析。
- `02_已解配置与索引/`：已有的可读配置和索引，可直接打开。
- `03_Rice报告/report.json`：对应游戏与包版本的已有报告。
- `00_工具/`、`00_开始使用.txt`、`00_文件校验清单.csv`：使用说明、通用解析与逐文件SHA256校验工具。

没有将原始容器当成已解码的PNG、模型或动画工程；各产品已解程度不同。无尽冬日受保护的核心资源仍未完整恢复。无尽冬日为全球APP包，疯狂水世界也为全球包，不能直接当作国内微信小游戏同版配置。

## 已导出内容与边界

| 项目 | 直接可读内容 | 未恢复/格式说明 |
|---|---|---|
| 正中靶心 | 185张原始图像、2169张精灵PNG、374组动画（1558张PNG帧和374个GIF）、25份配置JSON、69包FGUI结构 | PNG是素材区域，FGUI界面组合与逻辑未重建；GIF是资源预览 |
| 向僵尸开炮 | 3212张PNG、1031份TextAsset、1430份动画结构JSON、4671份材质JSON、214份OBJ | 17个零尺寸字体纹理没有静态像素；OBJ不保留绑定动画 |
| 永远的蔚蓝星球 | 33227份原始文件、构建索引及单位/特效清点 | **核心Unity容器保护尚未恢复，不能把原始.single/.folder当成已解码PNG或完整Spine工程** |
| 向末日开炮（补充） | 4341张PNG、3250份TextAsset、368份动画结构JSON、2294份材质JSON、2262份OBJ | 768个AB中767个完成读取；1个登录背景容器未额外解码，原文件保留；浮点纹理以数据形式保存 |


以上素材数包含部件与变体，不等于独立角色或技能数量。原始二进制配置并非全部已还原为JSON；OBJ是几何，不是带完整动画绑定的可运行工程。

## 命令行按项目下载（可选）

可直接在浏览器下载；需要批量下载时可使用GitHub CLI：

```bash
python download_projects.py --list
python download_projects.py --game 01
python download_projects.py --game 05 --extract
python download_projects.py --game 07 --extract
python download_projects.py --game all --extract --remove-zip
```

脚本会验证整包SHA256；解压启用时再核对文件CRC。`--remove-zip`只在校验、解压成功后删除下载副本。桌面上原先的总包不受影响。

## 校验与重新导出

每个项目ZIP都附逐文件SHA256清单，可用其中的工具独立校验。解析工具支持普通Unity Bundle、已验证的末日0xef35变体，以及靶心Cocos/FGUI；不宣称支持蔚蓝核心容器解密。

```bash
python "00_工具/verify_share.py" "项目压缩包.zip"
python -m pip install -r "00_工具/requirements.txt"
```

详细格式说明见各项目ZIP内的`00_开始使用.txt`与`_导出总表.json`。01—04号原始条目来自已校验的桌面总包；05—12号原包与Rice记录SHA256一致。全部ZIP均已逐文件读回校验，并核对GitHub服务端整包SHA256。

## 存储方式

大素材使用Releases，每款一个小于2 GiB的独立ZIP；说明、工具、索引及现有配置保留在Git仓库中。[GitHub大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) · [Releases大小限制](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)

资料版本与清点日期：2026-11-20。
