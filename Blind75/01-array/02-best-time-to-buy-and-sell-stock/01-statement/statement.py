from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class Statement(Scene):
    def construct(self):
        from components.typography import Typography, ITypography
        from components.screenTemplate import ScreenTemplate, IScreenTemplate

        typo: ITypography = Typography()
        self.camera.background_color = typo.bg()
        tracker: IScreenTemplate = ScreenTemplate(self, typo)
        
        # Color Theme Constants
        WHITE = typo.color_white()
        GRAY = typo.color_gray()
        GREEN = typo.color_green()
        RED = typo.color_red()
        BLUE = typo.color_blue()
        YELLOW = typo.color_yellow()
        
        # ==========================================
        # 1. SCREEN TITLE & DESCRIPTION
        # ==========================================
        tracker.screen_statement("Statement: Best Time to Buy and Sell Stock")

        # ==========================================
        # 2. PROBLEM STATEMENT & ARRAY
        # ==========================================
        statement_text = Text(
            "Find the maximum profit you can achieve by buying on one day\nand selling on a different day in the future.",
            font=typo.font_ui(), font_size=20, color=WHITE
        )
        statement_text.move_to(UP * 2.2)
        
        self.play(FadeIn(statement_text), run_time=1)
        self.wait(1)
        
        prices_label = Text("prices =", font=typo.font_code(), font_size=24, color=WHITE)
        prices_array = [7, 1, 5, 3, 6, 4]
        
        cells = VGroup()
        for idx, val in enumerate(prices_array):
            cell_bg = Square(side_length=0.7, color=WHITE, stroke_width=2)
            cell_val = Text(str(val), font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=16, color=GRAY).next_to(cell_bg, UP, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            cells.add(cell)
        
        cells.arrange(RIGHT, buff=0)
        array_group = VGroup(prices_label, cells).arrange(RIGHT, buff=0.5)
        array_group.next_to(statement_text, DOWN, buff=0.5)
        
        self.play(FadeIn(array_group, shift=UP * 0.3), run_time=1)
        self.wait(1)

        # ==========================================
        # 3. GRAPH VISUALIZATION
        # ==========================================
        axes = Axes(
            x_range=[-0.5, 5.5, 1],
            y_range=[0, 8, 2],
            x_length=7,
            y_length=3,
            axis_config={"color": GRAY, "include_numbers": False},
        )
        
        # Add Custom Numbers using Text to avoid LaTeX
        x_nums = VGroup(*[
            Text(str(i), font=typo.font_ui(), font_size=12, color=GRAY)
            .next_to(axes.x_axis.n2p(i), DOWN, buff=0.2)
            for i in range(6)
        ])
        y_nums = VGroup(*[
            Text(str(i), font=typo.font_ui(), font_size=12, color=GRAY)
            .next_to(axes.y_axis.n2p(i), LEFT, buff=0.2)
            for i in range(0, 9, 2)
        ])
        
        # Add titles to axes manually using Typography fonts to avoid missing font issues
        x_label = Text("Day", font=typo.font_ui(), font_size=16, color=GRAY).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("Price", font=typo.font_ui(), font_size=16, color=GRAY).next_to(axes.y_axis, UP, buff=0.1)
        axes_labels = VGroup(x_nums, y_nums, x_label, y_label)

        graph_group = VGroup(axes, axes_labels).next_to(array_group, DOWN, buff=0.5)
        self.play(Create(axes), FadeIn(axes_labels), run_time=1.5)
        
        # Plot points and lines
        points = [axes.coords_to_point(i, p) for i, p in enumerate(prices_array)]
        
        line_graph = VMobject()
        line_graph.set_points_as_corners(points)
        line_graph.set_stroke(color=BLUE, width=4)
        
        dots = VGroup(*[Dot(point, color=YELLOW, radius=0.08) for point in points])
        
        self.play(Create(line_graph), run_time=1.5)
        self.play(FadeIn(dots), run_time=0.5)
        self.wait(1)

        # ==========================================
        # 4. EXPLANATION: BUY LOW, SELL HIGH
        # ==========================================
        # Highlight Buy Day (Day 1, Price 1)
        buy_idx = 1
        buy_dot = dots[buy_idx]
        buy_cell = cells[buy_idx][0]
        
        buy_text = Text("Buy", font=typo.font_ui(), font_size=20, weight=BOLD, color=GREEN)
        buy_arrow = Arrow(start=DOWN, end=UP, color=GREEN, buff=0.1).scale(0.5)
        buy_arrow.next_to(buy_dot, DOWN)
        buy_text.next_to(buy_arrow, DOWN)
        buy_group = VGroup(buy_arrow, buy_text)
        
        self.play(
            buy_cell.animate.set_fill(GREEN, opacity=0.3).set_stroke(GREEN, width=4),
            FadeIn(buy_group, shift=UP*0.2),
            buy_dot.animate.set_color(GREEN).scale(1.5),
            run_time=1
        )
        self.wait(1)
        
        # Highlight Sell Day (Day 4, Price 6)
        sell_idx = 4
        sell_dot = dots[sell_idx]
        sell_cell = cells[sell_idx][0]
        
        sell_text = Text("Sell", font=typo.font_ui(), font_size=20, weight=BOLD, color=RED)
        sell_arrow = Arrow(start=UP, end=DOWN, color=RED, buff=0.1).scale(0.5)
        sell_arrow.next_to(sell_dot, UP)
        sell_text.next_to(sell_arrow, UP)
        sell_group = VGroup(sell_arrow, sell_text)
        
        self.play(
            sell_cell.animate.set_fill(RED, opacity=0.3).set_stroke(RED, width=4),
            FadeIn(sell_group, shift=DOWN*0.2),
            sell_dot.animate.set_color(RED).scale(1.5),
            run_time=1
        )
        self.wait(1)
        
        # Show profit calculation
        profit_line = DashedLine(
            start=axes.coords_to_point(sell_idx, prices_array[buy_idx]),
            end=axes.coords_to_point(sell_idx, prices_array[sell_idx]),
            color=GREEN,
            stroke_width=4
        )
        
        # Horizontal line from buy price to sell day
        horizontal_line = DashedLine(
            start=axes.coords_to_point(buy_idx, prices_array[buy_idx]),
            end=axes.coords_to_point(sell_idx, prices_array[buy_idx]),
            color=GRAY,
            stroke_width=2
        )
        
        self.play(Create(horizontal_line), run_time=1)
        self.play(Create(profit_line), run_time=1)
        
        profit_val = prices_array[sell_idx] - prices_array[buy_idx]
        profit_text = Text(f"Profit = {profit_val}", font=typo.font_code(), font_size=20, weight=BOLD, color=GREEN)
        profit_text.next_to(profit_line, RIGHT, buff=0.2)
        
        self.play(Write(profit_text), run_time=1)
        self.wait(2)

        # Clear explanation for next steps
        self.play(
            FadeOut(buy_group), FadeOut(sell_group), 
            FadeOut(horizontal_line), FadeOut(profit_line), FadeOut(profit_text),
            buy_cell.animate.set_fill(opacity=0).set_stroke(WHITE, width=2),
            sell_cell.animate.set_fill(opacity=0).set_stroke(WHITE, width=2),
            buy_dot.animate.set_color(YELLOW).scale(1/1.5),
            sell_dot.animate.set_color(YELLOW).scale(1/1.5),
            run_time=1
        )
        
        self.wait(1)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = Statement()
    scene.render()
