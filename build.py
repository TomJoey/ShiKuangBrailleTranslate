"""打包 NVDA 插件：python build.py  ->  <name>-<版本>.nvda-addon

需要先编好两个 DLL：
  braille-ffi/target/release/braille_ffi.dll                          （64 位，NVDA 2026.1 起）
  braille-ffi/target/i686-pc-windows-msvc/release/braille_ffi.dll     （32 位，NVDA 2025.x 及以前）
cd braille-ffi && cargo build --release --no-default-features --features math-builtin,data-crypto [--target i686-pc-windows-msvc]
瘦身版：不带语言判断模型（34MB）、乐谱、PDF/Word 读入；数据不编进 DLL，用 tools/release/stage_data.py 压缩加密后放 lib/data
（需要 braille-core/secrets/data.key，和 win/build.bat 同一把密钥）。
"""
import os
import re
import subprocess
import sys
import tempfile
import zipfile

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
dlls = {
    "lib/x64/braille_ffi.dll": os.path.join(root, "braille-ffi", "target", "release", "braille_ffi.dll"),
    "lib/x86/braille_ffi.dll": os.path.join(root, "braille-ffi", "target", "i686-pc-windows-msvc", "release", "braille_ffi.dll"),
}
version = re.search(r"^version\s*=\s*(\S+)", open(os.path.join(here, "manifest.ini"), encoding="utf-8").read(), re.M).group(1)
name = re.search(r"^name\s*=\s*(\S+)", open(os.path.join(here, "manifest.ini"), encoding="utf-8").read(), re.M).group(1)
out = os.path.join(here, f"{name}-{version}.nvda-addon")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(here, "manifest.ini"), "manifest.ini")
    for doc in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        z.write(os.path.join(here, doc), doc)
    for sub in ("globalPlugins", "brailleTables"):
        for d, _, files in os.walk(os.path.join(here, sub)):
            for f in files:
                if f.endswith(".pyc"):
                    continue
                p = os.path.join(d, f)
                z.write(p, os.path.relpath(p, here).replace(os.sep, "/"))
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, os.path.join(root, "tools", "release", "stage_data.py"), tmp], check=True)
        for f in sorted(os.listdir(tmp)):
            z.write(os.path.join(tmp, f), "lib/data/" + f)
    for name, path in dlls.items():
        if os.path.isfile(path):
            z.write(path, name)
        else:
            print("缺少", path, "（该位数的 NVDA 用不了）")
print("已生成", out)
