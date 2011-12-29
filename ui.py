#!/usr/bin/env python
import curses
import curses.panel

curses.KEY_ENTER = 10
from menu import Menu

try:
    # Init curses
    scr = curses.initscr()
    scr.keypad(1)

    curses.cbreak()
    curses.noecho()
    curses.curs_set(0) #turn off the cursor

    max_y,max_x = scr.getmaxyx()

    #scr.addstr(0,0,str(max_x)+" "+str(max_y))
    m = Menu(max_x,max_y,["1. Login",
                          "2. Create account (locally)",
                          "3. Create account (on server)",
                          "4. Exit"])
    scr.refresh()
    m.display()
    key = None
    while True:
        key = scr.getch()
        #scr.addstr(1,0,str(curses.KEY_UP))
        #scr.addstr(2,0,str(key))

        if key == curses.KEY_UP: m.prev_opt()
        elif key == curses.KEY_DOWN: m.next_opt()
        elif key == curses.KEY_ENTER: break
        m.display()

finally:
    curses.endwin()
