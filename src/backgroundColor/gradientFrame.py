import tkinter as tk

class GradientFrame(tk.Canvas):
    """创建一个支持多色渐变的画布"""

    def __init__(self, parent, colors=None, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.colors = colors or ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        """绘制多色渐变背景"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1 or len(self.colors) < 2:
            return

        # 计算每个颜色区段的宽度
        segment_width = width / (len(self.colors) - 1)

        # 为每个像素位置计算颜色
        for i in range(width):
            # 确定当前像素在哪个颜色区段
            segment_index = int(i / segment_width)

            if segment_index >= len(self.colors) - 1:
                # 最后一个像素，使用最后一个颜色
                color = self.colors[-1]
            else:
                # 计算在当前区段内的位置比例 (0到1)
                segment_pos = (i % segment_width) / segment_width

                # 获取当前区段的两个颜色
                color1 = self.colors[segment_index]
                color2 = self.colors[segment_index + 1]

                # 计算渐变颜色
                color = self._interpolate_color(color1, color2, segment_pos)

            # 绘制垂直线
            self.create_line(i, 0, i, height, tags=("gradient",), fill=color)

        self.lower("gradient")

    def _interpolate_color(self, color1, color2, ratio):
        """在两个颜色之间进行插值"""
        # 将颜色从16进制转换为RGB
        r1 = int(color1[1:3], 16)
        g1 = int(color1[3:5], 16)
        b1 = int(color1[5:7], 16)

        r2 = int(color2[1:3], 16)
        g2 = int(color2[3:5], 16)
        b2 = int(color2[5:7], 16)

        # 线性插值
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)

        return f"#{r:02x}{g:02x}{b:02x}"

