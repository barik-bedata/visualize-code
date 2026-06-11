from manim import *
from abc import ABC, abstractmethod
import numpy as np

config.flush_cache = True

class StepPanel:
    """
    A vertical step list that lives on the right side of the screen.

    Usage:
        panel = StepPanel(scene, typo, steps=[
            ("Copy nums2 → nums1", "fill empty slots"),
            ("Sort nums1",         "sort(nums1, m+n)"),
            ("Done",               "in-place, sorted"),
        ])
        panel.show()          # fade in entire panel
        panel.activate(0)     # highlight step 0 as active (blue)
        panel.complete(0)     # mark step 0 done (green ✓)
        panel.activate(1)     # highlight step 1
        ...
        panel.hide()          # fade out entire panel
    """

    # ── colors (match Typography) ──────────────────────────────────
    _C_ACTIVE   = "#1A73E8"   # blue  — currently running
    _C_DONE     = "#198754"   # green — finished
    _C_INACTIVE = "#424242"   # gray  — not yet started
    _C_TEXT     = "#E0E0E0"   # white
    _C_SUB      = "#B0B0B0"   # secondary

    def __init__(self, scene: Scene, typo, steps: list[tuple[str, str]]):
        self.scene  = scene
        self.typo   = typo
        self.steps  = steps
        self._rows  = []       # list of dicts per step
        self._group = VGroup() # entire panel mobject

        # complexity badges (optional — set before show())
        self._badges: VGroup | None = None

        self._build()

    # ─────────────────────────────────────────────────────────────
    #  BUILD
    # ─────────────────────────────────────────────────────────────
    def _build(self):
        rows_vgroup = VGroup()

        for i, (title, subtitle) in enumerate(self.steps):
            # circle with number
            circle = Circle(
                radius=0.18,
                color=self._C_INACTIVE,
                stroke_width=1.5,
                fill_opacity=0,
            )
            num = Text(
                str(i + 1),
                font=self.typo.font_ui(),
                font_size=13,
                color=self._C_INACTIVE,
            ).move_to(circle.get_center())
            badge = VGroup(circle, num)

            # title + subtitle
            title_text = Text(
                title,
                font=self.typo.font_code(),
                font_size=14,
                color=self._C_TEXT,
            )
            sub_text = Text(
                subtitle,
                font=self.typo.font_code(),
                font_size=11,
                color=self._C_SUB,
            )
            text_col = VGroup(title_text, sub_text).arrange(DOWN, buff=0.06, aligned_edge=LEFT)

            row = VGroup(badge, text_col).arrange(RIGHT, buff=0.2, aligned_edge=UP)
            row.set_opacity(0.3)   # inactive by default

            self._rows.append({
                "row":    row,
                "circle": circle,
                "num":    num,
                "title":  title_text,
                "sub":    sub_text,
            })
            rows_vgroup.add(row)

        rows_vgroup.arrange(DOWN, buff=0.35, aligned_edge=LEFT)

        # vertical divider line on the left of the panel
        divider = Line(
            start=rows_vgroup.get_top()    + LEFT * 0.4 + UP   * 0.1,
            end  =rows_vgroup.get_bottom() + LEFT * 0.4 + DOWN * 0.1,
            stroke_width=0.8,
            color=self._C_INACTIVE,
        ).set_opacity(0.3)

        self._group = VGroup(divider, rows_vgroup)
        # position: right side, vertically centered
        self._group.to_edge(RIGHT, buff=0.5)
        self._group.move_to(
            [self._group.get_center()[0], 0, 0]   # vertical center
        )

    # ─────────────────────────────────────────────────────────────
    #  PUBLIC API
    # ─────────────────────────────────────────────────────────────
    def add_complexity(self, time_text: str, space_text: str):
        """
        Add Time / Space complexity badges below the step list.
        Call BEFORE show().
        """
        t_badge = self._make_badge(f"Time  {time_text}", "#1e2a1e", "#4CAF50", "#2d4a2d")
        s_badge = self._make_badge(f"Space {space_text}", "#1e2a1e", "#1A73E8", "#1a3a4a")
        self._badges = VGroup(t_badge, s_badge).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        self._badges.next_to(self._group, DOWN, buff=0.4, aligned_edge=LEFT)

    def show(self, run_time: float = 0.7):
        anims = [FadeIn(self._group, shift=LEFT * 0.2)]
        if self._badges:
            anims.append(FadeIn(self._badges, shift=LEFT * 0.2))
        self.scene.play(*anims, run_time=run_time)

    def hide(self, run_time: float = 0.5):
        anims = [FadeOut(self._group)]
        if self._badges:
            anims.append(FadeOut(self._badges))
        self.scene.play(*anims, run_time=run_time)

    def activate(self, index: int, run_time: float = 0.4):
        """Highlight step as currently active (blue)."""
        r = self._rows[index]
        self.scene.play(
            r["row"].animate.set_opacity(1),
            r["circle"].animate.set_stroke(color=self._C_ACTIVE),
            r["num"].animate.set_color(self._C_ACTIVE),
            r["title"].animate.set_color(self._C_ACTIVE),
            run_time=run_time,
        )

    def complete(self, index: int, run_time: float = 0.4):
        """Mark step as done: green filled circle with checkmark."""
        r = self._rows[index]

        # swap number for checkmark
        checkmark = Text(
            "✓",
            font=self.typo.font_ui(),
            font_size=13,
            color="#FFFFFF",
        ).move_to(r["circle"].get_center())

        self.scene.play(
            r["circle"].animate.set_stroke(color=self._C_DONE)
                               .set_fill(color=self._C_DONE, opacity=1),
            FadeOut(r["num"]),
            FadeIn(checkmark),
            r["title"].animate.set_color(self._C_DONE),
            r["row"].animate.set_opacity(0.6),
            run_time=run_time,
        )
        # replace num ref so future calls don't break
        r["num"] = checkmark

    def deactivate(self, index: int, run_time: float = 0.3):
        """Dim a step back to inactive (without marking done)."""
        r = self._rows[index]
        self.scene.play(
            r["row"].animate.set_opacity(0.3),
            run_time=run_time,
        )

    # ─────────────────────────────────────────────────────────────
    #  HELPERS
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def _make_badge(label: str, bg: str, fg: str, border: str) -> VGroup:
        rect = RoundedRectangle(
            corner_radius=0.08,
            width=2.6,
            height=0.34,
            fill_color=bg,
            fill_opacity=1,
            stroke_color=border,
            stroke_width=1,
        )
        text = Text(label, font="Courier New", font_size=11, color=fg)
        text.move_to(rect.get_center())
        return VGroup(rect, text)




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


