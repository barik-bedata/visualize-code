from manim import *

from components.typography import Typography, ITypography
from components.screenTemplate import ScreenTemplate, IScreenTemplate
from components.highlighter import RangeHighlighter, IRangeHighlighter
from components.swapAnimator import SwapAnimator
from components.arrayBuilder import ArrayBuilder, IArrayBuilder
from components.stepPanel import StepPanel

config.flush_cache = True


class Walkthrough(Scene):
    def construct(self):
        typo: ITypography = Typography()
        self.camera.background_color = typo.bg()
        tracker: IScreenTemplate = ScreenTemplate(self, typo)
        swap_animator = SwapAnimator(self)

        tracker.screen_optimal_approach("Walkthrough")

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

        row1 = VGroup(nums1.group, m_box).arrange(RIGHT, buff=0.8).scale(0.7)
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

        row2 = VGroup(nums2.group, n_box).arrange(RIGHT, buff=3.2).scale(0.7)
        n_box.set_y(nums2.cells.get_y())
        row2.next_to(row1, DOWN, buff=1.5, aligned_edge=LEFT)

        # ── Step Panel ─────────────────────────────────────────────
        steps = [
            ("Setup Pointers", "Initialize p1, p2, and p"),
            ("Compare & Place", "Place larger element at p"),
            ("Drain nums1", "Mark visited elements")
        ]
        panel = StepPanel(self, typo, steps)

        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
            FadeIn(row2, shift=RIGHT * 0.3),
            run_time=1.2,
        )
        self.wait(0.5)
        
        panel.show()
        self.wait(0.5)

        # First array highlight with glow
        h1 = RangeHighlighter(self, typo.color_blue())
        h1.create(nums1.cells, 0, 5)
        h1.effect_highlight_show_glow()
        self.wait(1.0)
        
        # Second array highlight with glow
        h2 = RangeHighlighter(self, typo.color_yellow())
        h2.create(nums2.cells, 0, 2)
        h2.effect_highlight_show_glow()
        self.wait(1.0)
        h1.effect_highlight_hide_glow()
        h2.effect_highlight_hide_glow()
        self.wait(0.5)

        # ── Three Pointers Setup ─────────────────────────────────────
        panel.activate(0)
        
        p1_arrow = Arrow(start=UP, end=DOWN, color=typo.color_blue(), max_tip_length_to_length_ratio=0.3, stroke_width=10).scale(0.25)
        p1_arrow.next_to(nums1.cells[2], UP, buff=0.1)
        p1_text = Text("p1", font=typo.font_code(), font_size=16, weight=BOLD, color=typo.color_blue()).next_to(p1_arrow, UP, buff=0.1)
        p1_group = VGroup(p1_arrow, p1_text)

        p2_arrow = Arrow(start=DOWN, end=UP, color=typo.color_yellow(), max_tip_length_to_length_ratio=0.3, stroke_width=10).scale(0.25)
        p2_arrow.next_to(nums2.cells[2], DOWN, buff=0.1)
        p2_text = Text("p2", font=typo.font_code(), font_size=16, weight=BOLD, color=typo.color_yellow()).next_to(p2_arrow, DOWN, buff=0.1)
        p2_group = VGroup(p2_arrow, p2_text)

        p_arrow = Arrow(start=DOWN, end=UP, color=typo.color_green(), max_tip_length_to_length_ratio=0.3, stroke_width=10).scale(0.25)
        p_arrow.next_to(nums1.cells[5], DOWN, buff=0.1)
        p_text = Text("p", font=typo.font_code(), font_size=16, weight=BOLD, color=typo.color_green()).next_to(p_arrow, DOWN, buff=0.1)
        p_group = VGroup(p_arrow, p_text)

        self.play(FadeIn(p1_group), FadeIn(p2_group), FadeIn(p_group))
        self.wait(1.0)
        
        panel.complete(0)

        p1_idx = 2
        p2_idx = 2
        p_idx = 5

        v1 = [1, 2, 3]
        v2 = [2, 5, 6]

        panel.activate(1)
        
        while p2_idx >= 0:
            if p1_idx >= 0:
                nums1.cells[p1_idx].set_z_index(1)
                nums2.cells[p2_idx].set_z_index(1)
                self.play(
                    nums1.cells[p1_idx][0].animate.set_stroke(typo.color_blue()),
                    nums2.cells[p2_idx][0].animate.set_stroke(typo.color_yellow()),
                    run_time=0.3
                )
            else:
                nums2.cells[p2_idx].set_z_index(1)
                self.play(nums2.cells[p2_idx][0].animate.set_stroke(typo.color_yellow()), run_time=0.3)

            self.wait(0.5)

            if p1_idx >= 0 and v1[p1_idx] > v2[p2_idx]:
                val = v1[p1_idx]
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
                nums1.set_value(p_idx, val, run_time=0.2)
                source_cell.set_z_index(0)
                self.play(
                    source_cell[0].animate.set_stroke(typo.color_gray()),
                    nums1.cells[p_idx][0].animate.set_fill(typo.color_milestone_green(), opacity=0.3),
                    run_time=0.2
                )

                p1_idx -= 1
                p_idx -= 1

                anims = []
                if p_idx >= 0:
                    anims.append(p_group.animate.next_to(nums1.cells[p_idx], DOWN, buff=0.1))
                else:
                    target_x = nums1.cells[0].get_left()[0] - 1.2
                    out_of_bound_text_p = Text("Out of bound", font=typo.font_code(), font_size=12, weight=BOLD, color=typo.color_red())
                    out_of_bound_text_p.move_to(p_group[1].get_center()).set_x(target_x)
                    anims.append(p_group[0].animate.set_x(target_x))
                    anims.append(Transform(p_group[1], out_of_bound_text_p))

                if p1_idx >= 0:
                    anims.append(p1_group.animate.next_to(nums1.cells[p1_idx], UP, buff=0.1))
                else:
                    target_x = nums1.cells[0].get_left()[0] - 1.2
                    out_of_bound_text = Text("Out of bound", font=typo.font_code(), font_size=12, weight=BOLD, color=typo.color_red())
                    out_of_bound_text.move_to(p1_group[1].get_center()).set_x(target_x)
                    anims.append(p1_group[0].animate.set_x(target_x))
                    anims.append(Transform(p1_group[1], out_of_bound_text))
                self.play(*anims, run_time=0.5)
            else:
                val = v2[p2_idx]
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
                nums1.set_value(p_idx, val, run_time=0.2)
                source_cell.set_z_index(0)
                self.play(
                    source_cell[0].animate.set_stroke(typo.color_gray()),
                    nums1.cells[p_idx][0].animate.set_fill(typo.color_milestone_green(), opacity=0.3),
                    run_time=0.2
                )

                p2_idx -= 1
                p_idx -= 1

                anims = []
                if p_idx >= 0:
                    anims.append(p_group.animate.next_to(nums1.cells[p_idx], DOWN, buff=0.1))
                else:
                    target_x = nums1.cells[0].get_left()[0] - 1.2
                    out_of_bound_text_p = Text("Out of bound", font=typo.font_code(), font_size=12, weight=BOLD, color=typo.color_red())
                    out_of_bound_text_p.move_to(p_group[1].get_center()).set_x(target_x)
                    anims.append(p_group[0].animate.set_x(target_x))
                    anims.append(Transform(p_group[1], out_of_bound_text_p))

                if p2_idx >= 0:
                    anims.append(p2_group.animate.next_to(nums2.cells[p2_idx], DOWN, buff=0.1))
                else:
                    target_x = nums2.cells[0].get_left()[0] - 1.2
                    out_of_bound_text = Text("Out of bound", font=typo.font_code(), font_size=12, weight=BOLD, color=typo.color_red())
                    out_of_bound_text.move_to(p2_group[1].get_center()).set_x(target_x)
                    anims.append(p2_group[0].animate.set_x(target_x))
                    anims.append(Transform(p2_group[1], out_of_bound_text))
                self.play(*anims, run_time=0.5)

        panel.complete(1)
        
        # p1 draining loop to mark visited elements and place them in final position (p)
        if p1_idx >= 0:
            panel.activate(2)
            
        while p1_idx >= 0:
            nums1.cells[p1_idx].set_z_index(1)
            self.play(nums1.cells[p1_idx][0].animate.set_stroke(typo.color_blue()), run_time=0.3)
            self.wait(0.2)
            # Both p1_idx and p_idx are the same at this point
            nums1.cells[p1_idx].set_z_index(0)
            self.play(
                nums1.cells[p1_idx][0].animate.set_stroke(typo.color_gray()).set_fill(typo.color_milestone_green(), opacity=0.3),
                run_time=0.3
            )
            
            p1_idx -= 1
            p_idx -= 1
            
            anims = []
            if p_idx >= 0:
                anims.append(p_group.animate.next_to(nums1.cells[p_idx], DOWN, buff=0.1))
            else:
                target_x = nums1.cells[0].get_left()[0] - 1.2
                out_of_bound_text_p = Text("Out of bound", font=typo.font_code(), font_size=12, weight=BOLD, color=typo.color_red())
                out_of_bound_text_p.move_to(p_group[1].get_center()).set_x(target_x)
                anims.append(p_group[0].animate.set_x(target_x))
                anims.append(Transform(p_group[1], out_of_bound_text_p))

            if p1_idx >= 0:
                anims.append(p1_group.animate.next_to(nums1.cells[p1_idx], UP, buff=0.1))
            else:
                target_x = nums1.cells[0].get_left()[0] - 1.2
                out_of_bound_text_p1 = Text("Out of bound", font=typo.font_code(), font_size=12, weight=BOLD, color=typo.color_red())
                out_of_bound_text_p1.move_to(p1_group[1].get_center()).set_x(target_x)
                anims.append(p1_group[0].animate.set_x(target_x))
                anims.append(Transform(p1_group[1], out_of_bound_text_p1))
                
            self.play(*anims, run_time=0.5)

        if p1_idx < 0:
            try:
                panel.complete(2)
            except Exception:
                pass

        panel.hide()

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
