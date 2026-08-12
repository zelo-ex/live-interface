import json
import os
import random
from typing import Tuple
from dotenv import load_dotenv
from pathlib import Path

class MusicPlayer:
    _playlist_index = []
    _playlist_ptr = 0
    # range: 0~len(self._playlist_config)
    _playlist_config = []

    def __init__(self, file_path: str):
        MusicPlayer.load_config(self, file_path)
        self._playlist_index = [i for i in range(len(self._playlist_config))]
        random.shuffle(self._playlist_index)

        print("Init player: ")
        now_playlist = MusicPlayer.now_playlist(self)
        print(f"playlist have {now_playlist[1]} music.")
        now_song = MusicPlayer.now_song(self)
        print(f"now play [{now_playlist[0]}, {now_song[1]}]: {now_song[0]}")
        return

    def load_config(self, file_path: str):
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                self._playlist_config = json.load(file)
        except FileNotFoundError:
            print(f"Error: file not found -> {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error: invaild JSON -> {e}")

    def now_song(self) -> Tuple[str, int]:
        now_index = self._playlist_index[self._playlist_ptr]
        return self._playlist_config[now_index]["origin"], now_index

    def now_playlist(self) -> Tuple[int, int]:
        return (self._playlist_ptr, len(self._playlist_config))

    def move(self, offset: int):
        self._playlist_ptr += offset
        self._playlist_ptr %= len(self._playlist_config)
        now_playlist = MusicPlayer.now_playlist(self)
        now_song = MusicPlayer.now_song(self)
        print(f"now play [{now_playlist[0]}, {now_song[1]}]: {now_song[0]}")
        return

def main():
    load_dotenv()
    music_path = os.getenv("MUSIC_PATH")
    music_file = os.getenv("MUSIC_FILE")
    if music_path is None or music_file is None:
        print("Env error: lose MUSIC_PATH or MUSIC_FILE")
    assert music_path is not None
    assert music_file is not None
    path = Path(music_path) / music_file
    abs_path = path.absolute()
    mp = MusicPlayer(str(abs_path))
    mp.move(-1)


if __name__ == "__main__":
    main()
