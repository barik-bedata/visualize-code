from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class OptimalPython(Scene):
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
        
        tracker.screen_optimal_approach("Optimal Approach (Prefix/Suffix Products)")

        # ==========================================
        # 1. LAYOUT SETUP (Left Side)
        # ==========================================
        nums_array = [1, 2, 3, 4]
        
        cells = VGroup()
        for idx, val in enumerate(nums_array):
            cell_bg = Square(side_length=0.7, color=WHITE, stroke_width=2)
            cell_val = Text(str(val), font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=20, color="#B3B3B3").next_to(cell_bg, UP, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            cells.add(cell)
        
        cells.arrange(RIGHT, buff=0)
        nums_label = Text("nums =", font=typo.font_code(), font_size=24, color=WHITE).next_to(cells, LEFT, buff=0.5)
        nums_label.match_y(cells[0][0])
        array_group = VGroup(nums_label, cells)
        
        ans_array = [1, 1, 1, 1]
        ans_cells = VGroup()
        for idx, val in enumerate(ans_array):
            cell_bg = Square(side_length=0.7, color=WHITE, stroke_width=2)
            cell_val = Text("", font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=20, color="#B3B3B3").next_to(cell_bg, DOWN, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            ans_cells.add(cell)
            
        ans_cells.arrange(RIGHT, buff=0)
        ans_label = Text("answer =", font=typo.font_code(), font_size=24, color=WHITE).next_to(ans_cells, LEFT, buff=0.5)
        ans_label.match_y(ans_cells[0][0])
        ans_group = VGroup(ans_label, ans_cells)
        
        left_column = VGroup(array_group, ans_group).arrange(DOWN, buff=2.0, aligned_edge=LEFT)

        # ==========================================
        # 2. ALGORITHM LOGIC SETUP (Right Side)
        # ==========================================
        algo_title = Text("Algorithm:", font=typo.font_ui(), font_size=28, color=YELLOW, weight=BOLD)
        algo_lines = VGroup(
            Text("1. Initialize answer array", font=typo.font_code(), font_size=24, color=WHITE),
            Text("2. Left pass:", font=typo.font_code(), font_size=24, color=WHITE),
            Text("   Compute prefix products", font=typo.font_code(), font_size=24, color=WHITE),
            Text("3. Right pass:", font=typo.font_code(), font_size=24, color=WHITE),
            Text("   Compute suffix products", font=typo.font_code(), font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        algo_lines.next_to(algo_title, DOWN, buff=0.5, aligned_edge=LEFT)
        algo_group = VGroup(algo_title, algo_lines)

        main_layout = VGroup(left_column, algo_group).arrange(RIGHT, buff=1.5)
        main_layout.scale_to_fit_width(12.0)
        main_layout.move_to(ORIGIN)

        # ==========================================
        # 3. ANIMATION SEQUENCE
        # ==========================================
        self.play(
            FadeIn(array_group),
            FadeIn(ans_group),
            FadeIn(algo_group),
            run_time=2
        )
        self.wait(1)

        i_arrow = Triangle(color=BLUE).scale(0.12).set_fill(BLUE, opacity=1)
        i_label = Text("i", font=typo.font_code(), font_size=16, color=BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label)

        # Prefix Pass
        prefix = 1
        prefix_text = Text(f"prefix = {prefix}", font=typo.font_code(), font_size=24, color=BLUE).next_to(ans_group, UP, buff=0.5)
        self.play(FadeIn(prefix_text), run_time=0.5)

        for i in range(len(nums_array)):
            if i == 0:
                i_ptr.next_to(ans_cells[i][0], DOWN, buff=0.5)
                self.play(FadeIn(i_ptr), run_time=0.3)
            else:
                self.play(i_ptr.animate.next_to(ans_cells[i][0], DOWN, buff=0.5), run_time=0.3)
            
            ans_val = Text(str(prefix), font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[i][0].get_center())
            ans_cells[i].replace_submobject(1, ans_val)
            self.play(FadeIn(ans_val), ans_cells[i][0].animate.set_fill(GREEN, opacity=0.3), run_time=0.3)
            
            prefix *= nums_array[i]
            new_prefix_text = Text(f"prefix = {prefix}", font=typo.font_code(), font_size=24, color=BLUE).next_to(ans_group, UP, buff=0.5)
            self.play(Transform(prefix_text, new_prefix_text), run_time=0.3)

        self.play(FadeOut(prefix_text), run_time=0.5)

        # Postfix Pass
        postfix = 1
        postfix_text = Text(f"postfix = {postfix}", font=typo.font_code(), font_size=24, color=RED).next_to(ans_group, DOWN, buff=1.0)
        self.play(FadeIn(postfix_text), run_time=0.5)

        for i in range(len(nums_array)-1, -1, -1):
            self.play(i_ptr.animate.next_to(ans_cells[i][0], DOWN, buff=0.5), run_time=0.3)
            
            curr_val = int(ans_cells[i][1].text) if ans_cells[i][1].text else 1
            new_val = curr_val * postfix
            
            new_ans_val = Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[i][0].get_center())
            self.play(Transform(ans_cells[i][1], new_ans_val), run_time=0.3)
            
            postfix *= nums_array[i]
            new_postfix_text = Text(f"postfix = {postfix}", font=typo.font_code(), font_size=24, color=RED).next_to(ans_group, DOWN, buff=1.0)
            self.play(Transform(postfix_text, new_postfix_text), run_time=0.3)

        self.play(FadeOut(postfix_text), FadeOut(i_ptr), run_time=0.5)
        
        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(1) (excluding output array)", color_type="green", position="right")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = OptimalPython()
    scene.render()
