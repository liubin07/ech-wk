#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QTextCursor, QPixmap, QPainter, QColor, QFont
import sys
import os

def icon_to_ico(icon: QIcon, save_path: str, sizes=(16, 32, 48, 256)):
    """
    将 QIcon 导出为 Windows ico 文件（多尺寸合一）
    :param icon:      已填充好的 QIcon
    :param save_path: 目标 *.ico 路径
    :param sizes:     需要写入 ico 的各个尺寸序列
    """
    # Create a temporary pixmap at the largest size to save as ICO
    # Qt handles multi-resolution icons automatically when saving to ICO format
    max_size = max(sizes)
    pixmap = icon.pixmap(max_size, QIcon.Normal, QIcon.Off)

    if pixmap.isNull():
        raise ValueError('QIcon 中没有任何可用图像')

    ok = pixmap.save(save_path, 'ICO')
    if not ok:
        raise OSError('保存 ico 失败，请检查路径与权限')
    print(f'已生成 → {os.path.abspath(save_path)}')

def create_matrix_icon():
    """创建简洁风格图标"""
    # 创建不同尺寸的图标
    sizes = [16, 32, 48, 64, 128, 256]
    icon = QIcon()

    for size in sizes:
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(255, 255, 255))  # 白色背景

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制黑色边框
        painter.setPen(QColor(0, 0, 0))  # 黑色
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(2, 2, size - 4, size - 4)

        # 绘制内部装饰（简洁风格）
        if size >= 32:
            # 绘制一些黑色线条和点
            painter.setPen(QColor(0, 0, 0))

            # 绘制对角线
            if size >= 48:
                painter.drawLine(4, 4, size - 4, size - 4)
                painter.drawLine(size - 4, 4, 4, size - 4)

            # 绘制中心点
            center = size // 2
            painter.setBrush(QColor(0, 0, 0))
            painter.drawEllipse(center - 2, center - 2, 4, 4)

            # 绘制一些装饰线条
            if size >= 64:
                # 绘制四个角的装饰
                corner_size = size // 4
                painter.setPen(QColor(100, 100, 100))  # 灰色
                # 左上角
                painter.drawLine(4, 4, corner_size, 4)
                painter.drawLine(4, 4, 4, corner_size)
                # 右上角
                painter.drawLine(size - 4, 4, size - corner_size, 4)
                painter.drawLine(size - 4, 4, size - 4, corner_size)
                # 左下角
                painter.drawLine(4, size - 4, corner_size, size - 4)
                painter.drawLine(4, size - 4, 4, size - corner_size)
                # 右下角
                painter.drawLine(size - 4, size - 4, size - corner_size, size - 4)
                painter.drawLine(size - 4, size - 4, size - 4, size - corner_size)

        painter.end()
        icon.addPixmap(pixmap)

    return icon

# ----------------- 使用示例 -----------------
if __name__ == '__main__':
    app = QApplication(sys.argv)      # 必须实例化 QApplication

    # 1) 构造 QIcon（可从资源、磁盘或内存 addPixmap）
    icon = create_matrix_icon()

    # 2) 一键导出 gui.ico（16/32/48/256 四合一）
    icon_to_ico(icon, 'gui.ico')
