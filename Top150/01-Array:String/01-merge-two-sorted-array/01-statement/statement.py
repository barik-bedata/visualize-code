from manim import *

from components.typography import Typography
from components.screenTemplate import ScreenTemplate
from components.highligher import RangeHighlighter
from components.swapAnimator import SwapAnimator

config.flush_cache = True


class Statement(Scene):
    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)
        swap_animator = SwapAnimator(self)

        tracker.screen_statement("Problem Statement")

        # ── nums1 ───────────────────────────────────────────────────
        nums1_lbl = Text("nums1 = ", font=typo.font_code(), font_size=20, color=typo.color_white())
        vals1 = [1, 2, 3, 0, 0, 0]

        cells1 = VGroup(*[
            VGroup(
                Square(side_length=0.8, color=typo.color_gray(), stroke_width=2),
                Text(
                    str(v),
                    font=typo.font_code(),
                    font_size=20,
                    color=typo.color_white() if v != 0 else typo.color_secondary()
                )
            ) for v in vals1
        ]).arrange(buff=0)

        nums1_group = VGroup(nums1_lbl, cells1).arrange(RIGHT, buff=0.2)

        m_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        m_text = Text("m = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        m_text.move_to(m_rect.get_center())
        m_box = VGroup(m_rect, m_text)

        row1 = VGroup(nums1_group, m_box).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        row1.move_to(UP * 1.5 + LEFT * 1.5)

        # ── nums2 ───────────────────────────────────────────────────
        nums2_lbl = Text("nums2 = ", font=typo.font_code(), font_size=20, color=typo.color_white())
        vals2 = [2, 5, 6]

        cells2 = VGroup(*[
            VGroup(
                Square(side_length=0.8, color=typo.color_gray(), stroke_width=2),
                Text(str(v), font=typo.font_code(), font_size=20, color=typo.color_white())
            ) for v in vals2
        ]).arrange(buff=0)

        nums2_group = VGroup(nums2_lbl, cells2).arrange(RIGHT, buff=0.2)

        n_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        n_text = Text("n = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        n_text.move_to(n_rect.get_center())
        n_box = VGroup(n_rect, n_text)

        row2 = VGroup(nums2_group, n_box).arrange(RIGHT, buff=3.2, aligned_edge=UP)
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

        nums1_highlighter = RangeHighlighter(self, typo.color_yellow())
        nums1_highlighter.create(cells1, 0, 2)
        nums1_highlighter.effect_highlight_show()
        nums1_highlighter.effect_pulse()
        self.wait(2)
        nums1_highlighter.effect_highlight_hide()
        m_highlighter.effect_highlight_hide()
        self.wait(2)

        # ── highlight empty slots ────────────────────────────────────
        nums1_highlighter = RangeHighlighter(self, typo.color_blue_gray())
        nums1_highlighter.create(cells1, 3, 5)
        nums1_highlighter.effect_highlight_show()
        self.wait(2)
        nums1_highlighter.effect_highlight_hide()

        # ── highlight n=3 nums2 ──────────────────────────────────────
        n_highlighter = RangeHighlighter(self, typo.color_yellow())
        n_highlighter.create(n_box, 0, 0)
        n_highlighter.effect_highlight_show()

        nums2_highlighter = RangeHighlighter(self, typo.color_yellow())
        nums2_highlighter.create(cells2, 0, 2)
        nums2_highlighter.effect_highlight_show()
        self.wait(2)
        n_highlighter.effect_highlight_hide()
        nums2_highlighter.effect_highlight_hide()
        self.wait(2)

        # ── Data-flow: nums2 → empty slots in nums1 ─────────────────
        empty_highlighter = RangeHighlighter(self, "#5B6B7A")
        empty_highlighter.create(cells1, 3, 5)
        empty_highlighter.effect_highlight_show()

        source_highlighter = RangeHighlighter(self, typo.color_blue())
        source_highlighter.create(cells2, 0, 2)
        source_highlighter.effect_highlight_show()
        source_highlighter.effect_pulse()

        for i in range(3):
            source_cell = cells2[i]
            target_cell = cells1[i + 3]

            ghost = source_cell.copy()
            self.add(ghost)

            self.play(
                ghost.animate.move_to(target_cell.get_center()),
                run_time=0.55,
                rate_func=smooth,
            )
            self.play(FadeOut(ghost), run_time=0.15)

            new_text = Text(
                str(vals2[i]),
                font=typo.font_code(),
                font_size=20,
                color=typo.color_white(),
            ).move_to(target_cell[1].get_center())

            self.play(
                FadeOut(target_cell[1]),
                FadeIn(new_text),
                run_time=0.25,
            )
            target_cell.remove(target_cell[1])
            target_cell.add(new_text)

        self.play(
            empty_highlighter.border.animate.set_color(typo.color_green()),
            run_time=0.3,
        )
        source_highlighter.effect_highlight_hide()
        empty_highlighter.effect_highlight_hide()

        # ── fix cells1[2] and cells1[3] silently ────────────────────
        correct_text = Text(
            "2", font=typo.font_code(), font_size=20, color=typo.color_white()
        ).move_to(cells1[2][1].get_center())

        self.play(FadeOut(cells1[2][1]), FadeIn(correct_text), run_time=0.4)
        cells1[2].remove(cells1[2][1])
        cells1[2].add(correct_text)

        correct_text2 = Text(
            "3", font=typo.font_code(), font_size=20, color=typo.color_white()
        ).move_to(cells1[3][1].get_center())

        self.play(FadeOut(cells1[3][1]), FadeIn(correct_text2), run_time=0.4)
        cells1[3].remove(cells1[3][1])
        cells1[3].add(correct_text2)

        # ── FINAL HIGHLIGHT ──────────────────────────────────────────
        final_highlighter = RangeHighlighter(self, typo.color_green())
        final_highlighter.create(cells1, 0, 5)
        final_highlighter.effect_highlight_show()
        final_highlighter.effect_glow_show()

        self.play(final_highlighter.border.animate.set_stroke(width=6), run_time=0.2)
        self.play(final_highlighter.border.animate.set_stroke(width=3), run_time=0.2)
        final_highlighter.effect_pulse()

        self.wait(1.5)
