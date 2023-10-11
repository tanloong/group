# vim:ft=python

import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

a = Analysis(
    ['group.py'],
    pathex=[],
    binaries=[],
    datas=[('data/nltk_data/tokenizers/punkt/english.pickle', 'nltk_data/tokenizers/punkt'),
           ('data/nltk_data/tokenizers/punkt/PY3/english.pickle', 'nltk_data/tokenizers/punkt/PY3'),
           ('img', 'img')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='group',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console = False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Additional options
    icon='./img/icon.ico',
    contents_directory='libs'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='group',
)
