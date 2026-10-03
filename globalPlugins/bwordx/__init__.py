# -*- coding: utf-8 -*-
"""BWordX 中文盲文：接管 NVDA 对 bwordx.ctb 这张表的翻译，交给 braille_ffi.dll。

NVDA 把文字交给 liblouis 前后都经过 louisHelper.translate，这里包一层：表是 bwordx.ctb 就走我们的引擎，
其他表照旧走 liblouis。任何出错都退回 liblouis（用 bwordx.ctb 里 include 的 zh-chn.ctb），不影响盲文显示。
"""

import ctypes
import json
import os
import struct
import threading

import globalPluginHandler
import louisHelper
from logHandler import log

# 表名 -> 盲文方案 id（bw_set_scheme）
TABLES = {
    "bwordx.ctb": "tongyong",
    "bwordx-shuangpin.ctb": "shuangpin",
    "bwordx-biaoyi.ctb": "biaoyi",
}
_here = os.path.dirname(os.path.abspath(__file__))
# addon 根目录/lib/x86 或 x64
_lib_dir = os.path.abspath(os.path.join(_here, "..", "..", "lib"))
_dll_path = os.path.join(_lib_dir, "x64" if struct.calcsize("P") == 8 else "x86", "braille_ffi.dll")
# 字库、词库等数据（加密压缩过，两种位数共用一份）
_data_dir = os.path.join(_lib_dir, "data")

_lock = threading.Lock()
_lib = None
_engine = None
_failed = False
_cur_scheme = "tongyong"


def _load():
    """第一次用到时才加载（词库要零点几秒）。失败后不再重试。"""
    global _lib, _engine, _failed
    if _engine or _failed:
        return _engine
    try:
        lib = ctypes.CDLL(os.path.abspath(_dll_path))
        lib.bw_new.restype = ctypes.c_void_p
        lib.bw_translate.restype = ctypes.c_void_p
        lib.bw_translate.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        lib.bw_string_free.argtypes = [ctypes.c_void_p]
        lib.bw_set_scheme.restype = ctypes.c_void_p
        lib.bw_set_scheme.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.bw_set_layout.argtypes = [ctypes.c_void_p] + [ctypes.c_uint32] * 5
        if os.path.isdir(_data_dir):
            # 必须在第一次翻译前设好；返回值是缺文件的提示，这里只管释放
            lib.bw_set_data_dir.restype = ctypes.c_void_p
            lib.bw_set_data_dir.argtypes = [ctypes.c_char_p]
            res = lib.bw_set_data_dir(_data_dir.encode("utf-8"))
            if res:
                log.info("BWordX: 数据目录 %s，%s", _data_dir, ctypes.string_at(res).decode("utf-8", "replace"))
                lib.bw_string_free(res)
        engine = lib.bw_new()
        if not engine:
            raise RuntimeError("bw_new 返回空指针")
        lib.bw_set_layout(engine, 0, 0, 0, 0, 1)  # 不换行、不缩进、不分页：行宽由点显器决定
        _lib, _engine = lib, engine
        log.info("BWordX: 引擎已加载 %s", _dll_path)
    except Exception:
        _failed = True
        log.error("BWordX: 加载引擎失败，退回 liblouis", exc_info=True)
    return _engine


def _cells(braille):
    return [ord(c) - 0x2800 if 0x2800 <= ord(c) <= 0x28FF else 0 for c in braille]


def _mapping(text, data):
    """从 pieces 算出 (cells, brailleToRawPos, rawToBraillePos)。

    每个汉字对应它那个音节的盲文；其他片段（标点、数字、字母……）按字符比例对应。
    pieces 的盲文拼起来和 braille 不一致（连写空格等）时，整体按比例对应。
    """
    braille = data["braille"]
    n, m = len(text), len(braille)
    raw_to_start = None
    pieces = data.get("pieces", [])
    # 依次在 braille 里找每个片段的盲文，片段之间只允许隔着空方（连写分词、换行时加的）
    raw_to_start = []
    offset = 0
    for p in pieces:
        kind = p["kind"]
        cells = "".join(s["cells"] for s in p["syllables"]) if kind == "han" else p.get("cells", "")
        if cells:
            at = braille.find(cells, offset)
            if at < 0 or braille[offset:at].strip("⠀ \n"):
                raw_to_start = None
                break
            offset = at
        if kind == "han":
            for s in p["syllables"]:
                raw_to_start.append(offset)
                offset += len(s["cells"])
        elif kind == "text":
            t = p["text"]
            for k in range(len(t)):
                raw_to_start.append(offset + k * len(cells) // len(t))
            offset += len(cells)
        else:
            raw_to_start.extend([offset] * len(p["text"]))
    if raw_to_start is not None and len(raw_to_start) != n:
        raw_to_start = None
    if raw_to_start is None:
        log.debugWarning("BWordX: 位置对不上，改按比例对应: %r", text)
    if raw_to_start is None:
        raw_to_start = [i * m // n if n else 0 for i in range(n)]
    raw_to_start = [min(s, max(m - 1, 0)) for s in raw_to_start]

    braille_to_raw = [0] * m
    last = 0
    for cell in range(m):
        # 每个盲文方对应起点不超过它的最后一个原文字符
        while last + 1 < n and raw_to_start[last + 1] <= cell:
            last += 1
        braille_to_raw[cell] = last
    return _cells(braille), braille_to_raw, raw_to_start


def _scheme_for(tableList):
    """表名 -> 方案 id；不是我们的表返回 None。注意 bwordx.ctb 是 bwordx-xxx.ctb 的前缀之外的独立名字。"""
    for name, scheme in TABLES.items():
        if name in tableList:
            return scheme
    return None


def _translate_bw(inbuf, cursorPos, scheme):
    with _lock:
        engine = _load()
        if not engine:
            return None
        global _cur_scheme
        if scheme != _cur_scheme:
            res = _lib.bw_set_scheme(engine, scheme.encode("ascii"))
            _lib.bw_string_free(res)
            _cur_scheme = scheme
        ptr = _lib.bw_translate(engine, inbuf.encode("utf-8", "replace"), b"")
    try:
        data = json.loads(ctypes.string_at(ptr).decode("utf-8"))
    finally:
        _lib.bw_string_free(ptr)
    if "error" in data:
        log.debugWarning("BWordX 翻译出错: %s", data["error"])
        return None
    cells, b2r, r2b = _mapping(inbuf, data)
    cursor = None
    if cursorPos is not None and r2b:
        cursor = r2b[min(cursorPos, len(r2b) - 1)]
    return cells, b2r, r2b, cursor


_orig_translate = louisHelper.translate


def _translate(tableList, inbuf, typeform=None, cursorPos=None, mode=0):
    try:
        scheme = _scheme_for(tableList) if inbuf else None
        if scheme:
            result = _translate_bw(inbuf, cursorPos, scheme)
            if result is not None:
                return result
    except Exception:
        log.error("BWordX: 翻译失败，退回 liblouis", exc_info=True)
    return _orig_translate(tableList, inbuf, typeform=typeform, cursorPos=cursorPos, mode=mode)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        louisHelper.translate = _translate

    def terminate(self):
        louisHelper.translate = _orig_translate
        super().terminate()
