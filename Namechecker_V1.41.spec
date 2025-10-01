# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Namecheck.py'],
    pathex=[],
    binaries=[],
    datas=[('assets\\icons\\namechecker.ico', '.')],
    hiddenimports=['pandas', 'numpy', 'openpyxl', 'pandas.io.excel', 'pandas.io.formats.excel', 'pandas.io.parsers', 'et_xmlfile', 'pytz', 'dateutil'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Namechecker_V1.41',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\icons\\namechecker.ico'],
)
