from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class UIConfig:
    @staticmethod
    def configure_label(label, is_title=False):
        if is_title:
            label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            label.setFont(QFont("Arial", 12))
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    @staticmethod
    def configure_control(control):
        control.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    @staticmethod
    def configure_canvas(canvas):
        canvas.setFixedHeight(600)  # Increased height for larger graphs
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    @staticmethod
    def configure_layout(layout):
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
