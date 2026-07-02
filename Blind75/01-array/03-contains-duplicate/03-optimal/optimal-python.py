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
        
        tracker.screen_optimal_approach("Optimal Approach")

        # ==========================================
        # 1. LAYOUT SETUP (Left Side)
        # ==========================================
        nums_array = [1, 2, 3, 4, 5, 5]
        
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
        
        # Set Visualization
        set_box = RoundedRectangle(corner_radius=0.2, width=6.0, height=1.5, color=BLUE, stroke_width=2)
        set_title = Text("SET", font=typo.font_code(), font_size=24, color=BLUE).next_to(set_box, UP, buff=0.2)
        set_group = VGroup(set_title, set_box)
        
        # Elements in Set (will be populated dynamically)
        set_elements = VGroup()
        
        left_column = VGroup(array_group, set_group).arrange(DOWN, buff=1.2, aligned_edge=LEFT)

        # ==========================================
        # 2. ALGORITHM LOGIC SETUP (Right Side)
        # ==========================================
        algo_title = Text("Algorithm:", font=typo.font_ui(), font_size=28, color=YELLOW, weight=BOLD)
        algo_lines = VGroup(
            Text("* Initialize empty HashSet.", font=typo.font_code(), font_size=24, color=WHITE),
            Text("* Iterate through each element.", font=typo.font_code(), font_size=24, color=WHITE),
            Text("* if element exists in HashSet -> duplicate.", font=typo.font_code(), font_size=24, color=WHITE),
            Text("* else -> add element to HashSet.", font=typo.font_code(), font_size=24, color=WHITE)
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
            FadeIn(algo_group),
            run_time=2
        )
        self.wait(1)

        # Initialize HashSet
        self.play(FadeIn(set_group))
        
        i_arrow = Triangle(color=BLUE).scale(0.12).set_fill(BLUE, opacity=1)
        i_label = Text("i", font=typo.font_code(), font_size=16, color=BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label)

        found_duplicate = False

        for i in range(len(nums_array)):
            if found_duplicate:
                break
                
            # Iterate
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

            # Check if num in set
            curr_val = nums_array[i]
            
            # Find in set
            exists = False
            for elem in set_elements:
                if elem.text == str(curr_val):
                    exists = True
                    self.play(Indicate(elem, color=RED, scale_factor=1.5), run_time=0.8)
                    break
                    
            if exists:
                # Duplicate found
                dup_msg = Text(f"{curr_val} exists in HashSet", font=typo.font_ui(), font_size=20, color=GREEN).next_to(set_box, DOWN, buff=0.5)
                dup_box = SurroundingRectangle(dup_msg, color=GREEN, buff=0.1, corner_radius=0.1)
                dup_group = VGroup(dup_msg, dup_box)
                
                self.play(FadeIn(dup_group), run_time=0.5)
                self.play(Indicate(dup_group, color=GREEN, scale_factor=1.1), run_time=0.5)
                
                # Pulse the last cell AFTER showing the message
                self.play(Indicate(cells[i][0], color=GREEN, scale_factor=1.2), run_time=1)
                
                self.wait(0.5)
                self.play(FadeOut(dup_group), run_time=0.5)
                
                ans_box = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.7, color=GREEN, stroke_width=2).move_to(dup_msg.get_center())
                ans_text = Text("true", font=typo.font_code(), font_size=24, color=GREEN, weight=BOLD).move_to(ans_box.get_center())
                ans_group = VGroup(ans_box, ans_text)
                
                self.play(FadeIn(ans_group), run_time=0.5)
                self.play(Indicate(ans_group, scale_factor=1.2, color=GREEN), run_time=1)
                
                found_duplicate = True
            else:
                not_found_msg = Text(f"{curr_val} not in HashSet", font=typo.font_ui(), font_size=20, color=RED).next_to(set_box, DOWN, buff=0.5)
                not_found_box = SurroundingRectangle(not_found_msg, color=RED, buff=0.1, corner_radius=0.1)
                not_found_group = VGroup(not_found_msg, not_found_box)
                
                self.play(FadeIn(not_found_group), run_time=0.5)
                self.play(Indicate(not_found_group, color=RED, scale_factor=1.1), run_time=0.5)
                self.wait(0.3)
                self.play(FadeOut(not_found_group), run_time=0.4)
                
                # Add to set
                new_elem = Text(str(curr_val), font=typo.font_code(), font_size=24, color=WHITE)
                if len(set_elements) == 0:
                    new_elem.move_to(set_box.get_left() + RIGHT * 0.5)
                else:
                    new_elem.next_to(set_elements[-1], RIGHT, buff=0.5)
                
                # Animate from array to set
                flying_elem = Text(str(curr_val), font=typo.font_code(), font_size=24, color=WHITE).move_to(cells[i][0].get_center())
                self.play(
                    flying_elem.animate.move_to(new_elem.get_center()),
                    run_time=0.6
                )
                
                set_elements.add(new_elem)
                self.add(new_elem)
                self.remove(flying_elem)
                
        if not found_duplicate:
            ans_box = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.7, color=RED, stroke_width=2).next_to(set_box, DOWN, buff=0.5)
            ans_text = Text("false", font=typo.font_code(), font_size=24, color=RED, weight=BOLD).move_to(ans_box.get_center())
            ans_group = VGroup(ans_box, ans_text)
            
            self.play(FadeIn(ans_group), run_time=0.5)
            self.play(Indicate(ans_group, scale_factor=1.2, color=RED), run_time=1)
                
        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(N)", color_type="green", position="right")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = Optimal()
    scene.render()
