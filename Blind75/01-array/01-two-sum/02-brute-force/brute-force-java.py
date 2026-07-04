from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class BruteForce(Scene):
    def construct(self):
        # ১. প্রিমিয়াম ম্যাট অফ-ব্ল্যাক ব্যাকগ্রাউন্ড
        from components.typography import Typography
        from components.screenTemplate import ScreenTemplate
        
        typo = Typography()
        screen_template = ScreenTemplate(self, typo)
        
        self.camera.background_color = typo.bg()
        
        # কালার থিম কনস্ট্যান্টস (Pattern Problem Template)
        WHITE = typo.color_white()
        GRAY = typo.color_gray()
        YELLOW = typo.color_yellow()
        RED = typo.color_red()
        GREEN = typo.color_green()
        BLUE = typo.color_blue()
        BLACK = typo.text_on_yellow()

        
        # কালার থিম কনস্ট্যান্টস
        BG_I_BLUE = "#1A73E8"       # i পয়েন্টারের জন্য ব্লু
        BG_J_ORANGERED = "#DC3545"  # j পয়েন্টারের জন্য অরেঞ্জ-রেড
        BORDER_YELLOW = YELLOW
        HIGHLIGHT_BLUE = BLUE       # কমপ্লেক্সিটি বক্সের জন্য পিওর ব্লু
        
        # ==========================================
        # ২. LAYOUT SETUP (Fixed: Clean Title without Complexity)
        # ==========================================
        
        # স্ক্রিন ইন্ডিকেটর ব্যবহার করা হলো
        screen_template.screen_brute_force("Brute Force")


        nums_label = Text("nums = ", font="Sans", font_size=24, color=WHITE)
        
        nums = [2, 1, 3, 5, 8]
        array_cells = VGroup(*[
            VGroup(
                Square(side_length=1.0, color=WHITE, stroke_width=4, fill_opacity=0),
                Text(str(val), font="Sans", font_size=26, color=WHITE)
            ) for val in nums
        ]).arrange(buff=0)
        
        array_with_label = VGroup(nums_label, array_cells).arrange(RIGHT, buff=0.25)
        array_with_label.move_to(LEFT * 2.0 + UP * 0.6)
        
        indices = VGroup(*[
            Text(str(idx), font="Monospace", font_size=16, color=GRAY)
            .next_to(array_cells[idx][0], UP, buff=0.15)
            for idx in range(len(nums))
        ])
        
        left_content = VGroup(array_with_label, indices)

        target_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.9, color=WHITE, stroke_width=2.5, fill_opacity=0)
        target_txt = Text("Target = 9", font="Sans", font_size=22, color=WHITE)
        right_target_group = VGroup(target_box, target_txt).move_to(RIGHT * 4.2 + UP * 0.6)

        self.play(
            FadeIn(left_content, shift=RIGHT * 0.3),
            FadeIn(right_target_group, shift=LEFT * 0.3),
            run_time=1.2
        )
        self.wait(0.4)

        # ==========================================
        # ৩. POINTER GENERATION (Shortened 4x Thick Arrows)
        # ==========================================
        
        i_arrow = Arrow(DOWN * 0.35, ORIGIN, color=BG_I_BLUE, stroke_width=24, max_tip_length_to_length_ratio=0.45, buff=0)
        i_label = Text("i", font="Sans", font_size=30, weight=BOLD, color=BG_I_BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label).next_to(array_cells[0][0], DOWN, buff=0.2) 

        j_arrow = Arrow(UP * 0.35, ORIGIN, color=BG_J_ORANGERED, stroke_width=24, max_tip_length_to_length_ratio=0.45, buff=0)
        j_label = Text("j", font="Sans", font_size=30, weight=BOLD, color=BG_J_ORANGERED).next_to(j_arrow, UP, buff=0.1)
        j_ptr = VGroup(j_label, j_arrow).next_to(indices[1], UP, buff=0.2) 

        self.play(FadeIn(i_ptr), FadeIn(j_ptr), run_time=0.6)
        self.wait(0.3)

        # ==========================================
        # ৪. BRUTE FORCE SIMULATION CORE LOGIC
        # ==========================================
        
        calc_y_pos = -2.2 
        
        def check_pair(i, j, is_match=False):
            self.bring_to_front(array_cells[i], array_cells[j])
            
            self.play(
                i_ptr.animate.next_to(array_cells[i][0], DOWN, buff=0.2),
                j_ptr.animate.next_to(indices[j], UP, buff=0.2),
                array_cells[i][0].animate.set_fill(BG_I_BLUE, opacity=1),
                array_cells[j][0].animate.set_fill(BG_J_ORANGERED, opacity=1),
                run_time=0.8
            )
            
            val_i_copy = array_cells[i][1].copy()
            val_j_copy = array_cells[j][1].copy()
            
            plus_sign = Text("+", font="Sans", font_size=24, color=WHITE).move_to(np.array([-0.8, calc_y_pos, 0]))
            eq_sign = Text("=", font="Sans", font_size=24, color=WHITE).move_to(np.array([0.6, calc_y_pos, 0]))
            
            current_sum = nums[i] + nums[j]
            sum_txt = Text(str(current_sum), font="Sans", font_size=24, color=WHITE).move_to(np.array([1.4, calc_y_pos, 0]))
            
            self.play(
                val_i_copy.animate.next_to(plus_sign, LEFT, buff=0.3),
                val_j_copy.animate.next_to(plus_sign, RIGHT, buff=0.3),
                FadeIn(plus_sign),
                FadeIn(eq_sign),
                FadeIn(sum_txt),
                run_time=0.8
            )
            
            if not is_match:
                not_equal_sign = Text("≠ 9", font="Sans", font_size=24, color=RED).next_to(sum_txt, RIGHT, buff=0.4)
                self.play(Write(not_equal_sign), run_time=0.4)
                self.wait(0.4)
                
                self.play(
                    FadeOut(val_i_copy), FadeOut(val_j_copy), 
                    FadeOut(plus_sign), FadeOut(eq_sign), 
                    FadeOut(sum_txt), FadeOut(not_equal_sign),
                    array_cells[j][0].animate.set_fill(BLACK, opacity=0), 
                    run_time=0.5
                )
            else:
                equal_target = Text("== 9", font="Sans", font_size=24, color=GREEN).next_to(sum_txt, RIGHT, buff=0.4)
                self.play(
                    array_cells[i][0].animate.set_stroke(color=BORDER_YELLOW, width=8),
                    array_cells[j][0].animate.set_stroke(color=BORDER_YELLOW, width=8),
                    Write(equal_target),
                    run_time=0.6
                )
                self.wait(0.4)
                
                equation_group = VGroup(val_i_copy, plus_sign, val_j_copy, eq_sign, sum_txt, equal_target)
                
                final_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.8, color=BORDER_YELLOW, stroke_width=4, fill_opacity=0)
                final_box.move_to(np.array([0, calc_y_pos, 0]))
                
                final_txt = Text("[1, 4]", font="Sans", font_size=26, color=WHITE).move_to(final_box.get_center())
                
                idx1_flying_copy = indices[1].copy()
                idx4_flying_copy = indices[4].copy()
                self.bring_to_front(idx1_flying_copy, idx4_flying_copy)
                
                self.play(
                    ReplacementTransform(equation_group, final_box),
                    FadeOut(i_ptr), FadeOut(j_ptr),
                    FadeIn(final_txt[0]), 
                    FadeIn(final_txt[2]), 
                    FadeIn(final_txt[4]), 
                    ReplacementTransform(idx1_flying_copy, final_txt[1]), 
                    ReplacementTransform(idx4_flying_copy, final_txt[3]),
                    run_time=1.6,
                    rate_func=smooth
                )
                
                self.play(
                    Flash(final_box, color=BORDER_YELLOW, flash_radius=1.0, num_lines=16, line_stroke_width=4),
                    run_time=0.5
                )
                self.wait(0.4)

                # ==========================================
                # ৫. COMPLEXITY PANEL (Lower Third from ScreenTemplate)
                # ==========================================
                screen_template.show_lower_third("Complexity Analysis", "Time: O(N²), Space: O(1)", color_type="red")

        # ==========================================
        # ৬. SIMULATION EXECUTION STEPS
        # ==========================================
        check_pair(0, 1) 
        check_pair(0, 2) 
        check_pair(0, 3) 
        check_pair(0, 4) 
        
        self.play(array_cells[0][0].animate.set_fill(BLACK, opacity=0), run_time=0.3)
        
        check_pair(1, 2) 
        check_pair(1, 3) 
        
        # সলিউশন হিট এবং ফাইনাল সেলিব্রেশন!
        check_pair(1, 4, is_match=True)
        self.wait(3)