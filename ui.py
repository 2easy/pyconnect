#!/usr/bin/env python
import curses
import curses.panel

curses.KEY_ENTER = 10
from menu import Menu

try:
    scr = curses.initscr()
    curses.cbreak()
    curses.noecho()

    scr.keypad(1)
    max_y,max_x = scr.getmaxyx()

    #scr.addstr(0,0,str(max_x)+" "+str(max_y))

    m = Menu(max_x,max_y,["1. Create new account", "2. Exit"])
    scr.refresh()
    m.display()
    key = None
    while True:
        key = scr.getch()
        #scr.addstr(1,0,str(curses.KEY_UP))
        #scr.addstr(2,0,str(key))

        if key == curses.KEY_UP: m.next_opt()
        elif key == curses.KEY_DOWN: m.prev_opt()
        elif key == curses.KEY_ENTER: break
        m.display()

finally:
    curses.endwin()
