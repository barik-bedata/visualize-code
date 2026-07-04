from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class Optimal(Scene):
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
        
        tracker.screen_optimal_approach("Optimal Approach")

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
            x_range=[-0.8, 5.5, 1],
            y_range=[-0.8, 9.5, 2],
            x_length=6.3,
            y_length=3.0,
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
        
        # Trackers Box
        tracker_box = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.8, color=WHITE, stroke_width=2)
        tracker_box.move_to(RIGHT * 3.5 + UP * 1)
        
        min_price_title = Text("MinPrice: ", font=typo.font_ui(), font_size=16, color=WHITE)
        min_price_val = Text("∞", font=typo.font_code(), font_size=28, color=RED)
        min_group = VGroup(min_price_title, min_price_val).arrange(RIGHT, buff=0.15)
        
        max_profit_title = Text("MaxProfit: ", font=typo.font_ui(), font_size=16, color=WHITE)
        max_profit_val = Text("0", font=typo.font_code(), font_size=28, color=GREEN)
        max_group = VGroup(max_profit_title, max_profit_val).arrange(RIGHT, buff=0.15)
        
        trackers = VGroup(min_group, max_group).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        trackers.move_to(tracker_box.get_center())

        self.play(
            FadeIn(cells), Create(axes), FadeIn(axes_labels), 
            Create(line_graph), FadeIn(dots),
            FadeIn(tracker_box), FadeIn(trackers),
            run_time=1.5
        )
        self.wait(1)

        # ==========================================
        # 2. SIMULATION LOGIC
        # ==========================================
        i_arrow = Triangle(color=BLUE).scale(0.15).set_fill(BLUE, opacity=1)
        i_label = Text("i", font=typo.font_code(), font_size=16, color=BLUE).next_to(i_arrow, DOWN)
        i_ptr = VGroup(i_arrow, i_label)
        
        current_min = float('inf')
        current_max = 0
        
        min_line = None
        
        for i in range(len(prices_array)):
            p = prices_array[i]
            
            # Move pointer
            if i == 0:
                i_ptr.next_to(cells[i][0], DOWN, buff=0.3)
                self.play(FadeIn(i_ptr), cells[i][0].animate.set_fill(BLUE, opacity=0.3), run_time=0.5)
            else:
                self.play(
                    i_ptr.animate.next_to(cells[i][0], DOWN, buff=0.3),
                    cells[i-1][0].animate.set_fill(opacity=0),
                    cells[i][0].animate.set_fill(BLUE, opacity=0.3),
                    run_time=0.5
                )
            
            # Highlight current point
            self.play(Indicate(dots[i], color=BLUE, scale_factor=2), run_time=0.4)
            
            # Update min_price
            if p < current_min:
                current_min = p
                new_min_val = Text(str(current_min), font=typo.font_code(), font_size=28, color=RED).move_to(min_price_val.get_center())
                
                new_min_line = DashedLine(
                    start=axes.c2p(-0.8, current_min),
                    end=axes.c2p(5.5, current_min),
                    color=RED, stroke_width=2
                )
                
                if min_line is None:
                    self.play(
                        ReplacementTransform(min_price_val, new_min_val),
                        Create(new_min_line),
                        run_time=0.5
                    )
                else:
                    self.play(
                        ReplacementTransform(min_price_val, new_min_val),
                        ReplacementTransform(min_line, new_min_line),
                        run_time=0.5
                    )
                min_price_val = new_min_val
                min_line = new_min_line
                
            # Calculate profit
            profit = p - current_min
            
            if profit > 0:
                profit_segment = Line(
                    start=axes.c2p(i, current_min),
                    end=axes.c2p(i, p),
                    color=GREEN, stroke_width=6
                )
                self.play(Create(profit_segment), run_time=0.4)
                
                if profit > current_max:
                    current_max = profit
                    new_max_val = Text(str(current_max), font=typo.font_code(), font_size=28, color=GREEN).move_to(max_profit_val.get_center())
                    self.play(ReplacementTransform(max_profit_val, new_max_val), Indicate(profit_segment, color=WHITE), run_time=0.5)
                    max_profit_val = new_max_val
                
                self.play(FadeOut(profit_segment), run_time=0.3)
            else:
                self.wait(0.4)

        # ==========================================
        # 3. CONCLUSION
        # ==========================================
        anims_clean = [
            FadeOut(i_ptr),
            cells[-1][0].animate.set_fill(opacity=0)
        ]
        if min_line is not None:
            anims_clean.append(FadeOut(min_line))
            
        self.play(*anims_clean, run_time=1)
        
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(1)", color_type="green", position="right")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = Optimal()
    scene.render()
