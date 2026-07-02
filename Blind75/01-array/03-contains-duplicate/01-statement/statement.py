from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class Statement(Scene):
    def construct(self):
        from components.typography import Typography, ITypography
        from components.screenTemplate import ScreenTemplate, IScreenTemplate

        typo: ITypography = Typography()
        self.camera.background_color = typo.bg()
        tracker: IScreenTemplate = ScreenTemplate(self, typo)
        
        # Color Theme Constants
        WHITE = typo.color_white()
        GRAY = typo.color_gray()
        GREEN = typo.color_green()
        RED = typo.color_red()
        BLUE = typo.color_blue()
        YELLOW = typo.color_yellow()
        
        # ==========================================
        # 1. SCREEN TITLE & DESCRIPTION
        # ==========================================
        tracker.screen_statement("Problem Statement")

        # ==========================================
        # 2. EXAMPLE 1: WITH DUPLICATE
        # ==========================================
        nums_label_1 = Text("nums =", font=typo.font_code(), font_size=24, color=WHITE)
        nums_array_1 = [1, 2, 3, 1]
        
        cells_1 = VGroup()
        for idx, val in enumerate(nums_array_1):
            cell_bg = Square(side_length=0.7, color=WHITE, stroke_width=2)
            cell_val = Text(str(val), font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=20, color="#B3B3B3").next_to(cell_bg, UP, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            cells_1.add(cell)
        
        cells_1.arrange(RIGHT, buff=0)
        nums_label_1.next_to(cells_1, LEFT, buff=0.5)
        nums_label_1.match_y(cells_1[0][0])
        array_group_1 = VGroup(nums_label_1, cells_1)
        array_group_1.move_to(UP * 0.5 + LEFT * 0.5)
        
        self.play(FadeIn(array_group_1, shift=UP * 0.3), run_time=1)
        self.wait(1)

        # Highlight duplicates
        dup_text = Text("Duplicate found!", font=typo.font_ui(), font_size=20, color=RED).next_to(cells_1, DOWN, buff=0.5)
        self.play(
            cells_1[0][0].animate.set_fill(RED, opacity=0.3).set_stroke(RED, width=4),
            cells_1[3][0].animate.set_fill(RED, opacity=0.3).set_stroke(RED, width=4),
            FadeIn(dup_text),
            run_time=1
        )
        self.wait(0.5)

        return_true = Text("return true", font=typo.font_code(), font_size=24, weight=BOLD, color=GREEN).next_to(dup_text, DOWN, buff=0.5)
        self.play(Write(return_true), run_time=1)
        self.wait(2)

        self.play(
            FadeOut(array_group_1), FadeOut(dup_text), FadeOut(return_true),
            run_time=1
        )

        # ==========================================
        # 3. EXAMPLE 2: WITHOUT DUPLICATE
        # ==========================================
        nums_label_2 = Text("nums =", font=typo.font_code(), font_size=24, color=WHITE)
        nums_array_2 = [1, 2, 3, 4]
        
        cells_2 = VGroup()
        for idx, val in enumerate(nums_array_2):
            cell_bg = Square(side_length=0.7, color=WHITE, stroke_width=2)
            cell_val = Text(str(val), font=typo.font_code(), font_size=24, color=WHITE)
            cell_idx = Text(str(idx), font=typo.font_code(), font_size=20, color="#B3B3B3").next_to(cell_bg, UP, buff=0.1)
            cell = VGroup(cell_bg, cell_val, cell_idx)
            cells_2.add(cell)
        
        cells_2.arrange(RIGHT, buff=0)
        nums_label_2.next_to(cells_2, LEFT, buff=0.5)
        nums_label_2.match_y(cells_2[0][0])
        array_group_2 = VGroup(nums_label_2, cells_2)
        array_group_2.move_to(UP * 0.5 + LEFT * 0.5)
        
        self.play(FadeIn(array_group_2, shift=UP * 0.3), run_time=1)
        self.wait(1)

        # Highlight all unique
        unique_text = Text("All elements distinct", font=typo.font_ui(), font_size=20, color=BLUE).next_to(cells_2, DOWN, buff=0.5)
        self.play(
            *[c[0].animate.set_fill(BLUE, opacity=0.3).set_stroke(BLUE, width=4) for c in cells_2],
            FadeIn(unique_text),
            run_time=1
        )
        self.wait(0.5)

        return_false = Text("return false", font=typo.font_code(), font_size=24, weight=BOLD, color=RED).next_to(unique_text, DOWN, buff=0.5)
        self.play(Write(return_false), run_time=1)
        self.wait(2)

        self.play(
            FadeOut(array_group_2), FadeOut(unique_text), FadeOut(return_false),
            run_time=1
        )
        self.wait(1)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = Statement()
    scene.render()
