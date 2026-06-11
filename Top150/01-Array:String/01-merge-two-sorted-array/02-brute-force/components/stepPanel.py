from manim import *
from abc import ABC, abstractmethod


class IStepPanel(ABC):
    @abstractmethod
    def show(self, run_time: float) -> None: pass
    @abstractmethod
    def hide(self, run_time: float) -> None: pass
    @abstractmethod
    def activate(self, index: int, run_time: float) -> None: pass
    @abstractmethod
    def complete(self, index: int, run_time: float) -> None: pass
    @abstractmethod
    def deactivate(self, index: int, run_time: float) -> None: pass


class StepPanel(IStepPanel):
    _C_ACTIVE   = "#1A73E8"
    _C_DONE     = "#22C55E"
    _C_INACTIVE = "#6B7280"
    _C_TEXT     = "#F1F5F9"
    _C_SUB      = "#94A3B8"

    def __init__(self, scene: Scene, typo, steps: list[tuple[str, str]]):
        self.scene   = scene
        self.typo    = typo
        self.steps   = steps
        self._rows   = []
        self._group  = VGroup()
        self._badges = None
        self._build()

    def _build(self):
        rows_vgroup = VGroup()

        for i, (title, subtitle) in enumerate(self.steps):
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
            row.set_opacity(0.3)

            self._rows.append({
                "row":    row,
                "circle": circle,
                "num":    num,
                "title":  title_text,
                "sub":    sub_text,
            })
            rows_vgroup.add(row)

        rows_vgroup.arrange(DOWN, buff=0.35, aligned_edge=LEFT)

        top_y    = rows_vgroup.get_top()[1]    + 0.1
        bottom_y = rows_vgroup.get_bottom()[1] - 0.1
        line_x   = rows_vgroup.get_left()[0]   - 0.4

        divider = Line(
            start=np.array([line_x, top_y,    0]),
            end  =np.array([line_x, bottom_y, 0]),
            stroke_width=0.8,
            color=self._C_INACTIVE,
        ).set_opacity(0.3)

        self._group = VGroup(divider, rows_vgroup)
        self._group.to_edge(RIGHT, buff=1.2)
        self._group.move_to([self._group.get_center()[0], 0, 0])

    def show(self, run_time: float = 0.7) -> None:
        anims = [FadeIn(self._group, shift=LEFT * 0.2)]
        if self._badges:
            anims.append(FadeIn(self._badges, shift=LEFT * 0.2))
        self.scene.play(*anims, run_time=run_time)

    def hide(self, run_time: float = 0.5) -> None:
        anims = [FadeOut(self._group)]
        if self._badges:
            anims.append(FadeOut(self._badges))
        self.scene.play(*anims, run_time=run_time)

    def activate(self, index: int, run_time: float = 0.4) -> None:
        r = self._rows[index]
        self.scene.play(
            r["row"].animate.set_opacity(1),
            r["circle"].animate.set_stroke(color=self._C_ACTIVE),
            r["num"].animate.set_color(self._C_ACTIVE),
            r["title"].animate.set_color(self._C_ACTIVE),
            run_time=run_time,
        )

    def complete(self, index: int, run_time: float = 0.4) -> None:
        r = self._rows[index]
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
        r["num"] = checkmark

    def deactivate(self, index: int, run_time: float = 0.3) -> None:
        r = self._rows[index]
        self.scene.play(r["row"].animate.set_opacity(0.3), run_time=run_time)

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