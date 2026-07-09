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
        from components.highlighter import RangeHighlighter, IRangeHighlighter

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
        # 2. EXAMPLE 1
        # ==========================================
        nums_label_1 = Text("nums =", font=typo.font_code(), font_size=24, color=WHITE)
        nums_array_1 = [1, 2, 3, 4]
        
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
        array_group_1.move_to(UP * 1.5 + LEFT * 0.5)
        
        self.play(FadeIn(array_group_1, shift=UP * 0.3), run_time=1)
        self.wait(1)

        ans_label_1 = Text("answer =", font=typo.font_code(), font_size=24, color=WHITE)
        ans_array_1 = [24, 12, 8, 6]
        
        ans_cells_1 = VGroup()
        for idx, val in enumerate(ans_array_1):
            cell_bg = Square(side_length=0.7, color=GREEN, stroke_width=2)
            cell = VGroup(cell_bg)
            ans_cells_1.add(cell)
            
        ans_cells_1.arrange(RIGHT, buff=0)
        ans_label_1.next_to(ans_cells_1, LEFT, buff=0.5)
        ans_label_1.match_y(ans_cells_1[0][0])
        ans_group_1 = VGroup(ans_label_1, ans_cells_1)
        ans_group_1.next_to(array_group_1, DOWN, buff=2)
        
        self.play(FadeIn(ans_group_1, shift=UP * 0.3), run_time=1)
        self.wait(1)

        final_vals_1 = VGroup()

        for i in range(len(nums_array_1)):
            self.play(cells_1[i][0].animate.set_color(YELLOW), run_time=0.3)
            
            target_expr = VGroup()
            for k in range(len(nums_array_1)):
                if k != i:
                    target_val = Text(str(nums_array_1[k]), font=typo.font_code(), font_size=24, color=WHITE)
                    target_expr.add(target_val)
                    if len(target_expr) < (len(nums_array_1) - 1) * 2 - 1:
                        cross = Text("×", font=typo.font_code(), font_size=24, color=WHITE)
                        target_expr.add(cross)
            
            target_expr.arrange(RIGHT, buff=0.2)
            target_expr.move_to((array_group_1.get_center() + ans_group_1.get_center()) / 2)
            
            copies = VGroup()
            animations = []
            target_indices = 0
            for j in range(len(nums_array_1)):
                if j != i:
                    copy_val = cells_1[j][1].copy()
                    copies.add(copy_val)
                    animations.append(Transform(copy_val, target_expr[target_indices * 2]))
                    target_indices += 1
            
            cross_signs = VGroup()
            for k in range(1, len(target_expr), 2):
                cross_signs.add(target_expr[k])
                
            self.play(*animations, FadeIn(cross_signs), run_time=0.8)
            self.wait(0.3)
            
            product_val = Text(str(ans_array_1[i]), font=typo.font_code(), font_size=24, color=WHITE)
            product_val.move_to(target_expr.get_center())
            
            expr_group = VGroup(copies, cross_signs)
            self.play(FadeOut(expr_group), FadeIn(product_val), run_time=0.6)
            self.wait(0.3)
            
            final_val = Text(str(ans_array_1[i]), font=typo.font_code(), font_size=24, color=GREEN)
            final_val.move_to(ans_cells_1[i][0].get_center())
            
            self.play(ReplacementTransform(product_val, final_val), run_time=0.6)
            final_vals_1.add(final_val)
            
            self.play(cells_1[i][0].animate.set_color(WHITE), run_time=0.3)
            self.wait(0.3)

        hl_1 = RangeHighlighter(self, YELLOW)
        hl_1.create(ans_cells_1, 0, len(ans_cells_1) - 1)
        hl_1.effect_highlight_show()
        hl_1.effect_pulse()
        hl_1.effect_highlight_hide()
        self.wait(0.5)

        self.play(
            FadeOut(array_group_1), FadeOut(ans_group_1), FadeOut(final_vals_1),
            run_time=1
        )

        # ==========================================
        # 3. EXAMPLE 2
        # ==========================================
        nums_label_2 = Text("nums =", font=typo.font_code(), font_size=24, color=WHITE)
        nums_array_2 = [-1, 1, 0, -3, 3]
        
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
        array_group_2.move_to(UP * 1.5 + LEFT * 0.5)
        
        self.play(FadeIn(array_group_2, shift=UP * 0.3), run_time=1)
        self.wait(1)

        ans_label_2 = Text("answer =", font=typo.font_code(), font_size=24, color=WHITE)
        ans_array_2 = [0, 0, 9, 0, 0]
        
        ans_cells_2 = VGroup()
        for idx, val in enumerate(ans_array_2):
            cell_bg = Square(side_length=0.7, color=GREEN, stroke_width=2)
            cell = VGroup(cell_bg)
            ans_cells_2.add(cell)
            
        ans_cells_2.arrange(RIGHT, buff=0)
        ans_label_2.next_to(ans_cells_2, LEFT, buff=0.5)
        ans_label_2.match_y(ans_cells_2[0][0])
        ans_group_2 = VGroup(ans_label_2, ans_cells_2)
        ans_group_2.next_to(array_group_2, DOWN, buff=2)
        
        self.play(FadeIn(ans_group_2, shift=UP * 0.3), run_time=1)
        self.wait(1)

        final_vals_2 = VGroup()

        for i in range(len(nums_array_2)):
            self.play(cells_2[i][0].animate.set_color(YELLOW), run_time=0.3)
            
            target_expr = VGroup()
            for k in range(len(nums_array_2)):
                if k != i:
                    target_val = Text(str(nums_array_2[k]), font=typo.font_code(), font_size=24, color=WHITE)
                    target_expr.add(target_val)
                    if len(target_expr) < (len(nums_array_2) - 1) * 2 - 1:
                        cross = Text("×", font=typo.font_code(), font_size=24, color=WHITE)
                        target_expr.add(cross)
            
            target_expr.arrange(RIGHT, buff=0.2)
            target_expr.move_to((array_group_2.get_center() + ans_group_2.get_center()) / 2)
            
            copies = VGroup()
            animations = []
            target_indices = 0
            for j in range(len(nums_array_2)):
                if j != i:
                    copy_val = cells_2[j][1].copy()
                    copies.add(copy_val)
                    animations.append(Transform(copy_val, target_expr[target_indices * 2]))
                    target_indices += 1
            
            cross_signs = VGroup()
            for k in range(1, len(target_expr), 2):
                cross_signs.add(target_expr[k])
                
            self.play(*animations, FadeIn(cross_signs), run_time=1.2)
            self.wait(0.6)
            
            product_val = Text(str(ans_array_2[i]), font=typo.font_code(), font_size=24, color=WHITE)
            product_val.move_to(target_expr.get_center())
            
            expr_group = VGroup(copies, cross_signs)
            self.play(FadeOut(expr_group), FadeIn(product_val), run_time=1.0)
            self.wait(0.6)
            
            final_val = Text(str(ans_array_2[i]), font=typo.font_code(), font_size=24, color=GREEN)
            final_val.move_to(ans_cells_2[i][0].get_center())
            
            self.play(ReplacementTransform(product_val, final_val), run_time=1.0)
            final_vals_2.add(final_val)
            
            self.play(cells_2[i][0].animate.set_color(WHITE), run_time=0.3)
            self.wait(0.5)

        hl_2 = RangeHighlighter(self, YELLOW)
        hl_2.create(ans_cells_2, 0, len(ans_cells_2) - 1)
        hl_2.effect_highlight_show()
        hl_2.effect_pulse()
        hl_2.effect_highlight_hide()
        self.wait(0.5)

        self.play(
            FadeOut(array_group_2), FadeOut(ans_group_2), FadeOut(final_vals_2),
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
