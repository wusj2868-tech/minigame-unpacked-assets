# 小游戏拆包资料库

原有四款塔防，已新增三国：冰河时代和无尽冬日；其余六款正在补传。按项目独立打包，每款一个ZIP，解压即可查看已有PNG/GIF/OBJ/JSON和原始资源；不用下载其他游戏。

**仓库为私有，查看和下载需要仓库权限。** 素材存放于GitHub Releases；仓库正文保留配置、工具、原始索引与清单。

## 分项目下载

目前6款已上传并完成服务端SHA256校验，另6款正在补传：寻道大千、咸鱼之王、小小蚁国、生存33天、镇邪人、疯狂水世界。

| 项目 | 版本 | 独立压缩包 | 大小 | 状态 |
|---|---|---|---:|---|
| 正中靶心 | 34.0 | [01-zhengzhongbaxin-v34.0-20261120.zip](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/01-zhengzhongbaxin-v34.0-20261120.zip) | 389.7 MB | 已上传、校验通过 |
| 向僵尸开炮 | 1.10 | [02-xiangjiangshikaipao-v1.10-20261120.zip](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/02-xiangjiangshikaipao-v1.10-20261120.zip) | 826.5 MB | 已上传、校验通过 |
| 永远的蔚蓝星球 | 3.0.5 | [03-blueplanet-v3.0.5-20261120.zip](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/03-blueplanet-v3.0.5-20261120.zip) | 1,170.0 MB | 已上传、校验通过 |
| 向末日开炮（补充） | 1.12 | [04-xiangmorikaipao-v1.12-20261120.zip](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/04-xiangmorikaipao-v1.12-20261120.zip) | 1,076.2 MB | 已上传、校验通过 |
| 三国：冰河时代 | 2.1.12.0 | [05-sanguobinghe-v2.1.12.0-20261120.zip](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/05-sanguobinghe-v2.1.12.0-20261120.zip) | 410.1 MB | 已上传、校验通过 |
| 无尽冬日 | 1.34.19 | [06-whiteout-survival-v1.34.19-20261120.zip](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/download/v2026.11.20/06-whiteout-survival-v1.34.19-20261120.zip) | 829.9 MB | 已上传、校验通过 |

[进入完整下载页](https://github.com/wusj2868-tech/minigame-unpacked-assets/releases/tag/v2026.11.20) · [项目清单与SHA256](catalog/projects.json) · [原始逐文件清单](catalog/files/)

GitHub自动生成的“Source code”压缩包只含仓库里的工具、配置和索引，**不含Release中的大体积素材**。请下载表中按游戏命名的ZIP。

新增八款将保留完整原包条目及本地已有的Rice配置、索引和报告；原包从Rice记录来源复取并验证SHA256一致。已有解析文件不代表Rice服务器整个work目录的全量镜像。

## 每款ZIP里有什么

- `游戏名/01_原始解压/`：原APK里的全部文件条目，保留assets、lib、res、DEX与Manifest等相对路径。没有重复塞入原APK安装包。
- `游戏名/02_可读素材导出/`：已实际导出的纹理、图集、精灵、动画帧/GIF、OBJ、骨骼/配置TextAsset和结构JSON；按来源资源包组织。
- `游戏名/03_已解析配置/` 或 `03_解析索引/`：现有数值配置与结构索引。
- `00_工具/`：Python解析、校验和长路径解压工具；`00_文件校验清单.csv`记录该ZIP内文件的SHA256。
- `00_开始使用.txt`、`00_目录.html`：当前项目的使用说明与入口。

每款ZIP独立完整，建议分别解压到不同目录。打开已导出的PNG、GIF、JSON不需要Rice账号，也不需要安装解析依赖。

## 已导出内容与边界

| 项目 | 直接可读内容 | 未恢复/格式说明 |
|---|---|---|
| 正中靶心 | 185张原始图像、2169张精灵PNG、374组动画（1558张PNG帧和374个GIF）、25份配置JSON、69包FGUI结构 | PNG是素材区域，FGUI界面组合与逻辑未重建；GIF是资源预览 |
| 向僵尸开炮 | 3212张PNG、1031份TextAsset、1430份动画结构JSON、4671份材质JSON、214份OBJ | 17个零尺寸字体纹理没有静态像素；OBJ不保留绑定动画 |
| 永远的蔚蓝星球 | 33227份原始文件、构建索引及单位/特效清点 | **核心Unity容器保护尚未恢复，不能把原始.single/.folder当成已解码PNG或完整Spine工程** |
| 向末日开炮（补充） | 4341张PNG、3250份TextAsset、368份动画结构JSON、2294份材质JSON、2262份OBJ | 768个AB中767个完成读取；1个登录背景容器未额外解码，原文件保留；浮点纹理以数据形式保存 |

这些是导出文件/对象数，包含部件和变体，不等于独立角色或技能数量。原始二进制配置并非全部已还原为JSON；OBJ是几何，不是完整可运行工程。

## 命令行按项目下载（可选）

已安装并登录GitHub CLI、且有仓库权限时：

```bash
python download_projects.py --list
python download_projects.py --game 01
python download_projects.py --game 02 --extract
python download_projects.py --game all --extract --remove-zip
```

脚本会验证整包SHA256；解压启用时再核对文件CRC。`--remove-zip`只在校验、解压成功后删除下载副本。桌面上原先的总包不受影响。

## 校验与重新导出

每个项目ZIP都附逐文件SHA256清单，可用其中的工具独立校验。解析工具支持普通Unity Bundle、已验证的末日0xef35变体，以及靶心Cocos/FGUI；不宣称支持蔚蓝核心容器解密。

```bash
python "00_工具/verify_share.py" "项目压缩包.zip"
python -m pip install -r "00_工具/requirements.txt"
```

详细格式说明见各项目ZIP内的`00_开始使用.txt`与`_导出总表.json`。原始条目逐项来自已校验的桌面总包；项目ZIP另外保留自己的SHA256及服务端校验结果。

## 存储方式

大素材使用Releases，每款一个小于2 GiB的独立ZIP；说明、工具、索引及现有配置保留在Git仓库中。[GitHub大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) · [Releases大小限制](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)

资料版本与清点日期：2026-11-20。
