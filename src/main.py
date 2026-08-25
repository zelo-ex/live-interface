import threading
import os
from gui.display import GUIDisplay
from dotenv import load_dotenv
from services.listener import app
from services.danmaku import run_danmaku

def isDigits(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def run_fastapi():
    import uvicorn
    port = os.getenv("SERVICE_PORT", "8000")
    if not isDigits(port) or int(port) >= 65536 or int(port) < 1024:
        print("env error: invaild port")
    print(f"service port: {port}")
    uvicorn.run(app, host="127.0.0.1", port=int(port), reload=False)

if __name__ == "__main__":
    load_dotenv()
    gui = GUIDisplay()

    server_thread = threading.Thread(
        target=run_fastapi,
        daemon=True
    )
    server_thread.start()

    # danmaku_thread = threading.Thread(
    #     target=run_danmaku,
    #     daemon=True
    # )
    # danmaku_thread.start()
    
    gui.run()
