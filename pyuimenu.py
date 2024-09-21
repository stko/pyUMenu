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
        self.top_row = 1
        self.cursor_row = 1


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
        self._show()


    def _show(self):
        total_rows = self.menu.nr_of_items()
        for screen_row in range(self.screen.nr_of_rows + 1):
            if screen_row == 0:
                self.menu.print(self.screen, screen_row, 0)
                continue
            if self.menu.top_row + screen_row - 1 > total_rows:
                self.screen.text(screen_row, "", "")
                continue
            self.menu.print(self.screen, screen_row, self.menu.top_row + screen_row - 1)
        self._set_markers()

    def _set_markers(self):
        total_rows = self.menu.nr_of_items()
        actual_item = self._get_actual_item()
        actual_screen_row = (
            self.menu.cursor_row - self.menu.top_row + 1
        )  # in which screen row we are?
        if actual_item.slider:
            back_marker = actual_screen_row
        else:
            back_marker = 0
        top_marker_visible = self.menu.top_row > 1
        is_selectable=actual_item.callback != None or actual_item.slider
        bottom_marker_visible = self.menu.top_row + self.screen.nr_of_rows <= total_rows

        self.screen.markers(
            back_marker,
            actual_screen_row,
            top_marker_visible,
            bottom_marker_visible,
            is_selectable,
        )

    def _get_actual_item(self):
        return self.menu.rows[self.menu.cursor_row]

    def _adjust_layout(self):
        """
        get called after a cursor position change to redraw the screen, if necessary
        """

        redraw_needed = False
        total_rows = self.menu.nr_of_items()
        if self.menu.cursor_row < self.menu.top_row:  # we moved out of the top
            if self.menu.top_row > 1:  # we need to move the screen topwards
                redraw_needed = True
            self.menu.top_row = self.menu.cursor_row
            if self.menu.top_row < 1:  # did we reached the first item?
                self.menu.top_row = 1
            self.menu.cursor_row = self.menu.top_row
        elif (
            self.menu.cursor_row > self.menu.top_row + total_rows - 1
        ):  # we are over the end of a short list
            self.menu.cursor_row = self.menu.top_row + total_rows - 1
        elif (
            self.menu.cursor_row > self.menu.top_row + self.screen.nr_of_rows - 1
        ):  # we moved out of the bottom
            if (
                self.menu.top_row + self.screen.nr_of_rows <= total_rows
            ):  # we need to move the screen topwards
                redraw_needed = True
            self.menu.top_row = self.menu.cursor_row - self.screen.nr_of_rows + 1
            if (
                self.menu.top_row > total_rows - self.screen.nr_of_rows
            ):  # did we reached the end of the 
                self.menu.top_row = total_rows - self.screen.nr_of_rows +1
            self.menu.cursor_row = self.menu.top_row + self.screen.nr_of_rows - 1
        if redraw_needed:
            self._show()
        else:
            self._set_markers()

    def move_cursor(self, step_width):
        self.menu.cursor_row += step_width
        self.slider_active=False # moving the cursor leaves the slider mode, if any
        self._adjust_layout()

    def select(self,is_rotary_encoder:bool=False):
        """
        do all action when a item is selected

        with rotary encoders it's a little bit difficulty, as they have only one knob
        for both menu selection and also slider changes, so we'll need
        the knob button to switch between these both modes


        """
        actual_item = self._get_actual_item()
        if actual_item.slider and not self.slider_active:
            self.slider_active=True
        if self.slider_active:
            if actual_item.callback:
                actual_item.callback(self.menu.cursor_row,"up") # send a "up" notification to the callback
                return
            return
        if actual_item.callback:
            actual_item.callback(self.menu.cursor_row) # calls the callback
        
    def back(self):
        """
        do all action when back is selected a item is selected
        """
        actual_item = self._get_actual_item()
        if self.slider_active:
            if not actual_item.slider: # reset slider state just in case it has not properly done before anyhow
                self.slider_active=False
            else:
                if actual_item.callback:
                    actual_item.callback(self.menu.cursor_row,"up") # send a "up" notification to the callback
                    return
            return
        if len(self.menus)>1: # we are not on the lowest level already..
            self.menus=self.menus[:-1]
            self.menu=self.menus[-1]
            self._show()
        