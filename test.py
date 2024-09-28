from pyuimenu import UIMenu, Menu, Item

import random

uimenu = UIMenu(width=480, height=320,font_size=20)


def submenu(row, data=None):
    menu = Menu()
    menu.add_item(Item("submenu", ""))
    menu.add_item(Item("subitem", "1"))
    menu.add_item(Item("another", "2"))
    uimenu.add(menu)


def slider(item, direction, data):
    if direction == "up":
        data[0] += 10
    else:
        data[0] -= 10
    data[0] = item.set_percentage(data[0])


def loop():
    """
    this is the loop which is called whenever the UI is in idle

    do your stuff here and return asap
    """
    pass #print("loop")


def main():

    slider_value = [0]
    menu = Menu()
    menu.add_item(Item("Simulation", ""))
    menu.add_item(Item("Temperatur", "27°"))
    menu.add_item(Item("Pressure", "3.4 bar"))
    menu.add_item(Item("Submenu", "-", callback=submenu))
    menu.add_item(Item("Torque", "34 Nm"))
    menu.add_item(Item("Level", "12"))
    menu.add_item(Item("Speed", "17 km/h"))
    menu.add_item(Item("Weight", "88 kg"))
    menu.add_item(Item("Brightness", "70%"))

    percentage_control = Item("Percentage", 0)
    # make an item with to a percentage bar by set an percentage
    percentage_control.set_percentage(0)
    menu.add_item(percentage_control)

    # make an item with to a percentage bar by set an percentage
    # and add a callback, which makes it a slider
    slider_control = Item("slider", slider_value[0], callback=slider, data=slider_value)
    slider_control.set_percentage(0)
    menu.add_item(slider_control)

    uimenu.add(menu)
    uimenu.start(loop)

main()
