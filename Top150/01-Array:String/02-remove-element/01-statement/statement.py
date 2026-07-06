from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

from components.typography import Typography
from components.screenTemplate import ScreenTemplate
from components.highlighter import RangeHighlighter
from components.arrayBuilder import ArrayBuilder

config.flush_cache = True

class StatementRemoveDuplicate(Scene):
    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)

        tracker.screen_statement("Problem Statement")

        # ── Example 1 ───────────────────────────────────────────────────
        tracker.show_lower_third("Example 1", "nums = [1, 1, 2]", "yellow")

        nums1 = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[1, 1, 2],
            label="nums",
        ).build()
        row1 = nums1.group.move_to(UP * 0.5)

        self.play(FadeIn(row1, shift=RIGHT * 0.3))
        self.wait(1)

        # Highlight duplicate
        h_dup1 = RangeHighlighter(self, typo.color_red())
        h_dup1.create(nums1.cells, 1, 1)
        h_dup1.effect_highlight_show()
        self.play(nums1.cells[1][1].animate.set_opacity(0.3), run_time=0.5)
        h_dup1.effect_highlight_hide()
        self.wait(0.5)

        # Show k = 2
        k1_rect = Rectangle(width=1.4, height=0.8, color=typo.color_green(), stroke_width=0)
        k1_text = Text("k = 2", font=typo.font_code(), font_size=20, color=typo.color_green())
        k1_text.move_to(k1_rect.get_center())
        k1_box = VGroup(k1_rect, k1_text).next_to(row1, DOWN, buff=1.0)
        
        self.play(FadeIn(k1_box, shift=UP * 0.3))
        self.wait(1)

        # Expected output transformation
        self.play(nums1.cells[1][1].animate.set_opacity(1), run_time=0.1)
        nums1.set_value(0, 1, run_time=0.3)
        nums1.set_value(1, 2, run_time=0.3)
        nums1.set_value(2, 2, run_time=0.3)
        
        self.play(nums1.cells[2][1].animate.set_opacity(0.3), run_time=0.3)

        final_h1 = RangeHighlighter(self, typo.color_green())
        final_h1.create(nums1.cells, 0, 1)
        final_h1.effect_highlight_show()
        final_h1.effect_pulse()
        self.wait(2)

        # Transition to Example 2
        final_h1.effect_highlight_hide()
        self.play(
            FadeOut(row1),
            FadeOut(k1_box),
            run_time=0.5
        )
        self.wait(0.5)

        # ── Example 2 ───────────────────────────────────────────────────
        tracker.show_lower_third("Example 2", "nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]", "yellow")

        nums2 = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[0, 0, 1, 1, 1, 2, 2, 3, 3, 4],
            label="nums",
        ).build()
        row2 = nums2.group.move_to(UP * 0.5)

        self.play(FadeIn(row2, shift=RIGHT * 0.3))
        self.wait(1)

        # Highlight duplicates
        dup_indices = [1, 3, 4, 6, 8]
        dup_highlighters = []
        for i in dup_indices:
            h = RangeHighlighter(self, typo.color_red())
            h.create(nums2.cells, i, i)
            h.effect_highlight_show()
            dup_highlighters.append(h)
        
        self.wait(0.5)
        self.play(
            *[nums2.cells[i][1].animate.set_opacity(0.3) for i in dup_indices],
            run_time=0.5
        )
        
        for h in dup_highlighters:
            h.effect_highlight_hide()
            
        self.wait(0.5)

        # Show k = 5
        k2_rect = Rectangle(width=1.4, height=0.8, color=typo.color_green(), stroke_width=0)
        k2_text = Text("k = 5", font=typo.font_code(), font_size=20, color=typo.color_green())
        k2_text.move_to(k2_rect.get_center())
        k2_box = VGroup(k2_rect, k2_text).next_to(row2, DOWN, buff=1.0)
        
        self.play(FadeIn(k2_box, shift=UP * 0.3))
        self.wait(1)

        # Expected output transformation
        self.play(
            *[nums2.cells[i][1].animate.set_opacity(1) for i in dup_indices],
            run_time=0.1
        )
        
        expected_vals = [0, 1, 2, 3, 4, 2, 2, 3, 3, 4]
        for i, v in enumerate(expected_vals):
            nums2.set_value(i, v, run_time=0.08)
            
        self.play(
            *[nums2.cells[i][1].animate.set_opacity(0.3) for i in range(5, 10)],
            run_time=0.3
        )

        final_h2 = RangeHighlighter(self, typo.color_green())
        final_h2.create(nums2.cells, 0, 4)
        final_h2.effect_highlight_show()
        final_h2.effect_glow_show()
        final_h2.effect_pulse()
        
        self.wait(2.0)
        tracker.hide_lower_third()
        self.wait(1.0)