# 分析喜欢的颜色
import colorsys
import json
import os
import sys
import random

from src.colorConfig import color_table


class AnalyzeUserColor:
    def __init__(self):
        self.color_data = None

# -------------------加载Json-------------------
    def loadUserJson(self, path):
        try:
            # 获取完整的JSON文件路径
            json_path = self.get_relative_path("users/" + path)
            self.current_json_path = json_path  # 保存文件路径

            # 加载JSON文件
            with open(json_path, 'r', encoding='utf-8') as file:
                self.color_data = json.load(file)

            # 将JSON数据转换为对象属性
            self._create_attributes_from_json()

            print(f"成功加载JSON文件: {path}")
            return self.color_data

        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)

    def get_relative_path(self, relative_path):
        """获取相对路径的完整路径"""
        # 获取当前脚本文件的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建完整路径
        full_path = os.path.join(current_dir, relative_path)

        # 检查文件是否存在
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"文件不存在: {full_path}")

        return full_path

# 创建Json对象
    def _create_attributes_from_json(self):
        """将JSON数据转换为对象属性"""
        if not self.color_data:
            return

        # 为每个JSON键创建属性
        for category, values in self.color_data.items():
            if isinstance(values, dict):
                # 为嵌套字典创建子对象
                sub_obj = type(category.title(), (), values)()
                setattr(self, category, sub_obj)

                # 同时将子字典的属性直接设置为对象的属性
                for key, value in values.items():
                    attr_name = f"{category}_{key}"
                    setattr(self, attr_name, value)
            else:
                setattr(self, category, values)

    #------------------获取对应的值--------------------

    #颜色-用概率获取前三
    def get_top_colors_by_probability(self, count=1):
        """
        根据概率随机选择前count个不同的颜色
        值越大，被选中的概率越高
        """
        if not self.color_data or 'color' not in self.color_data:
            print("没有颜色数据")
            return []

        color_scores = self.color_data['color']

        # 检查是否有足够的颜色
        if len(color_scores) < count:
            print(f"颜色数量不足，只有 {len(color_scores)} 个颜色")
            return list(color_scores.keys())

        selected_colors = []

        # 复制颜色分数用于处理
        remaining_colors = color_scores.copy()

        for i in range(count):
            if not remaining_colors:
                break

            # 计算概率权重
            colors = list(remaining_colors.keys())
            weights = list(remaining_colors.values())

            # 根据权重随机选择
            selected_color = random.choices(colors, weights=weights, k=1)[0]
            selected_colors.append(selected_color)

            # 移除已选择的颜色，确保不重复
            del remaining_colors[selected_color]

        return selected_colors

    # 饱和度-用概率获取
    def get_random_sat_by_probability(self):
        """
        根据概率随机选择一个饱和度级别
        值越大，被选中的概率越高
        """
        if not self.color_data or 'sat' not in self.color_data:
            print("没有饱和度数据")
            return None

        print(f"饱和度数据--{self.color_data['sat']}")
        sat_scores = self.color_data['sat']

        # 计算概率权重
        sats = list(sat_scores.keys())
        weights = list(sat_scores.values())

        # 根据权重随机选择
        selected_sat = random.choices(sats, weights=weights, k=1)[0]
        return selected_sat

    # 色彩匹配-用概率获取
    def get_random_color_match_by_probability(self):
        """
        根据概率随机选择一个颜色匹配模式
        值越大，被选中的概率越高
        """
        if not self.color_data or 'color_match' not in self.color_data:
            print("没有颜色匹配数据")
            return None

        match_scores = self.color_data['color_match']

        # 计算概率权重
        matches = list(match_scores.keys())
        weights = list(match_scores.values())

        # 根据权重随机选择
        selected_match = random.choices(matches, weights=weights, k=1)[0]
        return selected_match

    # -------------------获取对应的rgb值，查表-------------------
    def get_color_rgb(self, color_name, saturation_level):
        """
        根据颜色名称和饱和度级别获取对应的RGB值

        Args:
            saturation_level: 饱和度级别 ("high", "medium", "low")

        Returns:
            RGB元组 或 None (如果找不到)
        """
        # 检查颜色是否存在
        if color_name not in color_table:
            print(f"错误: 不支持的颜色 '{color_name}'")
            return None

        # 检查饱和度级别是否存在
        if saturation_level not in color_table[color_name]:
            print(f"错误: 不支持的饱和度级别 '{saturation_level}'")
            return None

        return color_table[color_name][saturation_level]

    # -------------------色彩匹配的处理-------------------
    def get_color_match_handle(self, color_match, top_colors, sat):
        """
        根据颜色匹配类型处理颜色组合

        Args:
            color_match: 颜色匹配类型 (single_color, neighbor_color, complementary_color, tricolor)
            top_colors: 选中的颜色列表
            sat: 饱和度级别

        Returns:
            处理后的颜色组合和相关信息，包含RGB列表
        """
        if color_match == "single_color":
            result = self._handle_single_color(top_colors, sat)
        elif color_match == "neighbor_color":
            result = self._handle_neighbor_color(top_colors, sat)
        elif color_match == "complementary_color":
            result = self._handle_complementary_color(top_colors, sat)
        elif color_match == "tricolor":
            result = self._handle_tricolor(top_colors, sat)
        else:
            print(f"未知的颜色匹配类型: {color_match}")
            result = {"colors": top_colors, "type": "unknown"}

        return result

    def _handle_single_color(self, top_colors, sat,):
        """处理单色匹配 - 使用单一主色调
        Args:
            top_colors: 主颜色列表
            sat: 饱和度级别
            float_range: 饱和度和亮度浮动百分比，默认10%
        """
        if top_colors:
            main_color = top_colors[0]

            # 获取主色在当前饱和度下的RGB值
            main_rgb = self.get_color_rgb(main_color, sat)

            # 将RGB转换为HSV
            r, g, b = [x / 255.0 for x in main_rgb]
            h, s, v = colorsys.rgb_to_hsv(r, g, b)

            # 将色相转换为角度 (0-360度)
            h_deg = h * 360

            # 生成两个邻近色：色相加减15度
            h_range = 15

            # 将浮动百分比转换为小数
            float_range = 40
            float_factor = float_range / 100.0

            # 第一个邻近色：色相+n度，饱和度亮度浮动±n%
            h1 = (h_deg + h_range) % 360
            h1_normalized = h1 / 360.0
            # 饱和度和亮度在原本值的±n%范围内浮动
            s1 = max(0.0, min(1.0, s * (1 + random.uniform(-float_factor, float_factor))))
            v1 = v
            r1, g1, b1 = colorsys.hsv_to_rgb(h1_normalized, s1, v1)
            rgb1 = (int(r1 * 255), int(g1 * 255), int(b1 * 255))

            # 第二个邻近色：色相-n度，饱和度亮度浮动±n%
            h2 = (h_deg - h_range) % 360
            h2_normalized = h2 / 360.0
            # 饱和度和亮度在原本值的±n%范围内浮动
            s2 = max(0.0, min(1.0, s * (1 + random.uniform(-float_factor, float_factor))))
            v2 = v
            r2, g2, b2 = colorsys.hsv_to_rgb(h2_normalized, s2, v2)
            rgb2 = (int(r2 * 255), int(g2 * 255), int(b2 * 255))

            # 颜色排序
            rgb_list = [rgb1, main_rgb, rgb2]

            return rgb_list
        return []

    def _handle_neighbor_color(self, top_colors, sat):
        """处理邻近色匹配 - 使用色轮上相邻的颜色"""
        color_wheel = ["red", "orange", "yellow", "green", "aqua", "blue", "purple"]

        if top_colors:
            main_color = top_colors[0]
            main_index = color_wheel.index(main_color) if main_color in color_wheel else 0

            # 获取邻近色（包括自身和相邻颜色）
            neighbor_colors = [main_color]

            # 随机选择向左或向右的邻近色
            offset = random.choice([-1, 1])*2
            neighbor_index = (main_index + offset) % len(color_wheel)
            neighbor_color = color_wheel[neighbor_index]
            if neighbor_color not in neighbor_colors:
                neighbor_colors.append(neighbor_color)

            # 转换为RGB列表
            rgb_list = []
            for color in neighbor_colors[:2]:  # 只取前2个颜色
                rgb = self.get_color_rgb(color, sat)
                if rgb:
                    rgb_list.append(rgb)

            return rgb_list
        return []

    def _handle_complementary_color(self, top_colors, sat):
        """处理互补色匹配 - 使用色轮上相对的颜色"""
        if top_colors:
            main_color = top_colors[0]

            # 获取主色在当前饱和度下的RGB值
            main_rgb = self.get_color_rgb(main_color, sat)

            # 将RGB转换为HSV
            r, g, b = [x / 255.0 for x in main_rgb]
            h, s, v = colorsys.rgb_to_hsv(r, g, b)

            # 将色相转换为角度 (0-360度)
            h_deg = h * 360

            # 生成色：色相加减
            h_range =  random.choice([-1, 1])* random.randint(135,180)

            # 将浮动百分比转换为小数
            float_range = 20
            float_factor = float_range / 100.0

            # 第一个邻近色：色相+n度，饱和度亮度浮动±n%
            h1 = (h_deg + h_range) % 360
            h1_normalized = h1 / 360.0
            # 饱和度和亮度在原本值的±n%范围内浮动
            s1 = max(0.0, min(1.0, s * (1 + random.uniform(-float_factor, float_factor))))
            v1 = max(0.0, min(1.0, v * (1 + random.uniform(-float_factor, float_factor))))
            r1, g1, b1 = colorsys.hsv_to_rgb(h1_normalized, s1, v1)
            rgb1 = (int(r1 * 255), int(g1 * 255), int(b1 * 255))



            # 颜色排序
            rgb_list = [ main_rgb, rgb1]

            return rgb_list
        return []

    def _handle_tricolor(self, top_colors, sat):
        """处理三色匹配 - 使用三种协调的颜色"""
        if top_colors:
            main_color = top_colors[0]

            # 获取主色在当前饱和度下的RGB值
            main_rgb = self.get_color_rgb(main_color, sat)

            # 将RGB转换为HSV
            r, g, b = [x / 255.0 for x in main_rgb]
            h, s, v = colorsys.rgb_to_hsv(r, g, b)

            # 将色相转换为角度 (0-360度)
            h_deg = h * 360

            # 生成两个邻近色：色相加减15度
            h_range = random.randint(120-20,120+20)

            # 将浮动百分比转换为小数
            float_range = 40
            float_factor = float_range / 100.0

            # 第一个邻近色：色相+n度，饱和度亮度浮动±n%
            h1 = (h_deg + h_range) % 360
            h1_normalized = h1 / 360.0
            # 饱和度和亮度在原本值的±n%范围内浮动
            s1 = max(0.0, min(1.0, s * (1 + random.uniform(-float_factor, float_factor))))
            v1 = v
            r1, g1, b1 = colorsys.hsv_to_rgb(h1_normalized, s1, v1)
            rgb1 = (int(r1 * 255), int(g1 * 255), int(b1 * 255))

            # 第二个邻近色：色相-n度，饱和度亮度浮动±n%
            h2 = (h_deg - h_range) % 360
            h2_normalized = h2 / 360.0
            # 饱和度和亮度在原本值的±n%范围内浮动
            s2 = max(0.0, min(1.0, s * (1 + random.uniform(-float_factor, float_factor))))
            v2 = v
            r2, g2, b2 = colorsys.hsv_to_rgb(h2_normalized, s2, v2)
            rgb2 = (int(r2 * 255), int(g2 * 255), int(b2 * 255))

            # 颜色排序
            rgb_list = [rgb1, main_rgb, rgb2]

            return rgb_list
        return []
    # -------------------处理-最终色彩结果-------------------
    def get_color_result(self):
        top_colors = self.get_top_colors_by_probability(1)  # 只选一个主色
        random_sat = self.get_random_sat_by_probability()
        random_match = self.get_random_color_match_by_probability()
        print(f"-----------------新颜色----------------------------------------")
        print(f"选中的主色: {top_colors}")
        print(f"选中的饱和度: {random_sat}")
        print(f"选中色彩匹配: {random_match}")

        # 处理颜色匹配
        match_result = self.get_color_match_handle(random_match, top_colors, random_sat)
        print(f"RGB列表: {match_result}")

        # 记录这次选择
        self.set_last_selection(top_colors[0], random_sat, random_match)
        # 只返回RGB列表
        return match_result

    # -------------------喜欢与不喜欢的处理-------------------
    def likeColor(self):
        """
        喜欢当前颜色方案，将选中的颜色、饱和度、色彩匹配都加10分
        分数最高为其他值相加的分的60%
        """
        if not hasattr(self, 'last_selection'):
            print("没有最近的选择记录")
            return False

        try:
            # 获取最近的选择
            colors = self.last_selection.get('colors', [])
            selected_sat = self.last_selection.get('saturation')
            selected_color_match = self.last_selection.get('color_match')

            rate = 1.5  # 最高分数为其他值相加的分的平均分 的60%
            score = 45 #加分

            # 为选中的颜色加分
            # 确保colors是列表格式
            if isinstance(colors, str):
                colors_list = [colors]
            else:
                colors_list = colors

            for color in colors_list:
                if color in self.color_data['color']:
                    # 计算其他颜色的总分（排除当前颜色）
                    other_colors_total = sum(score for col, score in self.color_data['color'].items() if col != color)
                    color_max_score = int(other_colors_total/ (len(self.color_data['color'])-1) * rate)

                    current_score = self.color_data['color'][color]
                    new_score = min(current_score + score, color_max_score)
                    self.color_data['color'][color] = new_score
                    print(
                        f"颜色 {color} 分数: {current_score} -> {new_score} (上限: {color_max_score}, 其他颜色总分: {other_colors_total})")

            # 为饱和度加分
            if selected_sat and selected_sat in self.color_data['sat']:
                # 计算其他饱和度的总分（排除当前饱和度）
                other_sat_total = sum(score for s, score in self.color_data['sat'].items() if s != selected_sat)
                sat_max_score = int(other_sat_total/ (len(self.color_data['sat'])-1) * rate)

                current_score = self.color_data['sat'][selected_sat]
                new_score = min(current_score + score, sat_max_score)
                self.color_data['sat'][selected_sat] = new_score
                print(
                    f"饱和度 {selected_sat} 分数: {current_score} -> {new_score} (上限: {sat_max_score}, 其他饱和度总分: {other_sat_total})")

            # 为色彩匹配加分
            if selected_color_match and selected_color_match in self.color_data['color_match']:
                # 计算其他色彩匹配的总分（排除当前色彩匹配）
                other_match_total = sum(
                    score for cm, score in self.color_data['color_match'].items() if cm != selected_color_match)
                match_max_score = int(other_match_total/ (len(self.color_data['color_match'])-1) * rate)

                current_score = self.color_data['color_match'][selected_color_match]
                new_score = min(current_score + score, match_max_score)
                self.color_data['color_match'][selected_color_match] = new_score
                print(
                    f"色彩匹配 {selected_color_match} 分数: {current_score} -> {new_score} (上限: {match_max_score}, 其他匹配总分: {other_match_total})")

            # 保存到JSON文件
            self._save_to_json()
            print("喜欢操作完成，数据已保存")
            return True

        except Exception as e:
            print(f"喜欢操作出错: {e}")
            return False

    def unLikeColor(self):
        """
        不喜欢当前颜色方案，将选中的颜色、饱和度、色彩匹配都减10分
        分数最低为10分
        """
        if not hasattr(self, 'last_selection'):
            print("没有最近的选择记录")
            return False

        try:
            # 获取最近的选择
            colors = self.last_selection.get('colors', [])
            selected_sat = self.last_selection.get('saturation')
            selected_color_match = self.last_selection.get('color_match')

            # 最低分数限制
            min_score = 25
            score = 60  # 减分

            # 为选中的颜色减分
            # 确保colors是列表格式
            if isinstance(colors, str):
                colors_list = [colors]
            else:
                colors_list = colors

            for color in colors_list:
                if color in self.color_data['color']:
                    current_score = self.color_data['color'][color]
                    new_score = max(current_score - score, min_score)
                    self.color_data['color'][color] = new_score
                    print(f"颜色 {color} 分数: {current_score} -> {new_score}")

            # 为饱和度减分
            if selected_sat and selected_sat in self.color_data['sat']:
                current_score = self.color_data['sat'][selected_sat]
                new_score = max(current_score - score, min_score)
                self.color_data['sat'][selected_sat] = new_score
                print(f"饱和度 {selected_sat} 分数: {current_score} -> {new_score}")

            # 为色彩匹配减分
            if selected_color_match and selected_color_match in self.color_data['color_match']:
                current_score = self.color_data['color_match'][selected_color_match]
                new_score = max(current_score - score, min_score)
                self.color_data['color_match'][selected_color_match] = new_score
                print(f"色彩匹配 {selected_color_match} 分数: {current_score} -> {new_score}")

            # 保存到JSON文件
            self._save_to_json()
            print("不喜欢操作完成，数据已保存")
            return True

        except Exception as e:
            print(f"不喜欢操作出错: {e}")
            return False
    def _save_to_json(self):
        """保存数据到原来的JSON文件"""
        try:
            # 获取当前加载的JSON文件路径
            if not hasattr(self, 'current_json_path'):
                print("没有找到JSON文件路径")
                return False

            # 写入JSON文件
            with open(self.current_json_path, 'w', encoding='utf-8') as file:
                json.dump(self.color_data, file, ensure_ascii=False, indent=2)

            print(f"数据已保存到: {self.current_json_path}")
            return True

        except Exception as e:
            print(f"保存JSON文件出错: {e}")
            return False

    def set_last_selection(self, colors, saturation, color_match):
        """
        设置最近的选择记录
        """
        self.last_selection = {
            'colors': colors,
            'saturation': saturation,
            'color_match': color_match
        }
    # -------------------打印数据-------------------
    def print_clean_data(self):
        """简洁打印数据"""
        if hasattr(self, 'color_data'):
            data = self.color_data
            print("颜色分数:")
            for color, score in data.get('color', {}).items():
                print(f"  {color}: {score}")

            print("\n饱和度分数:")
            for sat, score in data.get('sat', {}).items():
                print(f"  {sat}: {score}")

            print("\n颜色匹配分数:")
            for match, score in data.get('color_match', {}).items():
                print(f"  {match}: {score}")

# 使用示例
if __name__ == "__main__":
    analyzer = AnalyzeUserColor()

    # 加载JSON文件
    analyzer.loadUserJson("myUser.json")  # 替换为你的JSON文件名

    # 显示数据
    # analyzer.print_clean_data()

    print("\n=== 概率随机选择结果 ===")

    # 直接获取RGB列表
    rgb_list = analyzer.get_color_result()
    print(f"生成的RGB列表: {rgb_list}")

