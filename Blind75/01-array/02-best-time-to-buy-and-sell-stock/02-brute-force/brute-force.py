from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class BruteForce(Scene):
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
        
        tracker.screen_brute_force("Brute Force")

        # ==========================================
        # 1. LAYOUT SETUP
        # ==========================================
        prices_array = [7, 1, 5, 3, 6, 4]
        
        cells = VGroup()
        for idx, val in enumerate(prices_array):
            cell_bg = Square(side_length=0.7, color=WHITE, stroke_width=2)
            cell_val = Text(str(val), font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=20, color="#B3B3B3").next_to(cell_bg, UP, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            cells.add(cell)
        
        cells.arrange(RIGHT, buff=0).move_to(UP * 1.5 + LEFT * 2)
        
        axes = Axes(
            x_range=[-0.5, 5.5, 1],
            y_range=[0, 8, 2],
            x_length=6,
            y_length=2.5,
            axis_config={"color": WHITE, "include_numbers": False},
        )
        
        x_nums = VGroup(*[
            Text(str(i), font=typo.font_ui(), font_size=12, color=WHITE).next_to(axes.x_axis.n2p(i), DOWN, buff=0.2)
            for i in range(6)
        ])
        y_nums = VGroup(*[
            Text(str(i), font=typo.font_ui(), font_size=12, color=WHITE).next_to(axes.y_axis.n2p(i), LEFT, buff=0.2)
            for i in range(0, 9, 2)
        ])
        
        x_label = Text("Day", font=typo.font_ui(), font_size=16, color=WHITE).next_to(axes.x_axis, RIGHT, buff=0.4)
        y_label = Text("Price", font=typo.font_ui(), font_size=16, color=WHITE).next_to(axes.y_axis, UP, buff=0.3)
        axes_labels = VGroup(x_nums, y_nums, x_label, y_label)

        graph_group = VGroup(axes, axes_labels).next_to(cells, DOWN, buff=0.8)
        
        points = [axes.coords_to_point(i, p) for i, p in enumerate(prices_array)]
        line_graph = VMobject()
        line_graph.set_points_as_corners(points)
        line_graph.set_stroke(color=BLUE, width=4)
        dots = VGroup(*[Dot(point, color=YELLOW, radius=0.08) for point in points])
        
        # Max Profit Tracker
        max_profit_box = RoundedRectangle(corner_radius=0.1, width=2.5, height=1.2, color=GRAY, stroke_width=2)
        max_profit_box.move_to(RIGHT * 3.5 + UP * 1)
        max_profit_title = Text("Max Profit", font=typo.font_ui(), font_size=20, color=GRAY).next_to(max_profit_box, UP, buff=0.1)
        max_profit_val = Text("0", font=typo.font_code(), font_size=36, color=GREEN).move_to(max_profit_box.get_center())
        
        tracker_group = VGroup(max_profit_box, max_profit_title, max_profit_val)

        # Algorithm Text
        algo_text = Text(
            "Try all pairs (i, j) where j > i\nProfit = prices[j] - prices[i]",
            font=typo.font_code(), font_size=16, color=WHITE
        ).next_to(max_profit_box, DOWN, buff=0.5)

        self.play(
            FadeIn(cells), Create(axes), FadeIn(axes_labels), 
            Create(line_graph), FadeIn(dots),
            FadeIn(tracker_group), FadeIn(algo_text),
            run_time=1.5
        )
        self.wait(1)

        # ==========================================
        # 2. SIMULATION LOGIC
        # ==========================================
        i_arrow = Triangle(color=BLUE).scale(0.15).set_fill(BLUE, opacity=1)
        i_label = Text("i (Buy)", font=typo.font_code(), font_size=16, color=BLUE).next_to(i_arrow, DOWN)
        i_ptr = VGroup(i_arrow, i_label)
        
        j_arrow = Triangle(color=RED).scale(0.15).set_fill(RED, opacity=1).rotate(PI)
        j_label = Text("j (Sell)", font=typo.font_code(), font_size=16, color=RED).next_to(j_arrow, UP)
        j_ptr = VGroup(j_arrow, j_label)
        
        current_max = 0
        
        # All possible pairs (i, j) where i < j
        all_pairs = [(i, j) for i in range(len(prices_array)) for j in range(i + 1, len(prices_array))]
        
        profit_calc = Text("", font=typo.font_code(), font_size=20, color=WHITE).next_to(algo_text, DOWN, buff=0.5)
        
        for idx_pair, (i, j) in enumerate(all_pairs):
            if idx_pair == 0:
                i_ptr.next_to(cells[i][0], DOWN, buff=0.3)
                j_ptr.next_to(cells[j][0], UP, buff=0.48)
                self.play(
                    FadeIn(i_ptr), cells[i][0].animate.set_fill(BLUE, opacity=0.3),
                    FadeIn(j_ptr), cells[j][0].animate.set_fill(RED, opacity=0.3),
                    run_time=0.4
                )
            else:
                anims = []
                # Remove old fills
                for k in range(len(prices_array)):
                    anims.append(cells[k][0].animate.set_fill(opacity=0))
                
                # Move pointers
                anims.append(i_ptr.animate.next_to(cells[i][0], DOWN, buff=0.3))
                anims.append(cells[i][0].animate.set_fill(BLUE, opacity=0.3))
                anims.append(j_ptr.animate.next_to(cells[j][0], UP, buff=0.48))
                anims.append(cells[j][0].animate.set_fill(RED, opacity=0.3))
                
                self.play(*anims, run_time=0.35)
            
            # Show Profit on Graph
            buy_val = prices_array[i]
            sell_val = prices_array[j]
            profit = sell_val - buy_val
            
            p_color = GREEN if profit > 0 else RED
            
            # Connect the two dots on graph
            graph_line = DashedLine(
                start=axes.coords_to_point(i, buy_val),
                end=axes.coords_to_point(j, sell_val),
                color=p_color, stroke_width=3
            )
            self.play(Create(graph_line), run_time=0.25)
            
            # Show calculation
            new_calc = Text(f"Profit: {sell_val} - {buy_val} = {profit}", font=typo.font_code(), font_size=20, color=p_color)
            
            if idx_pair == 0:
                new_calc.next_to(algo_text, DOWN, buff=0.5)
                self.play(FadeIn(new_calc), run_time=0.25)
            else:
                new_calc.move_to(profit_calc.get_center())
                self.play(ReplacementTransform(profit_calc, new_calc), run_time=0.25)
            profit_calc = new_calc
            
            if profit > current_max:
                current_max = profit
                self.play(Indicate(profit_calc, color=GREEN), run_time=0.35)
                
                new_max_val = Text(str(current_max), font=typo.font_code(), font_size=36, color=GREEN).move_to(max_profit_box.get_center())
                self.play(ReplacementTransform(max_profit_val, new_max_val), run_time=0.4)
                max_profit_val = new_max_val
            else:
                self.wait(0.2)
                
            self.play(FadeOut(graph_line), run_time=0.15)

        # Clear simulation elements
        self.play(
            FadeOut(i_ptr), FadeOut(j_ptr), FadeOut(profit_calc),
            *[cells[k][0].animate.set_fill(opacity=0) for k in range(len(prices_array))],
            run_time=0.8
        )
        
        # ==========================================
        # 4. COMPLEXITY ANALYSIS
        # ==========================================
        tracker.show_lower_third("Complexity Analysis", "Time: O(N²), Space: O(1)", color_type="red", position="right")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = BruteForce()
    scene.render()
