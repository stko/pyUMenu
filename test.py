# futval_graph . py
from graphics import *
from pscreen import Screen

def main():

    # Create a graphics window with labels on left edge
    screen = Screen(" pyUIMenu Test ", 320, 240,padding=10, gap=1,marker_width=10)
    screen.text("Title qg",0)
    screen.text("Item g 1",1)
    screen.text("Item q 2",2)
    screen.text("Item q 3",3)
    screen.text("Item q 4",4)
    screen.text("Item q 5",5)
    screen.text("Item q 6",0)
    screen.text("Item q 7",1)
    screen.text("Item q 8",2)
    screen.text("Item q 9",3)
    screen.text("Item q 10",4)
    screen.markers(0,2,True,True)

    """
    bar = Rectangle(Point(40, 230), Point(65, 230 - height))
    bar.setFill("green")
    bar.setWidth(2)
    bar.draw(win)
    # Draw bars for successive years
    for year in range(1, 11):
        # calculate value for the next year
        principal = principal * (1 + apr)
        # draw bar for this value
        xll = year * 25 + 40
        height = principal * 0.02
        bar = Rectangle(Point(xll, 230), Point(xll + 25, 230 - height))
        bar.setFill("green")
        bar.setWidth(2)
        bar.draw(win)
    """
    input("Press <Enter> to quit ")
    screen.close()


main()
