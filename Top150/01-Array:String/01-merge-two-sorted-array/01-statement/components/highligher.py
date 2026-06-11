from manim import *
from abc import ABC, abstractmethod


class IRangeHighlighter(ABC):
    @abstractmethod
    def create(self, group: VGroup, start: int, end: int): pass
    @abstractmethod
    def effect_highlight_show(self): pass
    @abstractmethod
    def effect_highlight_hide(self): pass
    @abstractmethod
    def effect_pulse(self, scale_up: float, scale_down: float): pass


class RangeHighlighter(IRangeHighlighter):
    def __init__(self, scene: Scene, color: str):
        self.scene  = scene
        self.color  = color
        self.border = None
        self.glow   = None

    def create(self, group, start: int, end: int, buff: float = 0.1, stroke_width: int = 3):
        target = VGroup(*group[start:end + 1])

        self.border = SurroundingRectangle(
            target,
            color=self.color,
            buff=buff,
            stroke_width=stroke_width,
        )
        self.glow = SurroundingRectangle(
            target,
            color=self.color,
            buff=buff + 0.05,
            stroke_width=8,
        )
        self.glow.set_fill(self.color, opacity=0.08)
        self.glow.set_stroke(opacity=0.3)

        return self.border

    def effect_highlight_show(self):
        if self.border:
            self.scene.play(Create(self.border), run_time=0.5)

    def effect_highlight_hide(self):
        if self.border:
            self.scene.play(FadeOut(self.border), run_time=0.5)

    def effect_pulse(self, scale_up: float = 1.08, scale_down: float = 0.92):
        if not self.border:
            return
        self.scene.play(self.border.animate.scale(scale_up),   run_time=0.25)
        self.scene.play(self.border.animate.scale(scale_down), run_time=0.25)

    def effect_glow_show(self):
        if self.glow:
            self.scene.play(FadeIn(self.glow), run_time=0.4)

    def effect_glow_hide(self):
        if self.glow:
            self.scene.play(FadeOut(self.glow), run_time=0.3)
