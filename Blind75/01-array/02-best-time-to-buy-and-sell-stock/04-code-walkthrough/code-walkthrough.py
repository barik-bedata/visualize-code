from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class Walkthrough(Scene):
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
        SCAN_BLUE = "#4A90E2"
        
        tracker.screen_code_walkthrough("Walkthrough: Best Time to Buy and Sell Stock")

        # ==========================================
        # 1. LAYOUT SETUP (Left Side)
        # ==========================================
        prices_array = [7, 1, 5, 3, 6, 4]
        
        # Array visualization
        cells = VGroup()
        for idx, val in enumerate(prices_array):
            cell_bg = Square(side_length=0.6, color=WHITE, stroke_width=2)
            cell_val = Text(str(val), font=typo.font_code(), font_size=20, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=14, color=GRAY).next_to(cell_bg, UP, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            cells.add(cell)
        
        cells.arrange(RIGHT, buff=0).move_to(UP * 2.2 + LEFT * 3.5)
        array_label = Text("prices =", font=typo.font_code(), font_size=20, color=WHITE).next_to(cells, LEFT, buff=0.3)
        
        # Trackers
        tracker_box = RoundedRectangle(corner_radius=0.1, width=2.5, height=1.5, color=GRAY, stroke_width=2)
        tracker_box.next_to(cells, DOWN, buff=0.5).align_to(cells, LEFT)
        
        min_price_title = Text("minPrice", font=typo.font_code(), font_size=16, color=GRAY)
        min_price_val = Text("∞", font=typo.font_code(), font_size=24, color=RED)
        
        max_profit_title = Text("maxProfit", font=typo.font_code(), font_size=16, color=GRAY)
        max_profit_val = Text("0", font=typo.font_code(), font_size=24, color=GREEN)
        
        trackers = VGroup(
            VGroup(min_price_title, min_price_val).arrange(RIGHT, buff=0.3),
            VGroup(max_profit_title, max_profit_val).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.3)
        trackers.move_to(tracker_box.get_center())
        
        # Graph
        axes = Axes(
            x_range=[-0.5, 5.5, 1],
            y_range=[0, 8, 2],
            x_length=4.5,
            y_length=2.0,
            axis_config={"color": GRAY, "include_numbers": False},
        ).next_to(tracker_box, DOWN, buff=0.5).align_to(cells, LEFT)
        
        points = [axes.coords_to_point(i, p) for i, p in enumerate(prices_array)]
        line_graph = VMobject()
        line_graph.set_points_as_corners(points)
        line_graph.set_stroke(color=BLUE, width=3)
        dots = VGroup(*[Dot(point, color=YELLOW, radius=0.06) for point in points])

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
        ).scale(0.65)
        code_block.move_to(RIGHT * 3.5 + DOWN * 0.5)

        # Highlighter logic matching Two Sum fix
        line_height = code_block[2][0].height
        line_width = code_block[2].width + 0.2
        start_y = code_block[2][0].get_y()
        line_spacing = code_block[2][0].get_y() - code_block[2][1].get_y()
        
        h_rect = Rectangle(width=line_width, height=line_height + 0.05, color=YELLOW, stroke_width=2)
        h_rect.set_fill(YELLOW, opacity=0.2)
        
        def highlight_line(line_num):
            target_y = start_y - (line_num - 1) * line_spacing
            target_pos = np.array([code_block[2].get_x(), target_y, 0])
            return h_rect.animate.move_to(target_pos)

        # ==========================================
        # 3. ANIMATION SEQUENCE
        # ==========================================
        self.play(
            FadeIn(array_label), FadeIn(cells),
            Create(axes), Create(line_graph), FadeIn(dots),
            FadeIn(tracker_box), FadeIn(trackers),
            FadeIn(code_block),
            run_time=2
        )
        self.wait(1)

        # Line 3: int minPrice = Integer.MAX_VALUE;
        h_rect.move_to(np.array([code_block[2].get_x(), start_y - 2 * line_spacing, 0]))
        self.play(FadeIn(h_rect))
        self.play(Indicate(min_price_val, color=RED), run_time=1)
        
        # Line 4: int maxProfit = 0;
        self.play(highlight_line(4))
        self.play(Indicate(max_profit_val, color=GREEN), run_time=1)
        
        # Line 6: for loop
        self.play(highlight_line(6))
        
        i_arrow = Arrow(start=DOWN, end=UP, color=SCAN_BLUE, buff=0.1).scale(0.5)
        i_label = Text("i", font=typo.font_code(), font_size=14, color=SCAN_BLUE).next_to(i_arrow, DOWN)
        i_ptr = VGroup(i_arrow, i_label)
        
        current_min = float('inf')
        current_max = 0
        min_line = DashedLine(start=axes.c2p(-0.5, 8), end=axes.c2p(5.5, 8), color=RED, stroke_width=2)
        
        for i in range(len(prices_array)):
            p = prices_array[i]
            
            # Loop condition
            self.play(highlight_line(6), run_time=0.5)
            
            if i == 0:
                i_ptr.next_to(cells[i][0], DOWN)
                self.play(FadeIn(i_ptr), cells[i][0].animate.set_fill(SCAN_BLUE, opacity=0.3), run_time=0.5)
            else:
                self.play(
                    i_ptr.animate.next_to(cells[i][0], DOWN),
                    cells[i-1][0].animate.set_fill(opacity=0),
                    cells[i][0].animate.set_fill(SCAN_BLUE, opacity=0.3),
                    run_time=0.5
                )
                
            self.play(Indicate(dots[i], color=SCAN_BLUE, scale_factor=2), run_time=0.4)
            
            # Line 7: minPrice = Math.min(...)
            self.play(highlight_line(7), run_time=0.5)
            
            if p < current_min:
                current_min = p
                new_min_val = Text(str(current_min), font=typo.font_code(), font_size=24, color=RED).move_to(min_price_val.get_center())
                
                new_min_line = DashedLine(
                    start=axes.c2p(-0.5, current_min),
                    end=axes.c2p(5.5, current_min),
                    color=RED, stroke_width=2
                )
                
                if i == 0:
                    self.play(
                        Transform(min_price_val, new_min_val),
                        Create(new_min_line),
                        run_time=0.5
                    )
                    min_line = new_min_line
                else:
                    self.play(
                        Transform(min_price_val, new_min_val),
                        Transform(min_line, new_min_line),
                        run_time=0.5
                    )
                min_price_val = new_min_val
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
                    new_max_val = Text(str(current_max), font=typo.font_code(), font_size=24, color=GREEN).move_to(max_profit_val.get_center())
                    self.play(Transform(max_profit_val, new_max_val), Indicate(profit_segment, color=WHITE), run_time=0.5)
                    max_profit_val = new_max_val
                
                self.play(FadeOut(profit_segment), run_time=0.3)
            else:
                self.wait(0.4)

        # Line 11: return maxProfit
        self.play(highlight_line(11))
        self.play(Indicate(max_profit_val, color=GREEN, scale_factor=1.5), run_time=1)
        
        self.play(FadeOut(h_rect))

        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(1)", color_type="green")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = Walkthrough()
    scene.render()
