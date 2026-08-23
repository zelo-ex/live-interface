import asyncio
import http.cookies
import os
import aiohttp
from typing import Optional
import blivedm
import blivedm.clients.ws_base as ws_base
import blivedm.models.web as web_models
from .signals import signal_bus

def isDigits(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

session: Optional[aiohttp.ClientSession] = None

def run_danmaku():
    asyncio.run(init_danmaku())

async def init_danmaku():
    init_session()
    try:
        await run_client()
    finally:
        await session.close()

def init_session():
    sess_data = os.getenv("LIVE_SESSDATA", "")
    if sess_data == "":
        print("[Warning] LIVE_SESSDATA not found, operations have limited...")
    cookies = http.cookies.SimpleCookie()
    cookies['SESSDATA'] = sess_data
    cookies['SESSDATA']['domain'] = 'bilibili.com'

    global session
    session = aiohttp.ClientSession()
    session.cookie_jar.update_cookies(cookies)
    return

async def run_client():
    room_id = os.getenv("LIVE_ID", "")
    if room_id == "":
        print("[Error] LIVE_ID not found")
    if not isDigits(room_id):
        print("[Error] invaild LIVE_ID")
    client = blivedm.BLiveClient(int(room_id), session=session)
    handler = danmaku_handler()
    client.set_handler(handler)
    client.start()

    try:
        await asyncio.gather(client.join())
    finally:
        await asyncio.gather(client.stop_and_close())

class danmaku_handler(blivedm.BaseHandler):
    def _on_danmaku(self, client: ws_base.WebSocketClientBase,
                    message: web_models.DanmakuMessage):
        signal_bus.danmaku_source.emit(message.uname, message.msg)
        return super()._on_danmaku(client, message)
