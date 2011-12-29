#!/usr/bin/env python
import curses
import curses.panel

from menu import Menu

try:
    scr = curses.initscr()
    curses.cbreak()
    curses.noecho()

    scr.keypad(1)
    max_y,max_x = scr.getmaxyx()

    scr.addstr(0,0,str(max_x)+" "+str(max_y))

    m = Menu(max_x,max_y,["1. Create new account", "2. Exit"])
    scr.refresh()
    m.display()
    scr.getch()
finally:
    curses.endwin()
