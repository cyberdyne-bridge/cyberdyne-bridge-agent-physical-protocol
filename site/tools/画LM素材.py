#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把官网素材改成洛马风：白底、细线、一个蓝喵。"""
import os, sys
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QApplication

蓝 = QColor("#0033a0")
墨 = QColor("#111418")
灰 = QColor("#5b6470")
浅 = QColor("#8b93a0")
线 = QColor("#cfd4dc")
底 = QColor("#ffffff")
面 = QColor("#f6f7f9")

def 字(p, x, y, s, 号=20, 色=墨, 粗=False, 距=0.0, 等宽=False):
    f = QFont("DejaVu Sans Mono" if 等宽 else "Noto Sans CJK SC", 号,
              QFont.Weight.DemiBold if 粗 else QFont.Weight.Normal)
    f.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 距)
    p.setFont(f); p.setPen(色); p.drawText(QPointF(x, y), s)

def 框(p, x, y, w, h, 标, 副="", 填=底, 边=线, 色=墨):
    p.setBrush(填); p.setPen(QPen(边, 2)); p.drawRect(QRectF(x, y, w, h))
    p.setPen(色); p.setFont(QFont("Noto Sans CJK SC", 24, QFont.Weight.DemiBold))
    p.drawText(QRectF(x + 18, y + 6, w - 36, 44), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, 标)
    if 副:
        字(p, x + 18, y + h - 16, 副, 15, 浅)

def 箭头(p, a: QPointF, b: QPointF, 色=线):
    p.setPen(QPen(色, 2))
    p.drawLine(a, b)
    import math
    ang = math.atan2(b.y() - a.y(), b.x() - a.x())
    L, W = 14, 7
    p1 = QPointF(b.x() - L * math.cos(ang) + W * math.sin(ang), b.y() - L * math.sin(ang) - W * math.cos(ang))
    p2 = QPointF(b.x() - L * math.cos(ang) - W * math.sin(ang), b.y() - L * math.sin(ang) + W * math.cos(ang))
    p.setBrush(色); p.setPen(Qt.NoPen); p.drawPolygon(QPolygonF([b, p1, p2]))

