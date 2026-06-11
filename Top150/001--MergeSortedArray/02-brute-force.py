from manim import *
from abc import ABC, abstractmethod
import numpy as np

config.flush_cache = True

# ═══════════════════════════════════════════════════════════════════
#  0. Bulletproof Custom Rate Function
# ═══════════════════════════════════════════════════════════════════
def custom_ease_out_cubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


# ═══════════════════════════════════════════════════════════════════
#  1. Interfaces & Typography Classes
# ═══════════════════════════════════════════════════════════════════
class ITypography(ABC):
    @abstractmethod
    def bg(self) -> str: pass
    @abstractmethod
    def color_white(self) -> str: pass
    @abstractmethod
    def color_secondary(self) -> str: pass
    @abstractmethod
    def color_red(self) -> str: pass
    @abstractmethod
    def color_yellow(self) -> str: pass
    @abstractmethod
    def color_blue(self) -> str: pass
    @abstractmethod
    def color_green(self) -> str: pass
    @abstractmethod
    def color_milestone_green(self) -> str: pass
    @abstractmethod
    def font_ui(self) -> str: pass
    @abstractmethod
    def font_code(self) -> str: pass
    @abstractmethod
    def title_size(self) -> int: pass
    @abstractmethod
    def dot_radius(self) -> float: pass


class Typography(ITypography):
    def __init__(self):
        self.__BG               = "#121212"
        self.__WHITE            = "#E0E0E0"
        self.__SECONDARY        = "#B0B0B0"
        self.__RED              = "#DC3545"
        self.__YELLOW           = "#EAB308"
        self.__BLUE             = "#1A73E8"
        self.__BLUE_GRAY        = "#6C7A89"
        self.__GREEN            = "#198754"
        self.__MILESTONE_GREEN  = "#4CAF50"
        self.__GRAY             = "#424242"
        self.__PURE_WHITE       = "#FFFFFF"
        self.__PURE_BLACK       = "#000000"

        self.__FONT_UI    = "Inter"
        self.__FONT_CODE  = "Courier New"
        self.__SCENE_TITLE_SIZE = 28
        self.__DOT_RADIUS = 0.22

    def bg(self) -> str:                    return self.__BG
    def color_white(self) -> str:           return self.__WHITE
    def color_secondary(self) -> str:       return self.__SECONDARY
    def color_red(self) -> str:             return self.__RED
    def color_yellow(self) -> str:          return self.__YELLOW
    def color_blue(self) -> str:            return self.__BLUE
    def color_blue_gray(self) -> str:       return self.__BLUE_GRAY
    def color_green(self) -> str:           return self.__GREEN
    def color_milestone_green(self) -> str: return self.__MILESTONE_GREEN
    def color_gray(self) -> str:            return self.__GRAY
    def text_on_dark(self) -> str:          return self.__PURE_WHITE
    def text_on_yellow(self) -> str:        return self.__PURE_BLACK
    def font_ui(self) -> str:               return self.__FONT_UI
    def font_code(self) -> str:             return self.__FONT_CODE
    def title_size(self) -> int:            return self.__SCENE_TITLE_SIZE
    def dot_radius(self) -> float:          return self.__DOT_RADIUS


class IScreenTemplate(ABC):
    @abstractmethod
    def screen_statement(self, text: str = "PROBLEM ANALYSIS") -> None: pass
    @abstractmethod
    def screen_brute_force(self, text: str = "BRUTE FORCE") -> None: pass
    @abstractmethod
    def screen_optimal_approach(self, text: str = "OPTIMAL APPROACH") -> None: pass
    @abstractmethod
    def screen_code_walkthrough(self, text: str = "CODE WALKTHROUGH") -> None: pass
    @abstractmethod
    def screen_code_submission(self, text: str = "CODE SUBMISSION") -> None: pass


