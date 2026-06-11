from manim import *
from abc import ABC, abstractmethod
import numpy as np


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

