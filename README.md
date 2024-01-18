# mc3dslib
- **A python Library for Minecraft 3DS, allowing for easy Modification of the SaveGames, and romfs Files.**

## Note:
- **Documentation is Extremely barebones currently. A more in-depth documentation will be added soon.**
- **I've made a Documentation on both MC3DS's [Options.txt](https://github.com/Cracko298/MC3DS-Options-Documentation), and [ARGB .3DST](https://github.com/Cracko298/MC-3DST-Documentation), if you want a more "in-depth explantaion of things."**



# mc3dslib Function(s):

- **Extract Bytes:    `extract_bytes(filename, arg1, arg2)`**
- **Convert Bytes:    `convert_bytes(bytestring,order)`**
- **Extract Color:    `extract_colors(image_path)`**
- **Invert Colors:    `invertclrs(image_path)`**
- **Set Green Hue:    `greenify(image_path)`**
- **Set Orange Hue:   `orangify(image_path)`**
- **Set Blue Hue:     `bluify(image_path)`**
- **Set Red Hue       `redify(image_path)`**
- **Grab Meta Data:   `meta_grab(image_path)`**
- **Material To Json: `mat2json(file_path)`**
- **Convert Options:  `convert_options(file_path,output_file_path)`**
- **Revert Options:   `revert_options(file_path,output_file_path`**
- **Blang To Json: `toJson(blang_file)`**
- **Json To Blang: `fromJson(json_file)`**
- **Extract Lines: `extract_lines(image_path`**
- **Extract Head: `extract_head(image_path)`**

## Importing the Module(s):
### Defualt Importing:
```py
import mc3dslib
```
### Blang Only Importing:
```py
from mc3dslib import BlangFile
```
### Import Everything:
```py
from mc3dslib import *
```
### Importing as 'mc3ds'
```py
import mc3dslib as mc3ds
```

## Blang Conversion(s):
### Initializing the File:
```py
import mc3dslib

file = mc3dslib.BlangFile().open("en_GB.json") # Initialzation of Example File
```

### JSON TO BLANG
```py
import mc3dslib

## YOU NEED TO INITIALIZE THE FILE YOU WANT TO CONVERT FIRST!

output_path = ".\\" ## Any Valid Path can go here
mc3dslib.BlangFile().fromJson(output_path)
```
### BLANG TO JSON
```py
import mc3dslib

## YOU NEED TO INITIALIZE THE FILE YOU WANT TO CONVERT FIRST!

output_path = ".\\" # Any Valid Path can go here
mc3dslib.BlangFile().toJson(output_path)
```

# Panning Additions:
- **Convert Achievements**
- **Revert Achievements**
- **Extract Arms**
- **Extract Legs**
- **Extract Body**

## Credit(s):
- **[@Wolfyxon](https://github.com/Wolfyxon) - Few of the Functions in the Code.**
- **[@STBrian](https://github.com/STBrian) - MC3DS Blang Format Conversion Code.**
- **[@Cracko298](https://github.com/Cracko298) - Developer of Most Functions in the Code.**
