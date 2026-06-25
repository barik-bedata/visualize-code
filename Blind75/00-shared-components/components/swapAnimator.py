from manim import *


class SwapAnimator:
    def __init__(self, scene: Scene):
        self.scene = scene

    def animate_swap(self, cell_a: VGroup, cell_b: VGroup):
        """
        Swap the TEXT content between two cells with a smooth arc animation.
        The boxes stay fixed — only the label mobjects move.
        """
        text_a = cell_a[1]
        text_b = cell_b[1]

        center_a = text_a.get_center()
        center_b = text_b.get_center()

        # arc peak above both cells
        mid_y = max(center_a[1], center_b[1]) + 0.7

        # 1. lift both texts upward
        self.scene.play(
            text_a.animate.move_to([center_a[0], mid_y, 0]),
            text_b.animate.move_to([center_b[0], mid_y, 0]),
            run_time=0.25,
            rate_func=smooth,
        )

        # 2. cross-slide at the same height
        self.scene.play(
            text_a.animate.move_to([center_b[0], mid_y, 0]),
            text_b.animate.move_to([center_a[0], mid_y, 0]),
            run_time=0.45,
            rate_func=smooth,
        )

        # 3. settle into the opposite cells
        self.scene.play(
            text_a.animate.move_to(center_b),
            text_b.animate.move_to(center_a),
            run_time=0.25,
            rate_func=smooth,
        )