def 架构图(出):
    W, H = 2400, 1320
    img = QImage(W, H, QImage.Format.Format_ARGB32); img.fill(底)
    p = QPainter(img); p.setRenderHint(QPainter.Antialiasing); p.setRenderHint(QPainter.TextAntialiasing)
    字(p, 90, 112, "CPNC / CBAP v1  /  ARCHITECTURE", 26, 蓝, True, 5, True)
    字(p, 90, 205, "Agent 在上面，事实在下面。", 62, 墨, True)
    p.setPen(QPen(线, 2)); p.drawLine(QPointF(90, 230), QPointF(W - 90, 230))

    # 上层：规划器
    字(p, 90, 292, "外部规划器 / 决策者", 24, 浅, False, 3, True)
    xs = [90, 660, 1230, 1800]
    for x, (t, s) in zip(xs, [("Qwen3-4B", "本地推理"), ("Mindcraft", "LLM 规划"), ("Voyager", "技能库"), ("Human", "手动介入")]):
        框(p, x, 310, 510, 110, t, s)

    # 中间：三层
    字(p, 90, 500, "协议层", 24, 浅, False, 3, True)
    框(p, 90, 520, 1590, 120, "CBAP-U  /  Agent 面", "Unix socket · 一行一条 JSON · 请求 / 取消", 面, 线)
    框(p, 90, 660, 1590, 150, "CBAP KERNEL  /  控制面", "租约 · 安全 · 急停 · 审计 · 幂等 · 服务端事实校验", 蓝, 蓝, QColor("#ffffff"))
    框(p, 90, 830, 1590, 120, "CBAP-D  /  设备面", "MCP · Mindcraft · Voyager adapter · 设备契约", 面, 线)

    # 下层：身体
    字(p, 90, 1010, "身体 / 事实源", 24, 浅, False, 3, True)
    for x, (t, s) in zip([90, 660, 1230, 1800], [("Bodies", "真实身体"), ("Minecraft", "服务端事实"), ("Forge", "模组 / 世界"), ("Audit", "审计锚点")]):
        框(p, x, 1030, 510, 110, t, s)

    # 右侧observability
    框(p, 1740, 520, 570, 120, "可观测性", "JSONL 审计 · 事实查询 · 仪表盘", 面, 蓝)
    框(p, 1740, 660, 570, 150, "", "")
    字(p, 1760, 700, "FACTS / VERIFY", 18, 蓝, True, 4, True)
    字(p, 1760, 740, "位置 · 背包 · 方块", 18, 灰)
    字(p, 1760, 772, "任务终态才算完成", 18, 灰)

    # 箭头
    箭头(p, QPointF(345, 420), QPointF(345, 515))
    箭头(p, QPointF(345, 640), QPointF(345, 655))
    箭头(p, QPointF(345, 810), QPointF(345, 825))
    箭头(p, QPointF(345, 950), QPointF(345, 1025))
    箭头(p, QPointF(1685, 735), QPointF(1735, 735), 蓝)

    字(p, 90, 1192, "→ 动作 / 请求        ← 事实 / 校验        蓝 = 控制面与事实源", 18, 浅, 等宽=True)
    p.setPen(QPen(线, 2)); p.drawLine(QPointF(90, 1212), QPointF(2310, 1212))
    字(p, 90, 1256, "CPNC / CBAP v1  ·  129/129 CONFORMANCE  ·  P0 AUDIT IN PROGRESS", 17, 蓝, True, 3, True)
    p.end(); img.save(出); print("已存：", 出)

def 截图框(出):
    W, H = 2000, 1180
    img = QImage(W, H, QImage.Format.Format_ARGB32); img.fill(底)
    p = QPainter(img); p.setRenderHint(QPainter.Antialiasing); p.setRenderHint(QPainter.SmoothPixmapTransform)
    字(p, 60, 70, "CPNC OS 0.1  /  SYSTEM IMAGES", 16, 蓝, True, 3, True)
    for i, (f, t) in enumerate([("cbap-os-desktop.png", "DESKTOP"), ("cbap-os-control.png", "CONTROL CENTER")]):
        x = 60 + i * 950
        图 = QImage(os.path.join(os.path.dirname(__file__), "..", "assets", f))
        p.setPen(QPen(线, 2)); p.setBrush(QColor("#0d141d")); p.drawRect(QRectF(x, 110, 880, 880))
        if not 图.isNull():
            s = 图.scaled(860, 860, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            p.drawImage(QPointF(x + (880 - s.width()) / 2, 110 + (880 - s.height()) / 2), s)
        字(p, x, 1030, t, 15, 墨, True, 3, True)
        字(p, x, 1058, "CPNC / DSH runtime", 13, 浅, 等宽=True)
    p.setPen(QPen(蓝, 4)); p.drawLine(QPointF(60, 1090), QPointF(W - 60, 1090))
    字(p, 90, 1192, "→ 动作 / 请求        ← 事实 / 校验        蓝 = 控制面与事实源", 18, 浅, 等宽=True)
    p.setPen(QPen(线, 2)); p.drawLine(QPointF(90, 1212), QPointF(2310, 1212))
    字(p, 90, 1256, "CPNC / CBAP v1  ·  129/129 CONFORMANCE  ·  P0 AUDIT IN PROGRESS", 17, 蓝, True, 3, True)
    p.end(); img.save(出); print("已存：", 出)

if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    架构图(os.path.join(os.path.dirname(__file__), "..", "assets-lm", "cbap-architecture-lm.png"))
    截图框(os.path.join(os.path.dirname(__file__), "..", "assets-lm", "cbap-os-lm.png"))
