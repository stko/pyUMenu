"""

pyuimenu - show device independed a menu and provides all routines for
nested menus and user selections via bottons, rotary know or touchscreen

"""

# from cpscreen import Screen # uncomment for circuitpython with displayio
from pscreen import Screen  # uncomment for python with tkinter


class Item:
    """
    single menu item
    """

    def __init__(
        self,
        title: str,
        value: str = "",
        callback=None,
        data=None,
    ):
        self.title = title
        self.value = value
        self.slider = False
        self.callback = callback
        self.data = data
        self.percentage = 0

    def set_percentage(self, percentage: int):
        """
        setting an items percentage makes that item to a slider
        """
        self.slider = True
        self.percentage

    def print(self, screen: Screen, row: int):
        screen.text(row, self.title, self.value, percent=self.percentage)


class Menu:
    def __init__(self):
        self.row = 0
        self.top = True
        self.screen = None
        self.rows = []

    def add_item(self, item: Item) -> int:
        """
        adds a new row to the module
        """
        self.rows.append(item)
        return len(self.rows) - 1

    def nr_of_items(self) -> int:
        return len(self.rows) - 1

    def print(self, screen: Screen, row: int, index: int):
        """
        prints item "index" in row "row" on screen
        """
        self.rows[index].print(screen, row)


class UIMenu:
    """

    UIMenu - show device independed a menu and provides all routines for
    nested menus and user selections via bottons, rotary know or touchscreen

    """

    # https://docs.circuitpython.org/projects/miniqr/en/1.3.4/examples.html

    def __init__(self):
        self.screen = Screen(
            " pyUIMenu Test ", 320, 240, padding=10, gap=1, marker_width=10
        )
        self.menus = []
        self.menu = None
        self.top_row = 1  # 0 is always the title
        self.cursor_row = 0
        self.slider_active = False

    def authenticate(self, title, abort_text, qrcode, wait_for_authorisation) -> bool:
        """
        a all in one (optional) login screen:
        title: screen header
        abort_text: text of the cancel button. If None, loops forever
        qrcode: the adafruit miniqr qrcode bit matrix
        wait_for_authorisation: callback function. If given, it is called each second to wait
            for authorisation. callback returns True, if authorized
        """
        pass

    def add(self, menu: Menu):
        menu.top = len(self.menus) == 0
        self.menus.append(menu)
        self.menu = menu

        # item 0 of the menu is always the header, so the real menu part starts at index 1
        self.top_row = 1
        self.cursor_row = 1

    def _show(self):
        total_rows = self.menu.nr_of_items()
        for screen_row in range(self.screen.nr_of_rows + 1):
            if screen_row == 0:
                self.menu.print(self.screen, screen_row, 0)
                continue
            print("halfful menus need to be tested!")
            if self.top_row + screen_row > total_rows:
                self.screen.text(screen_row, "", "")
                continue
            self.menu.print(self.screen, screen_row, self.top_row + screen_row - 1)
        self._set_markers()

    def _set_markers(self):
        total_rows = self.menu.nr_of_items()
        actual_item = self._get_actual_item()
        actual_screen_row = (
            self.cursor_row - self.top_row + 1
        )  # in which screen row we are?
        if self.slider_active:
            back_marker = actual_screen_row
        else:
            back_marker = 0
        top_marker_visible = self.top_row > 1
        bottom_marker_visible = self.top_row + self.screen.nr_of_rows < total_rows

        self.screen.markers(
            back_marker,
            actual_screen_row,
            top_marker_visible,
            bottom_marker_visible,
            False,
        )

    def _get_actual_item(self):
        return self.menu.rows[self.cursor_row]

    def _adjust_layout(self):
        """
        get called after a cursor position change to redraw the screen, if necessary
        """

        redraw_needed = False
        total_rows = self.menu.nr_of_items()
        if self.cursor_row < self.top_row:  # we moved out of the top
            if self.top_row > 1:  # we need to move the screen topwards
                redraw_needed = True
            self.top_row = self.cursor_row
            if self.top_row < 1:  # did we reached the first item?
                self.top_row = 1
            self.cursor_row = self.top_row
        elif (
            self.cursor_row > self.top_row + self.screen.nr_of_rows - 1
        ):  # we moved out of the bottom
            if (
                self.top_row + self.screen.nr_of_rows < total_rows
            ):  # we need to move the screen topwards
                redraw_needed = True
            self.top_row = self.cursor_row - self.screen.nr_of_rows + 1
            if (
                self.top_row > total_rows - self.screen.nr_of_rows
            ):  # did we reached the first item?
                self.top_row = total_rows - self.screen.nr_of_rows
            self.cursor_row = self.top_row + self.screen.nr_of_rows - 1
        if redraw_needed:
            self._show()
        else:
            self._set_markers()

    def move_cursor(self, step_width):
        self.cursor_row += step_width
        self._adjust_layout()
