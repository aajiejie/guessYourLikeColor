import tkinter as tk
from tkinter import Button
from src.analyzeUserColor import AnalyzeUserColor
from src.backgroundColor.breathingGradientFrame import BreathingGradientFrame
from src.backgroundColor.dynamicGradientFrame import DynamicGradientFrame
from src.backgroundColor.gradientFrame import GradientFrame
from src.backgroundColor.waveGradientFrame import WaveGradientFrame


class App:
    def __init__(self, root, analyzer):
        self.root = root
        self.analyzer = analyzer
        self.root.title("Guess you like colors.")
        self.root.geometry("600x400")

        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 获取初始颜色方案
        self._generate_new_scheme()

        # 创建渐变色背景效果
        self.gradient_frame = GradientFrame(
            root,
            colors=self.current_colors,

        )

        # 创建扫描背景效果
        # self.gradient_frame = DynamicGradientFrame(  # 或者 BreathingGradientFrame / WaveGradientFrame
        #     root,
        #     colors=self.current_colors,
        #     animation_speed=0.02,  # 调整速度
        #     highlightthickness=0
        # )

        # 创建呼吸背景效果
        # self.gradient_frame = BreathingGradientFrame(  # 或者 BreathingGradientFrame / WaveGradientFrame
        #     root,
        #     colors=self.current_colors,
        # )

        # 创建波浪背景效果
        # self.gradient_frame = WaveGradientFrame(  # 或者 BreathingGradientFrame / WaveGradientFrame
        #     root,
        #     colors=self.current_colors,
        # )
        self.gradient_frame.pack(fill=tk.BOTH, expand=True)

        # 创建UI元素
        self._create_ui()

    def _rgb_to_hex(self, rgb):
        """将RGB元组转换为十六进制颜色"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def _generate_new_scheme(self):
        """生成新的颜色方案"""
        try:
            self.rgb_list = self.analyzer.get_color_result()
            print(f"生成的RGB列表: {self.rgb_list}")

            # 确保有足够的颜色进行渐变
            if len(self.rgb_list) < 2:
                # 如果颜色不足，复制最后一个颜色来补足
                while len(self.rgb_list) < 3:
                    self.rgb_list.append(self.rgb_list[-1] if self.rgb_list else (255, 255, 255))

            self.current_colors = [self._rgb_to_hex(rgb) for rgb in self.rgb_list]

        except Exception as e:
            print(f"生成颜色方案时出错: {e}")
            # 使用默认颜色作为备选
            self.current_colors = ["#FF0000", "#00FF00", "#0000FF"]

    def _create_text_with_outline(self, x, y, text, font, text_color="white", outline_color="#808080" , outline_width=1):
        """创建带黑边的文字"""
        # 创建黑边效果 - 在8个方向创建轮廓
        directions = [(-outline_width, -outline_width), (-outline_width, 0), (-outline_width, outline_width),
                      (0, -outline_width), (0, outline_width),
                      (outline_width, -outline_width), (outline_width, 0), (outline_width, outline_width)]

        outline_ids = []
        for dx, dy in directions:
            outline_id = self.gradient_frame.create_text(
                x + dx, y + dy,
                text=text,
                font=font,
                fill=outline_color,
                anchor=tk.CENTER
            )
            outline_ids.append(outline_id)

        # 创建主文字
        text_id = self.gradient_frame.create_text(
            x, y,
            text=text,
            font=font,
            fill=text_color,
            anchor=tk.CENTER
        )
        return text_id, outline_ids

    def _create_ui(self):
        """创建UI元素"""

        # 创建标题（带黑边）
        self.title_id, self.title_outline_ids = self._create_text_with_outline(
            300, 120,
            "Do you like the color?",
            ("Arial", 30, "bold"),

        )

        # 左侧按钮 - 喜欢颜色方案
        self.left_button = Button(
            self.gradient_frame,
            text="Yes, I like it",
            command=self.like_scheme,
            bg="#4CAF50",  # 绿色背景
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.gradient_frame.create_window(200, 250, window=self.left_button)

        # 右侧按钮 - 不喜欢颜色方案
        self.right_button = Button(
            self.gradient_frame,
            text="No, I don't like it",
            command=self.unlike_scheme,
            bg="#F44336",  # 红色背景
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.gradient_frame.create_window(400, 250, window=self.right_button)

        # 颜色数值显示 - 保存ID以便后续更新（带黑边）
        self.color_text_id, self.color_outline_ids = self._create_text_with_outline(
            300, 180,
            f"colors: {self.rgb_list}",
            ("Arial", 10, "bold"),

        )

    def _update_color_display(self):
        """更新颜色数值显示（包括黑边）"""
        new_text = f"colors: {self.rgb_list}"

        # 更新所有黑边文字
        for outline_id in self.color_outline_ids:
            self.gradient_frame.itemconfig(outline_id, text=new_text)

        # 更新主文字
        self.gradient_frame.itemconfig(self.color_text_id, text=new_text)

    def like_scheme(self):
        """喜欢当前颜色方案"""
        # 先保存用户偏好
        self.analyzer.likeColor()
        # 再生成新的颜色方案
        self._generate_new_scheme()
        self.gradient_frame.colors = self.current_colors
        self.gradient_frame._draw_gradient()
        # 更新颜色数值显示
        self._update_color_display()

    def unlike_scheme(self):
        """不喜欢当前颜色方案"""
        # 先保存用户偏好
        self.analyzer.unLikeColor()
        # 再生成新的颜色方案
        self._generate_new_scheme()
        self.gradient_frame.colors = self.current_colors
        self.gradient_frame._draw_gradient()
        # 更新颜色数值显示
        self._update_color_display()

    def on_closing(self):
        """处理窗口关闭事件"""
        print("应用程序关闭")
        self.root.destroy()


if __name__ == "__main__":
    try:
        analyzer = AnalyzeUserColor()
        # 加载JSON文件
        analyzer.loadUserJson("myUser.json")

        root = tk.Tk()
        app = App(root, analyzer)
        root.mainloop()

    except KeyboardInterrupt:
        print("程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")