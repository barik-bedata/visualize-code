from manim import *
from abc import ABC, abstractmethod


class IRangeHighlighter(ABC):
    @abstractmethod
    def create(self, group: VGroup, start: int, end: int): pass
    @abstractmethod
    def effect_highlight_show(self): pass
    @abstractmethod
    def effect_highlight_show_glow(self): pass
    @abstractmethod
    def effect_highlight_hide(self): pass
    @abstractmethod
    def effect_highlight_hide_glow(self): pass
    @abstractmethod
    def effect_pulse(self, scale_up: float, scale_down: float): pass
    @abstractmethod
    def effect_pulse_glow(self, scale_up: float, scale_down: float): pass
    @abstractmethod
    def effect_glow_show(self): pass
    @abstractmethod
    def effect_glow_hide(self): pass


class RangeHighlighter(IRangeHighlighter):
    def __init__(self, scene: Scene, color: str):
        self.scene  = scene
        self.color  = color
        self.border = None
        self.glow   = None

    # create a highlighter for a range of elements in a VGroup, with optional glow effect
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

    # show only the border, keep the glow hidden if it exists
    def effect_highlight_show(self):
        if self.border:
            self.scene.play(Create(self.border), run_time=0.5)

    # show both border and glow together
    def effect_highlight_show_glow(self):
        if self.border and self.glow:
            self.scene.play(
                Create(self.border),
                FadeIn(self.glow),
                run_time=0.5,
            )

    # hide only the border, keep the glow if it exists
    def effect_highlight_hide(self):
        if self.border:
            self.scene.play(FadeOut(self.border), run_time=0.5)
    
    # hide both border and glow together
    def effect_highlight_hide_glow(self):
        if self.border and self.glow:
            self.scene.play(
                FadeOut(self.border),
                FadeOut(self.glow),
                run_time=0.5,
            )

    # pulse effect: scale up and down the border to create a pulsating effect
    def effect_pulse(self, scale_up: float = 1.08, scale_down: float = 0.92):
        if not self.border:
            return
        self.scene.play(self.border.animate.scale(scale_up),  run_time=0.25)
        self.scene.play(self.border.animate.scale(scale_down), run_time=0.25)

    # pulse effect for glow: scale up and down the border while fading the glow in and out
    def effect_pulse_glow(self, scale_up: float = 1.08, scale_down: float = 0.92):
        if not self.border:
            return
        self.scene.play(self.border.animate.scale(scale_up), FadeIn(self.glow), run_time=0.25)
        self.scene.play(self.border.animate.scale(scale_down), FadeOut(self.glow), run_time=0.25)

    # glow effect: simply fade in or out the glow rectangle without affecting the border
    def effect_glow_show(self):
        if self.glow:
            self.scene.play(FadeIn(self.glow), run_time=0.4)

    # glow effect: simply fade in or out the glow rectangle without affecting the border
    def effect_glow_hide(self):
        if self.glow:
            self.scene.play(FadeOut(self.glow), run_time=0.3)
