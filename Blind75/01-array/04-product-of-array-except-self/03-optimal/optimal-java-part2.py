from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class OptimalJavaPart2(Scene):
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
            val_str = ""
            cell_val = Text(val_str, font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=20, color="#B3B3B3").next_to(cell_bg, UP, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            ans_cells.add(cell)
            
        ans_cells.arrange(RIGHT, buff=0)
        ans_cells.next_to(cells, DOWN, buff=2.0)
        ans_label = Text("answer =", font=typo.font_code(), font_size=24, color=WHITE).next_to(ans_cells, LEFT, buff=0.5)
        ans_label.match_y(ans_cells[0][0])
        ans_group = VGroup(ans_label, ans_cells)
        
        left_column = VGroup(array_group, ans_group)

        # ==========================================
        # 2. ALGORITHM LOGIC SETUP (Right Side)
        # ==========================================
        algo_title = Text("Algorithm:", font=typo.font_ui(), font_size=28, color=YELLOW, weight=BOLD)
        algo_lines = VGroup(
            Text("1. Initialize answer array", font=typo.font_code(), font_size=24, color=WHITE),
            Text("2. Left pass:", font=typo.font_code(), font_size=24, color=WHITE),
            Text("      Compute prefix products", font=typo.font_code(), font_size=24, color=WHITE),
            Text("3. Right pass:", font=typo.font_code(), font_size=24, color=WHITE),
            Text("      Compute suffix products", font=typo.font_code(), font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        algo_lines.next_to(algo_title, DOWN, buff=0.5, aligned_edge=LEFT)
        algo_group = VGroup(algo_title, algo_lines)

        main_layout = VGroup(left_column, algo_group).arrange(RIGHT, buff=2.5)
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
        
        # Initially first element e 1 thakbe animation diye
        ans_val_0 = Text("1", font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[0][0].get_center())
        self.play(
            FadeIn(ans_val_0),
            ans_cells[0][0].animate.set_fill(GREEN, opacity=0.3),
            run_time=0.5
        )
        ans_cells[0].remove(ans_cells[0][1])
        ans_cells[0].insert(1, ans_val_0)

        i_ptr.next_to(ans_cells[1][0], DOWN, buff=0.2)
        self.play(FadeIn(i_ptr), run_time=0.3)

        ans_vals_array = [1] * len(nums_array)
        for i in range(1, len(nums_array)):
            if i > 1:
                self.play(i_ptr.animate.next_to(ans_cells[i][0], DOWN, buff=0.2), run_time=0.3)
            
            # Highlight i-1 in nums and i-1 in answer
            cells[i-1][0].set_z_index(1)
            ans_cells[i-1][0].set_z_index(1)
            self.play(
                cells[i-1][0].animate.set_stroke(YELLOW, width=4),
                ans_cells[i-1][0].animate.set_stroke(YELLOW, width=4),
                run_time=0.3
            )
            
            # Highlight current answer cell where the result will be placed
            ans_cells[i][0].set_z_index(1)
            self.play(ans_cells[i][0].animate.set_stroke(BLUE, width=4), run_time=0.3)
            
            # Build equation nums[i-1] x ans[i-1] = new_val
            mid_y = (cells[0][0].get_y() + ans_cells[0][0].get_y()) / 2 + 0.3
            
            curr_ans_val = ans_vals_array[i-1]
            curr_num_val = nums_array[i-1]
            new_val = curr_ans_val * curr_num_val
            ans_vals_array[i] = new_val
            
            calc_group = VGroup(
                Text("prefixProd =", font=typo.font_code(), font_size=20, color=WHITE),
                Text(str(curr_num_val), font=typo.font_code(), font_size=24, color=WHITE),
                Text("×", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(curr_ans_val), font=typo.font_code(), font_size=24, color=WHITE),
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN)
            ).arrange(RIGHT, buff=0.2)
            calc_group.set_y(mid_y)
            calc_group.align_to(cells[0][0], LEFT)
            
            self.play(FadeIn(calc_group[0]), run_time=0.3)
            
            # Animate copies
            copy_num = cells[i-1][1].copy()
            copy_ans = ans_cells[i-1][1].copy()
            
            self.play(
                copy_num.animate.move_to(calc_group[1].get_center()),
                copy_ans.animate.move_to(calc_group[3].get_center()),
                run_time=0.5
            )
            
            self.play(FadeIn(calc_group[2]), run_time=0.2) # ×
            self.play(FadeIn(calc_group[4]), FadeIn(calc_group[5]), run_time=0.3) # = new_val
            self.wait(0.2)
            
            ans_val = Text(str(new_val), font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[i][0].get_center())
            
            # Remove all copies, cross signs, eq text
            fade_outs = [FadeOut(copy_num), FadeOut(copy_ans), FadeOut(calc_group), FadeOut(ans_cells[i][1])]
            
            self.play(
                ReplacementTransform(calc_group[5].copy(), ans_val),
                ans_cells[i][0].animate.set_fill(GREEN, opacity=0.3),
                *fade_outs,
                run_time=0.5
            )
            
            ans_cells[i].remove(ans_cells[i][1])
            ans_cells[i].insert(1, ans_val)
            
            # Unhighlight
            un_hl_anims = [
                ans_cells[i][0].animate.set_stroke(WHITE, width=2),
                ans_cells[i-1][0].animate.set_stroke(WHITE, width=2),
                cells[i-1][0].animate.set_stroke(WHITE, width=2)
            ]
            ans_cells[i][0].set_z_index(0)
            ans_cells[i-1][0].set_z_index(0)
            cells[i-1][0].set_z_index(0)
            self.play(*un_hl_anims, run_time=0.2)
            
        self.wait(5)

        # Postfix Pass
        for i in range(len(nums_array)-1, -1, -1):
            self.play(i_ptr.animate.next_to(ans_cells[i][0], DOWN, buff=0.2), run_time=0.3)
            
            # Highlight i+1 to N-1 in nums
            hl_anims = []
            for j in range(i+1, len(nums_array)):
                cells[j][0].set_z_index(1)
                hl_anims.append(cells[j][0].animate.set_stroke(YELLOW, width=4))
            if hl_anims:
                self.play(*hl_anims, run_time=0.3)
            
            # Create copies
            copies = []
            for j in range(i+1, len(nums_array)):
                copies.append(cells[j][1].copy())
                
            # Build equation postfixProd = el_i+1 x ...
            mid_y = (cells[0][0].get_y() + ans_cells[0][0].get_y()) / 2 + 0.3
            
            eq_items = [Text("postfixProd =", font=typo.font_code(), font_size=20, color=WHITE)]
            if len(copies) == 0:
                eq_items.append(Text("1", font=typo.font_code(), font_size=24, color=WHITE))
            else:
                for j in range(i+1, len(nums_array)):
                    eq_items.append(Text(str(nums_array[j]), font=typo.font_code(), font_size=24, color=WHITE))
                    if j < len(nums_array) - 1:
                        eq_items.append(Text("×", font=typo.font_code(), font_size=24, color=WHITE))
            
            calc_group = VGroup(*eq_items).arrange(RIGHT, buff=0.2)
            calc_group.set_y(mid_y)
            calc_group.align_to(cells[0][0], LEFT)
            
            # Highlight current answer cell
            ans_cells[i][0].set_z_index(1)
            
            # Animate copies to calc_group
            self.play(
                FadeIn(calc_group[0]),
                ans_cells[i][0].animate.set_stroke(BLUE, width=4),
                run_time=0.3
            )
            if len(copies) == 0:
                self.play(FadeIn(calc_group[1]), run_time=0.5)
                p_val = 1
            else:
                move_anims = []
                eq_idx = 1
                for j in range(len(copies)):
                    move_anims.append(copies[j].animate.move_to(calc_group[eq_idx].get_center()))
                    eq_idx += 2
                self.play(*move_anims, run_time=0.5)
                
                # Show cross signs
                cross_anims = []
                eq_idx = 2
                for j in range(len(copies)-1):
                    cross_anims.append(FadeIn(calc_group[eq_idx]))
                    eq_idx += 2
                if cross_anims:
                    self.play(*cross_anims, run_time=0.2)
                
                # Compute postfix product
                p_val = 1
                for j in range(i+1, len(nums_array)):
                    p_val *= nums_array[j]
            
            self.wait(0.2)
            
            eq_res = VGroup(
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(p_val), font=typo.font_code(), font_size=24, color=RED)
            ).arrange(RIGHT, buff=0.2).next_to(calc_group, RIGHT, buff=0.2)
            
            self.play(FadeIn(eq_res), run_time=0.3)
            self.wait(0.2)
            
            # Now compute final: ans[i] * p_val
            curr_val = ans_vals_array[i]
            final_val = curr_val * p_val
            
            final_eq = VGroup(
                Text(str(curr_val), font=typo.font_code(), font_size=24, color=GREEN),
                Text("×", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(p_val), font=typo.font_code(), font_size=24, color=RED),
                Text("=", font=typo.font_code(), font_size=24, color=WHITE),
                Text(str(final_val), font=typo.font_code(), font_size=24, color=GREEN)
            ).arrange(RIGHT, buff=0.2)
            final_eq.next_to(calc_group, DOWN, buff=0.4)
            final_eq.align_to(calc_group, LEFT)
            
            copy_curr = ans_cells[i][1].copy()
            copy_pval = eq_res[1].copy()
            
            self.play(
                copy_curr.animate.move_to(final_eq[0].get_center()),
                copy_pval.animate.move_to(final_eq[2].get_center()),
                FadeIn(final_eq[1]),
                run_time=0.4
            )
            self.play(FadeIn(final_eq[3]), FadeIn(final_eq[4]), run_time=0.3)
            self.wait(0.2)
            
            new_ans_val = Text(str(final_val), font=typo.font_code(), font_size=24, color=GREEN).move_to(ans_cells[i][0].get_center())
            
            fade_outs = [FadeOut(c) for c in copies] + [FadeOut(calc_group), FadeOut(eq_res), FadeOut(copy_curr), FadeOut(copy_pval), FadeOut(final_eq[1]), FadeOut(final_eq[3]), FadeOut(final_eq[0]), FadeOut(final_eq[2]), FadeOut(ans_cells[i][1])]
            
            self.play(
                ReplacementTransform(final_eq[4], new_ans_val),
                *fade_outs,
                run_time=0.5
            )
            
            ans_cells[i].remove(ans_cells[i][1])
            ans_cells[i].insert(1, new_ans_val)
            
            # Unhighlight
            un_hl_anims = [ans_cells[i][0].animate.set_stroke(WHITE, width=2)]
            ans_cells[i][0].set_z_index(0)
            for j in range(i+1, len(nums_array)):
                un_hl_anims.append(cells[j][0].animate.set_stroke(WHITE, width=2))
                cells[j][0].set_z_index(0)
            if un_hl_anims:
                self.play(*un_hl_anims, run_time=0.2)

        self.play(FadeOut(i_ptr), run_time=0.5)
        
        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(1) (excluding output array)", color_type="green", position="right")
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = OptimalJavaPart2()
    scene.render()
