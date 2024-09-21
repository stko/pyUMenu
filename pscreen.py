"""
python class for all screen related primitives in TKinter
"""

import graphics as gr
try:                        # In order to be able to import tkinter for
    import tkinter.font as tkf # either in python 2 or in python 3
except ImportError:
    import tkFont as tkf

from ascreen import AScreen

class Screen(AScreen):
    """
    provides all graphics primitives and other informations to

    colors see https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
    """
    FONT_SIZE=8
    BACKGROUND="thistle3"
    TITLE_BG="cornflower blue"
    TITLE_COLOR="white"
    TEXT_BG="chartreuse2"
    TEXT_COLOR="black"
    VALUE_COLOR="blue"
    FONT_NAME="arial"
    FONT_SIZE=16
    FONT_WEIGHT="normal"
    MARKER_BACK="blue2"
    MARKER_SELECT="red2"
    MARKER_UP="green3"
    MARKER_DOWN="yellow2"
    MARKER_INACTIVE="grey"

    def __init__(self, title:str,width: int, height: int, padding: int=1, gap: int=1, marker_width: int = 2,orientation: int = 0):
        self.win = gr.GraphWin(title, width, height)
        self._mouseCallback = None
        self.win.setBackground(self.BACKGROUND)
        self.win.setMouseHandler(self.mouseHandler)
        # https://www.tutorialspoint.com/measure-the-height-of-a-string-in-tkinter-python
        # create a font object 
        self.font = tkf.Font(family=self.FONT_NAME, size=self.FONT_SIZE, weight=self.FONT_WEIGHT)
        # measure the dimensions
        ascent = self.font.metrics("ascent")
        self.descent = self.font.metrics("descent")
        linespace=self.font.metrics("linespace")
        self.font_height=ascent+self.descent

        super().__init__(width, height, self.font_height, padding, gap, marker_width, orientation)


    def text(self, row:int, title:str, value:str, style:str="arial",percent:int=0):
        if row>self.nr_of_rows:
            return
        x1,y1,x2,y2=self.frame_coords(row)
        bar = gr.Rectangle(gr.Point(x1, y1), gr.Point(x2, y2))
        if row==0:
            bar.setFill(self.TITLE_BG)
        else:
            bar.setFill(self.TEXT_BG)
        bar.setWidth(0)
        bar.draw(self.win)
        x,y=self.text_start(row)
        output=[title, value] # beeing lazy and write the whole textformating just once...
        for i in range(2):
            content=output[i]
            if i==0:
                text=gr.Text(gr.Point(x, y- self.descent), content)
                color=self.TEXT_COLOR
            else:
                text=gr.Text(gr.Point(self.actual_width -self.marker_width -self.gap -self.padding, y- self.descent), content)
                text.setOrientation("se")
                color=self.VALUE_COLOR
            if row==0:
                text.setFill(self.TITLE_COLOR)
            else:
                text.setFill(color)
            text.setFace(self.FONT_NAME)
            text.setSize(self.FONT_SIZE)
            text.setStyle(self.FONT_WEIGHT)
            text.draw(self.win)

    def markers(self, back: int, select: int, up: bool, down: bool,select_active):
        """
        paint all markers in one go
        """
        x1,y1,x2,y2=self.marker_area(False)
        bar = gr.Rectangle(gr.Point(x1, y1), gr.Point(x2, y2))
        bar.setFill(self.BACKGROUND)
        bar.setWidth(0)
        bar.draw(self.win)        
        x1,y1,x2,y2=self.marker_area(True)
        bar = gr.Rectangle(gr.Point(x1, y1), gr.Point(x2, y2))
        bar.setFill(self.BACKGROUND)
        bar.setWidth(0)
        bar.draw(self.win)        
        if back > -1 and back <= self.nr_of_rows:
            x1,y1,x2,y2=self.marker_coords(False, back)
            bar = gr.Rectangle(gr.Point(x1, y1), gr.Point(x2, y2))
            bar.setFill(self.MARKER_BACK)
            bar.setWidth(0)
            bar.draw(self.win) 
        if select > -1 and select <= self.nr_of_rows:
            x1,y1,x2,y2=self.marker_coords(True, select)
            bar = gr.Rectangle(gr.Point(x1, y1), gr.Point(x2, y2))
            if select_active:
                bar.setFill(self.MARKER_SELECT)
            else:
                bar.setFill(self.MARKER_INACTIVE)
            bar.setWidth(0)
            bar.draw(self.win) 
        x1,y1,x2,y2=self.marker_up_down_coords(False)
        bar = gr.Rectangle(gr.Point(x1, y1), gr.Point(x2, y2))
        if up:
            bar.setFill(self.MARKER_UP)
        else:
            bar.setFill(self.BACKGROUND)
        bar.setWidth(0)
        bar.draw(self.win) 
        x1,y1,x2,y2=self.marker_up_down_coords(True)
        bar = gr.Rectangle(gr.Point(x1, y1), gr.Point(x2, y2))
        if down:
            bar.setFill(self.MARKER_DOWN)
        else:
            bar.setFill(self.BACKGROUND)
        bar.setWidth(0)
        bar.draw(self.win) 
    def close(self):
        self.win.close()


    def setMouseHandler(self, func):
        self._mouseCallback = func

    def mouseHandler(self, point):
        print(point.x,point.y)
        if self._mouseCallback:
            self._mouseCallback(point.x, point.y)