from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

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
            cell_val = Text("0", font=typo.font_code(), font_size=24, color=WHITE)
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
        java_code = """class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] ans = new int[n];
        
        ans[0] = 1;
        for (int i = 1; i < n; i++) {
            ans[i] = ans[i-1] * nums[i-1];
        }
        
        int suffixProd = 1;
        for (int i = n - 1; i >= 0; i--) {
            ans[i] = ans[i] * suffixProd;
            suffixProd = suffixProd * nums[i];
        }
        
        return ans;
    }
}"""
        code_block = Code(
            code_string=java_code,
            tab_width=4,
            background="window",
            language="java",
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

        # Line 3: int n = nums.length;
        h_rect.move_to(np.array([code_block[0].get_center()[0], start_y - 2 * line_spacing - 0.045, 0]))
        self.play(FadeIn(h_rect))
        self.wait(0.5)

        # Line 4: int[] ans = new int[n];
        self.play(highlight_line(4))
        self.play(FadeIn(ans_group))
        self.wait(0.5)
        
        # Line 6: ans[0] = 1;
        self.play(highlight_line(6))
        ans_cells[0][0].set_z_index(1)
        self.play(ans_cells[0][0].animate.set_stroke(BLUE, width=4), run_time=0.3)
        ans_val_0 = Text("1", font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[0][0].get_center())
        self.play(
            FadeOut(ans_cells[0][1]),
            FadeIn(ans_val_0),
            ans_cells[0][0].animate.set_fill(GREEN, opacity=0.3),
            run_time=0.5
        )
        ans_cells[0].submobjects[1] = ans_val_0
        self.play(ans_cells[0][0].animate.set_stroke(WHITE, width=2), run_time=0.2)
        ans_cells[0][0].set_z_index(0)

        i_arrow = Triangle(color=BLUE).scale(0.12).set_fill(BLUE, opacity=1)
        i_label = Text("i", font=typo.font_code(), font_size=16, color=BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label)

        ans_vals_array = [0] * len(nums_array)
        ans_vals_array[0] = 1

        # First pass (Prefix calculation)
        for i in range(1, len(nums_array)):
            # Line 7: for (int i = 1; i < n; i++)
            self.play(highlight_line(7), run_time=0.3)
            
            if i == 1:
                i_ptr.next_to(ans_cells[i][0], DOWN, buff=0.4)
                self.play(FadeIn(i_ptr), run_time=0.3)
            else:
                self.play(i_ptr.animate.next_to(ans_cells[i][0], DOWN, buff=0.4), run_time=0.3)
            
            # Line 8: ans[i] = ans[i-1] * nums[i-1];
            self.play(highlight_line(8), run_time=0.3)
            
            # Highlight source cells
            cells[i-1][0].set_z_index(1)
            ans_cells[i-1][0].set_z_index(1)
            self.play(
                cells[i-1][0].animate.set_stroke(YELLOW, width=4),
                ans_cells[i-1][0].animate.set_stroke(YELLOW, width=4),
                run_time=0.3
            )
            
            # Highlight target cell
            ans_cells[i][0].set_z_index(1)
            self.play(ans_cells[i][0].animate.set_stroke(BLUE, width=4), run_time=0.3)

            # Equation in the middle
            mid_y = (cells[0][0].get_y() + ans_cells[0][0].get_y()) / 2
            curr_ans = ans_vals_array[i-1]
            curr_num = nums_array[i-1]
            new_val = curr_ans * curr_num
            ans_vals_array[i] = new_val

            calc = VGroup(
                Text("ans[i] =", font=typo.font_code(), font_size=20, color=WHITE),
                Text(str(curr_ans), font=typo.font_code(), font_size=24, color=GREEN),
                Text("×", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(curr_num), font=typo.font_code(), font_size=24, color=WHITE),
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN)
            ).arrange(RIGHT, buff=0.2)
            calc.set_y(mid_y)
            calc.align_to(nums_label, LEFT)

            copy_ans = ans_cells[i-1][1].copy()
            copy_num = cells[i-1][1].copy()

            self.play(
                FadeIn(calc[0]),
                copy_ans.animate.move_to(calc[1].get_center()),
                copy_num.animate.move_to(calc[3].get_center()),
                run_time=0.5
            )
            self.play(FadeIn(calc[2]), FadeIn(calc[4]), FadeIn(calc[5]), run_time=0.3)
            self.wait(0.2)

            ans_val = Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[i][0].get_center())
            self.play(
                FadeOut(ans_cells[i][1]),
                ReplacementTransform(calc[5].copy(), ans_val),
                FadeOut(calc), FadeOut(copy_ans), FadeOut(copy_num),
                run_time=0.5
            )
            ans_cells[i].remove(ans_cells[i][1])
            ans_cells[i].insert(1, ans_val)

            # Unhighlight
            self.play(
                ans_cells[i][0].animate.set_stroke(WHITE, width=2).set_fill(GREEN, opacity=0.3),
                ans_cells[i-1][0].animate.set_stroke(WHITE, width=2),
                cells[i-1][0].animate.set_stroke(WHITE, width=2),
                run_time=0.2
            )
            ans_cells[i][0].set_z_index(0)
            ans_cells[i-1][0].set_z_index(0)
            cells[i-1][0].set_z_index(0)

        # Line 11: int suffixProd = 1;
        self.play(highlight_line(11), run_time=0.5)
        suffix_prod = 1
        suffix_label = Text("suffixProd = ", font=typo.font_code(), font_size=24, color=RED)
        suffix_val = Text(str(suffix_prod), font=typo.font_code(), font_size=24, color=RED)
        suffix_text = VGroup(suffix_label, suffix_val).arrange(RIGHT, buff=0.1)
        suffix_text.next_to(ans_group, DOWN, buff=1.0)
        suffix_text.align_to(ans_group, LEFT)
        self.play(FadeIn(suffix_text), run_time=0.5)

        # Second pass (Postfix calculation)
        for i in range(len(nums_array)-1, -1, -1):
            # Line 12: for (int i = n - 1; i >= 0; i--)
            self.play(highlight_line(12), run_time=0.3)
            self.play(i_ptr.animate.next_to(ans_cells[i][0], DOWN, buff=0.4), run_time=0.3)
            
            mid_y = (cells[0][0].get_y() + ans_cells[0][0].get_y()) / 2 + 0.3

            # Line 13: ans[i] = ans[i] * suffixProd;
            self.play(highlight_line(13), run_time=0.3)
            ans_cells[i][0].set_z_index(1)
            self.play(ans_cells[i][0].animate.set_stroke(BLUE, width=4), run_time=0.3)

            curr_val = ans_vals_array[i]
            new_val = curr_val * suffix_prod
            ans_vals_array[i] = new_val

            calc = VGroup(
                Text("ans[i] =", font=typo.font_code(), font_size=20, color=WHITE),
                Text(str(curr_val), font=typo.font_code(), font_size=24, color=GREEN),
                Text("×", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(suffix_prod), font=typo.font_code(), font_size=24, color=RED),
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN)
            ).arrange(RIGHT, buff=0.2)
            calc.set_y(mid_y)
            calc.align_to(nums_label, LEFT)

            copy_ans = ans_cells[i][1].copy()
            copy_suffix = suffix_text[1].copy()

            self.play(
                FadeIn(calc[0]),
                copy_ans.animate.move_to(calc[1].get_center()),
                copy_suffix.animate.move_to(calc[3].get_center()),
                run_time=0.5
            )
            self.play(FadeIn(calc[2]), FadeIn(calc[4]), FadeIn(calc[5]), run_time=0.3)
            self.wait(0.2)

            ans_val = Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[i][0].get_center())
            self.play(
                FadeOut(ans_cells[i][1]),
                ReplacementTransform(calc[5].copy(), ans_val),
                FadeOut(calc), FadeOut(copy_ans), FadeOut(copy_suffix),
                run_time=0.5
            )
            ans_cells[i].remove(ans_cells[i][1])
            ans_cells[i].insert(1, ans_val)

            self.play(ans_cells[i][0].animate.set_stroke(WHITE, width=2), run_time=0.2)
            ans_cells[i][0].set_z_index(0)
            
            # Line 14: suffixProd = suffixProd * nums[i];
            self.play(highlight_line(14), run_time=0.3)
            
            cells[i][0].set_z_index(1)
            self.play(cells[i][0].animate.set_stroke(YELLOW, width=4), run_time=0.3)

            calc = VGroup(
                Text("suffixProd =", font=typo.font_code(), font_size=20, color=WHITE),
                Text(str(suffix_prod), font=typo.font_code(), font_size=24, color=RED),
                Text("×", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(nums_array[i]), font=typo.font_code(), font_size=24, color=WHITE),
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(suffix_prod * nums_array[i]), font=typo.font_code(), font_size=24, color=RED)
            ).arrange(RIGHT, buff=0.2)
            calc.set_y(mid_y)
            calc.align_to(nums_label, LEFT)

            copy_suffix = suffix_text[1].copy()
            copy_num = cells[i][1].copy()

            self.play(
                FadeIn(calc[0]),
                copy_suffix.animate.move_to(calc[1].get_center()),
                copy_num.animate.move_to(calc[3].get_center()),
                run_time=0.5
            )
            self.play(FadeIn(calc[2]), FadeIn(calc[4]), FadeIn(calc[5]), run_time=0.3)
            self.wait(0.2)

            suffix_prod *= nums_array[i]
            new_suffix_val = Text(str(suffix_prod), font=typo.font_code(), font_size=24, color=RED).next_to(suffix_text[0], RIGHT, buff=0.1)

            fade_outs = [FadeOut(calc[0]), FadeOut(calc[1]), FadeOut(calc[2]), FadeOut(calc[3]), FadeOut(calc[4]), FadeOut(copy_suffix), FadeOut(copy_num), FadeOut(suffix_text[1])]
            self.play(
                ReplacementTransform(calc[5], new_suffix_val),
                *fade_outs,
                run_time=0.5
            )
            suffix_text.remove(suffix_text[1])
            suffix_text.add(new_suffix_val)

            self.play(cells[i][0].animate.set_stroke(WHITE, width=2), run_time=0.2)
            cells[i][0].set_z_index(0)

        # Line 17: return ans;
        self.play(highlight_line(17))
        self.play(FadeOut(suffix_text), FadeOut(i_ptr), run_time=0.5)
        
        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(1)", color_type="green", position="left")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = WalkthroughJava()
    scene.render()