class ScreenTemplate(IScreenTemplate):
    def __init__(self, scene: Scene, typo: Typography):
        self.__scene = scene
        self.__typo = typo
        self.__current_tracker = None

    def __update_tracker(self, text: str, dot_color: str, run_time: float = 0.8):
        dot = Circle(radius=self.__typo.dot_radius(), color=dot_color, fill_opacity=1, stroke_width=0)
        processed_text = text.upper()
        title_text = Text(processed_text, font=self.__typo.font_ui(), font_size=self.__typo.title_size(), color=self.__typo.color_white())
        new_tracker = VGroup(dot, title_text).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN)
        new_tracker.to_edge(UP + LEFT, buff=0.5)

        if self.__current_tracker is None:
            self.__scene.play(FadeIn(new_tracker, shift=RIGHT * 0.3), run_time=run_time)
        else:
            self.__scene.play(ReplacementTransform(self.__current_tracker, new_tracker), run_time=run_time)
        self.__current_tracker = new_tracker

    def screen_statement(self, text: str = "PROBLEM ANALYSIS") -> None:     self.__update_tracker(text, self.__typo.color_white())
    def screen_brute_force(self, text: str = "BRUTE FORCE") -> None:        self.__update_tracker(text, self.__typo.color_red())
    def screen_optimal_approach(self, text: str = "OPTIMAL APPROACH") -> None: self.__update_tracker(text, self.__typo.color_yellow())
    def screen_code_walkthrough(self, text: str = "CODE WALKTHROUGH") -> None: self.__update_tracker(text, self.__typo.color_blue())
    def screen_code_submission(self, text: str = "CODE SUBMISSION") -> None:   self.__update_tracker(text, self.__typo.color_green())

class IRangeHighlighter(ABC):

    @abstractmethod
    def create(self, group: VGroup, start: int, end: int):
        pass

    @abstractmethod
    def effect_highlight_show(self):
        pass

    @abstractmethod
    def effect_highlight_hide(self):
        pass

    @abstractmethod
    def effect_pulse(self, scale_up: float = 1.08, scale_down: float = 0.92):
        pass

class RangeHighlighter(IRangeHighlighter):

    def __init__(self, scene, color):
        self.scene = scene
        self.color = color
        self.border = None
        self.glow = None

    def create(self, group, start, end, buff=0.1, stroke_width=3):
        target = VGroup(*group[start:end + 1])

        self.border = SurroundingRectangle(
            target,
            color=self.color,
            buff=buff,
            stroke_width=stroke_width
        )

        self.glow = SurroundingRectangle(
            target,
            color=self.color,
            buff=buff + 0.05,
            stroke_width=8
        )
        self.glow.set_fill(self.color, opacity=0.08)
        self.glow.set_stroke(opacity=0.3)

        return self.border

    def effect_highlight_show(self):
        if self.border:
            self.scene.play(Create(self.border), run_time=0.5)

    def effect_highlight_hide(self):
        if self.border:
            self.scene.play(FadeOut(self.border), FadeOut(self.border), run_time=0.5)

    def effect_pulse(self, scale_up=1.08, scale_down=0.92):
        if not self.border:
            return
        self.scene.play(self.border.animate.scale(scale_up), run_time=0.25)
        self.scene.play(self.border.animate.scale(scale_down), run_time=0.25)

    def effect_glow_show(self):
        if self.glow:
            self.scene.play(FadeIn(self.glow), run_time=0.4)

    def effect_glow_hide(self):
        if self.glow:
            self.scene.play(FadeOut(self.glow), run_time=0.3)




