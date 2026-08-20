from gui.display import GUIDisplay
from dotenv import load_dotenv

def main():
    load_dotenv()
    gui = GUIDisplay()
    gui.run()


if __name__ == "__main__":
    main()
