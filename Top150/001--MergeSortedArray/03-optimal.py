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
        self.__GREEN            = "#198754"
        self.__MILESTONE_GREEN  = "#4CAF50"
        self.__GRAY             = "#424242"
        self.__PURE_WHITE       = "#FFFFFF"
        self.__PURE_BLACK       = "#000000"

        self.__FONT_UI    = "Inter"
        self.__FONT_CODE  = "Courier New"   # changed from "Fira Code" to avoid warnings
        self.__SCENE_TITLE_SIZE = 28
        self.__DOT_RADIUS = 0.22

    def bg(self) -> str:                    return self.__BG
    def color_white(self) -> str:           return self.__WHITE
    def color_secondary(self) -> str:       return self.__SECONDARY
    def color_red(self) -> str:             return self.__RED
    def color_yellow(self) -> str:          return self.__YELLOW
    def color_blue(self) -> str:            return self.__BLUE
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


# ═══════════════════════════════════════════════════════════════════
#  2. Main Scene
# ═══════════════════════════════════════════════════════════════════
class MergeSortedArrayAnimation(Scene):
    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        tracker = ScreenTemplate(self, typo)

        # ─────────────────────────────────────────────────────────────
        #  SCENE 3: OPTIMAL SOLUTION (Three Pointers from Back)
        # ─────────────────────────────────────────────────────────────
        tracker.screen_optimal_approach("Optimal Approach: Three Pointers O(m+n)")

        p1_ptr = Arrow(DOWN, UP, max_tip_length_to_length_ratio=0.2, color=typo.color_blue()).scale(0.4).next_to(cells1[2], DOWN, buff=0.1)
        p1_lbl = Text("p1 (m-1)", font=typo.font_code(), font_size=14, color=typo.color_blue()).next_to(p1_ptr, DOWN, buff=0.05)

        p2_ptr = Arrow(DOWN, UP, max_tip_length_to_length_ratio=0.2, color=typo.color_red()).scale(0.4).next_to(cells2[2], DOWN, buff=0.1)
        p2_lbl = Text("p2 (n-1)", font=typo.font_code(), font_size=14, color=typo.color_red()).next_to(p2_ptr, DOWN, buff=0.05)

        p_ptr = Arrow(UP, DOWN, max_tip_length_to_length_ratio=0.2, color=typo.color_green()).scale(0.4).next_to(cells1[5], UP, buff=0.1)
        p_lbl = Text("p (tail)", font=typo.font_code(), font_size=14, color=typo.color_green()).next_to(p_ptr, UP, buff=0.05)

        self.play(FadeIn(p1_ptr), FadeIn(p1_lbl), FadeIn(p2_ptr), FadeIn(p2_lbl), FadeIn(p_ptr), FadeIn(p_lbl))
        self.wait(1.5)

        # Step 1: Compare 3 and 6 -> 6 Wins
        self.play(cells1[2][0].animate.set_stroke(color=typo.color_yellow(), width=4),
                  cells2[2][0].animate.set_stroke(color=typo.color_yellow(), width=4))
        self.wait(0.5)
        self.play(cells1[5][1].animate.become(Text("6", font=typo.font_code(), font_size=20, color=typo.color_white()).move_to(cells1[5][0].get_center())))
        self.play(
            p2_ptr.animate.next_to(cells2[1], DOWN, buff=0.1), p2_lbl.animate.next_to(cells2[1], DOWN, buff=0.25),
            p_ptr.animate.next_to(cells1[4], UP, buff=0.1),    p_lbl.animate.next_to(cells1[4], UP, buff=0.25),
            cells1[2][0].animate.set_stroke(color=typo.color_gray(), width=2),
            cells2[2][0].animate.set_stroke(color=typo.color_gray(), width=2)
        )

        # Step 2: Compare 3 and 5 -> 5 Wins
        self.play(cells1[2][0].animate.set_stroke(color=typo.color_yellow(), width=4),
                  cells2[1][0].animate.set_stroke(color=typo.color_yellow(), width=4))
        self.wait(0.5)
        self.play(cells1[4][1].animate.become(Text("5", font=typo.font_code(), font_size=20, color=typo.color_white()).move_to(cells1[4][0].get_center())))
        self.play(
            p2_ptr.animate.next_to(cells2[0], DOWN, buff=0.1), p2_lbl.animate.next_to(cells2[0], DOWN, buff=0.25),
            p_ptr.animate.next_to(cells1[3], UP, buff=0.1),    p_lbl.animate.next_to(cells1[3], UP, buff=0.25),
            cells1[2][0].animate.set_stroke(color=typo.color_gray(), width=2),
            cells2[1][0].animate.set_stroke(color=typo.color_gray(), width=2)
        )

        # Step 3: Compare 3 and 2 -> 3 Wins
        self.play(cells1[2][0].animate.set_stroke(color=typo.color_yellow(), width=4),
                  cells2[0][0].animate.set_stroke(color=typo.color_yellow(), width=4))
        self.wait(0.5)
        self.play(cells1[3][1].animate.become(Text("3", font=typo.font_code(), font_size=20, color=typo.color_white()).move_to(cells1[3][0].get_center())))
        self.play(
            p1_ptr.animate.next_to(cells1[1], DOWN, buff=0.1), p1_lbl.animate.next_to(cells1[1], DOWN, buff=0.25),
            p_ptr.animate.next_to(cells1[2], UP, buff=0.1),    p_lbl.animate.next_to(cells1[2], UP, buff=0.25),
            cells1[2][0].animate.set_stroke(color=typo.color_gray(), width=2),
            cells2[0][0].animate.set_stroke(color=typo.color_gray(), width=2)
        )

        # Step 4: Remaining nums2[0] = 2 -> place it
        self.play(cells1[2][1].animate.become(Text("2", font=typo.font_code(), font_size=20, color=typo.color_white()).move_to(cells1[2][0].get_center())))
        self.wait(1.0)

        self.play(FadeOut(p1_ptr), FadeOut(p1_lbl), FadeOut(p2_ptr), FadeOut(p2_lbl),
                  FadeOut(p_ptr), FadeOut(p_lbl))
        self.play(FadeOut(g1), FadeOut(g2), FadeOut(meta_info))
