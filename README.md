# live-interface
A simple live interface used in OBS live streaming.

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
MUSIC_PATH=[the position of music config file]
MUSIC_FILE=[music config file name]
SCREEN_SCALE=[scale factor of the preview area, e.g. 0.75]
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
