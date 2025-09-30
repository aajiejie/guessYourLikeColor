import math
import tkinter as tk
class WaveGradientFrame(tk.Canvas):
    """波浪效果的渐变背景"""

    def __init__(self, parent, colors=None, wave_speed=0.03, wave_frequency=0.02, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.colors = colors or ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
        self.wave_speed = wave_speed
        self.wave_frequency = wave_frequency
        self.wave_offset = 0
        self.is_animating = True

        self.bind("<Configure>", self._draw_gradient)
        self._start_wave()

    def _start_wave(self):
        """开始波浪效果动画"""

        def wave():
            if self.is_animating:
                self.wave_offset += self.wave_speed
                self._draw_gradient()
            self.after(40, wave)

        wave()

    def _draw_gradient(self, event=None):
        """绘制波浪效果的渐变"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1 or len(self.colors) < 2:
            return

        segment_width = width / (len(self.colors) - 1)

        for i in range(width):
            # 添加波浪效果
            wave_effect = math.sin(i * self.wave_frequency + self.wave_offset) * 10

            adjusted_i = (i + wave_effect) % width

            segment_index = int(adjusted_i / segment_width)

            if segment_index >= len(self.colors) - 1:
                color = self.colors[-1]
            else:
                segment_pos = (adjusted_i % segment_width) / segment_width
                color1 = self.colors[segment_index]
                color2 = self.colors[segment_index + 1]
                color = self._interpolate_color(color1, color2, segment_pos)

            self.create_line(i, 0, i, height, tags=("gradient",), fill=color)

        self.lower("gradient")

    def _interpolate_color(self, color1, color2, ratio):
        """颜色插值（同前）"""
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