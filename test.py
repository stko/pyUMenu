# futval_graph . py
from graphics import *
from pscreen import Screen
from pyuimenu import UIMenu, Menu, Item

from time import sleep

# If Windows getch() available, use that.  If not, use a
# Unix version.
try:
    import msvcrt
    getch = msvcrt.getch
except:
    import sys, tty, termios
    def _unix_getch():
        """Get a single character from stdin, Unix version"""

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())          # Raw read
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    getch = _unix_getch

uimenu=UIMenu()

def submenu(row):
    menu=Menu()
    menu.add_item(Item("submenu",""))
    menu.add_item(Item("subitem","1"))
    menu.add_item(Item("another","2"))
    uimenu.add(menu)

def main():


    menu=Menu()
    menu.add_item(Item("Simulation",""))
    menu.add_item(Item("Temperatur","27°"))
    menu.add_item(Item("Pressure","3.4 bar"))
    menu.add_item(Item("Submenu","-",callback=submenu))
    menu.add_item(Item("Torque","34 Nm"))
    menu.add_item(Item("Level","12"))
    menu.add_item(Item("Speed","17 km/h"))
    menu.add_item(Item("Weight","88 kg"))
    menu.add_item(Item("Brightness","70%"))
    menu.add_item(Item("Volume","half"))
    uimenu.add(menu)
    c="a"
    esc_sequence=""
    while c != "q":
        c=getch()
        #print(hex(ord(c)))
        esc_sequence+=c
        if len(esc_sequence)>3:
            esc_sequence=esc_sequence[1:4]
        if esc_sequence=="\x1b[D": # back
            uimenu.back()
        if esc_sequence=="\x1b[C": # select
            uimenu.select()
        if esc_sequence=="\x1b[A": # up
            uimenu.move_cursor(-1)
        if esc_sequence=="\x1b[B": # down
            uimenu.move_cursor(1)
    uimenu.screen.close()


main()