# ═══════════════════════════════════════════════════════════════════
#  2. Main Scene
# ═══════════════════════════════════════════════════════════════════
class BruteForce(Scene):

    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)
        swap_animator = SwapAnimator(self)

        # ─────────────────────────────────────────────────────────────
        #  SCENE 1: PROBLEM STATEMENT
        # ─────────────────────────────────────────────────────────────
        tracker.screen_brute_force("Brute Force")



        # ── nums1 ───────────────────────────────────────────────────
        nums1_lbl = Text("nums1 = ", font=typo.font_code(), font_size=20, color=typo.color_white())
        vals1 = [1, 2, 3, 0, 0, 0]

        cells1 = VGroup(*[
            VGroup(
                Square(side_length=0.8, color=typo.color_gray(), stroke_width=2),
                Text(
                    str(v),
                    font=typo.font_code(),
                    font_size=20,
                    color=typo.color_white() if v != 0 else typo.color_secondary()
                )
            ) for v in vals1
        ]).arrange(buff=0)

        nums1_group = VGroup(nums1_lbl, cells1).arrange(RIGHT, buff=0.2)

        # m‑box
        m_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        m_text = Text("m = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        m_text.move_to(m_rect.get_center())
        m_box = VGroup(m_rect, m_text)

        row1 = VGroup(nums1_group, m_box).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        row1.move_to(UP * 1.5 + LEFT * 1.5)

        # ── nums2 ───────────────────────────────────────────────────
        nums2_lbl = Text("nums2 = ", font=typo.font_code(), font_size=20, color=typo.color_white())
        vals2 = [2, 5, 6]

        cells2 = VGroup(*[
            VGroup(
                Square(side_length=0.8, color=typo.color_gray(), stroke_width=2),
                Text(str(v), font=typo.font_code(), font_size=20, color=typo.color_white())
            ) for v in vals2
        ]).arrange(buff=0)

        nums2_group = VGroup(nums2_lbl, cells2).arrange(RIGHT, buff=0.2)

        # n‑box
        n_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        n_text = Text("n = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        n_text.move_to(n_rect.get_center())
        n_box = VGroup(n_rect, n_text)

        row2 = VGroup(nums2_group, n_box).arrange(RIGHT, buff=3.2, aligned_edge=UP)
        row2.next_to(row1, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
            FadeIn(row2, shift=RIGHT * 0.3),
            run_time=1.2
        )
        self.wait(2.0)

        # ── Data‑flow: nums2 → empty slots in nums1 ─────────────────
        empty_highlighter = RangeHighlighter(self, "#5B6B7A")
        empty_highlighter.create(cells1, 3, 5)
        empty_highlighter.effect_highlight_show()

        source_highlighter = RangeHighlighter(self, typo.color_blue())
        source_highlighter.create(cells2, 0, 2)
        source_highlighter.effect_highlight_show()
        source_highlighter.effect_pulse()

        # FIX: copy animation – fade the ghost OUT before updating the real cell
        for i in range(3):
            source_cell = cells2[i]
            target_cell = cells1[i + 3]

            # ghost starts at source center, flies to target center
            ghost = source_cell.copy()
            self.add(ghost)

            self.play(
                ghost.animate.move_to(target_cell.get_center()),
                run_time=0.55,
                rate_func=smooth,
            )

            # fade ghost out FIRST …
            self.play(FadeOut(ghost), run_time=0.15)

            # … then reveal the real value (no overlap / duplicate)
            new_text = Text(
                str(vals2[i]),
                font=typo.font_code(),
                font_size=20,
                color=typo.color_white(),
            ).move_to(target_cell[1].get_center())

            self.play(
                FadeOut(target_cell[1]),
                FadeIn(new_text),
                run_time=0.25,
            )
            # replace the mobject in the VGroup so future moves track correctly
            target_cell.remove(target_cell[1])
            target_cell.add(new_text)


        # colour the empty border green
        self.play(
            empty_highlighter.border.animate.set_color(typo.color_green()),
            run_time=0.3,
        )

        source_highlighter.effect_highlight_hide()
        empty_highlighter.effect_highlight_hide()


        # subtle scale bump
        self.play(cells1.animate.scale(1.02), run_time=0.2)
        self.play(cells1.animate.scale(1.0 / 1.02), run_time=0.2)

        # ── SORT ANIMATION (fixed swap) ──────────────────────────────
        # nums1 state now: [1, 2, 3, 2, 5, 6]
        # need one swap: index 2 (value 3) ↔ index 3 (value 2)
        swap_animator.animate_swap(cells1[2], cells1[3])
        # after swap: [1, 2, 2, 3, 5, 6]  ✓ already sorted; one swap is enough

        # ── FINAL HIGHLIGHT ──────────────────────────────────────────
        final_highlighter = RangeHighlighter(self, typo.color_green())
        final_highlighter.create(cells1, 0, 5)
        final_highlighter.effect_highlight_show()
        final_highlighter.effect_glow_show()

        self.play(final_highlighter.border.animate.set_stroke(width=6), run_time=0.2)
        self.play(final_highlighter.border.animate.set_stroke(width=3), run_time=0.2)
        final_highlighter.effect_pulse()

        self.wait(1.5)