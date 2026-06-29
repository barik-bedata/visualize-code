from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class Statement(Scene):
    def construct(self):
        # ১. প্রিমিয়াম ম্যাট অফ-ব্ল্যাক ব্যাকগ্রাউন্ড 
        from components.typography import Typography
        from components.screenTemplate import ScreenTemplate
        from components.highlighter import RangeHighlighter
        
        typo = Typography()
        screen_template = ScreenTemplate(self, typo)
        
        self.camera.background_color = typo.bg()
        
        # কালার থিম কনস্ট্যান্টস (Pattern Problem Template)
        WHITE = typo.color_white()
        GRAY = typo.color_gray()
        YELLOW = typo.color_yellow()
        BLUE = typo.color_blue()
        
        # কালার কনস্ট্যান্টস
        BG_SELECTED_PURPLE = BLUE # রয়্যাল পার্পল ফিল
        BORDER_YELLOW = YELLOW

        # ==========================================
        # ২. LAYOUT SETUP (Title, Array with Label, Target)
        # ==========================================
        
        # টপ-লেফট কর্নারে স্ক্রিন ইন্ডিকেটর
        screen_template.screen_statement("Problem Statement")


        # বামপাশের "nums = " লেবেল
        nums_label = Text("nums = ", font="Sans", font_size=24, color=WHITE)
        
        # জিরো-গ্যাপ মেমোরি অ্যারে
        nums = [2, 1, 3, 5, 8]
        array_cells = VGroup(*[
            VGroup(
                Square(side_length=1.0, color=WHITE, stroke_width=4, fill_opacity=0),
                Text(str(val), font="Sans", font_size=26, color=WHITE)
            ) for val in nums
        ]).arrange(buff=0)
        
        # [FIXED SPACE] স্ক্রিনের ডেড স্পেস কমাতে অ্যারে উইন্ডোকে UP * 0.6 পজিশনে ওপরে তোলা হলো
        array_with_label = VGroup(nums_label, array_cells).arrange(RIGHT, buff=0.25)
        array_with_label.move_to(LEFT * 2.0 + UP * 0.6)
        
        # বক্সগুলো ওপরে সেটেল হওয়ার পর তাদের মাথার ওপর পারফেক্টলি ইনডেক্স প্লেস করা হলো
        indices = VGroup(*[
            Text(str(idx), font="Monospace", font_size=16, color=GRAY)
            .next_to(array_cells[idx][0], UP, buff=0.15)
            for idx in range(len(nums))
        ])
        
        # পুরো কমপ্লিট লেফট গ্রুপ
        left_content = VGroup(array_with_label, indices)

        # [FIXED SPACE] ডানপাশের মডার্ন টার্গেট ক্যাপসুলকেও অ্যারের সমান্তরালে UP * 0.6 এ তোলা হলো
        target_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.9, color=WHITE, stroke_width=2.5, fill_opacity=0)
        target_txt = Text("Target = 9", font="Sans", font_size=22, color=WHITE)
        right_target_group = VGroup(target_box, target_txt).move_to(RIGHT * 4.2 + UP * 0.6)

        # স্ক্রিনে লেআউট লোড হওয়া
        self.play(
            FadeIn(left_content, shift=RIGHT * 0.3),
            FadeIn(right_target_group, shift=LEFT * 0.3),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Reusable Highlighter Component for Array & Target Box
        hl_array = RangeHighlighter(self, BORDER_YELLOW)
        hl_array.create(array_cells, 0, len(nums) - 1, buff=0.08, stroke_width=3)
        
        hl_target = RangeHighlighter(self, BORDER_YELLOW)
        hl_target.create(VGroup(target_box), 0, 0, buff=0.08, stroke_width=3)
        
        # Border highlight show
        self.play(
            Create(hl_array.border),
            Create(hl_target.border),
            run_time=0.6
        )
        self.wait(0.4)
        
        # Border highlight hide (fadeout)
        self.play(
            FadeOut(hl_array.border),
            FadeOut(hl_target.border),
            run_time=0.6
        )
        self.wait(0.3)

        # ==========================================
        # ৩. SELECTION PHASE (Zero-Gap Fix - Border then Purple Fill)
        # ==========================================
        
        cell_1 = array_cells[1]
        cell_4 = array_cells[4]
        
        # নোড দুটিকে লেয়ারের সামনে আনা হলো যেন বর্ডার গ্লিচ না করে
        self.bring_to_front(cell_1, cell_4)
        
        # স্কয়ারের ৪টি বর্ডারই কমপ্লিটলি মোটা এবং চওড়া হলুদ হবে
        self.play(
            cell_1[0].animate.set_stroke(color=BORDER_YELLOW, width=8),
            cell_4[0].animate.set_stroke(color=BORDER_YELLOW, width=8),
            run_time=0.7,
            rate_func=smooth
        )
        
        # ব্যাকগ্রাউন্ড কালার গর্জিয়াস পার্পল ফিল হবে এবং ফ্ল্যাশ ফুটবে
        self.play(
            cell_1[0].animate.set_fill(BG_SELECTED_PURPLE, opacity=1),
            cell_4[0].animate.set_fill(BG_SELECTED_PURPLE, opacity=1),
            Flash(cell_1[0], color=BORDER_YELLOW, flash_radius=0.7, num_lines=12, line_stroke_width=4),
            Flash(cell_4[0], color=BORDER_YELLOW, flash_radius=0.7, num_lines=12, line_stroke_width=4),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(0.6)

        # ==========================================
        # ৪. SUMMATION PHASE (Values Move Down & Replace with Sum)
        # ==========================================
        
        val1_copy = cell_1[1].copy()
        val2_copy = cell_4[1].copy()
        
        # ওপরে স্পেস তৈরি হওয়ায় ক্যালকুলেশন পজিশনটি আরেকটু ওপরে (y = -1.4) সেট করা হলো
        calc_y_pos = -1.4
        plus_sign = Text("+", font="Sans", font_size=24, color=WHITE).move_to(np.array([0, calc_y_pos, 0]))
        
        self.play(
            val1_copy.animate.next_to(plus_sign, LEFT, buff=0.4),
            val2_copy.animate.next_to(plus_sign, RIGHT, buff=0.4),
            FadeIn(plus_sign),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(0.5)
        
        equation_group = VGroup(val1_copy, plus_sign, val2_copy)
        
        sum_box = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.6, color=WHITE, stroke_width=2, fill_opacity=0)
        sum_txt = Text("9", font="Sans", font_size=24, color=WHITE)
        sum_card = VGroup(sum_box, sum_txt).move_to(np.array([0, calc_y_pos, 0]))
        
        self.play(
            ReplacementTransform(equation_group, sum_card),
            run_time=0.8
        )
        self.wait(0.6)

        # ==========================================
        # ৫. FINAL REPLACEMENT (Perfect Spacing & Flying Indices)
        # ==========================================
        
        # হলুদ বর্ডারযুক্ত চূড়ান্ত আউটপুট বক্স
        final_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.8, color=BORDER_YELLOW, stroke_width=4, fill_opacity=0)
        final_box.move_to(np.array([0, calc_y_pos, 0]))
        
        # ইন্টিগ্রেটেড পারফেক্ট টেক্সট লেআউট
        final_txt = Text("[1, 4]", font="Sans", font_size=26, color=WHITE).move_to(final_box.get_center())
        
        # ওপরের ইনডেক্স ট্র্যাকারের নতুন পজিশন থেকে নিখুঁত লাইভ কপি জেনারেশন
        idx1_flying_copy = indices[1].copy()
        idx4_flying_copy = indices[4].copy()
        
        self.bring_to_front(idx1_flying_copy, idx4_flying_copy)
        
        # ম্যাজিক ট্র্যান্সফর্ম: সংখ্যা '9' চলে যাবে, এবং উপর থেকে ইনডেক্স দুটি উড়ে এসে ক্যারেক্টার পজিশনে লক হবে
        self.play(
            ReplacementTransform(sum_box, final_box),
            FadeOut(sum_txt),
            FadeIn(final_txt[0]), # '['
            FadeIn(final_txt[2]), # ','
            FadeIn(final_txt[4]), # ']'
            ReplacementTransform(idx1_flying_copy, final_txt[1]), 
            ReplacementTransform(idx4_flying_copy, final_txt[3]),
            run_time=1.6,
            rate_func=smooth
        )
        
        # এজের ফাইনাল সাকসেস ফ্ল্যাশ
        self.play(
            Flash(final_box, color=BORDER_YELLOW, flash_radius=1.0, num_lines=16, line_stroke_width=4),
            run_time=0.5
        )
        self.wait(3)