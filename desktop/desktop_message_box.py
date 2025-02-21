import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenu, QSizeGrip
from PyQt5.QtCore import Qt, QUrl, QPoint, QRectF
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QIcon


class WebFrameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口为无边框和置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口图标和标题
        self.setWindowIcon(QIcon('imgs/logo.png'))
        self.setWindowTitle('origin')

        # 隐藏窗口，直到网页加载完成
        self.hide()

        # 创建一个 QWebEngineView 用于加载网页
        self.web_view = QWebEngineView(self)
        self.web_view.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置webview背景为透明
        self.web_view.setStyleSheet("background: transparent")  # 设置样式表为透明背景
        self.web_view.loadFinished.connect(self.on_load_finished)  # 监听加载完成信号
        self.web_view.load(QUrl("https://www.baidu.com"))  # 使用 QUrl 加载网页地址
        self.setCentralWidget(self.web_view)  # 将 QWebEngineView 设置为中心部件

        # 获取屏幕大小并计算窗口位置
        screen = QApplication.primaryScreen().geometry()
        x = int(screen.width() * 0.98 - 400)  # 屏幕宽度的5%
        y = int(screen.height() * 0.30)  # 屏幕高度的5%
        self.setGeometry(x, y, 400, 600)  # 设置初始位置和大小

        # 创建遮罩
        self.overlay = Overlay(self)
        self.overlay.setGeometry(0, 0, self.width(), 50)  # 设置遮罩位置和大小

        # 设置 webview 的上部 margin
        self.web_view.setContentsMargins(0, self.overlay.height(), 0, 0)

        # 初始化鼠标位置
        self.oldPos = self.pos()
        
        # 添加四个方向的 QSizeGrip
        self.sizeGrips = []
        # 右下角
        self.sizeGrips.append(QSizeGrip(self))
        # 左下角
        self.sizeGrips.append(QSizeGrip(self))
        # 右上角
        self.sizeGrips.append(QSizeGrip(self))
        # 左上角
        self.sizeGrips.append(QSizeGrip(self))
        
        for grip in self.sizeGrips:
            grip.setStyleSheet("background: transparent;")
            grip.setFixedSize(20, 20)

    def on_load_finished(self, success):
        """当网页加载完成时调用"""
        if success:
            # 如果加载成功，显示窗口
            self.show()
        else:
            print("网页加载失败")

    def resizeEvent(self, event):
        """确保 QWebEngineView 始终与窗口大小一致"""
        # 调整大小时保持左上角位置不变
        self.web_view.resize(self.size())
        self.overlay.setGeometry(0, 0, self.width(), 50)
        
        # 更新四个 QSizeGrip 的位置
        self.sizeGrips[0].move(self.width() - 20, self.height() - 20)  # 右下
        self.sizeGrips[1].move(0, self.height() - 20)  # 左下
        self.sizeGrips[2].move(self.width() - 20, 0)  # 右上
        self.sizeGrips[3].move(0, 0)  # 左上

    def paintEvent(self, event):
        """设置窗口和webview圆角"""
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)  # 设置窗口圆角半径为20
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setClipPath(path)
        painter.fillRect(self.rect(), QColor(255, 255, 255, 0))  # 填充透明背景

        # 设置webview的圆角
        webview_path = QPainterPath()
        webview_path.addRoundedRect(QRectF(self.web_view.rect()), 20, 20)  # 设置webview圆角半径为20
        painter.setClipPath(webview_path)
        painter.fillRect(self.web_view.rect(), QColor(255, 255, 255, 0))  # 填充透明背景

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


class Overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # 允许遮罩接收鼠标事件

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.2)  # 设置透明度

        # 创建上部圆角矩形路径
        path = QPainterPath()
        rect = QRectF(self.rect())
        path.moveTo(rect.bottomLeft())
        path.lineTo(rect.topLeft())
        path.arcTo(rect.x(), rect.y(), 40, 40, 180, -90)  # 左上角圆角
        path.lineTo(rect.topRight() - QPoint(20, 0))
        path.arcTo(rect.right() - 40, rect.y(), 40, 40, 90, -90)  # 右上角圆角
        path.lineTo(rect.bottomRight())
        path.lineTo(rect.bottomLeft())
        painter.setClipPath(path)

        painter.fillRect(self.rect(), QColor(0, 0, 0))  # 填充黑色背景

    def contextMenuEvent(self, event):
        """右键菜单事件"""
        contextMenu = QMenu(self)
        closeAction = contextMenu.addAction("隐藏")
        contextMenu.setWindowIcon(QIcon('imgs/logo.png'))
        contextMenu.setWindowTitle('origin')

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == closeAction:
            self.parent().hide()

    def mousePressEvent(self, event):
        """记录鼠标按下时的位置"""
        if event.button() == Qt.LeftButton:
            self.parent().oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        """根据鼠标移动调整窗口位置"""
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.parent().oldPos)
            self.parent().move(self.parent().x() + delta.x(), self.parent().y() + delta.y())
            self.parent().oldPos = event.globalPos()

