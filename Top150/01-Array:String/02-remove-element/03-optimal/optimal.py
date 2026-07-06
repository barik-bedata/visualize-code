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

class Optimal(Scene):
    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)

        tracker.screen_optimal_approach("Optimal Approach")

        # ─────────────────────────────────────────────────────────────
        #  BUILD nums ROW
        # ─────────────────────────────────────────────────────────────
        vals = [1, 1, 2, 2, 3]
        nums = ArrayBuilder(
            scene=self,
            typo=typo,
            values=vals,
            label="nums =",
        ).build()
        cells = nums.cells
        nums_group = nums.group
        
        content = nums_group
        content.move_to(ORIGIN)
        
        self.play(FadeIn(content, shift=RIGHT * 0.3), run_time=1.2)
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
        #  STEP PANEL
        # ─────────────────────────────────────────────────────────────
        panel = StepPanel(scene=self, typo=typo, steps=[
            ("Start write and read at index 1.", ""),
            ("If nums[read] != nums[read - 1],", ""),
            ("Copy read to write, increment write.", ""),
            ("Always increment read.", "")
        ])
        panel._group.next_to(content, RIGHT, buff=1.0).align_to(content, UP)
        panel.show()

        # Step 1: Initialize
        panel.activate(0)
        
        read_arrow = Arrow(start=UP, end=DOWN, color=typo.color_blue(), max_tip_length_to_length_ratio=0.3, stroke_width=12).scale(0.33)
        read_arrow.next_to(cells[1], UP, buff=0.1)
        read_text = Text("read", font=typo.font_code(), font_size=20, weight=BOLD, color=typo.color_blue()).next_to(read_arrow, UP, buff=0.1)
        read_group = VGroup(read_arrow, read_text)
        
        write_arrow = Arrow(start=DOWN, end=UP, color=typo.color_green(), max_tip_length_to_length_ratio=0.3, stroke_width=12).scale(0.33)
        write_arrow.next_to(cells[1], DOWN, buff=0.1)
        write_text = Text("write", font=typo.font_code(), font_size=20, weight=BOLD, color=typo.color_green()).next_to(write_arrow, DOWN, buff=0.1)
        write_group = VGroup(write_arrow, write_text)
        
        self.play(FadeIn(read_group), FadeIn(write_group))
        self.wait(1.0)
        
        write_idx = 1
        for read_idx in range(1, len(vals)):
            if read_idx > 1:
                panel.activate(3)
                self.play(read_group.animate.next_to(cells[read_idx], UP, buff=0.1), run_time=0.5)
            
            # Highlight cell checking (read and read-1)
            cell_highlighter = RangeHighlighter(self, typo.color_blue())
            cell_highlighter.create(cells, read_idx - 1, read_idx)
            cell_highlighter.effect_highlight_show()
            self.wait(0.5)
            
            panel.activate(1)
            if vals[read_idx] != vals[read_idx - 1]:
                self.wait(0.5)
                panel.activate(2)
                if read_idx != write_idx:
                    ghost = cells[read_idx][1].copy()
                    self.add(ghost)
                    target_pos = cells[write_idx][1].get_center()
                    
                    self.play(
                        ghost.animate.move_to(target_pos),
                        run_time=0.5,
                        rate_func=smooth
                    )
                    self.play(FadeOut(ghost), run_time=0.1)
                    nums.set_value(write_idx, vals[read_idx], run_time=0.2)
                    vals[write_idx] = vals[read_idx]
                else:
                    self.play(Indicate(cells[read_idx][1], color=typo.color_green()), run_time=0.5)

                write_idx += 1
                if write_idx < len(vals):
                    self.play(write_group.animate.next_to(cells[write_idx], DOWN, buff=0.1), run_time=0.5)
                else:
                    self.play(write_group.animate.shift(RIGHT * 0.8), run_time=0.5)
            else:
                # Same element, ignore
                cross = Cross(cells[read_idx], stroke_color=typo.color_red(), stroke_width=6)
                self.play(Create(cross), run_time=0.3)
                self.play(FadeOut(cross), run_time=0.3)
            
            cell_highlighter.effect_highlight_hide()
            
        self.play(FadeOut(read_group), FadeOut(write_group))
        
        # Dim the rest
        if write_idx < len(vals):
            self.play(
                *[cells[j][1].animate.set_opacity(0.3) for j in range(write_idx, len(vals))],
                run_time=0.5
            )

        self.wait(1.5)
        panel.hide()
        self.wait(1.0)