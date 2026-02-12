from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QBrush, QColor, QRadialGradient, QPen
import math
import random

class NeuralOrb(QWidget):
    def __init__(self, parent=None, size=100):
        super().__init__(parent)
        self.setFixedSize(size, size)
        
        # animation properties
        self.angle = 0
        self.pulse = 0
        self.particles = []
        self.state = "idle"  # idle, listening, thinking, speaking
        
        # Timer for 60 FPS animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS

    def set_state(self, state):
        self.state = state

    def update_animation(self):
        self.angle += 2
        if self.angle >= 360:
            self.angle = 0
            
        # Pulse effect
        self.pulse = (math.sin(math.radians(self.angle * 2)) + 1) / 2  # 0.0 to 1.0
        
        self.update()  # Trigger paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 10
        
        # Dynamic Colors based on State
        if self.state == "idle":
            base_color = QColor(0, 240, 255) # Cyan
        elif self.state == "listening":
            base_color = QColor(0, 255, 100) # Green
        elif self.state == "thinking":
            base_color = QColor(255, 0, 255) # Magenta
        elif self.state == "speaking":
            base_color = QColor(255, 100, 0) # Orange
        else:
            base_color = QColor(255, 255, 255)

        # Draw Outer Glow (Pulsing)
        current_radius = radius + (self.pulse * 5)
        gradient = QRadialGradient(center, current_radius)
        gradient.setColorAt(0, QColor(base_color.red(), base_color.green(), base_color.blue(), 150))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, current_radius, current_radius)
        
        # Draw Core
        painter.setBrush(QBrush(base_color))
        painter.drawEllipse(center, radius / 2, radius / 2)
        
        # Draw Rotating Ring
        painter.setBrush(Qt.NoBrush)
        pen = QPen(QColor(255, 255, 255, 200))
        pen.setWidth(2)
        painter.setPen(pen)
        
        painter.save()
        painter.translate(center)
        painter.rotate(self.angle)
        painter.drawArc(-radius + 5, -radius + 5, (radius - 5) * 2, (radius - 5) * 2, 0, 120 * 16)
        painter.drawArc(-radius + 5, -radius + 5, (radius - 5) * 2, (radius - 5) * 2, 180 * 16, 120 * 16)
        painter.restore()
