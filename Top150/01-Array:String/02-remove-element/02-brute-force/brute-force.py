from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

from components.typography import Typography
from components.screenTemplate import ScreenTemplate
from components.highlighter import RangeHighlighter
from components.stepPanel import StepPanel
from components.arrayBuilder import ArrayBuilder

config.flush_cache = True

class BruteForce(Scene):

    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)

        tracker.screen_brute_force("Brute Force")

        # ─────────────────────────────────────────────────────────────
        #  BUILD nums ROW
        # ─────────────────────────────────────────────────────────────
        vals = [3, 2, 2, 3]
        nums = ArrayBuilder(
            scene=self,
            typo=typo,
            values=vals,
            label="nums =",
        ).build()
        cells = nums.cells
        nums_group = nums.group
        
        # ── val ───────────────────────────────────────────────────
        val_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        val_text = Text("val = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        val_text.move_to(val_rect.get_center())
        val_box = VGroup(val_rect, val_text)
        
        row1 = VGroup(nums_group, val_box).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        row1.move_to(UP * 1.5)

        # ─────────────────────────────────────────────────────────────
        #  BUILD temp ROW
        # ─────────────────────────────────────────────────────────────
        temp = ArrayBuilder(
            scene=self,
            typo=typo,
            values=["", "", "", ""],
            label="temp =",
        ).build()
        temp_cells = temp.cells
        temp_group = temp.group
        
        row2 = temp_group.copy()
        row2.next_to(row1, DOWN, buff=2.0, aligned_edge=LEFT)

        # ── Stack rows, center on screen ──
        content = VGroup(row1, row2).arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        content.move_to(ORIGIN)

        # ─────────────────────────────────────────────────────────────
        #  FADE IN centered
        # ─────────────────────────────────────────────────────────────
        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
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
        #  STEP PANEL  — aligned to nums top border, right side
        # ─────────────────────────────────────────────────────────────
        panel = StepPanel(scene=self, typo=typo, steps=[
            "Create a temp array.",
            "Iterate nums. If element != val,",
            "add it to temp array.",
            "Copy temp back to nums."
        ])
        panel.group.next_to(content, RIGHT, buff=1.0).align_to(content, UP)
        panel.show()

        # Step 1: Create a temp array
        panel.highlight_step(0)
        self.play(FadeIn(row2, shift=UP * 0.3), run_time=1.0)
        self.wait(1.0)

        # Step 2 & 3: Iterate and copy
        panel.highlight_step(1)
        self.wait(0.5)
        panel.highlight_step(2)
        
        # Pointers
        i_arrow = Arrow(start=UP, end=DOWN, color=typo.color_blue(), max_tip_length_to_length_ratio=0.3, stroke_width=12).scale(0.33)
        i_arrow.next_to(cells[0], UP, buff=0.1)
        i_text = Text("i", font=typo.font_code(), font_size=20, weight=BOLD, color=typo.color_blue()).next_to(i_arrow, UP, buff=0.1)
        i_group = VGroup(i_arrow, i_text)
        
        self.play(FadeIn(i_group))
        
        temp_idx = 0
        for i in range(len(vals)):
            if i > 0:
                self.play(i_group.animate.next_to(cells[i], UP, buff=0.1), run_time=0.5)
            
            # Highlight cell checking
            cell_highlighter = RangeHighlighter(self, typo.color_blue())
            cell_highlighter.create(cells, i, i)
            cell_highlighter.effect_highlight_show()
            self.wait(0.5)
            
            if vals[i] != 3:
                # Copy to temp
                ghost = cells[i][1].copy()
                self.add(ghost)
                target_pos = temp_cells[temp_idx].get_center()
                
                self.play(
                    ghost.animate.move_to(target_pos),
                    run_time=0.5,
                    rate_func=smooth
                )
                self.play(FadeOut(ghost), run_time=0.1)
                temp.set_value(temp_idx, vals[i], run_time=0.2)
                
                temp_idx += 1
            else:
                # Show rejection or skip
                cross = Cross(cells[i], stroke_color=typo.color_red(), stroke_width=6)
                self.play(Create(cross), run_time=0.3)
                self.play(FadeOut(cross), run_time=0.3)
                
            cell_highlighter.effect_highlight_hide()
        
        self.play(FadeOut(i_group))

        # Step 4: Copy temp back to nums
        panel.highlight_step(3)
        
        source_h = RangeHighlighter(self, typo.color_blue())
        source_h.create(temp_cells, 0, temp_idx - 1)
        source_h.effect_highlight_show()
        
        target_h = RangeHighlighter(self, typo.color_green())
        target_h.create(cells, 0, temp_idx - 1)
        target_h.effect_highlight_show()
        
        for i in range(temp_idx):
            source_cell = temp_cells[i][1]
            target_cell = cells[i][1]
            
            ghost = source_cell.copy()
            self.add(ghost)
            
            self.play(
                ghost.animate.move_to(target_cell.get_center()),
                run_time=0.5
            )
            self.play(FadeOut(ghost), run_time=0.1)
            nums.set_value(i, vals[i] if vals[i] != 3 else 2, run_time=0.2)
        
        source_h.effect_highlight_hide()
        target_h.effect_highlight_hide()

        # Dim the rest
        self.play(
            cells[2][1].animate.set_opacity(0.3),
            cells[3][1].animate.set_opacity(0.3),
            run_time=0.5
        )

        self.wait(1.5)
        panel.hide()
        self.wait(1.0)