from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class HashMapSolution0(Scene):
    def construct(self):
        # ১. প্রিমিয়াম ম্যাট অফ-ব্ল্যাক ব্যাকগ্রাউন্ড
        from components.typography import Typography
        from components.screenTemplate import ScreenTemplate
        
        typo = Typography()
        screen_template = ScreenTemplate(self, typo)
        
        self.camera.background_color = typo.bg()
        
        # কালার থিম কনস্ট্যান্টস
        WHITE = typo.color_white()
        GRAY = typo.color_gray()
        GRAY_A = typo.color_secondary()
        YELLOW = typo.color_yellow()
        RED = typo.color_red()
        GREEN = typo.color_green()
        BLUE = typo.color_blue()
        BLACK = typo.text_on_yellow()
        
        SCAN_BLUE = "#1A73E8"       
        SUCCESS_BOOTSTRAP_GREEN = "#198754" 
        BORDER_ORANGERED = "#DC3545" 
        
        # ==========================================
        # ২. LAYOUT SETUP (WITHOUT HASH MAP)
        # ==========================================
        
        screen_template.screen_optimal_approach("Optimal Approach")

        nums_label = Text("nums = ", font="Sans", font_size=24, color=WHITE)
        
        nums = [2, 1, 3, 5, 8]
        array_cells = VGroup(*[
            VGroup(
                Square(side_length=1.0, color=WHITE, stroke_width=4, fill_opacity=0),
                Text(str(val), font="Sans", font_size=26, color=WHITE)
            ) for val in nums
        ]).arrange(buff=0)
        
        array_with_label = VGroup(nums_label, array_cells).arrange(RIGHT, buff=0.25)
        array_with_label.move_to(UP * 0.8) 
        
        indices = VGroup(*[
            Text(str(idx), font="Monospace", font_size=16, color=GRAY)
            .next_to(array_cells[idx][0], UP, buff=0.15)
            for idx in range(len(nums))
        ])
        
        center_content = VGroup(array_with_label, indices)

        target_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.9, color=WHITE, stroke_width=2.5, fill_opacity=0)
        target_txt = Text("Target = 9", font="Sans", font_size=22, color=WHITE)
        right_target_group = VGroup(target_box, target_txt).move_to(RIGHT * 4.0 + UP * 2.6)

        self.play(
            FadeIn(center_content, shift=UP * 0.2),
            FadeIn(right_target_group, shift=LEFT * 0.3),
            run_time=1.2
        )
        self.wait(0.3)

        # ==========================================
        # ৩. POINTER GENERATION
        # ==========================================
        i_arrow = Arrow(DOWN * 0.35, ORIGIN, color=SCAN_BLUE, stroke_width=24, max_tip_length_to_length_ratio=0.45, buff=0)
        i_label = Text("i", font="Sans", font_size=30, weight=BOLD, color=SCAN_BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label).next_to(array_cells[0][0], DOWN, buff=0.2) 
        
        self.play(FadeIn(i_ptr), run_time=0.5)

        # ==========================================
        # ৪. FAST TRAVERSAL (INDEX 0 -> 1 -> 2)
        # ==========================================
        # Index 0 active -> inactive -> Index 1 active -> 2 active -> 3
        self.play(array_cells[0][0].animate.set_fill(SCAN_BLUE, opacity=1), run_time=0.4)
        self.wait(0.2)
        self.play(
            array_cells[0][0].animate.set_fill(SCAN_BLUE, opacity=0.2),
            i_ptr.animate.next_to(array_cells[1][0], DOWN, buff=0.2),
            array_cells[1][0].animate.set_fill(SCAN_BLUE, opacity=1),
            run_time=0.5
        )
        self.wait(0.2)
        self.play(
            array_cells[1][0].animate.set_fill(SCAN_BLUE, opacity=0.2),
            i_ptr.animate.next_to(array_cells[2][0], DOWN, buff=0.2),
            array_cells[2][0].animate.set_fill(SCAN_BLUE, opacity=1),
            run_time=0.5
        )
        self.wait(0.2)
        self.play(
            array_cells[2][0].animate.set_fill(SCAN_BLUE, opacity=0.2),
            i_ptr.animate.next_to(array_cells[3][0], DOWN, buff=0.2),
            run_time=0.5
        )

        # ==========================================
        # ৫. INDEX 3 DETAILED EVALUATION
        # ==========================================
        # Mark Index 3 as current
        self.play(array_cells[3][0].animate.set_fill(SCAN_BLUE, opacity=1), run_time=0.4)
        self.wait(0.3)

        # Create Bracket [first, second]
        b_open = Text("[ ", font="Sans", font_size=26, color=WHITE)
        first_txt = Text("first", font="Sans", font_size=24, color=GRAY_A)
        comma_txt = Text(",  ", font="Sans", font_size=26, color=WHITE)
        second_txt = Text("second", font="Sans", font_size=24, color=GRAY_A)
        b_close = Text(" ]", font="Sans", font_size=26, color=WHITE)

        bracket_group = VGroup(b_open, first_txt, comma_txt, second_txt, b_close).arrange(RIGHT, buff=0.08)
        bracket_group.move_to(DOWN * 1.2)

        self.play(Write(bracket_group), run_time=0.6)
        self.wait(0.3)

        # Animate update second to 5 (nums[3])
        val_5 = Text("5", font="Sans", font_size=26, color=YELLOW)
        val_5.move_to(second_txt.get_center())
        
        fly_curr_3 = array_cells[3][1].copy()
        self.play(
            ReplacementTransform(second_txt, val_5),
            fly_curr_3.animate.move_to(val_5.get_center()).set_color(YELLOW),
            run_time=0.6
        )
        self.remove(fly_curr_3)
        self.wait(0.4)

        # Formula & complement calculation: target - 5 = 4
        formula_txt = Text("complement = target - nums[i]  =  9 - 5 = 4", font="Sans", font_size=20, color=WHITE)
        formula_txt.move_to(DOWN * 2.2)
        self.play(FadeIn(formula_txt, shift=UP * 0.2), run_time=0.5)
        self.wait(0.4)

        # Replace first with 4
        val_4 = Text("4", font="Sans", font_size=26, color=YELLOW)
        val_4.move_to(first_txt.get_center())
        self.play(ReplacementTransform(first_txt, val_4), run_time=0.6)
        self.wait(0.4)

        # Highlight index 0 to index 2 history
        history_group_3 = VGroup(*[array_cells[k][0] for k in range(3)])
        history_border_3 = SurroundingRectangle(history_group_3, color=BORDER_ORANGERED, stroke_width=4, buff=0.1)
        
        lookup_txt = Text("", font="Sans", font_size=20, color=BORDER_ORANGERED)
        lookup_txt.next_to(history_border_3, UP, buff=0.4)
        
        self.play(Create(history_border_3), Write(lookup_txt), run_time=0.6)
        self.wait(0.3)

        # 4 not found -> Red border pulse effect (stroke width pulses without hiding)
        self.play(history_border_3.animate.set_stroke(width=10), run_time=0.25)
        self.play(history_border_3.animate.set_stroke(width=4), run_time=0.25)
        self.play(history_border_3.animate.set_stroke(width=10), run_time=0.25)
        self.play(history_border_3.animate.set_stroke(width=4), run_time=0.25)
        self.wait(0.3)

        # Deactivate border and cleanup text
        self.play(
            FadeOut(history_border_3),
            FadeOut(lookup_txt),
            FadeOut(formula_txt),
            FadeOut(bracket_group),
            FadeOut(val_4),
            FadeOut(val_5),
            array_cells[3][0].animate.set_fill(SCAN_BLUE, opacity=0.2),
            run_time=0.6
        )
        self.wait(0.3)

        # ==========================================
        # ৬. INDEX 4 DETAILED EVALUATION
        # ==========================================
        # Pointer to Index 4
        self.play(
            i_ptr.animate.next_to(array_cells[4][0], DOWN, buff=0.2),
            array_cells[4][0].animate.set_fill(SCAN_BLUE, opacity=1),
            run_time=0.5
        )
        self.wait(0.3)

        # Create Bracket [first, second]
        b_open_4 = Text("[ ", font="Sans", font_size=26, color=WHITE)
        first_txt_4 = Text("first", font="Sans", font_size=24, color=GRAY_A)
        comma_txt_4 = Text(",  ", font="Sans", font_size=26, color=WHITE)
        second_txt_4 = Text("second", font="Sans", font_size=24, color=GRAY_A)
        b_close_4 = Text(" ]", font="Sans", font_size=26, color=WHITE)

        bracket_group_4 = VGroup(b_open_4, first_txt_4, comma_txt_4, second_txt_4, b_close_4).arrange(RIGHT, buff=0.08)
        bracket_group_4.move_to(DOWN * 1.2)

        self.play(Write(bracket_group_4), run_time=0.6)
        self.wait(0.3)

        # Animate update second to 8 (nums[4])
        val_8 = Text("8", font="Sans", font_size=26, color=YELLOW)
        val_8.move_to(second_txt_4.get_center())
        
        fly_curr_4 = array_cells[4][1].copy()
        self.play(
            ReplacementTransform(second_txt_4, val_8),
            fly_curr_4.animate.move_to(val_8.get_center()).set_color(YELLOW),
            run_time=0.6
        )
        self.remove(fly_curr_4)
        self.wait(0.4)

        # Formula & complement calculation: target - 8 = 1
        formula_txt_4 = Text("complement = target - nums[i]  =  9 - 8 = 1", font="Sans", font_size=20, color=WHITE)
        formula_txt_4.move_to(DOWN * 2.2)
        self.play(FadeIn(formula_txt_4, shift=UP * 0.2), run_time=0.5)
        self.wait(0.4)

        # Replace first with 1
        val_1 = Text("1", font="Sans", font_size=26, color=YELLOW)
        val_1.move_to(first_txt_4.get_center())
        self.play(ReplacementTransform(first_txt_4, val_1), run_time=0.6)
        self.wait(0.4)

        # Highlight index 0 to index 3 history border
        history_group_4 = VGroup(*[array_cells[k][0] for k in range(4)])
        history_border_4 = SurroundingRectangle(history_group_4, color=BORDER_ORANGERED, stroke_width=4, buff=0.1)
        
        lookup_txt_4 = Text("", font="Sans", font_size=20, color=BORDER_ORANGERED)
        lookup_txt_4.next_to(history_border_4, UP, buff=0.4)

        self.play(Create(history_border_4), Write(lookup_txt_4), run_time=0.6)
        self.wait(0.4)

        # Match found at Index 1 (nums[1] = 1)
        match_found_txt = Text(" ", font="Sans", font_size=20, color=GREEN)
        match_found_txt.move_to(lookup_txt_4.get_center())
        
        self.play(ReplacementTransform(lookup_txt_4, match_found_txt), run_time=0.4)
        
        # Bring matched nodes to front so green border draws cleanly on top of adjacent elements
        self.bring_to_front(array_cells[1], array_cells[4])
        
        # Success highlight on matching nodes
        self.play(
            FadeOut(history_border_4),
            array_cells[1][0].animate.set_stroke(color=SUCCESS_BOOTSTRAP_GREEN, width=8).set_fill(BLACK, opacity=0),
            array_cells[4][0].animate.set_stroke(color=SUCCESS_BOOTSTRAP_GREEN, width=8).set_fill(BLACK, opacity=0),
            run_time=0.7
        )
        self.wait(0.3)

        # Final Solution Box [1, 4]
        final_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.8, color=SUCCESS_BOOTSTRAP_GREEN, stroke_width=4, fill_opacity=0)
        final_box.move_to(DOWN * 1.8)
        
        sol_open = Text("[", font="Sans", font_size=26, color=WHITE)
        sol_1 = Text("1", font="Sans", font_size=26, color=WHITE)
        sol_comma = Text(",  ", font="Sans", font_size=26, color=WHITE) 
        sol_4 = Text("4", font="Sans", font_size=26, color=WHITE)
        sol_close = Text("]", font="Sans", font_size=26, color=WHITE)
        
        final_txt_group = VGroup(sol_open, sol_1, sol_comma, sol_4, sol_close).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        final_txt_group.move_to(final_box.get_center())

        self.play(
            FadeOut(match_found_txt),
            FadeOut(formula_txt_4),
            FadeOut(bracket_group_4),
            FadeOut(val_1),
            FadeOut(val_8),
            FadeOut(i_ptr),
            Create(final_box),
            Write(final_txt_group),
            run_time=1.2
        )

        self.play(
            Flash(final_box, color=SUCCESS_BOOTSTRAP_GREEN, flash_radius=1.0, num_lines=16, line_stroke_width=4),
            run_time=0.5
        )
        self.wait(0.5)

        # ==========================================
        # ৭. COMPLEXITY ANALYSIS
        # ==========================================
        # screen_template.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(1)", color_type="green")
        self.wait(3)
