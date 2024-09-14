"""
abstract class for all screen related primitives
"""


class AScreen:
    """
    abstract class for all screen related primitives
    """

    def __init__(
        self,
        width: int,
        height: int,
        font_height: int,
        padding: int = 1,
        gap: int = 1,
        marker_width: int = 2,
        orientation: int = 0,
    ):
        """
        init
        """
        self.width = width
        self.height = height
        self.orientation = orientation
        if orientation==0 or orientation ==2:
            self.actual_width=width
            self.actual_height=height
        else:
            self.actual_width=height
            self.actual_height=width
        self.font_height = font_height
        self.padding = padding
        self.gap = gap
        self.marker_width = marker_width
        # calculate some constants
        self.row_height = self.font_height + self.padding + self.gap
        self.frame_x_offset = self.marker_width + 2 * self.gap
        self.text_x_offset = self.frame_x_offset + self.padding

    def nr_of_rows(self):
        """
        calculates the number of awailable menu rows
        """
        y=self.actual_height
        # first we remove two markers at the top and buttom
        y -= 2 * (self.marker_width + 2 * self.gap)
        total_nr_of_rows = y // self.row_height
        return total_nr_of_rows - 1  # without header

    def text_start(self, row: int):
        """
        calculates the start coordinates for a text of a given row
        """
        if row == 0:  # header
            y = self.padding + self.font_height
        else:
            y = (
                self.padding
                + self.font_height
                + row * self.row_height
                + self.marker_width
                + self.gap
            )
        return self.text_x_offset, y

    def frame_coords(self, row: int):
        """
        calculates the start coordinates for a text of a given row
        """
        if row == 0:  # header
            y1 = 2 * self.padding + self.font_height - self.marker_width
            y2 = 0
        else:
            y1 = (
                # 2 * self.padding
                self.padding
                + self.font_height
                + row * self.row_height
                + self.marker_width
                - self.gap
            )
            y2 = y1 - self.row_height + self.gap
        return self.frame_x_offset, y1, self.actual_width, y2

    def marker_area(self, right_side: bool):
        x1 = 0
        y1 = (
            # 2 * self.padding
            self.padding
            + self.font_height
            + self.nr_of_rows() * self.row_height
            + self.marker_width
            - self.gap
        )
        x2 = self.gap + self.marker_width
        y2 = 0
        if right_side:
            x1 += self.actual_width - self.marker_width - self.gap
            x2 += self.actual_width - self.marker_width - self.gap
        return x1, y1, x2, y2

    def marker_coords(self, right_side: bool, row: int):
        """
        calculates the marker coordinates for a text of a given row
        """
        x1=0
        x2=self.marker_width
        if row == 0:  # header
            y1 = 2 * self.padding + self.font_height - self.marker_width
            y2 = 0
        else:
            y1 = (
                # 2 * self.padding
                self.padding
                + self.font_height
                + row * self.row_height
                + self.marker_width
                - self.gap
            )
            y2 = y1 - self.row_height + self.gap
        if right_side:
            x1 += self.actual_width - self.marker_width +1
            x2 += self.actual_width - self.marker_width
        return x1, y1, x2, y2

    def marker_up_down_coords(self, down: bool):
        """
        calculates the marker coordinates for the up or down marker
        """
        x1 = self.marker_width + self.gap + 1
        x2 = self.actual_width
        x2 -= self.marker_width - self.gap +2
        y1 = (
            # 2 * self.padding
            self.padding
            + self.font_height
            + self.gap
        )
        if down:
            y1 += self.nr_of_rows() * self.row_height + self.marker_width - 1
        y2 = y1 + self.marker_width - 2
        return x1, y1, x2, y2
