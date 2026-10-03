# 第三方许可声明 / Third-party notices

本插件（Python 源码）以 **GNU GPL v2** 发布（见 `LICENSE`）。安装包里另带两类二进制内容：翻译引擎 `braille_ffi.dll`（BWordX，TomJoey）和压缩加密过的数据文件 `lib/data/`。它们用到了下列第三方成果，许可证各自适用。

## 数据来源

| 数据 | 用途 | 来源与许可 |
|---|---|---|
| pinyin-data | 汉字读音（字库） | mozillazg/pinyin-data，MIT，Copyright (c) 2016 mozillazg。https://github.com/mozillazg/pinyin-data |
| phrase-pinyin-data | 词组读音（词库） | mozillazg/phrase-pinyin-data，MIT，Copyright (c) 2017 mozillazg。https://github.com/mozillazg/phrase-pinyin-data |
| CC-CEDICT | 轻声词表（`phrases_neutral`，从中提取“哪些词里哪个音节读轻声”） | Copyright 1997- Paul Andrew Denisowski 及 CC-CEDICT 贡献者，CC BY-SA 4.0。https://www.mdbg.net/chinese/dictionary?page=cc-cedict ；https://creativecommons.org/licenses/by-sa/4.0/ |
| liblouis 盲文表 | 外文盲文（`louis_tables.zip`，由 liblouis 的表转换成数据，由 BWordX 自己的代码解释，运行时不使用 liblouis 程序） | liblouis 项目，表文件为 LGPL-2.1 或更新版本，各表头部保留了原版权和来源。https://github.com/liblouis/liblouis |
| jieba 分词词典 | 分词连写 | jieba-rs 自带，MIT |
| 中国盲文标准与方案 | 盲文规则（GB/T 18028、《中国盲文》、GF0019-2018、汉语双拼盲文、汉语表意盲文方案等） | 规则内容依据相应标准和方案原文整理，不含其原文版式。以各标准的著作权为准。 |

### 关于数据文件加密
`lib/data/` 里的数据文件经过压缩并加密，只是为了缩小体积、防止直接复制文件。上表中 CC BY-SA 和 LGPL 的部分，**原始数据都可以从上面给出的原项目地址取得**，你可以按原许可证自行使用和修改。

## Rust 依赖（编进 `braille_ffi.dll`，含编译期依赖）

