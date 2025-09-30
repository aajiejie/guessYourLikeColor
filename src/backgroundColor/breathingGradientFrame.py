import tkinter as tk
class BreathingGradientFrame(tk.Canvas):
    """呼吸灯效果的渐变背景"""

    def __init__(self, parent, colors=None, breath_speed=0.05, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.base_colors = colors or ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
        self.breath_speed = breath_speed
        self.breath_intensity = 0
        self.breath_direction = 1
        self.is_animating = True

        self.bind("<Configure>", self._draw_gradient)
        self._start_breathing()

    def _start_breathing(self):
        """开始呼吸效果动画"""

        def breathe():
            if self.is_animating:
                self.breath_intensity += self.breath_direction * self.breath_speed

                if self.breath_intensity >= 1:
                    self.breath_intensity = 1
                    self.breath_direction = -1
                elif self.breath_intensity <= 0:
                    self.breath_intensity = 0
                    self.breath_direction = 1

                self._draw_gradient()
            self.after(60, breathe)

        breathe()

    def _draw_gradient(self, event=None):
        """绘制呼吸效果的渐变"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1 or len(self.base_colors) < 2:
            return

        # 根据呼吸强度调整颜色亮度
        adjusted_colors = self._adjust_colors_brightness(self.base_colors, self.breath_intensity)

        segment_width = width / (len(adjusted_colors) - 1)

        for i in range(width):
            segment_index = int(i / segment_width)

            if segment_index >= len(adjusted_colors) - 1:
                color = adjusted_colors[-1]
            else:
                segment_pos = (i % segment_width) / segment_width
                color1 = adjusted_colors[segment_index]
                color2 = adjusted_colors[segment_index + 1]
                color = self._interpolate_color(color1, color2, segment_pos)

            self.create_line(i, 0, i, height, tags=("gradient",), fill=color)

        self.lower("gradient")

    def _adjust_colors_brightness(self, colors, intensity):
        """根据强度调整颜色亮度"""
        adjusted = []
        for color in colors:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            # 呼吸效果：在原始亮度和稍暗之间变化
            factor = 0.7 + 0.3 * intensity
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))

            adjusted.append(f"#{r:02x}{g:02x}{b:02x}")
        return adjusted

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