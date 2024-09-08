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
        if self.orientation == 0 or self.orientation == 2:  ## actual rotation
            y = self.height
        else:
            y = self.width
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
        if self.orientation == 0 or self.orientation == 2:  ## actual rotation
            width = self.width
        else:
            width = self.height
        return self.frame_x_offset, y1, width, y2

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
            if self.orientation == 0 or self.orientation == 2:  ## actual rotation
                width = self.width
            else:
                width = self.height
            x1 += width - self.marker_width - self.gap
            x2 += width - self.marker_width - self.gap
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
            if self.orientation == 0 or self.orientation == 2:  ## actual rotation
                width = self.width
            else:
                width = self.height
            x1 += width - self.marker_width +1
            x2 += width - self.marker_width
        return x1, y1, x2, y2

    def marker_up_down_coords(self, down: bool):
        """
        calculates the marker coordinates for the up or down marker
        """
        x1 = self.marker_width + self.gap + 1
        if self.orientation == 0 or self.orientation == 2:  ## actual rotation
            x2 = self.width
        else:
            x2 = self.height
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
