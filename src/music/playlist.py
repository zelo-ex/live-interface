import random
import json
from typing import Tuple
import os
from dotenv import load_dotenv
from pathlib import Path

class playlist:
    def __init__(self):
        self._playlist_index= []
        self._playlist_ptr = 0
        # range: 0~len(self._playlist_config)
        self._playlist_config = []
        
        playlist.load_config(self, self.parse_config_path())
        if not self._playlist_config:
            raise RuntimeError("Playlist config is empty or failed to load")
        self._playlist_index = [i for i in range(len(self._playlist_config))]
        random.shuffle(self._playlist_index)

        # print("Init player: ")
        # now_playlist = playlist.now_playlist(self)
        # print(f"playlist have {now_playlist[1]} music.")
        # now_song = playlist.now_song(self)
        # print(f"now play [{now_playlist[0]}, {now_song[1]}]: {now_song[0]}")

        return

    def parse_config_path(self) -> str:
        load_dotenv()
        self.music_path = os.getenv("MUSIC_PATH")
        self.music_file = os.getenv("MUSIC_FILE")
        if self.music_path is None or self.music_file is None:
            raise RuntimeError(
                "Env error: MUSIC_PATH or MUSIC_FILE is missing in .env"
            )
        assert self.music_path is not None
        assert self.music_file is not None
        path = Path(self.music_path) / self.music_file
        abs_path = path.absolute()
        return str(abs_path)

    def load_config(self, file_path: str):
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                self._playlist_config = json.load(file)
        except FileNotFoundError:
            print(f"Error: file not found -> {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error: invaild JSON -> {e}")

    def now_composer(self) -> Tuple[str, int]:
        now_index = self._playlist_index[self._playlist_ptr]
        return self._playlist_config[now_index]["composer"], now_index

    def now_song(self) -> Tuple[str, int]:
        now_index = self._playlist_index[self._playlist_ptr]
        return self._playlist_config[now_index]["origin"], now_index

    def now_filename(self) -> Tuple[str, int]:
        now_index = self._playlist_index[self._playlist_ptr]
        now_filename = self._playlist_config[now_index]["filename"]
        assert self.music_path is not None
        return (str((Path(self.music_path) / now_filename).absolute()),
                now_index)

    def now_playlist(self) -> Tuple[int, int]:
        return (self._playlist_ptr, len(self._playlist_config))

    def move(self, offset: int) -> None:
        total = len(self._playlist_config)
        if total == 0:
            return
        self._playlist_ptr += offset
        self._playlist_ptr %= total
        # now_playlist = playlist.now_playlist(self)
        # now_song = playlist.now_song(self)
        # print(f"now play [{now_playlist[0]}, {now_song[1]}]: {now_song[0]}")
        return
