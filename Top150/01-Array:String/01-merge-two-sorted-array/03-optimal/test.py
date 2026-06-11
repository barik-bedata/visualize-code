from manim import *

from components.typography import Typography, ITypography
from components.highlighter import RangeHighlighter, IRangeHighlighter
from components.arrayBuilder import ArrayBuilder, IArrayBuilder


class ExampleUsage(Scene):

    def construct(self):
        typo: ITypography = Typography()
        self.camera.background_color = typo.bg()

        nums1, nums2 = self._build_arrays(typo)
        content = self._layout_arrays(nums1, nums2)

        self._demo_show_arrays(nums1, nums2)
        self._demo_indices(nums1, nums2)
        self._demo_highlighters(typo, nums1, nums2)
        self._demo_set_values(nums1)
        self._demo_move_left(content)
        self._demo_hide_arrays(nums1, nums2)

    # ── Setup ────────────────────────────────────────────────────────

    def _build_arrays(self, typo: ITypography) -> tuple[IArrayBuilder, IArrayBuilder]:
        nums1 = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[1, 2, 3, 0, 0, 0],
            label="nums1",
        ).build()

        nums2 = ArrayBuilder(
            scene=self,
            typo=typo,
            values=[2, 5, 6],
            label="nums2",
            index_position="above",
        ).build()

        return nums1, nums2

    def _layout_arrays(self, nums1: IArrayBuilder, nums2: IArrayBuilder) -> VGroup:
        content = VGroup(nums1.group, nums2.group).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT,
        )
        content.move_to(ORIGIN)
        return content

    # ── Demos ────────────────────────────────────────────────────────

    def _demo_show_arrays(self, nums1: IArrayBuilder, nums2: IArrayBuilder) -> None:
        nums1.show()
        nums2.show()
        self.wait(0.8)

    def _demo_indices(self, nums1: IArrayBuilder, nums2: IArrayBuilder) -> None:
        nums1.show_indices()
        self.wait(0.5)

        nums2.show_indices()
        self.wait(0.8)

        nums1.hide_indices()
        self.wait(0.4)

        nums2.toggle_indices()
        self.wait(0.5)

    def _demo_highlighters(
        self,
        typo: ITypography,
        nums1: IArrayBuilder,
        nums2: IArrayBuilder,
    ) -> None:
        empty_hl: IRangeHighlighter = RangeHighlighter(self, "#5B6B7A")
        empty_hl.create(nums1.cells, 3, 5)
        empty_hl.effect_highlight_show()

        source_hl: IRangeHighlighter = RangeHighlighter(self, typo.color_blue())
        source_hl.create(nums2.cells, 0, 2)
        source_hl.effect_highlight_show()
        source_hl.effect_pulse()

        self.wait(1.0)
        source_hl.effect_highlight_hide()
        empty_hl.effect_highlight_hide()

    def _demo_set_values(self, nums1: IArrayBuilder) -> None:
        nums1.set_value(3, 2)
        nums1.set_value(4, 5)
        nums1.set_value(5, 6)
        self.wait(0.5)

    def _demo_move_left(self, content: VGroup) -> None:
        self.play(
            content.animate.to_edge(LEFT, buff=0.6),
            run_time=0.7,
            rate_func=smooth,
        )
        self.wait(0.5)

    def _demo_hide_arrays(self, nums1: IArrayBuilder, nums2: IArrayBuilder) -> None:
        nums1.hide()
        nums2.hide()
        self.wait(0.5)
