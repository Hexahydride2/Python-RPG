# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('craftpix-net-270096-free-forest-battle-backgrounds/*', 'craftpix-net-270096-free-forest-battle-backgrounds'),
        ('Fonts/*', 'Fonts'),
        ('Icons/*', 'Icons'),
        ('images/*', 'images'),
        ('JsonData/*', 'JsonData'),
        ('Monsters/*', 'Monsters'),
        ('Music/*', 'Music'),
        ('SaveData/*', 'SaveData'),
        ('SE/*', 'SE'),
        ('Sound_Effects/*', 'Sound_Effects'),
        ('sounds/*', 'sounds'),
        ('tf_svbattle/*', 'tf_svbattle'),
        ('timefantasy_characters/*', 'timefantasy_characters')
    ],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='dragonquest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='dragonquest',
)
