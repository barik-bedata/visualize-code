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
        nums_array = [1, 2, 3, 4, 4]
        
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
        
        # Status Text Area (for comparisons)
        status_text = Text("Comparing elements...", font=typo.font_ui(), font_size=24, color=GRAY)
        
        left_column = VGroup(array_group, status_text).arrange(DOWN, buff=2.0, aligned_edge=LEFT)

        # ==========================================
        # 2. ALGORITHM LOGIC SETUP (Right Side)
        # ==========================================
        algo_title = Text("Algorithm:", font=typo.font_ui(), font_size=28, color=YELLOW, weight=BOLD)
        algo_lines = VGroup(
            Text("* check all pairs (i, j) where i < j.", font=typo.font_code(), font_size=24, color=WHITE),
            Text("* if nums[i] == nums[j] -> duplicate found.", font=typo.font_code(), font_size=24, color=WHITE)
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
            FadeIn(status_text),
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
        
        all_pairs = [(i, j) for i in range(len(nums_array)) for j in range(i + 1, len(nums_array))]
        found_duplicate = False

        for idx_pair, (i, j) in enumerate(all_pairs):
            if found_duplicate:
                break
                
            # Move i pointer
            if idx_pair == 0 or all_pairs[idx_pair-1][0] != i:
                if idx_pair == 0:
                    i_ptr.next_to(cells[i][0], DOWN, buff=0.2)
                    self.play(FadeIn(i_ptr), cells[i][0].animate.set_fill(BLUE, opacity=0.3), run_time=0.3)
                else:
                    self.play(
                        i_ptr.animate.next_to(cells[i][0], DOWN, buff=0.2),
                        cells[i-1][0].animate.set_fill(opacity=0),
                        cells[i][0].animate.set_fill(BLUE, opacity=0.3),
                        run_time=0.3
                    )

            # Move j pointer
            # Note: We increase the UP buff to 0.5 to clear the index text
            if idx_pair == 0 or all_pairs[idx_pair-1][0] != i:
                j_ptr.next_to(cells[j][0], UP, buff=0.5)
                self.play(FadeIn(j_ptr), cells[j][0].animate.set_fill(RED, opacity=0.3), run_time=0.3)
            else:
                self.play(
                    j_ptr.animate.next_to(cells[j][0], UP, buff=0.5),
                    cells[j-1][0].animate.set_fill(opacity=0),
                    cells[j][0].animate.set_fill(RED, opacity=0.3),
                    run_time=0.3
                )
            
            # Condition check with flying copy effect
            is_dup = (nums_array[i] == nums_array[j])
            sign_str = "==" if is_dup else "!="
            sign_color = GREEN if is_dup else RED
            
            comp_i = Text(str(nums_array[i]), font=typo.font_code(), font_size=28, color=BLUE)
            comp_sign = Text(sign_str, font=typo.font_code(), font_size=28, color=sign_color)
            comp_j = Text(str(nums_array[j]), font=typo.font_code(), font_size=28, color=RED)
            
            new_status = VGroup(comp_i, comp_sign, comp_j).arrange(RIGHT, buff=0.3).move_to(status_text.get_center())
            
            flying_i = Text(str(nums_array[i]), font=typo.font_code(), font_size=24, color=WHITE).move_to(cells[i][0].get_center())
            flying_j = Text(str(nums_array[j]), font=typo.font_code(), font_size=24, color=WHITE).move_to(cells[j][0].get_center())
            
            self.play(
                FadeOut(status_text, run_time=0.2),
                flying_i.animate.move_to(comp_i.get_center()).set_color(BLUE).scale(28/24),
                flying_j.animate.move_to(comp_j.get_center()).set_color(RED).scale(28/24),
                run_time=0.4
            )
            
            self.play(FadeIn(comp_sign), run_time=0.2)
            
            # Combine flying texts into the new_status group implicitly by treating them as updated
            self.remove(flying_i, flying_j)
            self.add(new_status)
            status_text = new_status
            
            if is_dup:
                dup_msg = Text("Duplicate found!", font=typo.font_ui(), font_size=24, color=GREEN).next_to(status_text, DOWN, buff=0.5)
                self.play(FadeIn(dup_msg), Indicate(cells[i][0], color=GREEN), Indicate(cells[j][0], color=GREEN), run_time=0.8)
                found_duplicate = True
            else:
                self.wait(0.2)
                
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
