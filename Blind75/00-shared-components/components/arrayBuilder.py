from manim import *
from abc import ABC, abstractmethod


class IArrayBuilder(ABC):
    @property
    @abstractmethod
    def cells(self) -> VGroup: pass

    @property
    @abstractmethod
    def group(self) -> VGroup: pass

    @abstractmethod
    def build(self) -> "IArrayBuilder": pass

    @abstractmethod
    def show(self, run_time: float = 1.2, shift: float = 0.3) -> None: pass

    @abstractmethod
    def hide(self, run_time: float = 0.6) -> None: pass

    @abstractmethod
    def show_indices(self, position: str = None, run_time: float = 0.5) -> None: pass

    @abstractmethod
    def hide_indices(self, run_time: float = 0.4) -> None: pass

    @abstractmethod
    def toggle_indices(self, position: str = None, run_time: float = 0.5) -> None: pass

    @abstractmethod
    def set_value(self, index: int, new_value, run_time: float = 0.3) -> None: pass

    @abstractmethod
    def highlight_cell(self, index: int, color, run_time: float = 0.3) -> None: pass

    @abstractmethod
    def reset_cell(self, index: int, run_time: float = 0.3) -> None: pass

    @abstractmethod
    def move_to(self, point, run_time: float = 0.7) -> None: pass

    @abstractmethod
    def to_edge(self, edge=LEFT, buff: float = 0.6, run_time: float = 0.7) -> None: pass