class ISwapAnimator(ABC):
    @abstractmethod
    def animate_swap(self, cell_a, cell_b):
        pass


class SwapAnimator(ISwapAnimator):
    def __init__(self, scene, lift_height=0.6):
        self.scene = scene
        self.lift_height = lift_height

    def animate_swap(self, cell_a, cell_b):
        """
        cell_a, cell_b = VGroup elements like cells1[i], cells1[j]
        """

        a_text = cell_a[1]
        b_text = cell_b[1]

        a_pos = a_text.get_center()
        b_pos = b_text.get_center()

        # ─────────────────────────
        # STEP 1: LIFT (visual separation)
        # ─────────────────────────
        self.scene.play(
            a_text.animate.shift(UP * self.lift_height),
            b_text.animate.shift(UP * self.lift_height),
            run_time=0.2
        )

        # ─────────────────────────
        # STEP 2: CROSS MOVE (swap path)
        # ─────────────────────────
        self.scene.play(
            a_text.animate.move_to(b_pos + UP * self.lift_height),
            b_text.animate.move_to(a_pos + UP * self.lift_height),
            run_time=0.5,
            rate_func=smooth
        )

        # ─────────────────────────
        # STEP 3: DROP (settle into place)
        # ─────────────────────────
        self.scene.play(
            a_text.animate.move_to(b_pos),
            b_text.animate.move_to(a_pos),
            run_time=0.25
        )


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
        #  SCREEN HEADER
        # ─────────────────────────────────────────────────────────────
        tracker.screen_brute_force("Brute Force")

        # ─────────────────────────────────────────────────────────────
        #  STEP PANEL  (right side)
        # ─────────────────────────────────────────────────────────────
        panel = StepPanel(scene=self, typo=typo, steps=[
            ("Copy nums2 → nums1", "fill empty slots"),
            ("Sort nums1",         "sort(nums1, m+n)"),
            ("Done",               "in-place, sorted"),
        ])
        panel.add_complexity("O((m+n) log(m+n))", "O(1)")
        panel.show()

        # ─────────────────────────────────────────────────────────────
        #  BUILD nums1 ROW
        # ─────────────────────────────────────────────────────────────
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

        m_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        m_text = Text("m = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        m_text.move_to(m_rect.get_center())
        m_box = VGroup(m_rect, m_text)

        row1 = VGroup(nums1_group, m_box).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        row1.move_to(UP * 1.5 + LEFT * 1.5)

        # ─────────────────────────────────────────────────────────────
        #  BUILD nums2 ROW
        # ─────────────────────────────────────────────────────────────
        nums2_lbl = Text("nums2 = ", font=typo.font_code(), font_size=20, color=typo.color_white())
        vals2 = [2, 5, 6]

        cells2 = VGroup(*[
            VGroup(
                Square(side_length=0.8, color=typo.color_gray(), stroke_width=2),
                Text(str(v), font=typo.font_code(), font_size=20, color=typo.color_white())
            ) for v in vals2
        ]).arrange(buff=0)

        nums2_group = VGroup(nums2_lbl, cells2).arrange(RIGHT, buff=0.2)

        n_rect = Rectangle(width=1.4, height=0.8, color=typo.color_yellow(), stroke_width=0)
        n_text = Text("n = 3", font=typo.font_code(), font_size=20, color=typo.color_yellow())
        n_text.move_to(n_rect.get_center())
        n_box = VGroup(n_rect, n_text)

        row2 = VGroup(nums2_group, n_box).arrange(RIGHT, buff=3.2, aligned_edge=UP)
        row2.next_to(row1, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            FadeIn(row1, shift=RIGHT * 0.3),
            FadeIn(row2, shift=RIGHT * 0.3),
            run_time=1.2,
        )
        self.wait(2.0)

        # ─────────────────────────────────────────────────────────────
        #  STEP 1 — Copy nums2 → nums1
        # ─────────────────────────────────────────────────────────────
        empty_highlighter = RangeHighlighter(self, "#5B6B7A")
        empty_highlighter.create(cells1, 3, 5)
        empty_highlighter.effect_highlight_show()

        source_highlighter = RangeHighlighter(self, typo.color_blue())
        source_highlighter.create(cells2, 0, 2)
        source_highlighter.effect_highlight_show()
        source_highlighter.effect_pulse()

        panel.activate(0)

        for i in range(3):
            source_cell = cells2[i]
            target_cell = cells1[i + 3]

            ghost = source_cell.copy()
            self.add(ghost)

            self.play(
                ghost.animate.move_to(target_cell.get_center()),
                run_time=0.55,
                rate_func=smooth,
            )
            self.play(FadeOut(ghost), run_time=0.15)

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
            target_cell.remove(target_cell[1])
            target_cell.add(new_text)

        panel.complete(0)

        # clean up highlighters
        self.play(
            empty_highlighter.border.animate.set_color(typo.color_green()),
            run_time=0.3,
        )
        source_highlighter.effect_highlight_hide()
        empty_highlighter.effect_highlight_hide()

        # subtle scale bump to signal copy done
        self.play(cells1.animate.scale(1.02), run_time=0.2)
        self.play(cells1.animate.scale(1.0 / 1.02), run_time=0.2)

        # ─────────────────────────────────────────────────────────────
        #  STEP 2 — Sort nums1
        # ─────────────────────────────────────────────────────────────
        panel.activate(1)

        # brief sort label
        sort_label = Text(
            "sort(nums1, m+n)",
            font=typo.font_code(),
            font_size=16,
            color=typo.color_blue(),
        ).next_to(cells1, DOWN, buff=0.5)

        self.play(FadeIn(sort_label, shift=UP * 0.15), run_time=0.5)
        self.wait(0.6)

        # nums1 is [1,2,3,2,5,6] → one swap: index 2 ↔ index 3
        self.play(FadeOut(sort_label), run_time=0.3)
        swap_animator.animate_swap(cells1[2], cells1[3])
        # result: [1, 2, 2, 3, 5, 6] ✓

        panel.complete(1)

        # ─────────────────────────────────────────────────────────────
        #  STEP 3 — Done
        # ─────────────────────────────────────────────────────────────
        panel.activate(2)

        final_highlighter = RangeHighlighter(self, typo.color_green())
        final_highlighter.create(cells1, 0, 5)
        final_highlighter.effect_highlight_show()
        final_highlighter.effect_glow_show()

        self.play(final_highlighter.border.animate.set_stroke(width=6), run_time=0.2)
        self.play(final_highlighter.border.animate.set_stroke(width=3), run_time=0.2)
        final_highlighter.effect_pulse()

        panel.complete(2)

        self.wait(1.5)