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
        
        # Answer array
        ans_array = [1, 1, 1, 1]
        ans_cells = VGroup()
        for idx, val in enumerate(ans_array):
            cell_bg = Square(side_length=0.7, color=WHITE, stroke_width=2)
            cell_val = Text("", font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=20, color="#B3B3B3").next_to(cell_bg, UP, buff=0.1)
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
            Text("* for each element i in nums", font=typo.font_code(), font_size=24, color=WHITE),
            Text("*     product = 1", font=typo.font_code(), font_size=24, color=WHITE),
            Text("*     for each element j in nums", font=typo.font_code(), font_size=24, color=WHITE),
            Text("*         if i != j", font=typo.font_code(), font_size=24, color=WHITE),
            Text("*             product *= nums[j]", font=typo.font_code(), font_size=24, color=WHITE),
            Text("*     answer[i] = product", font=typo.font_code(), font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        algo_lines.next_to(algo_title, DOWN, buff=0.5, aligned_edge=LEFT)
        algo_group = VGroup(algo_title, algo_lines)

        # Main Layout Arrangement
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
        
        j_arrow = Triangle(color=RED).scale(0.12).set_fill(RED, opacity=1).rotate(PI)
        j_label = Text("j", font=typo.font_code(), font_size=16, color=RED).next_to(j_arrow, UP, buff=0.1)
        j_ptr = VGroup(j_arrow, j_label)

        for i in range(len(nums_array)):
            if i == 0:
                i_ptr.next_to(cells[i][0], DOWN, buff=0.2)
                self.play(FadeIn(i_ptr), cells[i][0].animate.set_fill(BLUE, opacity=0.3), run_time=0.3)
            else:
                self.play(
                    i_ptr.animate.next_to(cells[i][0], DOWN, buff=0.2),
                    cells[i-1][0].animate.set_fill(opacity=0),
                    cells[i][0].animate.set_fill(BLUE, opacity=0.3),
                    run_time=0.3
                )
            
            product = 1
            prod_text = Text(f"product = {product}", font=typo.font_code(), font_size=24, color=WHITE).next_to(cells, DOWN, buff=1)
            self.play(FadeIn(prod_text), run_time=0.3)
            
            for j in range(len(nums_array)):
                if j == 0:
                    j_ptr.next_to(cells[j][0], UP, buff=0.5)
                    if 'j_ptr' not in self.mobjects:
                        self.play(FadeIn(j_ptr), run_time=0.3)
                    else:
                        self.play(j_ptr.animate.next_to(cells[j][0], UP, buff=0.5), run_time=0.3)
                else:
                    self.play(
                        j_ptr.animate.next_to(cells[j][0], UP, buff=0.5),
                        run_time=0.3
                    )
                
                cells[j][0].set_z_index(1)
                cells[j][0].set_stroke(RED, width=4)
                self.wait(0.2)
                
                if i != j:
                    product *= nums_array[j]
                    new_prod_text = Text(f"product = {product}", font=typo.font_code(), font_size=24, color=GREEN).next_to(cells, DOWN, buff=1)
                    self.play(Transform(prod_text, new_prod_text), run_time=0.3)
                else:
                    cross = Cross(cells[j][0], stroke_color=RED)
                    self.play(Create(cross), run_time=0.3)
                    self.play(FadeOut(cross), run_time=0.3)
                
                cells[j][0].set_stroke(WHITE, width=2)
                cells[j][0].set_z_index(0)
            
            # Update ans array
            ans_val = Text(str(product), font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[i][0].get_center())
            ans_cells[i].remove(ans_cells[i][1])
            
            prod_copy = prod_text.copy()
            self.play(
                ReplacementTransform(prod_copy, ans_val),
                ans_cells[i][0].animate.set_fill(GREEN, opacity=0.3),
                run_time=0.5
            )
            ans_cells[i].add(ans_val)
            self.play(FadeOut(prod_text), run_time=0.3)
        
        self.play(FadeOut(i_ptr), FadeOut(j_ptr), cells[-1][0].animate.set_fill(opacity=0), run_time=0.5)
                
        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N²), Space: O(1)", color_type="red", position="right")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = BruteForce()
    scene.render()
