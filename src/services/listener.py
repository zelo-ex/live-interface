from fastapi import FastAPI, Request
from .signals import signal_bus

def isDigits(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

app = FastAPI()

@app.post("/api/danmaku")
async def danmaku(request: Request):
    json = await request.json()
    user = json.get("user", "")
    msg = json.get("msg", "")
    signal_bus.danmaku_source.emit(user, msg)
    return {"status": "ok"}

@app.post("/api/music")
async def music(request: Request):
    commands = [
        "prev", "next", "play", "pause", "restart"
    ]
    
    json = await request.json()
    command = json.get("command", "")
    offset = json.get("offset", "1")
    if command in commands:
        if not isDigits(offset):
            return {
                "status": "error",
                "message": "invaild offset value"
            }
        signal_bus.music_source.emit(command, int(offset))
        return {"status": "ok"}
    return {
        "status": "error",
        "message": "unknown command"
    }
    
@app.post("/api/event")
async def event(request: Request):
    events = [
        "noticeReload",
        "headerReload"
    ]

    json = await request.json()
    event_name = json.get("eventName", "")
    print(event_name)
    if event_name in events:
        signal_bus.event_source.emit(event_name)
        return {"status": "ok"}
    return {
        "status": "error",
        "message": f"unknown event: {event_name}"
    }
