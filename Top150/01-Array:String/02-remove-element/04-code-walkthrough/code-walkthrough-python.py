from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

from components.typography import Typography
from components.screenTemplate import ScreenTemplate
from components.highlighter import RangeHighlighter
from components.arrayBuilder import ArrayBuilder

config.flush_cache = True

class CodeWalkthroughPython(Scene):
    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)

        tracker.screen_code_walkthrough("Code Walkthrough")

        # ── nums ───────────────────────────────────────────────────
        vals = [1, 1, 2]
        nums = ArrayBuilder(
            scene=self,
            typo=typo,
            values=vals,
            label="nums =",
        ).build()
        cells = nums.cells
        nums_group = nums.group
        
        row1 = nums_group.scale(0.8)
        row1.move_to(UP * 1.5 + LEFT * 3.0)

        # ── Python Code ─────────────────────────────────────────────
        python_code_string = """def removeDuplicates(nums):
    write_idx = 1
    
    for read_idx in range(1, len(nums)):
        if nums[read_idx] != nums[read_idx - 1]:
            nums[write_idx] = nums[read_idx]
            write_idx += 1
            
    return write_idx"""
        code_block = Code(
            code_string=python_code_string,
            language="python",
            tab_width=4,
            background="window",
            formatter_style="monokai"
        ).scale(0.7)
        code_block.to_edge(RIGHT, buff=0.5)

        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
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
            return h_rect.animate(run_time=run_time).move_to(line).match_width(line, stretch=True, about_edge=LEFT)

        self.play(Create(h_rect))
        self.wait(0.5)
        
        # Line 1: write_idx = 1
        self.play(highlight_line(1))
        
        write_arrow = Arrow(start=DOWN, end=UP, color=typo.color_green(), max_tip_length_to_length_ratio=0.3, stroke_width=12).scale(0.33 * 0.8)
        write_arrow.next_to(cells[1], DOWN, buff=0.1)
        write_text = Text("w", font=typo.font_code(), font_size=20 * 0.8, weight=BOLD, color=typo.color_green()).next_to(write_arrow, DOWN, buff=0.1)
        write_group = VGroup(write_arrow, write_text)
        self.play(FadeIn(write_group))
        
        read_arrow = Arrow(start=UP, end=DOWN, color=typo.color_blue(), max_tip_length_to_length_ratio=0.3, stroke_width=12).scale(0.33 * 0.8)
        read_arrow.next_to(cells[1], UP, buff=0.1)
        read_text = Text("r", font=typo.font_code(), font_size=20 * 0.8, weight=BOLD, color=typo.color_blue()).next_to(read_arrow, UP, buff=0.1)
        read_group = VGroup(read_arrow, read_text)
        
        write_idx = 1
        for read_idx in range(1, len(vals)):
            # Line 3: for read_idx in range(1, len(nums)):
            self.play(highlight_line(3))
            if read_idx == 1:
                self.play(FadeIn(read_group))
            else:
                self.play(read_group.animate.next_to(cells[read_idx], UP, buff=0.1), run_time=0.5)
            self.wait(0.3)
            
            # Line 4: if nums[read_idx] != nums[read_idx - 1]:
            self.play(highlight_line(4))
            
            cell_highlighter = RangeHighlighter(self, typo.color_blue())
            cell_highlighter.create(cells, read_idx - 1, read_idx)
            cell_highlighter.effect_highlight_show()
            self.wait(0.3)
            
            if vals[read_idx] != vals[read_idx - 1]:
                # Line 5: nums[write_idx] = nums[read_idx]
                self.play(highlight_line(5))
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

                # Line 6: write_idx += 1
                self.play(highlight_line(6))
                write_idx += 1
                if write_idx < len(vals):
                    self.play(write_group.animate.next_to(cells[write_idx], DOWN, buff=0.1), run_time=0.5)
                else:
                    self.play(write_group.animate.shift(RIGHT * 0.8), run_time=0.5)
            else:
                cross = Cross(cells[read_idx], stroke_color=typo.color_red(), stroke_width=6)
                self.play(Create(cross), run_time=0.3)
                self.play(FadeOut(cross), run_time=0.3)
            
            cell_highlighter.effect_highlight_hide()
            
        # Line 8: return write_idx
        self.play(highlight_line(8))
        self.play(FadeOut(read_group), FadeOut(write_group))
        
        # Dim the rest
        if write_idx < len(vals):
            self.play(
                *[cells[j][1].animate.set_opacity(0.3) for j in range(write_idx, len(vals))],
                run_time=0.5
            )

        self.wait(1.5)
        self.play(FadeOut(h_rect))
        self.wait(1.0)
