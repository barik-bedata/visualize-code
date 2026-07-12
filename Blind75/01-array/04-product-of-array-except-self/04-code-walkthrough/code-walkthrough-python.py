from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class WalkthroughPython(Scene):
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
        
        tracker.screen_code_walkthrough("Code Walkthrough")

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
            cell_val = Text("1", font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=20, color="#B3B3B3").next_to(cell_bg, DOWN, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            ans_cells.add(cell)
            
        ans_cells.arrange(RIGHT, buff=0)
        ans_label = Text("ans =", font=typo.font_code(), font_size=24, color=WHITE).next_to(ans_cells, LEFT, buff=0.5)
        ans_label.match_y(ans_cells[0][0])
        ans_group = VGroup(ans_label, ans_cells)
        
        left_column = VGroup(array_group, ans_group).arrange(DOWN, buff=2.2, aligned_edge=LEFT)

        # ==========================================
        # 2. CODE BLOCK SETUP
        # ==========================================
        python_code = """class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [1] * n
        
        prefix = 1
        for i in range(n):
            ans[i] = prefix
            prefix *= nums[i]
            
        postfix = 1
        for i in range(n - 1, -1, -1):
            ans[i] *= postfix
            postfix *= nums[i]
            
        return ans"""
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

        # Line 3: n = len(nums)
        h_rect.move_to(np.array([code_block[0].get_center()[0], start_y - 2 * line_spacing - 0.045, 0]))
        self.play(FadeIn(h_rect))
        self.wait(0.5)

        # Line 4: ans = [1] * n
        self.play(highlight_line(4))
        self.play(FadeIn(ans_group))
        self.wait(0.5)
        
        # Line 6: prefix = 1
        self.play(highlight_line(6))
        prefix = 1
        prefix_text = Text(f"prefix = {prefix}", font=typo.font_code(), font_size=24, color=BLUE).next_to(ans_group, UP, buff=0.4)
        self.play(FadeIn(prefix_text), run_time=0.5)

        i_arrow = Triangle(color=BLUE).scale(0.12).set_fill(BLUE, opacity=1)
        i_label = Text("i", font=typo.font_code(), font_size=16, color=BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label)

        ans_vals_array = [1] * len(nums_array)

        # First pass (Prefix calculation)
        for i in range(len(nums_array)):
            # Line 7: for i in range(n):
            self.play(highlight_line(7), run_time=0.3)
            
            if i == 0:
                i_ptr.next_to(ans_cells[i][0], DOWN, buff=0.4)
                self.play(FadeIn(i_ptr), run_time=0.3)
            else:
                self.play(i_ptr.animate.next_to(ans_cells[i][0], DOWN, buff=0.4), run_time=0.3)
            
            # Line 8: ans[i] = prefix
            self.play(highlight_line(8), run_time=0.3)
            ans_cells[i][0].set_z_index(1)
            self.play(ans_cells[i][0].animate.set_stroke(BLUE, width=4), run_time=0.3)

            # Copy value from prefix_text
            copy_pref = prefix_text.copy()
            self.play(
                FadeOut(ans_cells[i][1]),
                copy_pref.animate.move_to(ans_cells[i][0].get_center()).set_color(GREEN),
                ans_cells[i][0].animate.set_fill(GREEN, opacity=0.3),
                run_time=0.5
            )
            ans_cells[i].submobjects[1] = copy_pref
            ans_vals_array[i] = prefix

            self.play(ans_cells[i][0].animate.set_stroke(WHITE, width=2), run_time=0.2)
            ans_cells[i][0].set_z_index(0)
            
            # Line 9: prefix *= nums[i]
            self.play(highlight_line(9), run_time=0.3)
            
            # Highlight nums[i] cell
            cells[i][0].set_z_index(1)
            self.play(cells[i][0].animate.set_stroke(YELLOW, width=4), run_time=0.3)

            # Show calculation equation in the middle
            mid_y = (cells[0][0].get_y() + ans_cells[0][0].get_y()) / 2
            
            calc = VGroup(
                Text("prefix =", font=typo.font_code(), font_size=20, color=WHITE),
                Text(str(prefix), font=typo.font_code(), font_size=24, color=BLUE),
                Text("×", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(nums_array[i]), font=typo.font_code(), font_size=24, color=WHITE),
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(prefix * nums_array[i]), font=typo.font_code(), font_size=24, color=BLUE)
            ).arrange(RIGHT, buff=0.2)
            calc.set_y(mid_y)
            calc.align_to(cells[0][0], LEFT)

            copy_prefix_val = prefix_text.copy()
            copy_num_val = cells[i][1].copy()

            self.play(
                FadeIn(calc[0]),
                copy_prefix_val.animate.move_to(calc[1].get_center()),
                copy_num_val.animate.move_to(calc[3].get_center()),
                run_time=0.5
            )
            self.play(FadeIn(calc[2]), FadeIn(calc[4]), FadeIn(calc[5]), run_time=0.3)

            prefix *= nums_array[i]
            new_prefix_text = Text(f"prefix = {prefix}", font=typo.font_code(), font_size=24, color=BLUE).move_to(prefix_text.get_center())

            self.play(
                Transform(prefix_text, new_prefix_text),
                FadeOut(calc), FadeOut(copy_prefix_val), FadeOut(copy_num_val),
                run_time=0.5
            )

            self.play(cells[i][0].animate.set_stroke(WHITE, width=2), run_time=0.2)
            cells[i][0].set_z_index(0)

        self.play(FadeOut(prefix_text), run_time=0.5)

        # Line 11: postfix = 1
        self.play(highlight_line(11), run_time=0.5)
        postfix = 1
        postfix_text = Text(f"postfix = {postfix}", font=typo.font_code(), font_size=24, color=RED).next_to(ans_group, DOWN, buff=1.0)
        self.play(FadeIn(postfix_text), run_time=0.5)

        # Second pass (Postfix calculation)
        for i in range(len(nums_array)-1, -1, -1):
            # Line 12: for i in range(n - 1, -1, -1):
            self.play(highlight_line(12), run_time=0.3)
            self.play(i_ptr.animate.next_to(ans_cells[i][0], DOWN, buff=0.4), run_time=0.3)
            
            # Line 13: ans[i] *= postfix
            self.play(highlight_line(13), run_time=0.3)
            ans_cells[i][0].set_z_index(1)
            self.play(ans_cells[i][0].animate.set_stroke(BLUE, width=4), run_time=0.3)

            curr_val = ans_vals_array[i]
            new_val = curr_val * postfix
            ans_vals_array[i] = new_val

            mid_y = (cells[0][0].get_y() + ans_cells[0][0].get_y()) / 2

            calc = VGroup(
                Text("ans[i] =", font=typo.font_code(), font_size=20, color=WHITE),
                Text(str(curr_val), font=typo.font_code(), font_size=24, color=GREEN),
                Text("×", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(postfix), font=typo.font_code(), font_size=24, color=RED),
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN)
            ).arrange(RIGHT, buff=0.2)
            calc.set_y(mid_y)
            calc.align_to(cells[0][0], LEFT)

            copy_ans_val = ans_cells[i][1].copy()
            copy_postfix_val = postfix_text.copy()

            self.play(
                FadeIn(calc[0]),
                copy_ans_val.animate.move_to(calc[1].get_center()),
                copy_postfix_val.animate.move_to(calc[3].get_center()),
                run_time=0.5
            )
            self.play(FadeIn(calc[2]), FadeIn(calc[4]), FadeIn(calc[5]), run_time=0.3)

            ans_val = Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[i][0].get_center())
            
            self.play(
                FadeOut(ans_cells[i][1]),
                ReplacementTransform(calc[5].copy(), ans_val),
                FadeOut(calc), FadeOut(copy_ans_val), FadeOut(copy_postfix_val),
                run_time=0.5
            )
            ans_cells[i].submobjects[1] = ans_val

            self.play(ans_cells[i][0].animate.set_stroke(WHITE, width=2), run_time=0.2)
            ans_cells[i][0].set_z_index(0)
            
            # Line 14: postfix *= nums[i]
            self.play(highlight_line(14), run_time=0.3)
            
            cells[i][0].set_z_index(1)
            self.play(cells[i][0].animate.set_stroke(YELLOW, width=4), run_time=0.3)

            calc = VGroup(
                Text("postfix =", font=typo.font_code(), font_size=20, color=WHITE),
                Text(str(postfix), font=typo.font_code(), font_size=24, color=RED),
                Text("×", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(nums_array[i]), font=typo.font_code(), font_size=24, color=WHITE),
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(postfix * nums_array[i]), font=typo.font_code(), font_size=24, color=RED)
            ).arrange(RIGHT, buff=0.2)
            calc.set_y(mid_y)
            calc.align_to(cells[0][0], LEFT)

            copy_postfix_val = postfix_text.copy()
            copy_num_val = cells[i][1].copy()

            self.play(
                FadeIn(calc[0]),
                copy_postfix_val.animate.move_to(calc[1].get_center()),
                copy_num_val.animate.move_to(calc[3].get_center()),
                run_time=0.5
            )
            self.play(FadeIn(calc[2]), FadeIn(calc[4]), FadeIn(calc[5]), run_time=0.3)

            postfix *= nums_array[i]
            new_postfix_text = Text(f"postfix = {postfix}", font=typo.font_code(), font_size=24, color=RED).move_to(postfix_text.get_center())

            self.play(
                Transform(postfix_text, new_postfix_text),
                FadeOut(calc), FadeOut(copy_postfix_val), FadeOut(copy_num_val),
                run_time=0.5
            )

            self.play(cells[i][0].animate.set_stroke(WHITE, width=2), run_time=0.2)
            cells[i][0].set_z_index(0)

        # Line 16: return ans
        self.play(highlight_line(16))
        self.play(FadeOut(postfix_text), FadeOut(i_ptr), run_time=0.5)
        
        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(1) (excluding output array)", color_type="green", position="right")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = WalkthroughPython()
    scene.render()
