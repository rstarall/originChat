import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QPainter, QPixmap, QPainterPath, QIcon
from PyQt5.QtCore import Qt, QRectF, QPoint
from desktop.desktop_message_box import WebFrameWindow
from desktop.desktop_main_window import MainWindow

class CircularFloatingWindow(QWidget):
    def __init__(self, message_box_window: WebFrameWindow):
        super().__init__()
        self.message_box_window = message_box_window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)  # 无边框，置顶，不在任务栏显示
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
        
        # 设置窗口图标和标题
        self.setWindowIcon(QIcon('./imgs/logo.png'))
        self.setWindowTitle('origin')

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./imgs/logo.png'))
        self.tray_icon.setToolTip('origin')
        
        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = tray_menu.addAction("显示")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(QApplication.instance().quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # 获取屏幕大小
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 根据屏幕大小计算窗口宽高
        self.window_size = int(min(screen_width, screen_height) * 0.1)  # 假设窗口大小为屏幕最小边的10%
        
        # 设置窗口位于屏幕右下角
        self.setGeometry(int(screen_width - self.window_size - 60), int(screen_height - self.window_size - 60), int(self.window_size), int(self.window_size))  # 设置窗口大小和位置
        self.oldPos = self.pos()  # 初始化鼠标位置

        # 设置图片宽高为窗口的80%
        self.image_width = int(self.window_size * 1)
        self.image_height = int(self.window_size * 1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 创建圆形路径
        path = QPainterPath()
        path.addEllipse(QRectF(self.rect()))  # 使用 QRectF 代替 QRect

        # 设置剪切路径
        painter.setClipPath(path)

        # 绘制背景图片，居中显示
        pixmap = QPixmap("./imgs/logo.png").scaled(self.image_width, self.image_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        x = (self.width() - self.image_width) / 2
        y = (self.height() - self.image_height) / 2
        painter.drawPixmap(int(x), int(y), self.image_width, self.image_height, pixmap)

    def mousePressEvent(self, event):
        """记录鼠标按下时的位置"""
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        """根据鼠标移动调整窗口位置"""
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def contextMenuEvent(self, event):
        """右键菜单事件"""
        contextMenu = QMenu(self)
        contextMenu.setWindowIcon(QIcon('./imgs/logo.png'))
        contextMenu.setWindowTitle('origin')
        
        showMessageBoxAction = contextMenu.addAction("显示消息框")
        hideMessageBoxAction = contextMenu.addAction("隐藏消息框") 
        hideAction = contextMenu.addAction("隐藏")
        closeAction = contextMenu.addAction("关闭")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == hideAction:
            self.hide()
        elif action == showMessageBoxAction:
            self.message_box_window.show()
        elif action == hideMessageBoxAction:
            self.message_box_window.hide()
        elif action == closeAction:
            self.close()
            QApplication.instance().quit()



    