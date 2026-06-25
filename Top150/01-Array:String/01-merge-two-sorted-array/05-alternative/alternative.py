from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))


from components.typography import Typography, ITypography
from components.screenTemplate import ScreenTemplate, IScreenTemplate
from components.highlighter import RangeHighlighter, IRangeHighlighter
from components.swapAnimator import SwapAnimator
from components.arrayBuilder import ArrayBuilder, IArrayBuilder

config.flush_cache = True


class AlternativeWalkthrough(Scene):
    def construct(self):
        typo: ITypography = Typography()
        self.camera.background_color = typo.bg()
        tracker: IScreenTemplate = ScreenTemplate(self, typo)
        swap_animator = SwapAnimator(self)

        tracker.screen_code_walkthrough("Code Walkthrough")

        # ── nums1 ───────────────────────────────────────────────────
        nums1: IArrayBuilder = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[1, 2, 3, 0, 0, 0],
            label="nums1",
        ).build()

        m_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        m_text = Text("m = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        m_text.move_to(m_rect.get_center())
        m_box = VGroup(m_rect, m_text)

        row1 = VGroup(nums1.group, m_box).arrange(RIGHT, buff=0.6).scale(0.7)
        m_box.set_y(nums1.cells.get_y())
        row1.move_to(UP * 1.5 + LEFT * 3.5)

        # ── nums2 ───────────────────────────────────────────────────
        nums2: IArrayBuilder = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[2, 5, 6],
            label="nums2",
        ).build()

        n_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        n_text = Text("n = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        n_text.move_to(n_rect.get_center())
        n_box = VGroup(n_rect, n_text)

        row2 = VGroup(nums2.group, n_box).arrange(RIGHT, buff=3).scale(0.7)
        n_box.set_y(nums2.cells.get_y())
        row2.next_to(row1, DOWN, buff=1.5, aligned_edge=LEFT)

        # ── Java Code ─────────────────────────────────────────────
        java_code_string = """public void merge(int[] nums1, int m, int[] nums2, int n) {
    int p1 = m - 1;
    int p2 = n - 1;
    int p = nums1.length - 1;

    while (p >= 0) {
        int val1 = (p1 >= 0) ? nums1[p1] : Integer.MIN_VALUE;
        int val2 = (p2 >= 0) ? nums2[p2] : Integer.MIN_VALUE;

        if (val1 > val2) {
            nums1[p] = val1;
            p1--;
        } else {
            nums1[p] = val2;
            p2--;
        }

        p--;
    }
}"""
        code_block = Code(
            code_string=java_code_string,
            language="java",
            tab_width=4,
            background="window",
            formatter_style="monokai"
        ).scale(0.55)
        code_block.to_edge(RIGHT, buff=0.2)

        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
            FadeIn(row2, shift=RIGHT * 0.3),
            FadeIn(code_block, shift=LEFT * 0.3),
            run_time=1.2,
        )
        self.wait(0.5)
        
        # Highlighter logic
        h_rect = SurroundingRectangle(code_block[2][0], color=typo.color_yellow(), corner_radius=0.05, buff=0.05)
        h_rect.set_stroke(width=2)
        
        def highlight_line(line_num: int, run_time=0.4):
            # line_num is 0-indexed
            line = code_block[2][line_num]
            new_rect = SurroundingRectangle(line, color=typo.color_yellow(), corner_radius=0.05, buff=0.05)
            new_rect.set_stroke(width=2)
            self.play(Transform(h_rect, new_rect), run_time=run_time)

        self.play(FadeIn(h_rect))
        self.wait(0.5)

        # ── Setup Pointers ─────────────────────────────────────
        # int p1 = m - 1;
        highlight_line(1)
        p1_arrow = Arrow(start=UP, end=DOWN, color=typo.color_blue(), max_tip_length_to_length_ratio=0.3, stroke_width=10).scale(0.25)
        p1_arrow.next_to(nums1.cells[2], UP, buff=0.1)
        p1_text = Text("p1", font=typo.font_code(), font_size=16, weight=BOLD, color=typo.color_blue()).next_to(p1_arrow, UP, buff=0.1)
        p1_group = VGroup(p1_arrow, p1_text)
        self.play(FadeIn(p1_group))

        # int p2 = n - 1;
        highlight_line(2)
        p2_arrow = Arrow(start=DOWN, end=UP, color=typo.color_yellow(), max_tip_length_to_length_ratio=0.3, stroke_width=10).scale(0.25)
        p2_arrow.next_to(nums2.cells[2], DOWN, buff=0.1)
        p2_text = Text("p2", font=typo.font_code(), font_size=16, weight=BOLD, color=typo.color_yellow()).next_to(p2_arrow, DOWN, buff=0.1)
        p2_group = VGroup(p2_arrow, p2_text)
        self.play(FadeIn(p2_group))

        # int p = nums1.length - 1;
        highlight_line(3)
        p_arrow = Arrow(start=DOWN, end=UP, color=typo.color_green(), max_tip_length_to_length_ratio=0.3, stroke_width=10).scale(0.25)
        p_arrow.next_to(nums1.cells[5], DOWN, buff=0.1)
        p_text = Text("p", font=typo.font_code(), font_size=16, weight=BOLD, color=typo.color_green()).next_to(p_arrow, DOWN, buff=0.1)
        p_group = VGroup(p_arrow, p_text)
        self.play(FadeIn(p_group))

        self.wait(1.0)
        
        p1_idx = 2
        p2_idx = 2
        p_idx = 5

        v1 = [1, 2, 3]
        v2 = [2, 5, 6]

        # while (p >= 0)
        highlight_line(5)
        
        while p_idx >= 0:
            # int val1 = ...
            highlight_line(6)
            val1 = v1[p1_idx] if p1_idx >= 0 else float('-inf')
            if p1_idx >= 0:
                nums1.cells[p1_idx].set_z_index(1)
                self.play(nums1.cells[p1_idx][0].animate.set_stroke(typo.color_blue()), run_time=0.3)
            
            # int val2 = ...
            highlight_line(7)
            val2 = v2[p2_idx] if p2_idx >= 0 else float('-inf')
            if p2_idx >= 0:
                nums2.cells[p2_idx].set_z_index(1)
                self.play(nums2.cells[p2_idx][0].animate.set_stroke(typo.color_yellow()), run_time=0.3)

            # if (val1 > val2)  →  line 9
            highlight_line(9)
            self.wait(0.5)

            takeFromNums1 = val1 > val2

            # Save comparison indices now — used to clean up highlights after the branch
            cmp_p1_idx = p1_idx
            cmp_p2_idx = p2_idx
            
            if takeFromNums1:
                # nums1[p] = val1;  →  line 10
                highlight_line(10)
                source_cell = nums1.cells[p1_idx]
                target_cell = nums1.cells[p_idx]

                ghost = source_cell[1].copy()
                self.add(ghost)

                self.play(
                    ghost.animate.move_to(target_cell.get_center()),
                    run_time=0.6,
                    rate_func=smooth,
                )
                self.play(FadeOut(ghost), run_time=0.1)
                nums1.set_value(p_idx, val1, run_time=0.2)
                source_cell.set_z_index(0)
                
                self.play(
                    source_cell[0].animate.set_stroke(typo.color_gray()),
                    nums1.cells[p_idx][0].animate.set_fill(typo.color_milestone_green(), opacity=0.3),
                    *([nums2.cells[p2_idx][0].animate.set_stroke(typo.color_gray())] if p2_idx >= 0 else []),
                    run_time=0.2
                )

                # p1--;  →  line 11
                highlight_line(11)
                p1_idx -= 1
                if p1_idx >= 0:
                    self.play(p1_group.animate.next_to(nums1.cells[p1_idx], UP, buff=0.1), run_time=0.5)
                elif p1_idx == -1: # Only move it out of bounds once!
                    target_x = nums1.cells[0].get_left()[0] - 1.2
                    out_text = Text("-∞", font=typo.font_code(), font_size=20, weight=BOLD, color=typo.color_red())
                    out_text.move_to(p1_group[1].get_center()).set_x(target_x)
                    self.play(
                        p1_group[0].animate.set_x(target_x),
                        Transform(p1_group[1], out_text),
                        run_time=0.5
                    )
            else:
                # } else {  →  line 12
                highlight_line(12)
                
                # nums1[p] = val2;  →  line 13
                highlight_line(13)
                source_cell = nums2.cells[p2_idx]
                target_cell = nums1.cells[p_idx]

                ghost = source_cell[1].copy()
                self.add(ghost)

                self.play(
                    ghost.animate.move_to(target_cell.get_center()),
                    run_time=0.6,
                    rate_func=smooth,
                )
                self.play(FadeOut(ghost), run_time=0.1)
                nums1.set_value(p_idx, val2, run_time=0.2)
                source_cell.set_z_index(0)
                self.play(
                    source_cell[0].animate.set_stroke(typo.color_gray()),
                    nums1.cells[p_idx][0].animate.set_fill(typo.color_milestone_green(), opacity=0.3),
                    *([nums1.cells[p1_idx][0].animate.set_stroke(typo.color_gray())] if p1_idx >= 0 else []),
                    run_time=0.2
                )

                # p2--;  →  line 14
                highlight_line(14)
                p2_idx -= 1
                if p2_idx >= 0:
                    self.play(p2_group.animate.next_to(nums2.cells[p2_idx], DOWN, buff=0.1), run_time=0.5)
                elif p2_idx == -1: # Only move it out of bounds once!
                    target_x = nums2.cells[0].get_left()[0] - 1.2
                    out_text = Text("-∞", font=typo.font_code(), font_size=20, weight=BOLD, color=typo.color_red())
                    out_text.move_to(p2_group[1].get_center()).set_x(target_x)
                    self.play(
                        p2_group[0].animate.set_x(target_x),
                        Transform(p2_group[1], out_text),
                        run_time=0.5
                    )

            # ── Clean up any leftover comparison highlights ───────────
            clean = []
            if cmp_p1_idx >= 0:
                clean.append(nums1.cells[cmp_p1_idx][0].animate.set_stroke(typo.color_gray()))
            if cmp_p2_idx >= 0:
                clean.append(nums2.cells[cmp_p2_idx][0].animate.set_stroke(typo.color_gray()))
            if clean:
                self.play(*clean, run_time=0.15)

            # p--;  →  line 17
            highlight_line(17)          # highlight p--
            p_idx -= 1
            if p_idx >= 0:
                self.play(
                    p_group.animate.next_to(nums1.cells[p_idx], DOWN, buff=0.1),
                    run_time=0.5
                )
            else:
                # p exhausted — slide p pointer off screen left
                target_x = nums1.cells[0].get_left()[0] - 1.2
                self.play(p_group.animate.set_x(target_x), run_time=0.4)

            # Jump straight back to while condition — no closing-brace highlight
            if p_idx >= 0:
                highlight_line(5)

        self.play(FadeOut(h_rect))

        self.wait(1.0)
        self.play(FadeOut(p_group), FadeOut(p1_group), FadeOut(p2_group))

        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(m + n), Space: O(1)", color_type="green")
        self.wait(2)

        # ── FINAL HIGHLIGHT ──────────────────────────────────────────
        final_highlighter = RangeHighlighter(self, typo.color_green())
        final_highlighter.create(nums1.cells, 0, 5)
        final_highlighter.effect_highlight_show()
        final_highlighter.effect_glow_show()

        self.play(final_highlighter.border.animate.set_stroke(width=6), run_time=0.2)
        self.play(final_highlighter.border.animate.set_stroke(width=3), run_time=0.2)
        final_highlighter.effect_pulse()

        self.wait(2.0)
