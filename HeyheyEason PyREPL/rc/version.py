# PyREPL version info
# version.py
# type: ignore

VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 0, 0, 0), # File version
        prodvers=(3, 0, 0, 0), # Product version
        
        mask=0x3f, 
        flags=0x0, # Configuration: Release
        # Set flags to 0x1L if debug
        # flags=0x1L, 
        
        OS=0x4,        # OS：Windows NT
        fileType=0x1,  # File type：Application
        subtype=0x0,
        date=(0, 0)
    ),
    
    kids=[
        StringFileInfo(
            [
                StringTable(
                    u'040904b0', # English US with Unicode
                    [
                        StringStruct(u'CompanyName', u'HeyheyEason'),
                        StringStruct(u'FileDescription', u'A lightweight Python REPL app.'),
                        StringStruct(u'FileVersion', u'1.0.0'), 
                        StringStruct(u'InternalName', u'HeyheyEason.PyREPL.App'),
                        StringStruct(u'LegalCopyright', u'Copyright © 2025 HeyheyEason'),
                        StringStruct(u'OriginalFilename', u'pyrepl_v3.0.0.exe'),
                        StringStruct(u'ProductName', u'HeyheyEason PyREPL'),
                        StringStruct(u'ProductVersion', u'3.0.0'),
                    ]
                )
            ]
        ), 
        
        VarFileInfo(
            [
                VarStruct(u'Translation', [1033, 1200]) # 0x0409, 1200
            ]
        )
    ]
)