| 库 | 版本 | 许可证 |
|---|---|---|
| adler2 | 2.0.1 | 0BSD OR MIT OR Apache-2.0 |
| adler32 | 1.2.0 | Zlib |
| aead | 0.5.2 | MIT OR Apache-2.0 |
| allocator-api2 | 0.2.21 | MIT OR Apache-2.0 |
| block-buffer | 0.10.4 | MIT OR Apache-2.0 |
| bytecount | 0.6.9 | Apache-2.0/MIT |
| cc | 1.4.7 | MIT OR Apache-2.0 |
| cfg-if | 1.0.5 | MIT OR Apache-2.0 |
| chacha20 | 0.9.1 | Apache-2.0 OR MIT |
| chacha20poly1305 | 0.10.1 | Apache-2.0 OR MIT |
| chardetng | 1.0.0 | Apache-2.0 OR MIT |
| cipher | 0.4.4 | MIT OR Apache-2.0 |
| core_detect | 1.0.0 | MIT/Apache-2.0 |
| cpufeatures | 0.2.17 | MIT OR Apache-2.0 |
| crc32fast | 1.5.2 | MIT OR Apache-2.0 |
| crypto-common | 0.1.7 | MIT OR Apache-2.0 |
| dary_heap | 0.3.9 | MIT OR Apache-2.0 |
| digest | 0.10.7 | MIT OR Apache-2.0 |
| encoding_rs | 0.8.42 | (Apache-2.0 OR MIT) AND BSD-3-Clause |
| equivalent | 1.0.2 | Apache-2.0 OR MIT |
| find-msvc-tools | 0.1.13 | MIT OR Apache-2.0 |
| foldhash | 0.2.0 | Zlib |
| generic-array | 0.14.7 | MIT |
| getrandom | 0.2.17 | MIT OR Apache-2.0 |
| getrandom | 0.4.3 | MIT OR Apache-2.0 |
| hashbrown | 0.16.1 | MIT OR Apache-2.0 |
| include-flate | 0.3.4 | Apache-2.0 |
| include-flate-codegen | 0.3.4 | Apache-2.0 |
| include-flate-compress | 0.3.4 | Apache-2.0 |
| inout | 0.1.4 | MIT OR Apache-2.0 |
| itoa | 1.0.18 | MIT OR Apache-2.0 |
| jieba-macros | 0.11.0 | MIT |
| jieba-rs | 0.11.0 | MIT |
| jobserver | 0.1.35 | MIT OR Apache-2.0 |
| libflate | 2.3.2 | MIT |
| libflate_lz77 | 2.3.0 | MIT |
| memchr | 2.8.3 | Unlicense OR MIT |
| miniz_oxide | 0.8.9 | MIT OR Zlib OR Apache-2.0 |
| multiversion_no_op | 1.0.0 | Apache-2.0 OR MIT |
| no_std_io2 | 0.9.4 | Apache-2.0 OR MIT |
| opaque-debug | 0.3.1 | MIT OR Apache-2.0 |
| pkg-config | 0.3.34 | MIT OR Apache-2.0 |
| poly1305 | 0.8.0 | Apache-2.0 OR MIT |
| proc-macro-error-attr3 | 3.1.1 | MIT OR Apache-2.0 |
| proc-macro-error3 | 3.1.1 | MIT OR Apache-2.0 |
| proc-macro2 | 1.0.107 | MIT OR Apache-2.0 |
| quote | 1.0.47 | MIT OR Apache-2.0 |
| rand_core | 0.6.4 | MIT OR Apache-2.0 |
| rle-decode-fast | 1.0.3 | MIT OR Apache-2.0 |
| rustc-hash | 2.1.3 | Apache-2.0 OR MIT |
| rustversion | 1.0.23 | MIT OR Apache-2.0 |
| scopeguard | 1.2.0 | MIT OR Apache-2.0 |
| serde | 1.0.229 | MIT OR Apache-2.0 |
| serde_core | 1.0.229 | MIT OR Apache-2.0 |
| serde_derive | 1.0.229 | MIT OR Apache-2.0 |
| serde_json | 1.0.151 | MIT OR Apache-2.0 |
| sha2 | 0.10.9 | MIT OR Apache-2.0 |
| shlex | 2.0.1 | MIT OR Apache-2.0 |
| simdutf8 | 0.1.5 | MIT OR Apache-2.0 |
| subtle | 2.6.1 | BSD-3-Clause |
| syn | 2.0.119 | MIT OR Apache-2.0 |
| syn | 3.0.6 | MIT OR Apache-2.0 |
| tinyvec | 1.13.3 | Zlib OR Apache-2.0 OR MIT |
| typenum | 1.20.1 | MIT OR Apache-2.0 |
| unicode-ident | 1.0.26 | (MIT OR Apache-2.0) AND Unicode-3.0 |
| unicode-normalization | 0.1.25 | MIT OR Apache-2.0 |
| universal-hash | 0.5.1 | MIT OR Apache-2.0 |
| version_check | 0.9.5 | MIT/Apache-2.0 |
| zeroize | 1.9.0 | Apache-2.0 OR MIT |
| zmij | 1.0.23 | MIT |
| zstd | 0.13.3 | MIT |
| zstd-safe | 7.3.0 | BSD-3-Clause |
| zstd-sys | 2.1.0+zstd.1.5.7 | BSD-3-Clause |

以上许可证信息由 `cargo tree` 读取各库 Cargo.toml 的 `license` 字段得出。“A OR B”表示可任选其一。各库的版权声明见其源码仓库。

## MIT 许可证原文（pinyin-data、phrase-pinyin-data 适用，版权人见上表）

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
