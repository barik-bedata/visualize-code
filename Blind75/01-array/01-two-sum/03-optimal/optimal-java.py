from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

import numpy as np

config.flush_cache = True

class HashMapSolutionJava(Scene):
    def construct(self):
        # ১. প্রিমিয়াম ম্যাট অফ-ব্ল্যাক ব্যাকগ্রাউন্ড
        from components.typography import Typography
        from components.screenTemplate import ScreenTemplate
        
        typo = Typography()
        screen_template = ScreenTemplate(self, typo)
        
        self.camera.background_color = typo.bg()
        
        # কালার থিম কনস্ট্যান্টস (Pattern Problem Template)
        WHITE = typo.color_white()
        GRAY = typo.color_gray()
        GRAY_A = typo.color_secondary()
        YELLOW = typo.color_yellow()
        RED = typo.color_red()
        GREEN = typo.color_green()
        BLUE = typo.color_blue()
        BLACK = typo.text_on_yellow()
        
        # কালার থিম কনস্ট্যান্টস
        SCAN_BLUE = "#1A73E8"       
        SUCCESS_BOOTSTRAP_GREEN = "#198754" 
        BORDER_ORANGERED = "#DC3545" 
        MAP_SCAN_YELLOW = YELLOW    
        
        # ==========================================
        # ২. LAYOUT SETUP
        # ==========================================
        
        screen_template.screen_optimal_approach("Optimal Approach")


        nums_label = Text("nums = ", font="Sans", font_size=24, color=WHITE)
        
        nums = [2, 1, 3, 5, 8]
        array_cells = VGroup(*[
            VGroup(
                Square(side_length=1.0, color=WHITE, stroke_width=4, fill_opacity=0),
                Text(str(val), font="Sans", font_size=26, color=WHITE)
            ) for val in nums
        ]).arrange(buff=0)
        
        array_with_label = VGroup(nums_label, array_cells).arrange(RIGHT, buff=0.25)
        array_with_label.move_to(LEFT * 2.8 + UP * 0.8) 
        
        indices = VGroup(*[
            Text(str(idx), font="Monospace", font_size=16, color=GRAY)
            .next_to(array_cells[idx][0], UP, buff=0.15)
            for idx in range(len(nums))
        ])
        
        left_content = VGroup(array_with_label, indices)

        target_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.9, color=WHITE, stroke_width=2.5, fill_opacity=0)
        target_txt = Text("Target = 9", font="Sans", font_size=22, color=WHITE)
        right_target_group = VGroup(target_box, target_txt).move_to(RIGHT * 4.0 + UP * 2.6)

        # ==========================================
        # ৩. STRUCTURED TWO-COLUMN TABLE SETUP
        # ==========================================
        
        map_title = Text("Hash Map", font="Sans", font_size=24, weight=BOLD, color=WHITE)
        map_title.move_to(RIGHT * 4.0 + UP * 1.0)
        
        map_box = RoundedRectangle(corner_radius=0.15, width=3.6, height=2.8, color=GRAY, stroke_width=2.5, fill_opacity=0)
        map_box.next_to(map_title, DOWN, buff=0.2)
        
        divider_v = Line(
            [map_box.get_center()[0], map_box.get_top()[1], 0],
            [map_box.get_center()[0], map_box.get_bottom()[1], 0],
            color=GRAY, stroke_width=1.5
        )
        
        line_y = map_box.get_top()[1] - 0.6
        header_line = Line(
            [map_box.get_left()[0], line_y, 0],
            [map_box.get_right()[0], line_y, 0],
            color=GRAY, stroke_width=2
        )
        
        header_y = map_box.get_top()[1] - 0.3
        key_header = Text("Key", font="Sans", font_size=18, weight=BOLD, color=GRAY_A).move_to([map_box.get_center()[0] - 0.9, header_y, 0])
        val_header = Text("Value", font="Sans", font_size=18, weight=BOLD, color=GRAY_A).move_to([map_box.get_center()[0] + 0.9, header_y, 0])
        
        table_grid = VGroup(map_title, map_box, divider_v, header_line, key_header, val_header)

        self.play(
            FadeIn(left_content, shift=RIGHT * 0.3),
            FadeIn(right_target_group, shift=LEFT * 0.3),
            FadeIn(table_grid, shift=UP * 0.2),
            run_time=1.2
        )
        self.wait(0.3)

        # ==========================================
        # ৪. POINTER GENERATION
        # ==========================================
        i_arrow = Arrow(DOWN * 0.35, ORIGIN, color=SCAN_BLUE, stroke_width=24, max_tip_length_to_length_ratio=0.45, buff=0)
        i_label = Text("i", font="Sans", font_size=30, weight=BOLD, color=SCAN_BLUE).next_to(i_arrow, DOWN, buff=0.1)
        i_ptr = VGroup(i_arrow, i_label).next_to(array_cells[0][0], DOWN, buff=0.2) 
        
        self.play(FadeIn(i_ptr), run_time=0.5)

        # ==========================================
        # ৫. HASH MAP ITERATION SIMULATION LOGIC
        # ==========================================
        
        calc_y_pos = -2.2
        inserted_rows_items = [] 
        inserted_rows_bgs = [] 
        inserted_array_nodes = {} 

        def insert_to_map(val, idx):
            num_rows = len(inserted_rows_items)
            y_pos = map_box.get_top()[1] - 0.9 - (num_rows * 0.5)
            key_x = map_box.get_center()[0] - 0.9
            val_x = map_box.get_center()[0] + 0.9
            
            row_bg = RoundedRectangle(corner_radius=0.08, width=3.4, height=0.45, color=WHITE, stroke_width=0, fill_opacity=0)
            row_bg.move_to([map_box.get_center()[0], y_pos, 0])
            
            key_item = Text(str(val), font="Sans", font_size=20, color=WHITE).move_to([key_x, y_pos, 0])
            val_item = Text(str(idx), font="Sans", font_size=20, color=WHITE).move_to([val_x, y_pos, 0])
            
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
                run_time=0.8
            )

        def step_hash_map(i, comp, is_found=False, match_row_idx=None):
            self.bring_to_front(array_cells[i])
            
            self.play(
                i_ptr.animate.next_to(array_cells[i][0], DOWN, buff=0.2),
                array_cells[i][0].animate.set_fill(SCAN_BLUE, opacity=1),
                run_time=0.6
            )
            
            # --- FLYING EQUATION ---
            comp_lbl = Text("complement = ", font="Sans", font_size=22, color=WHITE)
            val_target = Text("9", font="Sans", font_size=22, color=WHITE)
            minus_sign = Text("- ", font="Sans", font_size=22, color=WHITE)
            val_curr = Text(str(nums[i]), font="Sans", font_size=22, color=WHITE)
            
            expr_group = VGroup(comp_lbl, val_target, minus_sign, val_curr).arrange(RIGHT, buff=0.15)
            expr_group.move_to(LEFT * 2.2 + DOWN * 1.5)
            
            fly_9 = Text("9", font="Sans", font_size=22, color=WHITE).move_to(target_txt.get_right() + LEFT * 0.15)
            fly_curr = array_cells[i][1].copy()
            
            self.play(Write(comp_lbl), run_time=0.4)
            self.play(fly_9.animate.move_to(val_target.get_center()), run_time=0.5)
            self.play(
                FadeIn(minus_sign), 
                fly_curr.animate.move_to(val_curr.get_center()).scale(22/26), 
                run_time=0.5
            )
            self.wait(0.2)
            
            result_val = Text(str(comp), font="Sans", font_size=22, color=WHITE)
            result_val.next_to(comp_lbl, RIGHT, buff=0.15)
            
            self.play(ReplacementTransform(VGroup(fly_9, minus_sign, fly_curr), result_val), run_time=0.5)
            self.wait(0.2)
            
            calc_txt = VGroup(comp_lbl, result_val)
            
            # --- HISTORY BORDER ---
            history_border = None
            if i > 0:
                history_group = VGroup(*[array_cells[k][0] for k in range(i)])
                history_border = SurroundingRectangle(history_group, color=BORDER_ORANGERED, stroke_width=10, buff=0.1)
                self.play(Create(history_border), run_time=0.4)
                self.play(history_border.animate.set_stroke(opacity=0.3), run_time=0.15)
                self.play(history_border.animate.set_stroke(opacity=1.0), run_time=0.15)
                self.wait(0.2)
            
            # ====================================================
            # [NEW LOGIC] ১. প্রথমে Checking Map (Question Mark) টেক্সট আসবে
            # ====================================================
            search_status_txt = Text(f"Checking Map: {comp} ?", font="Sans", font_size=20, color=YELLOW)
            search_status_txt.next_to(map_box, DOWN, buff=0.2)
            self.play(Write(search_status_txt), run_time=0.4)
            
            # ২. এবার ম্যাপের Key কলামে স্ক্যানিং হবে
            if len(inserted_rows_items) > 0:
                for row_idx, row_content in enumerate(inserted_rows_items):
                    key_item = row_content[0] 
                    
                    key_scan_box = SurroundingRectangle(key_item, color=MAP_SCAN_YELLOW, stroke_width=5, buff=0.1)
                    self.play(Create(key_scan_box), run_time=0.2)
                    
                    if is_found and row_idx == match_row_idx:
                        self.play(FadeOut(key_scan_box), run_time=0.1)
                        break 
                    else:
                        self.play(FadeOut(key_scan_box), run_time=0.1)
            
            # ৩. স্ক্যানিং শেষে '?' চিহ্নটি অ্যানিমেট হয়ে '✗' বা '✓' এ রূপান্তরিত হবে
            if not is_found:
                final_status_txt = Text(f"Checking Map: {comp} ✗", font="Sans", font_size=20, color=RED)
                final_status_txt.move_to(search_status_txt.get_center())
                
                # Question mark turns into Red Cross
                self.play(ReplacementTransform(search_status_txt, final_status_txt), run_time=0.3)
                self.wait(0.4)
                
                animations = [FadeOut(calc_txt), FadeOut(final_status_txt)]
                if history_border:
                    animations.append(FadeOut(history_border))
                self.play(*animations, run_time=0.4)
                
                insert_to_map(nums[i], i)
                self.play(array_cells[i][0].animate.set_fill(SCAN_BLUE, opacity=0.2), run_time=0.3)
            else:
                final_status_txt = Text(f"Checking Map: {comp} Found! ✓", font="Sans", font_size=20, color=GREEN)
                final_status_txt.move_to(search_status_txt.get_center())
                
                # Question mark turns into Green Tick
                self.play(ReplacementTransform(search_status_txt, final_status_txt), run_time=0.3)
                self.wait(0.4)
                
                matched_row_content = inserted_rows_items[match_row_idx]
                row_bg = inserted_rows_bgs[match_row_idx]
                
                row_success_highlight = SurroundingRectangle(row_bg, color=SUCCESS_BOOTSTRAP_GREEN, stroke_width=6, buff=0.03)
                self.bring_to_front(matched_row_content) 
                self.play(FadeIn(row_success_highlight), run_time=0.3)
                
                complement_node = inserted_array_nodes[comp]
                self.bring_to_front(complement_node, array_cells[i])
                
                self.play(
                    array_cells[i][0].animate.set_stroke(color=SUCCESS_BOOTSTRAP_GREEN, width=8).set_fill(BLACK, opacity=0),
                    complement_node[0].animate.set_stroke(color=SUCCESS_BOOTSTRAP_GREEN, width=8).set_fill(BLACK, opacity=0),
                    run_time=0.7
                )
                
                self.play(FadeOut(calc_txt), FadeOut(final_status_txt), FadeOut(history_border), run_time=0.3)
                
                final_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.8, color=SUCCESS_BOOTSTRAP_GREEN, stroke_width=4, fill_opacity=0)
                final_box.move_to(np.array([0, calc_y_pos, 0]))
                
                open_b = Text("[", font="Sans", font_size=26, color=WHITE)
                t1 = Text("1", font="Sans", font_size=26, color=WHITE)
                comma_space = Text(",  ", font="Sans", font_size=26, color=WHITE) 
                t4 = Text("4", font="Sans", font_size=26, color=WHITE)
                close_b = Text("]", font="Sans", font_size=26, color=WHITE)
                
                final_txt_group = VGroup(open_b, t1, comma_space, t4, close_b).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
                final_txt_group.move_to(final_box.get_center())
                
                idx1_flying_copy = matched_row_content[1].copy().set_color(WHITE) 
                idx4_flying_copy = indices[i].copy().set_color(WHITE) 
                self.bring_to_front(idx1_flying_copy, idx4_flying_copy)
                
                val_travel = array_cells[i][1].copy() 
                self.play(
                    ReplacementTransform(VGroup(val_travel, calc_txt), final_box),
                    FadeOut(i_ptr),
                    FadeIn(open_b), FadeIn(comma_space), FadeIn(close_b),
                    ReplacementTransform(idx1_flying_copy, t1), 
                    ReplacementTransform(idx4_flying_copy, t4),
                    run_time=1.5,
                    rate_func=smooth
                )
                
                self.play(
                    Flash(final_box, color=SUCCESS_BOOTSTRAP_GREEN, flash_radius=1.0, num_lines=16, line_stroke_width=4),
                    run_time=0.5
                )
                self.wait(0.3)
                
                # ==========================================
                # ৬. COMPLEXITY PANEL (Lower Third from ScreenTemplate)
                # ==========================================
                screen_template.show_lower_third("Complexity Analysis", "Time: O(N), Space: O(N)", color_type="green")

        # ==========================================
        # 7. EXECUTION STEPS
        # ==========================================
        step_hash_map(i=0, comp=7, is_found=False) 
        step_hash_map(i=1, comp=8, is_found=False) 
        step_hash_map(i=2, comp=6, is_found=False) 
        step_hash_map(i=3, comp=4, is_found=False) 
        
        step_hash_map(i=4, comp=1, is_found=True, match_row_idx=1) 
        
        self.wait(3)