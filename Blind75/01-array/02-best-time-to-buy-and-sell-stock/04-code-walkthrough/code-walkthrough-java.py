from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class WalkthroughJava(Scene):
    def construct(self):
        from components.typography import Typography, ITypography
        from components.screenTemplate import ScreenTemplate, IScreenTemplate

        typo: ITypography = Typography()
        self.camera.background_color = typo.bg()
        tracker: IScreenTemplate = ScreenTemplate(self, typo)
        
        # Color Theme Constants
        LIGHT_TEXT = "#E0E0E0"
        GRAY_TEXT = "#A0A0A0"
        GREEN = typo.color_green()
        RED = typo.color_red()
        BLUE = typo.color_blue()
        YELLOW = typo.color_yellow()
        
        # Screen indicator removed as requested.

        # ==========================================
        # 1. LAYOUT SETUP (Left Side)
        # ==========================================
        prices_array = [7, 1, 5, 3, 6, 4]
        
        # Array visualization
        cells = VGroup()
        for idx, val in enumerate(prices_array):
            cell_bg = Square(side_length=0.6, color=LIGHT_TEXT, stroke_width=2)
            cell_val = Text(str(val), font=typo.font_code(), font_size=20, color=LIGHT_TEXT)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=16, color=GRAY_TEXT).next_to(cell_bg, UP, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            cells.add(cell)
        cells.arrange(RIGHT, buff=0)
        
        array_label = Text("prices =", font=typo.font_code(), font_size=20, color=LIGHT_TEXT).next_to(cells, LEFT, buff=0.3)
        array_label.match_y(cells[0][0])
        array_group = VGroup(array_label, cells)
        
        # Trackers
        tracker_box = RoundedRectangle(corner_radius=0.1, width=3.5, height=1.6, color=LIGHT_TEXT, stroke_width=2)
        
        min_price_title = Text("minPrice:", font=typo.font_code(), font_size=18, color=LIGHT_TEXT)
        min_price_val = Text("∞", font=typo.font_code(), font_size=20, color=RED)
        
        max_profit_title = Text("maxProfit:", font=typo.font_code(), font_size=18, color=LIGHT_TEXT)
        max_profit_val = Text("0", font=typo.font_code(), font_size=20, color=GREEN)
        
        trackers = VGroup(
            VGroup(min_price_title, min_price_val).arrange(RIGHT, buff=0.2),
            VGroup(max_profit_title, max_profit_val).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        trackers.move_to(tracker_box.get_center())
        tracker_group = VGroup(tracker_box, trackers)
        
        # Graph
        axes = Axes(
            x_range=[-0.8, 6.0, 1],
            y_range=[-0.8, 10.0, 2],
            x_length=5.0,
            y_length=2.5,
            axis_config={"color": LIGHT_TEXT, "include_numbers": False},
        )
        
        x_nums = VGroup(*[
            Text(str(i), font=typo.font_ui(), font_size=10, color=LIGHT_TEXT).next_to(
                axes.x_axis.n2p(i), DOWN + LEFT if i == 0 else DOWN, buff=0.2 if i == 0 else 0.15
            )
            for i in range(6)
        ])
        y_nums = VGroup(*[
            Text(str(i), font=typo.font_ui(), font_size=10, color=LIGHT_TEXT).next_to(axes.y_axis.n2p(i), LEFT, buff=0.15)
            for i in range(2, 9, 2)
        ])
        axes_labels = VGroup(x_nums, y_nums)

        points = [axes.coords_to_point(i, p) for i, p in enumerate(prices_array)]
        line_graph = VMobject()
        line_graph.set_points_as_corners(points)
        line_graph.set_stroke(color=BLUE, width=3)
        dots = VGroup(*[Dot(point, color=YELLOW, radius=0.06) for point in points])
        graph_group = VGroup(axes, axes_labels, line_graph, dots)

        # Left Column Arrangement
        left_column = VGroup(array_group, tracker_group, graph_group).arrange(DOWN, buff=1.2, aligned_edge=LEFT)

        # ==========================================
        # 2. CODE BLOCK SETUP (Right Side)
        # ==========================================
        java_code = """class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE;
        int maxProfit = 0;
        
        for (int i = 0; i < prices.length; i++) {
            minPrice = Math.min(minPrice, prices[i]);
            maxProfit = Math.max(maxProfit, prices[i] - minPrice);
        }
        
        return maxProfit;
    }
}"""
        code_block = Code(
            code_string=java_code,
            tab_width=4,
            background="window",
            language="java",
            formatter_style="monokai"
        ).scale(0.7)

        # Main Layout Arrangement
        main_layout = VGroup(left_column, code_block).arrange(RIGHT, buff=1.0)
        # Scale to ensure it fits well inside the screen boundaries
        main_layout.scale_to_fit_height(6.0)
        main_layout.move_to(ORIGIN)

        # Highlighter logic (Z-index so text stays on top)
        start_y = code_block[1][0].get_y()
        line_spacing = code_block[1][0].get_y() - code_block[1][1].get_y()
        
        h_rect = Rectangle(width=code_block[0].width - 0.1, height=line_spacing + 0.1, color=YELLOW, stroke_width=2)
        h_rect.set_fill(YELLOW, opacity=0.3)
        h_rect.set_z_index(-1)
        code_block.set_z_index(1)
        
        def highlight_line(line_num):
            target_y = start_y - (line_num - 1) * line_spacing
            target_pos = np.array([code_block[0].get_center()[0], target_y, 0])
            return h_rect.animate.move_to(target_pos)

        # ==========================================
        # 3. ANIMATION SEQUENCE
        # ==========================================
        self.play(
            FadeIn(array_group),
            FadeIn(tracker_group),
            FadeIn(axes), FadeIn(axes_labels), Create(line_graph), FadeIn(dots),
            FadeIn(code_block),
            run_time=2
        )
        self.wait(1)

        # Pointer: just a triangle (arrow head)
        i_arrow = Triangle(color=BLUE).scale(0.12).set_fill(BLUE, opacity=1)
        i_label = Text("i", font=typo.font_code(), font_size=16, color=BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label)

        # Line 3: int minPrice = Integer.MAX_VALUE;
        h_rect.move_to(np.array([code_block[0].get_center()[0], start_y - 2 * line_spacing, 0]))
        self.play(FadeIn(h_rect))
        self.play(Indicate(min_price_val, color=RED), run_time=1)
        
        # Line 4: int maxProfit = 0;
        self.play(highlight_line(4))
        self.play(Indicate(max_profit_val, color=GREEN), run_time=1)
        
        # Line 6: for loop
        self.play(highlight_line(6))
        self.wait(0.5)
        
        current_min = float('inf')
        current_max = 0
        min_line = None
        
        for i in range(len(prices_array)):
            p = prices_array[i]
            
            # Loop condition
            if i > 0:
                self.play(highlight_line(6), run_time=0.5)
            
            if i == 0:
                i_ptr.next_to(cells[i][0], DOWN, buff=0.2)
                self.play(FadeIn(i_ptr), cells[i][0].animate.set_fill(BLUE, opacity=0.3), run_time=0.5)
            else:
                self.play(
                    i_ptr.animate.next_to(cells[i][0], DOWN, buff=0.2),
                    cells[i-1][0].animate.set_fill(opacity=0),
                    cells[i][0].animate.set_fill(BLUE, opacity=0.3),
                    run_time=0.5
                )
            
            self.play(Indicate(dots[i], color=BLUE, scale_factor=2), run_time=0.4)
            
            # Line 7: minPrice = Math.min(...)
            self.play(highlight_line(7), run_time=0.5)
            
            if p < current_min:
                current_min = p
                new_min_val = Text(str(current_min), font=typo.font_code(), font_size=20, color=RED).move_to(min_price_val.get_center())
                
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
            else:
                self.wait(0.3)
                
            # Line 8: maxProfit = Math.max(...)
            self.play(highlight_line(8), run_time=0.5)
            
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
                    new_max_val = Text(str(current_max), font=typo.font_code(), font_size=20, color=GREEN).move_to(max_profit_val.get_center())
                    self.play(ReplacementTransform(max_profit_val, new_max_val), Indicate(profit_segment, color=LIGHT_TEXT), run_time=0.5)
                    max_profit_val = new_max_val
                
                self.play(FadeOut(profit_segment), run_time=0.3)
            else:
                self.wait(0.4)

        # Line 11: return maxProfit
        self.play(highlight_line(11))
        self.play(Indicate(max_profit_val, color=GREEN, scale_factor=1.5), run_time=1)
        
        self.play(FadeOut(h_rect))
        
        anims_clean = [
            FadeOut(i_ptr),
            cells[-1][0].animate.set_fill(opacity=0)
        ]
        if min_line is not None:
            anims_clean.append(FadeOut(min_line))
            
        self.play(*anims_clean, run_time=1)

        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(1)", color_type="green", position="right")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = WalkthroughJava()
    scene.render()
