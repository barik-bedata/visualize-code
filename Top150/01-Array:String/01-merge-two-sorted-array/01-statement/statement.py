from manim import *

from components.typography import Typography
from components.screenTemplate import ScreenTemplate
from components.highlighter import RangeHighlighter
from components.swapAnimator import SwapAnimator
from components.arrayBuilder import ArrayBuilder

config.flush_cache = True


class Statement(Scene):
    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)
        swap_animator = SwapAnimator(self)

        tracker.screen_statement("Problem Statement")

        # ── nums1 ───────────────────────────────────────────────────
        nums1 = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[1, 2, 3, 0, 0, 0],
            label="nums1",
        ).build()

        m_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        m_text = Text("m = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        m_text.move_to(m_rect.get_center())
        m_box = VGroup(m_rect, m_text)

        row1 = VGroup(nums1.group, m_box).arrange(RIGHT, buff=0.8)
        m_box.set_y(nums1.cells.get_y())
        row1.move_to(UP * 1.5 + LEFT * 1.5)

        # ── nums2 ───────────────────────────────────────────────────
        nums2 = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[2, 5, 6],
            label="nums2",
        ).build()

        n_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        n_text = Text("n = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        n_text.move_to(n_rect.get_center())
        n_box = VGroup(n_rect, n_text)

        row2 = VGroup(nums2.group, n_box).arrange(RIGHT, buff=3.2)
        n_box.set_y(nums2.cells.get_y())
        row2.next_to(row1, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
            FadeIn(row2, shift=RIGHT * 0.3),
            run_time=1.2,
        )
        self.wait(2.0)

        # ── highlight m=3 real cells ────────────────────────────────
        m_highlighter = RangeHighlighter(self, typo.color_yellow())
        m_highlighter.create(m_box, 0, 0)
        m_highlighter.effect_highlight_show()

        # ── highlight first m real cells ────────────────────────────────
        nums1_highlighter = RangeHighlighter(self, typo.color_yellow())
        nums1_highlighter.create(nums1.cells, 0, 2)
        nums1_highlighter.effect_highlight_show()
        nums1_highlighter.effect_pulse()
        self.wait(2)
        nums1_highlighter.effect_highlight_hide()
        m_highlighter.effect_highlight_hide()
        self.wait(2)

        # ── highlight empty slots in nums1 ────────────────────────────────────
        nums1_highlighter = RangeHighlighter(self, typo.color_blue_gray())
        nums1_highlighter.create(nums1.cells, 3, 5)
        nums1_highlighter.effect_highlight_show()
        self.wait(2)
        nums1_highlighter.effect_highlight_hide()

        # ── highlight n=3 nums2 ──────────────────────────────────────
        n_highlighter = RangeHighlighter(self, typo.color_yellow())
        n_highlighter.create(n_box, 0, 0)
        n_highlighter.effect_highlight_show()

        # ── highlight first n real cells in nums2 ────────────────────────────────
        nums2_highlighter = RangeHighlighter(self, typo.color_yellow())
        nums2_highlighter.create(nums2.cells, 0, 2)
        nums2_highlighter.effect_highlight_show()
        self.wait(2)
        n_highlighter.effect_highlight_hide()
        nums2_highlighter.effect_highlight_hide()
        self.wait(2)

        # ── Data-flow: nums2 → empty slots in nums1 ─────────────────
        empty_highlighter = RangeHighlighter(self, "#5B6B7A")
        empty_highlighter.create(nums1.cells, 3, 5)
        empty_highlighter.effect_highlight_show()

        source_highlighter = RangeHighlighter(self, typo.color_blue())
        source_highlighter.create(nums2.cells, 0, 2)
        source_highlighter.effect_highlight_show()
        source_highlighter.effect_pulse()

        vals2 = [2, 5, 6]
        for i in range(3):
            source_cell = nums2.cells[i]
            target_cell = nums1.cells[i + 3]

            ghost = source_cell.copy()
            self.add(ghost)

            self.play(
                ghost.animate.move_to(target_cell.get_center()),
                run_time=0.55,
                rate_func=smooth,
            )
            self.play(FadeOut(ghost), run_time=0.15)
            nums1.set_value(i + 3, vals2[i], run_time=0.25)

        self.play(
            empty_highlighter.border.animate.set_color(typo.color_green()),
            run_time=0.3,
        )
        source_highlighter.effect_highlight_hide()
        empty_highlighter.effect_highlight_hide()

        # ── fix cells1[2] and cells1[3] silently ────────────────────
        nums1.set_value(2, 2, run_time=0.4)
        nums1.set_value(3, 3, run_time=0.4)

        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(m + n), Space: O(1)", color_type="green")
        self.wait(3)

        # ── FINAL HIGHLIGHT ──────────────────────────────────────────
        final_highlighter = RangeHighlighter(self, typo.color_green())
        final_highlighter.create(nums1.cells, 0, 5)
        final_highlighter.effect_highlight_show()
        final_highlighter.effect_glow_show()

        self.play(final_highlighter.border.animate.set_stroke(width=6), run_time=0.2)
        self.play(final_highlighter.border.animate.set_stroke(width=3), run_time=0.2)
        final_highlighter.effect_pulse()

        self.wait(1.5)

