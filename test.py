# futval_graph . py
from graphics import *
from pscreen import Screen

def main():

    # Create a graphics window with labels on left edge
    screen = Screen(" pyUIMenu Test ", 320, 240,padding=10, gap=1,marker_width=10)
    screen.text("Simulation",0)
    screen.text("Temperatur",1)
    screen.text("Pressure",2)
    screen.text("Torque",3)
    screen.text("Level",4)
    screen.text("Speed",5)
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
