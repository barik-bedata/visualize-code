from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class WalkthroughPythonFalse(Scene):
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
        # 1. LAYOUT SETUP
        # ==========================================
        nums_array = [1, 2, 3, 4, 5, 6]
        
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
        set_title = Text("seen = {}", font=typo.font_code(), font_size=24, color=BLUE).next_to(set_box, UP, buff=0.2)
        set_group = VGroup(set_title, set_box)
        
        # Elements in Set (will be populated dynamically)
        set_elements = VGroup()
        
        left_column = VGroup(array_group, set_group).arrange(DOWN, buff=1.2, aligned_edge=LEFT)

        # ==========================================
        # 2. CODE BLOCK SETUP
        # ==========================================
        python_code = """class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
            
        return False"""
        code_block = Code(
            code_string=python_code,
            tab_width=4,
            background="window",
            language="python",
            formatter_style="monokai"
        ).scale(0.8)

        main_layout = VGroup(left_column, code_block).arrange(RIGHT, buff=1.0)
        main_layout.scale_to_fit_width(12.0)
        main_layout.move_to(ORIGIN)

        # Highlighter logic
        start_y = code_block[1][0].get_y()
        line_spacing = code_block[1][0].get_y() - code_block[1][1].get_y()
        
        h_rect = Rectangle(width=code_block[0].width - 0.1, height=line_spacing, color=YELLOW, stroke_width=2)
        h_rect.set_fill(YELLOW, opacity=0)
        
        code_block[0].set_z_index(0)
        h_rect.set_z_index(1)
        for idx in range(1, len(code_block)):
            code_block[idx].set_z_index(2)
        
        def highlight_line(line_num):
            target_y = start_y - (line_num - 1) * line_spacing - 0.045
            target_pos = np.array([code_block[0].get_center()[0], target_y, 0])
            return h_rect.animate.move_to(target_pos)

        # ==========================================
        # 3. ANIMATION SEQUENCE
        # ==========================================
        self.play(
            FadeIn(array_group),
            FadeIn(code_block),
            run_time=2
        )
        self.wait(1)

        # Line 3: seen = set()
        h_rect.move_to(np.array([code_block[0].get_center()[0], start_y - 2 * line_spacing - 0.045, 0]))
        self.play(FadeIn(h_rect), FadeIn(set_group))
        
        i_arrow = Triangle(color=BLUE).scale(0.12).set_fill(BLUE, opacity=1)
        i_label = Text("num", font=typo.font_code(), font_size=16, color=BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label)

        found_duplicate = False

        for i in range(len(nums_array)):
            if found_duplicate:
                break
                
            # Line 5: for num in nums
            self.play(highlight_line(5), run_time=0.5)
            
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

            # Line 6: if num in seen:
            self.play(highlight_line(6), run_time=0.5)
            
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
                # Line 7: return True
                self.play(highlight_line(7), run_time=0.5)
                self.play(Indicate(cells[i][0], color=GREEN, scale_factor=1.2), run_time=1)
                
                ans_box = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.7, color=GREEN, stroke_width=2).next_to(set_box, DOWN, buff=0.5)
                ans_text = Text("True", font=typo.font_code(), font_size=24, color=GREEN, weight=BOLD).move_to(ans_box.get_center())
                ans_group = VGroup(ans_box, ans_text)
                
                self.play(FadeIn(ans_group), run_time=0.5)
                self.play(Indicate(ans_group, scale_factor=1.2, color=GREEN), run_time=1)
                
                found_duplicate = True
            else:
                self.wait(0.3)
                
                # Line 8: seen.add(num)
                self.play(highlight_line(8), run_time=0.5)
                
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
                
        self.play(FadeOut(h_rect))
        
        # Line 10: return False
        self.play(highlight_line(10), run_time=0.5)
        
        ans_box = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.7, color=RED, stroke_width=2).next_to(set_box, DOWN, buff=0.5)
        ans_text = Text("False", font=typo.font_code(), font_size=24, color=RED, weight=BOLD).move_to(ans_box.get_center())
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
    scene = WalkthroughPythonFalse()
    scene.render()