class ArrayBuilder(IArrayBuilder):

    def __init__(
        self,
        scene: Scene,
        typo,
        values: list,
        label: str = "",
        cell_size: float = 0.8,
        font_size: int = 20,
        index_font_size: int = 14,
        zero_dim: bool = True,        # True হলে ০ মান dim রঙে দেখাবে
        index_position: str = "below", # "above" বা "below"
    ):
        self._scene = scene
        self._typo = typo
        self._values = list(values)
        self._label_text = label
        self._cell_size = cell_size
        self._font_size = font_size
        self._index_font_size = index_font_size
        self._zero_dim = zero_dim
        self._index_position = index_position  # default index position

        self._cells: VGroup = None       # শুধু cell গুলো (RangeHighlighter-এর জন্য)
        self._group: VGroup = None       # label + cells একসাথে
        self._label_mob: Mobject = None  # label mobject আলাদা রাখা হলো
        self._index_group: VGroup = None # index text গুলো আলাদা group-এ
        self._indices_visible = False    # index এখন visible কিনা track করা
        self._built = False

    @property
    def cells(self) -> VGroup:
        return self._cells

    @property
    def group(self) -> VGroup:
        return self._group

    # ──────────────────────────────────────────────────────────────────
    #  Build — Mobject তৈরি করা (scene-এ add করে না)
    # ──────────────────────────────────────────────────────────────────

    def build(self) -> "ArrayBuilder":
        """
        সব Mobject তৈরি করে।
        show() call করার আগে এটা call করতে হবে।
        Returns self, তাই chain করা যাবে: arr.build().show()
        """

        # ── প্রতিটা value-এর জন্য cell (Square + Text) তৈরি ──
        cell_list = []
        for v in self._values:
            square = Square(
                side_length=self._cell_size,
                color=self._typo.color_gray(),
                stroke_width=2,
            )
            # ০ হলে dim রঙ, নইলে সাদা
            text_color = (
                self._typo.color_secondary()
                if (self._zero_dim and v == 0)
                else self._typo.color_white()
            )
            number = Text(
                str(v),
                font=self._typo.font_code(),
                font_size=self._font_size,
                color=text_color,
            ).move_to(square.get_center())

            cell_list.append(VGroup(square, number))

        # cells গুলো পাশাপাশি সাজানো (gap নেই)
        self._cells = VGroup(*cell_list).arrange(RIGHT, buff=0)

        # ── Index group তৈরি (এখনো invisible) ──
        self._build_indices()

        # ── Label তৈরি (label_text ফাঁকা হলে বাদ)
        # Group-এ indices-ও include করা হচ্ছে, যাতে array move করলে
        # indices ও একসাথে move করে (misalignment fix)।
        if self._label_text:
            self._label_mob = Text(
                f"{self._label_text} = ",
                font=self._typo.font_code(),
                font_size=self._font_size,
                color=self._typo.color_white(),
            )
            # label_mob এবং cells-কে আগে horizontally arrange করি
            # index_group-কে আলাদাভাবে manage করব যাতে label centers cells-এর সাথে align থাকে
            self._group = VGroup(self._label_mob, self._cells).arrange(RIGHT, buff=0.2)
            # এখন index_group-কে cells-এর সাথে group করি but main group-এ indices-ও রাখি move logic-এর জন্য
            self._group.add(self._index_group)
        else:
            self._label_mob = None
            self._group = VGroup(VGroup(self._cells, self._index_group))

        self._built = True
        return self

    def _build_indices(self):
        """Index text গুলো তৈরি করে cells-এর উপরে বা নিচে position করা।"""
        index_mobs = []
        for i, cell in enumerate(self._cells):
            idx_text = Text(
                str(i),
                font=self._typo.font_code(),
                font_size=self._index_font_size,
                color=self._typo.color_secondary(),
            )
            # উপরে বা নিচে রাখা
            if self._index_position == "above":
                idx_text.next_to(cell, UP, buff=0.15)
            else:
                idx_text.next_to(cell, DOWN, buff=0.15)

            index_mobs.append(idx_text)

        self._index_group = VGroup(*index_mobs)
        # শুরুতে transparent রাখা
        self._index_group.set_opacity(0)

    # ──────────────────────────────────────────────────────────────────
    #  Show / Hide — পুরো array (label + cells)
    # ──────────────────────────────────────────────────────────────────

    def show(self, run_time: float = 1.2, shift: float = 0.3):
        """
        Array-কে animate করে Scene-এ দেখানো।
        shift: ডান থেকে হালকা slide করে আসবে।
        """
        self._assert_built()
        self._scene.play(
            FadeIn(self._group, shift=RIGHT * shift),
            run_time=run_time,
        )

    def hide(self, run_time: float = 0.6):
        """Array-কে animate করে লুকানো।"""
        self._assert_built()
        anims = [FadeOut(self._group, run_time=run_time)]
        if self._indices_visible:
            anims.append(FadeOut(self._index_group, run_time=run_time))
        self._scene.play(*anims)
        self._indices_visible = False

    # ──────────────────────────────────────────────────────────────────
    #  Index show / hide
    # ──────────────────────────────────────────────────────────────────

    def show_indices(
        self,
        position: str = None,
        run_time: float = 0.5,
    ):
        """
        Index গুলো দেখানো।
        position: "above" বা "below" — None হলে build()-এর default ব্যবহার হবে।
        """
        self._assert_built()

        # position পরিবর্তন চাইলে re-build করা
        if position and position != self._index_position:
            self._index_position = position
            self._build_indices()

        # _index_group এখন main group-এর অংশ — আলাদাভাবে add করা দরকার নেই
        self._scene.play(
            self._index_group.animate.set_opacity(1),
            run_time=run_time,
        )
        self._indices_visible = True

    def hide_indices(self, run_time: float = 0.4):
        """Index গুলো লুকানো।"""
        if not self._indices_visible:
            return
        self._scene.play(
            self._index_group.animate.set_opacity(0),
            run_time=run_time,
        )
        self._indices_visible = False

    def toggle_indices(self, position: str = None, run_time: float = 0.5):
        """Index visible হলে hide, না হলে show।"""
        if self._indices_visible:
            self.hide_indices(run_time=run_time)
        else:
            self.show_indices(position=position, run_time=run_time)

    # ──────────────────────────────────────────────────────────────────
    #  Cell value পরিবর্তন করা (FadeOut পুরনো → FadeIn নতুন)
    # ──────────────────────────────────────────────────────────────────

    def set_value(self, index: int, new_value, run_time: float = 0.3):
        """
        নির্দিষ্ট index-এর cell-এর value animate করে পরিবর্তন করা।
        RangeHighlighter-এর মতোই scene থেকে call করা যাবে।
        """
        self._assert_built()
        self._assert_index(index)

        cell = self.cells[index]
        old_text = cell[1]  # cell[0] = Square, cell[1] = Text

        text_color = (
            self._typo.color_secondary()
            if (self._zero_dim and new_value == 0)
            else self._typo.color_white()
        )
        new_text = Text(
            str(new_value),
            font=self._typo.font_code(),
            font_size=self._font_size,
            color=text_color,
        ).move_to(old_text.get_center())

        self._scene.play(
            FadeOut(old_text),
            FadeIn(new_text),
            run_time=run_time,
        )

        # VGroup-এর reference update করা
        cell.remove(old_text)
        cell.add(new_text)
        self._values[index] = new_value

    # ──────────────────────────────────────────────────────────────────
    #  Convenience: একটা cell-কে highlight রঙ দেওয়া / reset
    # ──────────────────────────────────────────────────────────────────

    def highlight_cell(self, index: int, color, run_time: float = 0.3):
        """নির্দিষ্ট cell-এর border রঙ পরিবর্তন।"""
        self._assert_built()
        self._assert_index(index)
        square = self.cells[index][0]
        self._scene.play(square.animate.set_color(color), run_time=run_time)

    def reset_cell(self, index: int, run_time: float = 0.3):
        """Cell-এর border রঙ default gray-তে ফেরানো।"""
        self.highlight_cell(index, self._typo.color_gray(), run_time=run_time)

    # ──────────────────────────────────────────────────────────────────
    #  Positioning helpers — group-কে সহজে সরানো
    # ──────────────────────────────────────────────────────────────────

    def move_to(self, point, run_time: float = 0.7):
        """animate করে নির্দিষ্ট position-এ সরানো।"""
        self._assert_built()
        self._scene.play(
            self._group.animate.move_to(point),
            run_time=run_time,
            rate_func=smooth,
        )

    def to_edge(self, edge=LEFT, buff: float = 0.6, run_time: float = 0.7):
        """animate করে screen-এর edge-এ সরানো।"""
        self._assert_built()
        self._scene.play(
            self._group.animate.to_edge(edge, buff=buff),
            run_time=run_time,
            rate_func=smooth,
        )

    # ──────────────────────────────────────────────────────────────────
    #  Internal helpers
    # ──────────────────────────────────────────────────────────────────

    def _assert_built(self):
        if not self._built:
            raise RuntimeError("build() আগে call করতে হবে।")

    def _assert_index(self, index: int):
        if not (0 <= index < len(self._values)):
            raise IndexError(
                f"index {index} out of range (array length = {len(self._values)})"
            )