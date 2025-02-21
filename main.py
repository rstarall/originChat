from desktop.desktop import start_gui
from desktop.desktop_web_server import start_web_server
import sys
sys.path.append('./')

if __name__ == "__main__":
    start_web_server()
    start_gui()
