import tkinter as tk
from tkinter import Button
from src.analyzeUserColor import AnalyzeUserColor
import time
import math


class DynamicGradientFrame(tk.Canvas):
    """创建动态渐变画布"""

    def __init__(self, parent, colors=None, animation_speed=0.02, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.colors = colors or ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
        self.animation_speed = animation_speed
        self.offset = 0  # 动画偏移量
        self.is_animating = True

        self.bind("<Configure>", self._draw_gradient)
        self._start_animation()

    def _start_animation(self):
        """开始动画循环"""

        def animate():
            if self.is_animating:
                self.offset += self.animation_speed
                if self.offset > 1:
                    self.offset = 0
                self._draw_gradient()
            self.after(50, animate)  # 每50ms更新一次

        animate()

    def _draw_gradient(self, event=None):
        """绘制动态渐变背景"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1 or len(self.colors) < 2:
            return

        # 扩展颜色列表以支持平滑动画
        extended_colors = self.colors + self.colors

        # 计算每个颜色区段的宽度
        segment_width = width / (len(self.colors) - 1)

        for i in range(width):
            # 应用偏移量
            adjusted_i = (i + self.offset * width) % width

            # 确定当前像素在哪个颜色区段
            segment_index = int(adjusted_i / segment_width) % len(extended_colors)

            if segment_index >= len(extended_colors) - 1:
                color = extended_colors[-1]
            else:
                segment_pos = (adjusted_i % segment_width) / segment_width
                color1 = extended_colors[segment_index]
                color2 = extended_colors[segment_index + 1]
                color = self._interpolate_color(color1, color2, segment_pos)

            self.create_line(i, 0, i, height, tags=("gradient",), fill=color)

        self.lower("gradient")

    def _interpolate_color(self, color1, color2, ratio):
        """在两个颜色之间进行插值"""
        r1 = int(color1[1:3], 16)
        g1 = int(color1[3:5], 16)
        b1 = int(color1[5:7], 16)

        r2 = int(color2[1:3], 16)
        g2 = int(color2[3:5], 16)
        b2 = int(color2[5:7], 16)

        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)

        return f"#{r:02x}{g:02x}{b:02x}"

    def stop_animation(self):
        """停止动画"""
        self.is_animating = False