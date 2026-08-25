# live-interface
A simple live interface used in OBS live streaming.

## Background
Used as an OBS live streaming interface while pracitcing Python.

## Project Architecture
```
UI Surface: PySide6
Sound Support: PySide6
Video Support: PySide6
Danmaku Support: blivedm
```

## Config File

### Executable File Config File (.env)
```
MUSIC_PATH=[the position of music config file]
MUSIC_FILE=[music config file name]
NOTICE_FILE=[the notice file to be read]
SCREEN_SCALE=[preview to home screen ratio]
HEADER_HEIGHT=[height of the title (in px)]
SERVICE_PORT=[HTTP server port]
LIVE_ID=[listened live room id]
LIVE_SESSDATA=[SESSDATA ley in cookies]
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

### Usage

1. Clone project source code and run build script
``` sh
git clone --depth=1 https://codeberg.org/zelo-ex/live-interface
cd ./live-interface
./build.sh
```

2. Copy `src/.env_example` to the directory where the live_interface executable is located.

3. Set up your environment and rename `.env_example` to `.env`.
