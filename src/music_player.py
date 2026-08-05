import json
import os
import random
from dotenv import load_dotenv
from pathlib import Path


class MusicPlayer:
    __playlist_index = []
    __playlist_ptr = 0
    # range: 0~len(self.__playlist_config)
    __playlist_play_status = 0
    # 0 Pause
    # 1 Play
    # -1 error(set error code and send)
    __playlist_config = []

    def __init__(self, file_path: str):
        MusicPlayer.load_config(self, file_path)
        self.__playlist_index = [i for i in range(len(self.__playlist_config))]
        random.shuffle(self.__playlist_index)

        print("Init player: ")
        now_playlist = MusicPlayer.now_playlist(self)
        print(f"playlist have {now_playlist[1]} music.")
        now_song = MusicPlayer.now_song(self)
        print(f"now play [{now_playlist[0]}, {now_song[1]}]: {now_song[0]}")
        return

    def load_config(self, file_path: str):
        file = open(file=file_path, mode="r")
        file_data = file.read()
        file.close()

        self.__playlist_config = json.loads(file_data)
        return

    def now_song(self) -> (str, int):
        now_index = self.__playlist_index[self.__playlist_ptr]
        return (self.__playlist_config[now_index]["origin"], now_index)

    def now_playlist(self) -> (int, int):
        return (self.__playlist_ptr, len(self.__playlist_config))

    def move(self, offset: int):
        self.__playlist_ptr += offset
        self.__playlist_ptr %= len(self.__playlist_config)
        now_playlist = MusicPlayer.now_playlist(self)
        now_song = MusicPlayer.now_song(self)
        print(f"now play [{now_playlist[0]}, {now_song[1]}]: {now_song[0]}")
        return

    def play():
        print("playing.")
        return

    def pause(self):
        print("stopped.")
        return


def main():
    load_dotenv()
    music_path = Path(os.getenv("CONFIG_PATH"))
    music_file = os.getenv("CONFIG_FILE")
    path = music_path / music_file
    mp = MusicPlayer(path.absolute())
    mp.move(-1)


if __name__ == "__main__":
    main()
