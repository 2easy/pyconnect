#!/usr/bin/env python
import curses
import curses.panel
import curses.textpad

curses.KEY_ENTER = 10
curses.KEY_ESCAPE = 27
from menu import Menu

def main(scr):
    # Init curses
    #scr = curses.initscr()
    #scr.keypad(1)

    #curses.cbreak()
    #curses.noecho()
    curses.curs_set(0) #turn off the cursor

    max_y,max_x = scr.getmaxyx()

    #scr.addstr(0,0,str(max_x)+" "+str(max_y))
    m = Menu(max_x,max_y,["1. Login",
                          "2. Create account (locally)",
                          "3. Create account (on server)",
                          "4. Exit"])
    ################################################3
    #tmp_win = curses.newwin(5, 60, 5, 10)
    #tb = curses.textpad.Textbox(tmp_win)
    #text = tb.edit()
    #curses.beep()
    #scr.addstr(1,1,text.encode('utf_8'))
    #scr.addstr(0,0,str(dir(entry)))
    ################################################
    p0 = curses.panel.new_panel(scr)
    p1 = curses.panel.new_panel(m.win)
    curses.panel.update_panels()
    scr.refresh()
    m.display()
    key = None
    while True:
        key = scr.getch()
        #scr.addstr(1,0,str(curses.KEY_UP))
        #scr.addstr(2,0,str(key))
        if   key == curses.KEY_UP:   m.prev_opt()
        elif key == curses.KEY_DOWN: m.next_opt()
        elif key == curses.KEY_ESCAPE:
            if p1.hidden():
                p1.show()
                curses.noecho()
                curses.curs_set(0)
            else:
                p1.hide()
                curses.echo()
                curses.curs_set(1)
            curses.panel.update_panels()
        elif key == curses.KEY_ENTER:
            scr.addstr(2,0,str(m.curr_opt))
            if m.curr_opt == 0: pass
            elif m.curr_opt == 1: pass
            elif m.curr_opt == 2: pass
            elif m.curr_opt == 3: break
        curses.doupdate()

curses.wrapper(main)
