from manim import *
from abc import ABC, abstractmethod
from components.typography import Typography


class IScreenTemplate(ABC):
    # ── Top Left Tracker ──
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

    # ── Lower Third ──
    @abstractmethod
    def show_lower_third(self, title: str, subtitle: str, color_type: str = "blue", position: str = "left") -> None: pass
    @abstractmethod
    def hide_lower_third(self) -> None: pass


class ScreenTemplate(IScreenTemplate):
    def __init__(self, scene: Scene, typo: Typography):
        self.__scene = scene
        self.__typo = typo
        self.__current_tracker = None
        self.__current_lower_third = None

    # ── Private: Tracker ──
    def __update_tracker(self, text: str, dot_color: str, run_time: float = 0.8):
        dot = Circle(
            radius=self.__typo.dot_radius(),
            color=dot_color,
            fill_opacity=1,
            stroke_width=0,
        )
        title_text = Text(
            text.upper(),
            font=self.__typo.font_ui(),
            font_size=self.__typo.title_size(),
            color=self.__typo.color_white(),
        )
        new_tracker = VGroup(dot, title_text).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN)
        new_tracker.to_edge(UP + LEFT, buff=0.5)

        if self.__current_tracker is None:
            self.__scene.play(FadeIn(new_tracker, shift=RIGHT * 0.3), run_time=run_time)
        else:
            self.__scene.play(ReplacementTransform(self.__current_tracker, new_tracker), run_time=run_time)

        self.__current_tracker = new_tracker

    # ── Public: Tracker ──
    def screen_statement(self, text: str = "PROBLEM ANALYSIS") -> None:
        self.__update_tracker(text, self.__typo.color_white())

    def screen_brute_force(self, text: str = "BRUTE FORCE") -> None:
        self.__update_tracker(text, self.__typo.color_red())

    def screen_optimal_approach(self, text: str = "OPTIMAL APPROACH") -> None:
        self.__update_tracker(text, self.__typo.color_yellow())

    def screen_code_walkthrough(self, text: str = "CODE WALKTHROUGH") -> None:
        self.__update_tracker(text, self.__typo.color_blue())

    def screen_code_submission(self, text: str = "CODE SUBMISSION") -> None:
        self.__update_tracker(text, self.__typo.color_green())

    # ── Public: Lower Third ──
    def show_lower_third(self, title: str, subtitle: str, color_type: str = "blue", position: str = "left") -> None:
        color_map = {
            "white":  self.__typo.color_white(),
            "red":    self.__typo.color_red(),
            "yellow": self.__typo.color_yellow(),
            "blue":   self.__typo.color_blue(),
            "green":  self.__typo.color_green(),
        }
        accent_color = color_map.get(color_type.lower(), self.__typo.color_blue())

        accent_bar  = Line(UP * 0.45, DOWN * 0.45, stroke_width=5, color=accent_color)
        title_mob   = Text(title,    font=self.__typo.font_ui(),   font_size=24, color=self.__typo.color_white(), weight=BOLD)
        subtitle_mob= Text(subtitle, font=self.__typo.font_code(), font_size=16, color=self.__typo.color_secondary())

        text_group  = VGroup(title_mob, subtitle_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        
        if position.lower() == "right":
            lt_group = VGroup(text_group, accent_bar).arrange(RIGHT, buff=0.25, aligned_edge=ORIGIN)
            lt_group.to_edge(DOWN + RIGHT, buff=0.6)
            shift_dir = LEFT
        else:
            lt_group = VGroup(accent_bar, text_group).arrange(RIGHT, buff=0.25, aligned_edge=ORIGIN)
            lt_group.to_edge(DOWN + LEFT, buff=0.6)
            shift_dir = RIGHT

        if self.__current_lower_third is not None:
            self.__scene.play(ReplacementTransform(self.__current_lower_third, lt_group), run_time=0.8)
        else:
            self.__scene.play(
                GrowFromCenter(accent_bar, run_time=0.4),
                FadeIn(text_group, shift=shift_dir * 0.3, run_time=0.6),
                rate_func=smooth,
            )

        self.__current_lower_third = lt_group

    def hide_lower_third(self) -> None:
        if self.__current_lower_third is not None:
            self.__scene.play(FadeOut(self.__current_lower_third, shift=LEFT * 0.3), run_time=0.5)
            self.__current_lower_third = None