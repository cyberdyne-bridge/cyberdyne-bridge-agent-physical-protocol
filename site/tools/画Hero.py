#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LM 风 Hero 底图（矢量，无版权风险）：深底 + 蓝图线 + 机翼/桥形。"""
import os, sys, math
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (QColor, QFont, QImage, QPainter, QPen, QPolygonF,
                           QLinearGradient)
from PySide6.QtWidgets import QApplication

W, H = 2560, 1440
底 = QColor("#080a0d")
蓝 = QColor("#2f5fd0")
青 = QColor("#8fb0ff")

def 线(p, a, b, c=蓝, w=1.4, alpha=120):
    x = QColor(c); x.setAlpha(alpha)
    p.setPen(QPen(x, w)); p.drawLine(QPointF(*a), QPointF(*b))

def main():
    app = QApplication.instance() or QApplication(sys.argv)
    img = QImage(W, H, QImage.Format.Format_ARGB32); img.fill(底)
    p = QPainter(img); p.setRenderHint(QPainter.Antialiasing)
    g = QLinearGradient(0, 0, W, 0)
    g.setColorAt(0, QColor("#080a0d")); g.setColorAt(.55, QColor("#0b1018")); g.setColorAt(1, QColor("#0d1526"))
    p.fillRect(QRectF(0, 0, W, H), g)

    # 网格
    for x in range(0, W, 80):
        线(p, (x, 0), (x, H), QColor("#8ea6d8"), 1, 16)
    for y in range(0, H, 80):
        线(p, (0, y), (W, y), QColor("#8ea6d8"), 1, 16)

    # 右侧机翼/桥形线稿
    cx, cy = W * .72, H * .52
    p.setBrush(Qt.NoBrush)
    for i, (sc, a) in enumerate([(1.0, 170), (.72, 120), (.44, 80)]):
        poly = QPolygonF([
            QPointF(cx, cy - 300 * sc), QPointF(cx + 120 * sc, cy - 60 * sc),
            QPointF(cx + 720 * sc, cy + 40 * sc), QPointF(cx + 300 * sc, cy + 120 * sc),
            QPointF(cx + 90 * sc, cy + 330 * sc), QPointF(cx, cy + 240 * sc),
            QPointF(cx - 90 * sc, cy + 330 * sc), QPointF(cx - 300 * sc, cy + 120 * sc),
            QPointF(cx - 720 * sc, cy + 40 * sc), QPointF(cx - 120 * sc, cy - 60 * sc),
        ])
        x = QColor(青); x.setAlpha(a)
        p.setPen(QPen(x, 1.6)); p.drawPolygon(poly)
    线(p, (cx, cy - 300), (cx, cy + 240), 青, 1.2, 70)
    线(p, (cx - 720, cy + 40), (cx + 720, cy + 40), 青, 1, 50)

    # 左侧压暗，给标题留空间
    g2 = QLinearGradient(0, 0, W * .62, 0)
    g2.setColorAt(0, QColor(8, 10, 13, 252)); g2.setColorAt(1, QColor(8, 10, 13, 0))
    p.fillRect(QRectF(0, 0, W, H), g2)

    # 底部细线 + 角标
    线(p, (80, H - 90), (W - 80, H - 90), 青, 1, 60)
    p.setPen(QPen(QColor(126, 160, 232, 160), 1.6))
    for x, y, sx, sy in ((60, 60, 1, 1), (W - 60, 60, -1, 1), (60, H - 60, 1, -1), (W - 60, H - 60, -1, -1)):
        p.drawLine(QPointF(x, y), QPointF(x + sx * 26, y)); p.drawLine(QPointF(x, y), QPointF(x, y + sy * 26))
    p.end()
    out = os.path.join(os.path.dirname(__file__), "..", "assets-lm", "hero-lm.png")
    img.save(out); print("已存：", out)

if __name__ == "__main__":
    main()
