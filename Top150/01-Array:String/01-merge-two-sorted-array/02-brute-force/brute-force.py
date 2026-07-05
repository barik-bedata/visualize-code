from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))


from components.typography import Typography
from components.screenTemplate import ScreenTemplate
from components.highlighter import RangeHighlighter
from components.swapAnimator import SwapAnimator
from components.stepPanel import StepPanel

config.flush_cache = True

class BruteForce(Scene):

    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)
        swap_animator = SwapAnimator(self)

        tracker.screen_brute_force("Brute Force")

        # ─────────────────────────────────────────────────────────────
        #  BUILD nums1 ROW  (centered first)
        # ─────────────────────────────────────────────────────────────
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

        row1 = VGroup(nums1_group, m_box).arrange(RIGHT, buff=0.4, aligned_edge=UP)

        # ─────────────────────────────────────────────────────────────
        #  BUILD nums2 ROW
        # ─────────────────────────────────────────────────────────────
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

        row2 = VGroup(nums2_group, n_box).arrange(RIGHT, buff=2.8, aligned_edge=UP)

        # ── Stack rows, center on screen ──
        content = VGroup(row1, row2).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        content.move_to(ORIGIN)

        # ─────────────────────────────────────────────────────────────
        #  FADE IN centered
        # ─────────────────────────────────────────────────────────────
        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
            FadeIn(row2, shift=RIGHT * 0.3),
            run_time=1.2,
        )
        self.wait(0.8)

        # ─────────────────────────────────────────────────────────────
        #  ANIMATE LEFT  →  make room for side panel
        # ─────────────────────────────────────────────────────────────
        self.play(
            content.animate.to_edge(LEFT, buff=0.6),
            run_time=0.7,
            rate_func=smooth,
        )

        # ─────────────────────────────────────────────────────────────
        #  STEP PANEL  — aligned to nums1 top border, right side
        # ─────────────────────────────────────────────────────────────
        panel = StepPanel(scene=self, typo=typo, steps=[
            ("Copy nums2 → nums1", "fill empty slots"),
            ("Sort nums1",         "sort(nums1, m+n)"),
            ("Done",               "in-place, sorted"),
        ])

        # Align panel top to nums1 row top
        nums1_top_y = row1.get_top()[1]
        panel._group.set_y(nums1_top_y - panel._group.get_top()[1] + panel._group.get_y())

        panel.show()
        self.wait(1.2)

        # ─────────────────────────────────────────────────────────────
        #  STEP 1 — Copy nums2 → nums1
        # ─────────────────────────────────────────────────────────────
        empty_highlighter = RangeHighlighter(self, "#5B6B7A")
        empty_highlighter.create(cells1, 3, 5)
        empty_highlighter.effect_highlight_show()

        source_highlighter = RangeHighlighter(self, typo.color_blue())
        source_highlighter.create(cells2, 0, 2)
        source_highlighter.effect_highlight_show()
        source_highlighter.effect_pulse()

        panel.activate(0)

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

        panel.complete(0)

        # clean up highlighters
        self.play(
            empty_highlighter.border.animate.set_color(typo.color_green()),
            run_time=0.3,
        )
        source_highlighter.effect_highlight_hide()
        empty_highlighter.effect_highlight_hide()

        # subtle scale bump to signal copy done
        self.play(cells1.animate.scale(1.02), run_time=0.2)
        self.play(cells1.animate.scale(1.0 / 1.02), run_time=0.2)

        # ─────────────────────────────────────────────────────────────
        #  STEP 2 — Sort nums1
        # ─────────────────────────────────────────────────────────────
        panel.activate(1)

        # sort_label = Text(
        #     "sort(nums1, m+n)",
        #     font=typo.font_code(),
        #     font_size=16,
        #     color=typo.color_blue(),
        # ).next_to(cells1, DOWN, buff=0.5)

        # self.play(FadeIn(sort_label, shift=UP * 0.15), run_time=0.5)
        # self.wait(0.6)

        # self.play(FadeOut(sort_label), run_time=0.3)
        swap_animator.animate_swap(cells1[2], cells1[3])

        panel.complete(1)

        # ─────────────────────────────────────────────────────────────
        #  STEP 3 — Done
        # ─────────────────────────────────────────────────────────────
        panel.activate(2)

        final_highlighter = RangeHighlighter(self, typo.color_green())
        final_highlighter.create(cells1, 0, 5)
        final_highlighter.effect_highlight_show()
        final_highlighter.effect_glow_show()

        self.play(final_highlighter.border.animate.set_stroke(width=6), run_time=0.2)
        self.play(final_highlighter.border.animate.set_stroke(width=3), run_time=0.2)
        final_highlighter.effect_pulse()

        panel.complete(2)

        self.wait(1.5)