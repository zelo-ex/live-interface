# live-interface

## Background
Used as an OBS live streaming interface while pracitcing Python.

## Project Architecture
```
UI Surface: PySide6
Sound Support: pygame
OBS Support: obsws-python
Wait to complete...
```

## Config File

### Executable File Config File (.env)
```
CONFIG_PATH=[the position of music config file]
CONFIG_FILE=[music config file name]
```

### Music Config File(*.json)
```
[
	{
		"filename": "[the relative file path of music, relative to the config file]",
		"origin": "[music origin name, will display in interface]",
		"composer": "[music composer, will display in interface]"
	},
	...
]
```
