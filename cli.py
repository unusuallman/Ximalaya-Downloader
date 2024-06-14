import time
import main
import asyncio
import re
from pathlib import Path
from fake_useragent import UserAgent
import tkinter as tk
from tkinter import filedialog

ximalaya = main.Ximalaya()
loop = asyncio.new_event_loop()
ua = UserAgent()


def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory()
    root.destroy()
    return directory_path


def my_cli():
    star_time = time.time()
    print("开始下载！")
    cookie, path = ximalaya.analyze_config()
    headers = {"user-agent": ua.chrome, "cookie": cookie}
    links = list(Path(__file__).parent.glob("*.txt"))
    links.remove(Path(__file__).parent / "requirements.txt")
    if not links:
        print("请将专辑链接放入txt文件中！")
        return
    for link in links:
        with open(link, "r", encoding="utf-8") as f:
            urls = f.read().splitlines()
        for input_album in urls:
            try:
                album_id = int(input_album)
            except ValueError:
                try:
                    album_id = re.search(r"album/(?P<album_id>\d+)", input_album)
                    if not album_id:
                        raise ValueError
                    album_id = album_id.group('album_id')
                except Exception:
                    print(f"链接有误，请检查{input_album}后重试！")
                    continue
            album_name, sounds = ximalaya.analyze_album(album_id)
            if not sounds:
                continue
            album_type = ximalaya.judge_album(album_id, headers)
            if album_type == 1 or album_type == 0:
                print(f"专辑{album_name}解析成功！")
            else:
                print(f"专辑{album_name}解析失败！")
                continue
            loop.run_until_complete(ximalaya.get_selected_sounds(
                sounds, album_name, 1, len(sounds), headers, 2, False, path))
    print("下载完成！")
    end_time = time.time()
    print(f"耗时：{end_time - star_time:.2f}秒")


if __name__ == "__main__":
    my_cli()