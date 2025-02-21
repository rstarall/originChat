import sys
from PyQt5.QtWidgets import QApplication
from desktop.desktop_message_box import WebFrameWindow
from desktop.desktop_ball import CircularFloatingWindow
from desktop.desktop_main_window import MainWindow
def start_gui():
    app = QApplication(sys.argv)
    
    # 创建消息框
    message_box_window = WebFrameWindow()
    #message_box_window.show()  # 启动时显示 message_box

    # 创建悬浮球
    floating_ball = CircularFloatingWindow(message_box_window)
    floating_ball.show()
    # 创建主窗口
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())