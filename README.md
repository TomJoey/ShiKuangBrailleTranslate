# ShiKuang Braille Translate 师旷中文盲文翻译（NVDA 插件）

在盲文点显器上显示**中文盲文**：汉字转拼音、分词连写，支持国家通用盲文、汉语双拼盲文、汉语表意盲文。
Chinese Braille translator for NVDA braille displays (Mandarin, pinyin, Braille translate).

名字取自春秋时期的盲人乐师师旷。翻译由 BWordX 引擎完成。

## 使用
1. 安装 `.nvda-addon`。
2. NVDA 设置 → 盲文 → 输出表，选“师旷 中文盲文（国家通用盲文）”“师旷 汉语双拼盲文”或“师旷 汉语表意盲文”。

## 本仓库内容
只有插件的 Python 源码（`globalPlugins/`）、占位表（`brailleTables/`）和打包脚本（`build.py`）。
翻译引擎是 `braille_ffi.dll`（32 位 / 64 位各一个，放在安装包的 `lib/x86`、`lib/x64`），不在本仓库里。

插件把 NVDA 的 `louisHelper.translate` 换成对引擎的调用；任何出错都退回 liblouis 自带的 `zh-chn` 表。
