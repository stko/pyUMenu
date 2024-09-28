"""
python class for all screen related primitives in TKinter
"""

import tkinter

try:  # In order to be able to import tkinter for
    import tkinter.font as tkf  # either in python 2 or in python 3
except ImportError:
    import tkFont as tkf

from ascreen import AScreen


class Screen(AScreen):
    """
    provides all graphics primitives and other informations to

    colors see https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
    """


    FONT_SIZE = 8
    BACKGROUND = "thistle3"
    TITLE_BG = "cornflower blue"
    TITLE_PERCENT = "blue2"
    TITLE_COLOR = "white"
    TEXT_BG = "chartreuse2"
    TEXT_PERCENT = "gold"
    TEXT_COLOR = "black"
    VALUE_COLOR = "blue"
    FONT_NAME = "arial"
    FONT_SIZE = 16
    FONT_WEIGHT = "normal"
    MARKER_BACK = "blue2"
    MARKER_SELECT = "red2"
    MARKER_UP = "green3"
    MARKER_DOWN = "yellow2"
    MARKER_INACTIVE = "grey"

    def __init__(
        self,
        title: str,
        width: int,
        height: int,
        padding: int = 1,
        gap: int = 1,
        marker_width: int = 2,
        orientation: int = 0,
        move_cursor = None,
        back=None,
        select=None,
        eval_mouse_move=None,
        font_size=FONT_SIZE

    ):
        ## the Tkinter specific stuff
        self.window = None
        self.canvas = None
        self.font = None
        self.font_size=font_size
        self.create_tk_window(title, width, height)
        self.window.protocol("WM_DELETE_WINDOW", self.quit)

        super().__init__(
            width, height, self.font_height, padding, gap, marker_width, orientation,move_cursor,back, select,eval_mouse_move
        )

    def quit(self):
        self.window.quit()

    def start(self, loop):
        """
        must be start after all the initial layout has been made
        to let the UI do their event handling

        """
        self.loop = loop
        self.tk_poll()
        self.window.mainloop()

    def tk_poll(self):
        ## https://stackoverflow.com/a/38817470
        self.window.update_idletasks()
        if self.loop:
            self.loop()
        self.window.after(1, self.tk_poll)

    def create_tk_window(self, title: str, width: int, height: int):
        """Opens a Tkinter window with a canvas"""
        self.window = tkinter.Tk()
        self.window.title(title)

        self.canvas = tkinter.Canvas(
            self.window, width=width, height=height, bg=self.BACKGROUND
        )
        self.canvas.pack()

        self.window.bind("<KeyPress>", self.onKeyPress)

        self.canvas.bind("<ButtonPress-1>", self.start_tk_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_tk_mouse_move)

        # https://www.tutorialspoint.com/measure-the-height-of-a-string-in-tkinter-python
        # create a font object
        self.font = tkf.Font(
            family=self.FONT_NAME, size=self.font_size, weight=self.FONT_WEIGHT
        )
        # measure the dimensions
        ascent = self.font.metrics("ascent")
        self.descent = self.font.metrics("descent")
        linespace = self.font.metrics("linespace")
        self.font_height = ascent + self.descent
        self.window.update()

    def start_tk_mouse_move(self, event):
        """transforms tk mouse event into x,y coords"""
        super().start_mouse_move(event.x, event.y)

    def stop_tk_mouse_move(self, event):
        """transforms tk mouse event into x,y coords"""
        if self.mouse_move:
            super().stop_mouse_move(event.x, event.y)

    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, color):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    def draw_text(
        self,
        text: str,
        x,
        y,
        color: str,
        font_name: str,
        font_size: int,
        font_weight: str,
        orientation="sw",
    ):
        self.canvas.create_text(
            x,
            y,
            text=text,
            fill=color,
            font=(f"{font_name} {font_size} {font_weight}"),
            anchor=orientation,
        )

    def refresh(self):
        self.window.update()

    def onKeyPress(self, event):
        if event.keysym=="Up" and self.move_cursor:
            self.move_cursor(-1)
        if event.keysym=="Down" and self.move_cursor:
            self.move_cursor(1)
        if event.keysym=="Left" and self.back:
            self.back()
        if event.keysym=="Right" and self.select:
            self.select()


    def text(self, row: int, title: str, value: str, percent: int = 0, refresh=False):
        if row > self.nr_of_rows:
            return
        x1, y1, x2, y2 = self.frame_coords(row)
        if percent:  # draw two bars
            x_middle = (x2 - x1) * percent // 100
            if row == 0:
                self.draw_rectangle(x1, y1, x_middle, y2, self.TITLE_PERCENT)
                self.draw_rectangle(x_middle, y1, x2, y2, self.TITLE_BG)

            else:
                self.draw_rectangle(x1, y1, x_middle, y2, self.TEXT_PERCENT)
                self.draw_rectangle(x_middle, y1, x2, y2, self.TEXT_BG)
        else:
            if row == 0:
                self.draw_rectangle(x1, y1, x2, y2, self.TITLE_BG)
            else:
                self.draw_rectangle(x1, y1, x2, y2, self.TEXT_BG)

        x, y = self.text_start(row)
        output = [
            title,
            value,
        ]  # beeing lazy and write the whole textformating just once...
        for i in range(2):
            content = output[i]
            if row == 0:
                color = self.TITLE_COLOR
            else:
                color = self.TEXT_COLOR
            if i == 0:
                self.draw_text(
                    content,
                    x,
                    y - self.descent,
                    color,
                    self.FONT_NAME,
                    self.FONT_SIZE,
                    self.FONT_WEIGHT,
                )
            else:
                self.draw_text(
                    content,
                    self.actual_width - self.marker_width - self.gap - self.padding,
                    y - self.descent,
                    self.VALUE_COLOR,
                    self.FONT_NAME,
                    self.FONT_SIZE,
                    self.FONT_WEIGHT,
                    orientation="se",
                )
        if refresh:
            self.refresh()

    def markers(
        self, back: int, select: int, up: bool, down: bool, select_active, refresh=False
    ):
        """
        paint all markers in one go
        """
        x1, y1, x2, y2 = self.marker_area(False)
        self.draw_rectangle(x1, y1, x2, y2, self.BACKGROUND)
        x1, y1, x2, y2 = self.marker_area(True)
        self.draw_rectangle(x1, y1, x2, y2, self.BACKGROUND)
        if back > -1 and back <= self.nr_of_rows:
            x1, y1, x2, y2 = self.marker_coords(False, back)
            self.draw_rectangle(x1, y1, x2, y2, self.MARKER_BACK)
        if select > -1 and select <= self.nr_of_rows:
            if select_active:
                color = self.MARKER_SELECT
            else:
                color = self.MARKER_INACTIVE

            x1, y1, x2, y2 = self.marker_coords(True, select)
            self.draw_rectangle(x1, y1, x2, y2, color)
        if up:
            color = self.MARKER_UP
        else:
            color = self.BACKGROUND

        x1, y1, x2, y2 = self.marker_up_down_coords(False)
        self.draw_rectangle(x1, y1, x2, y2, color)

        if down:
            color = self.MARKER_DOWN
        else:
            color = self.BACKGROUND

        x1, y1, x2, y2 = self.marker_up_down_coords(True)
        self.draw_rectangle(x1, y1, x2, y2, color)

        if refresh:
            self.refresh()

    def close(self):
        self.quit()
