import graphics as gr
try:                        # In order to be able to import tkinter for
    import tkinter.font as tkf # either in python 2 or in python 3
except ImportError:
    import tkFont as tkf

from ascreen import AScreen

class Screen(AScreen):
    """
    provides all graphics primitives and other informations to
    """
    FONT_SIZE=8
    BACKGROUND="yellow"
    TITLE_BG="blue"
    TITLE_COLOR="white"
    TEXT_BG="grey"
    TEXT_COLOR="black"
    FONT_NAME="arial"
    FONT_SIZE=16
    FONT_WEIGHT="normal"

    def __init__(self, title:str,width: int, height: int, padding: int=1, gap: int=1, marker_width: int = 2,orientation: int = 0):
        self.win = gr.GraphWin(title, width, height)
        self.win.setBackground(self.BACKGROUND)

        # https://www.tutorialspoint.com/measure-the-height-of-a-string-in-tkinter-python
        # create a font object 
        self.font = tkf.Font(family=self.FONT_NAME, size=self.FONT_SIZE, weight=self.FONT_WEIGHT)
        # measure the dimensions
        ascent = self.font.metrics("ascent")
        self.descent = self.font.metrics("descent")
        linespace=self.font.metrics("linespace")
        self.font_height=ascent+self.descent

        super().__init__(width, height, self.font_height, padding, gap, marker_width, orientation)


    def text(self, title:str, row:int, style:str="arial",percent:int=0):
        x1,y1,x2,y2=self.frame_coords(row)
        bar = gr.Rectangle(gr.Point(x1, y1), gr.Point(x2, y2))
        if row==0:
            bar.setFill(self.TITLE_BG)
        else:
            bar.setFill(self.TEXT_BG)
        bar.setWidth(0)
        bar.draw(self.win)
        x,y=self.text_start(row)
        text=gr.Text(gr.Point(x, y- self.descent), title)
        if row==0:
            text.setFill(self.TITLE_COLOR)
        else:
            text.setFill(self.TEXT_COLOR)
        text.setFace(self.FONT_NAME)
        text.setSize(self.FONT_SIZE)
        text.setStyle(self.FONT_WEIGHT)
        text.draw(self.win)

    def close(self):
        self.win.close()