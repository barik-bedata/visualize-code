from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class Walkthrough(Scene):
    def construct(self):
        from components.typography import Typography, ITypography
        from components.screenTemplate import ScreenTemplate, IScreenTemplate
        from components.highlighter import RangeHighlighter

        typo: ITypography = Typography()
        self.camera.background_color = typo.bg()
        tracker: IScreenTemplate = ScreenTemplate(self, typo)
        
        # Color Theme Constants
        WHITE = typo.color_white()
        GRAY = typo.color_gray()
        GRAY_A = typo.color_secondary()
        YELLOW = typo.color_yellow()
        RED = typo.color_red()
        GREEN = typo.color_green()
        BLUE = typo.color_blue()
        BLACK = typo.text_on_yellow()
        
        SCAN_BLUE = BLUE       
        SUCCESS_BOOTSTRAP_GREEN = GREEN 
        MAP_SCAN_YELLOW = YELLOW    

        # ==========================================
        # 1. SCREEN TITLE
        # ==========================================
        # tracker.screen_code_walkthrough("Code Walkthrough")

        # ==========================================
        # 2. LAYOUT SETUP (Left Side)
        # ==========================================
        
        nums_label = Text("nums = ", font=typo.font_ui(), font_size=20, color=WHITE)
        nums = [2, 1, 3, 5, 8]
        array_cells = VGroup(*[
            VGroup(
                Square(side_length=0.7, color=WHITE, stroke_width=3, fill_opacity=0),
                Text(str(val), font=typo.font_ui(), font_size=20, color=WHITE)
            ) for val in nums
        ]).arrange(buff=0)
        
        array_with_label = VGroup(nums_label, array_cells).arrange(RIGHT, buff=0.2)
        
        indices = VGroup(*[
            Text(str(idx), font=typo.font_code(), font_size=12, color=GRAY)
            .next_to(array_cells[idx][0], UP, buff=0.1)
            for idx in range(len(nums))
        ])
        
        left_content = VGroup(array_with_label, indices)

        target_box = RoundedRectangle(corner_radius=0.1, width=1.6, height=0.6, color=WHITE, stroke_width=2, fill_opacity=0)
        target_txt = Text("Target = 9", font=typo.font_ui(), font_size=16, color=WHITE)
        right_target_group = VGroup(target_box, target_txt)

        # ── DICTIONARY TABLE ──
        map_title = MarkupText("<b>Dictionary</b>", font=typo.font_ui(), font_size=20, color=WHITE)
        
        map_box = RoundedRectangle(corner_radius=0.15, width=2.8, height=2.6, color=GRAY, stroke_width=2.5, fill_opacity=0)
        map_box.next_to(map_title, DOWN, buff=0.2)
        
        divider_v = Line(
            [map_box.get_center()[0], map_box.get_top()[1], 0],
            [map_box.get_center()[0], map_box.get_bottom()[1], 0],
            color=GRAY, stroke_width=1.5
        )
        
        line_y = map_box.get_top()[1] - 0.5
        header_line = Line(
            [map_box.get_left()[0], line_y, 0],
            [map_box.get_right()[0], line_y, 0],
            color=GRAY, stroke_width=2
        )
        
        header_y = map_box.get_top()[1] - 0.25
        key_header = Text("Key", font=typo.font_ui(), font_size=14, weight=BOLD, color=GRAY_A).move_to([map_box.get_center()[0] - 0.7, header_y, 0])
        val_header = Text("Value", font=typo.font_ui(), font_size=14, weight=BOLD, color=GRAY_A).move_to([map_box.get_center()[0] + 0.7, header_y, 0])
        
        table_grid = VGroup(map_title, map_box, divider_v, header_line, key_header, val_header)


        # ==========================================
        # 3. PYTHON CODE BLOCK (Right Side)
        # ==========================================
        python_code_string = """def twoSum(nums, target):
    seen = {}
    
    for i in range(len(nums)):
        complement = target - nums[i]
        
        if complement in seen:
            return [seen[complement], i]
            
        seen[nums[i]] = i
        
    return []"""
        code_block = Code(
            code_string=python_code_string,
            language="python",
            tab_width=4,
            background="window",
            formatter_style="monokai"
        ).scale(0.55)
        # Position left column elements vertically with sufficient clearance for pointer 'i'
        right_target_group.next_to(left_content, DOWN, buff=1.6)
        table_grid.next_to(right_target_group, DOWN, buff=0.3)
        left_column = VGroup(left_content, right_target_group, table_grid)
        
        # Position and center all content dynamically
        all_content = VGroup(left_column, code_block).arrange(RIGHT, buff=1.2)
        all_content.move_to(ORIGIN)
        
        # Calculate dynamic mid_x for calculation displays in the middle gap
        mid_x = (map_box.get_right()[0] + code_block.get_left()[0]) / 2

        self.play(
            FadeIn(left_content, shift=RIGHT * 0.3),
            FadeIn(right_target_group, shift=RIGHT * 0.3),
            FadeIn(table_grid, shift=RIGHT * 0.3),
            FadeIn(code_block, shift=LEFT * 0.3),
            run_time=1.2
        )
        self.wait(0.5)

        # Highlighter logic
        line_width = code_block.width + 0.1
        box_height = 0.25
        
        h_rect = RoundedRectangle(width=line_width, height=box_height, color=YELLOW, corner_radius=0.05)
        h_rect.set_stroke(width=2)
        h_rect.set_y(code_block[1][0].get_y())
        h_rect.set_x(code_block.get_x())
        
        def highlight_line(line_num: int, run_time=0.4):
            target_y = code_block[1][line_num].get_y()
            new_rect = RoundedRectangle(width=line_width, height=box_height, color=YELLOW, corner_radius=0.05)
            new_rect.set_stroke(width=2)
            new_rect.set_y(target_y)
            new_rect.set_x(code_block.get_x())
            self.play(Transform(h_rect, new_rect), run_time=run_time)

        self.play(FadeIn(h_rect))
        self.wait(0.5)

        # ==========================================
        # 4. WALKTHROUGH SIMULATION
        # ==========================================
        
        # Line 1: seen = {}
        highlight_line(1)
        self.wait(0.5)
        
        # Prepare pointer 'i'
        i_arrow = Arrow(start=DOWN, end=UP, color=SCAN_BLUE, stroke_width=10, max_tip_length_to_length_ratio=0.3).scale(0.25)
        i_label = Text("i", font=typo.font_ui(), font_size=18, weight=BOLD, color=SCAN_BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label)

        inserted_rows_items = [] 
        inserted_rows_bgs = [] 
        inserted_array_nodes = {}

        def insert_to_map(val, idx):
            num_rows = len(inserted_rows_items)
            y_pos = map_box.get_top()[1] - 0.75 - (num_rows * 0.4)
            key_x = map_box.get_center()[0] - 0.7
            val_x = map_box.get_center()[0] + 0.7
            
            row_bg = RoundedRectangle(corner_radius=0.08, width=2.6, height=0.35, color=WHITE, stroke_width=0, fill_opacity=0)
            row_bg.move_to([map_box.get_center()[0], y_pos, 0])
            
            key_item = Text(str(val), font=typo.font_ui(), font_size=16, color=WHITE).move_to([key_x, y_pos, 0])
            val_item = Text(str(idx), font=typo.font_ui(), font_size=16, color=WHITE).move_to([val_x, y_pos, 0])
            
            row_content = VGroup(key_item, val_item)
            inserted_rows_items.append(row_content)
            inserted_rows_bgs.append(row_bg)
            inserted_array_nodes[nums[idx]] = array_cells[idx] 
            
            val_travel = array_cells[idx][1].copy()
            idx_travel = indices[idx].copy()
            
            self.play(
                ReplacementTransform(val_travel, key_item),
                ReplacementTransform(idx_travel, val_item),
                FadeIn(row_bg),
                run_time=0.6
            )

        for i in range(len(nums)):
            # Line 3: for i in range(len(nums)):
            highlight_line(3)
            
            self.bring_to_front(array_cells[i])
            if i == 0:
                i_ptr.next_to(array_cells[i][0], DOWN, buff=0.1)
                self.play(FadeIn(i_ptr), array_cells[i][0].animate.set_fill(SCAN_BLUE, opacity=1), run_time=0.5)
            else:
                self.play(
                    i_ptr.animate.next_to(array_cells[i][0], DOWN, buff=0.1),
                    array_cells[i][0].animate.set_fill(SCAN_BLUE, opacity=1),
                    run_time=0.5
                )
            
            # Line 4: complement = target - nums[i]
            highlight_line(4)
            
            comp = 9 - nums[i]
            
            comp_lbl = Text("comp = ", font=typo.font_ui(), font_size=16, color=WHITE)
            val_target = Text("9", font=typo.font_ui(), font_size=16, color=WHITE)
            minus_sign = Text("- ", font=typo.font_ui(), font_size=16, color=WHITE)
            val_curr = Text(str(nums[i]), font=typo.font_ui(), font_size=16, color=WHITE)
            
            expr_group = VGroup(comp_lbl, val_target, minus_sign, val_curr).arrange(RIGHT, buff=0.1)
            expr_group.move_to([mid_x, -0.2, 0])
            
            self.play(Write(comp_lbl), run_time=0.3)
            fly_9 = Text("9", font=typo.font_ui(), font_size=16, color=WHITE).move_to(target_txt.get_right() + LEFT * 0.1)
            self.play(fly_9.animate.move_to(val_target.get_center()), run_time=0.4)
            
            fly_curr = array_cells[i][1].copy()
            self.play(FadeIn(minus_sign), fly_curr.animate.move_to(val_curr.get_center()).scale(16/20), run_time=0.4)
            
            result_val = Text(str(comp), font=typo.font_ui(), font_size=16, color=WHITE)
            result_val.next_to(comp_lbl, RIGHT, buff=0.1)
            
            self.play(
                FadeOut(VGroup(fly_9, minus_sign, fly_curr)),
                FadeIn(result_val),
                run_time=0.4
            )
            calc_txt = VGroup(comp_lbl, result_val)
            
            # Line 6: if complement in seen:
            highlight_line(6)
            
            search_status_txt = Text(f"Checking Dict: {comp} ?", font=typo.font_ui(), font_size=16, color=YELLOW)
            search_status_txt.next_to(map_box, DOWN, buff=0.2)
            self.play(Write(search_status_txt), run_time=0.3)
            
            is_found = False
            match_row_idx = -1
            for idx, row in enumerate(inserted_rows_items):
                key_scan_box = SurroundingRectangle(row[0], color=MAP_SCAN_YELLOW, stroke_width=4, buff=0.1)
                self.play(Create(key_scan_box), run_time=0.15)
                if row[0].text == str(comp):
                    is_found = True
                    match_row_idx = idx
                    self.play(FadeOut(key_scan_box), run_time=0.1)
                    break
                self.play(FadeOut(key_scan_box), run_time=0.1)
                
            if is_found:
                final_status_txt = Text(f"Checking Dict: {comp} ✓", font=typo.font_ui(), font_size=16, color=GREEN)
                final_status_txt.move_to(search_status_txt.get_center())
                self.play(ReplacementTransform(search_status_txt, final_status_txt), run_time=0.3)
                
                # Highlight row
                matched_row_content = inserted_rows_items[match_row_idx]
                row_bg = inserted_rows_bgs[match_row_idx]
                row_success_highlight = SurroundingRectangle(row_bg, color=SUCCESS_BOOTSTRAP_GREEN, stroke_width=4, buff=0.03)
                self.bring_to_front(matched_row_content) 
                self.play(FadeIn(row_success_highlight), run_time=0.3)
                
                complement_node = inserted_array_nodes[comp]
                self.bring_to_front(complement_node, array_cells[i])
                
                self.play(
                    array_cells[i][0].animate.set_stroke(color=SUCCESS_BOOTSTRAP_GREEN, width=6).set_fill(BLACK, opacity=0),
                    complement_node[0].animate.set_stroke(color=SUCCESS_BOOTSTRAP_GREEN, width=6).set_fill(BLACK, opacity=0),
                    run_time=0.5
                )
                
                # Line 7: return [seen[complement], i]
                highlight_line(7)
                
                self.play(FadeOut(calc_txt), FadeOut(final_status_txt), run_time=0.2)
                
                final_box = RoundedRectangle(corner_radius=0.1, width=1.6, height=0.6, color=SUCCESS_BOOTSTRAP_GREEN, stroke_width=3, fill_opacity=0)
                final_box.move_to([mid_x, -0.2, 0])
                
                open_b = Text("[", font=typo.font_ui(), font_size=20, color=WHITE)
                idx1_str = matched_row_content[1].text
                t1 = Text(idx1_str, font=typo.font_ui(), font_size=20, color=WHITE)
                comma_space = Text(", ", font=typo.font_ui(), font_size=20, color=WHITE) 
                t4 = Text(str(i), font=typo.font_ui(), font_size=20, color=WHITE)
                close_b = Text("]", font=typo.font_ui(), font_size=20, color=WHITE)
                
                final_txt_group = VGroup(open_b, t1, comma_space, t4, close_b).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
                final_txt_group.move_to(final_box.get_center())
                
                idx1_flying_copy = matched_row_content[1].copy().set_color(WHITE) 
                idx4_flying_copy = indices[i].copy().set_color(WHITE) 
                self.bring_to_front(idx1_flying_copy, idx4_flying_copy)
                
                val_travel = array_cells[i][1].copy() 
                self.play(
                    ReplacementTransform(val_travel, final_box),
                    FadeOut(i_ptr),
                    FadeIn(open_b), FadeIn(comma_space), FadeIn(close_b),
                    ReplacementTransform(idx1_flying_copy, t1), 
                    ReplacementTransform(idx4_flying_copy, t4),
                    run_time=1.0
                )
                self.play(Flash(final_box, color=SUCCESS_BOOTSTRAP_GREEN, flash_radius=0.8, num_lines=12, line_stroke_width=3), run_time=0.5)
                break
                
            else:
                final_status_txt = Text(f"Checking Dict: {comp} ✗", font=typo.font_ui(), font_size=16, color=RED)
                final_status_txt.move_to(search_status_txt.get_center())
                self.play(ReplacementTransform(search_status_txt, final_status_txt), run_time=0.3)
                
                # Line 9: seen[nums[i]] = i
                highlight_line(9)
                
                self.play(FadeOut(calc_txt), FadeOut(final_status_txt), run_time=0.2)
                
                insert_to_map(nums[i], i)
                self.play(array_cells[i][0].animate.set_fill(SCAN_BLUE, opacity=0.1), run_time=0.3)
                
                # End of loop iteration

        self.play(FadeOut(h_rect))

        # --- lower third ---
        tracker.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(N)", color_type="green")
        self.wait(3)
