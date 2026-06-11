from manim import *

from components.typography import Typography
from components.screenTemplate import ScreenTemplate
from components.highlighter import RangeHighlighter
from components.swapAnimator import SwapAnimator
from components.stepPanel import StepPanel
from components.arrayBuilder import ArrayBuilder

config.flush_cache = True

class BruteForce1(Scene):

    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)
        swap_animator = SwapAnimator(self)

        tracker.screen_brute_force("Brute Force")

        # ─────────────────────────────────────────────────────────────
        #  BUILD nums1 ROW
        # ─────────────────────────────────────────────────────────────
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

        row1 = VGroup(nums1.group, m_box).arrange(RIGHT, buff=0.4)
        m_box.set_y(nums1.cells.get_y())

        # ─────────────────────────────────────────────────────────────
        #  BUILD nums2 ROW
        # ─────────────────────────────────────────────────────────────
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

        row2 = VGroup(nums2.group, n_box).arrange(RIGHT, buff=2.8)
        n_box.set_y(nums2.cells.get_y())

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
        empty_highlighter.create(nums1.cells, 3, 5)
        empty_highlighter.effect_highlight_show()

        source_highlighter = RangeHighlighter(self, typo.color_blue())
        source_highlighter.create(nums2.cells, 0, 2)
        source_highlighter.effect_highlight_show()
        source_highlighter.effect_pulse()

        panel.activate(0)

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

        panel.complete(0)

        # clean up highlighters
        self.play(
            empty_highlighter.border.animate.set_color(typo.color_green()),
            run_time=0.3,
        )
        source_highlighter.effect_highlight_hide()
        empty_highlighter.effect_highlight_hide()

        # subtle scale bump to signal copy done
        self.play(nums1.cells.animate.scale(1.02), run_time=0.2)
        self.play(nums1.cells.animate.scale(1.0 / 1.02), run_time=0.2)

        # ─────────────────────────────────────────────────────────────
        #  STEP 2 — Sort nums1
        # ─────────────────────────────────────────────────────────────
        panel.activate(1)

        sort_label = Text(
            "sort(nums1, m+n)",
            font=typo.font_code(),
            font_size=16,
            color=typo.color_blue(),
        ).next_to(nums1.cells, DOWN, buff=0.5)

        self.play(FadeIn(sort_label, shift=UP * 0.15), run_time=0.5)
        self.wait(0.6)

        self.play(FadeOut(sort_label), run_time=0.3)
        swap_animator.animate_swap(nums1.cells[2], nums1.cells[3])

        panel.complete(1)

        # ─────────────────────────────────────────────────────────────
        #  STEP 3 — Done
        # ─────────────────────────────────────────────────────────────
        panel.activate(2)

        final_highlighter = RangeHighlighter(self, typo.color_green())
        final_highlighter.create(nums1.cells, 0, 5)
        final_highlighter.effect_highlight_show()
        final_highlighter.effect_glow_show()

        self.play(final_highlighter.border.animate.set_stroke(width=6), run_time=0.2)
        self.play(final_highlighter.border.animate.set_stroke(width=3), run_time=0.2)
        final_highlighter.effect_pulse()

        panel.complete(2)

        self.wait(1.5)