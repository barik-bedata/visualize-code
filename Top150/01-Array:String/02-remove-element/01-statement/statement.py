from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

from components.typography import Typography
from components.screenTemplate import ScreenTemplate
from components.highlighter import RangeHighlighter
from components.arrayBuilder import ArrayBuilder

config.flush_cache = True

class Statement(Scene):
    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)

        tracker.screen_statement("Problem Statement")

        # ── nums ───────────────────────────────────────────────────
        nums = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[3, 2, 2, 3],
            label="nums",
        ).build()

        row1 = nums.group.move_to(UP * 1.5)

        # ── val ───────────────────────────────────────────────────
        val_rect = Rectangle(width=1.8, height=0.8, color=typo.color_yellow(), stroke_width=0)
        val_text = Text("val = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        val_text.move_to(val_rect.get_center())
        val_box = VGroup(val_rect, val_text)

        val_box.next_to(row1, DOWN, buff=1.5)

        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
            FadeIn(val_box, shift=RIGHT * 0.3),
            run_time=1.2,
        )
        self.wait(2.0)

        # ── highlight val ──────────────────────────────────────────
        val_highlighter = RangeHighlighter(self, typo.color_yellow())
        val_highlighter.create(val_box, 0, 0)
        val_highlighter.effect_highlight_show()
        val_highlighter.effect_pulse()

        # ── highlight instances of val in nums ────────────────────
        h_0 = RangeHighlighter(self, typo.color_red())
        h_0.create(nums.cells, 0, 0)
        h_0.effect_highlight_show()
        
        h_3 = RangeHighlighter(self, typo.color_red())
        h_3.create(nums.cells, 3, 3)
        h_3.effect_highlight_show()

        self.wait(2)
        val_highlighter.effect_highlight_hide()
        
        # ── hide val elements (pseudo remove) ─────────────────────
        self.play(
            nums.cells[0][1].animate.set_opacity(0.3),
            nums.cells[3][1].animate.set_opacity(0.3),
            run_time=0.5
        )
        h_0.effect_highlight_hide()
        h_3.effect_highlight_hide()
        self.wait(1)

        # ── move valid elements to front ──────────────────────────
        source_highlighter = RangeHighlighter(self, typo.color_blue())
        source_highlighter.create(nums.cells, 1, 2)
        source_highlighter.effect_highlight_show()
        source_highlighter.effect_pulse()
        
        target_highlighter = RangeHighlighter(self, typo.color_green())
        target_highlighter.create(nums.cells, 0, 1)
        target_highlighter.effect_highlight_show()
        
        vals = [2, 2]
        for i in range(2):
            source_cell = nums.cells[i + 1]
            target_cell = nums.cells[i]

            ghost = source_cell.copy()
            self.add(ghost)

            self.play(
                ghost.animate.move_to(target_cell.get_center()),
                run_time=0.55,
                rate_func=smooth,
            )
            self.play(FadeOut(ghost), run_time=0.15)
            nums.set_value(i, vals[i], run_time=0.25)
            # Make sure it's fully opaque now
            self.play(nums.cells[i][1].animate.set_opacity(1), run_time=0.1)

        source_highlighter.effect_highlight_hide()
        target_highlighter.effect_highlight_hide()

        # ── fix cells beyond k silently ───────────────────────────
        nums.set_value(2, 2, run_time=0.4)
        nums.set_value(3, 3, run_time=0.4)
        self.play(
            nums.cells[2][1].animate.set_opacity(0.3),
            nums.cells[3][1].animate.set_opacity(0.3),
            run_time=0.4
        )

        # ── FINAL HIGHLIGHT ──────────────────────────────────────────
        k_rect = Rectangle(width=1.4, height=0.8, color=typo.color_green(), stroke_width=0)
        k_text = Text("k = 2", font=typo.font_code(), font_size=20, color=typo.color_green())
        k_text.move_to(k_rect.get_center())
        k_box = VGroup(k_rect, k_text).next_to(val_box, RIGHT, buff=1.0)
        
        self.play(FadeIn(k_box, shift=LEFT * 0.3))

        final_highlighter = RangeHighlighter(self, typo.color_green())
        final_highlighter.create(nums.cells, 0, 1)
        final_highlighter.effect_highlight_show()
        final_highlighter.effect_glow_show()

        self.play(final_highlighter.border.animate.set_stroke(width=6), run_time=0.2)
        self.play(final_highlighter.border.animate.set_stroke(width=3), run_time=0.2)
        final_highlighter.effect_pulse()

        self.wait(2.0)