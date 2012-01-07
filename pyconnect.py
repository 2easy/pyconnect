#!/usr/bin/env python
import curses, curses.panel

curses.KEY_ENTER = 10
curses.KEY_ESCAPE = 27
from windows import Menu,Prompt,Notification
import menu_actions

import locale

from client import UserClient

def main(scr):
    curses.curs_set(0) #turn off the cursor

    max_y,max_x = scr.getmaxyx()

    #scr.addstr(0,0,str(max_x)+" "+str(max_y))
    m = Menu(max_y,max_x,["1. "+locale.Menu.login,
                          "2. "+locale.Menu.add_user,
                          "3. "+locale.Menu.create_user,
                          "4. "+locale.Menu.exit])
    m_logged = Menu(max_y,max_x,["1. "+locale.Menu.send_msg,
                                 "2. "+locale.Menu.add_buddy,
                                 "3. "+locale.Menu.remove_buddy,
                                 "4. "+locale.Menu.logout,
                                 "5. "+locale.Menu.exit])
    prompt = Prompt(max_y,max_x)
    note   = Notification(max_y,max_x)
    ################################################
    #tmp_win = curses.newwin(5, 60, 5, 10)
    #tb = curses.textpad.Textbox(tmp_win)
    #text = tb.edit()
    #curses.beep()
    #scr.addstr(1,1,text.encode('utf_8'))
    #scr.addstr(0,0,str(dir(entry)))
    ################################################
    scr_p = curses.panel.new_panel(scr)
    prompt_p = curses.panel.new_panel(prompt.win)
    note_p = curses.panel.new_panel(note.win)
    m_logged_p = curses.panel.new_panel(m_logged.win)
    menu_p = curses.panel.new_panel(m.win)
    panels = dict([('scr',scr_p),('prompt',prompt_p),('note',note_p),
                   ('menu',menu_p),('m_logged', m_logged_p)])
    panels["scr"].set_userptr(scr)
    panels["prompt"].set_userptr(prompt)
    panels["note"].set_userptr(note)
    panels["m_logged"].set_userptr(m_logged)
    # hide prompt and notification windows
    prompt_p.hide()
    note_p.hide()
    m_logged_p.hide()
    curses.panel.update_panels()
    scr.refresh()
    m.display()
    key = None
    while True:
        key = scr.getch()
        #scr.addstr(1,0,str("ble"))
        #scr.addstr(2,0,str(key))
        if   key == curses.KEY_UP:   m.prev_opt()
        elif key == curses.KEY_DOWN: m.next_opt()
        elif key == curses.KEY_ESCAPE:
            if panels['menu'].hidden():
                panels['menu'].show()
                curses.noecho()
                curses.curs_set(0)
            else:
                panels['menu'].hide()
                curses.echo()
                curses.curs_set(1)
            curses.panel.update_panels()
        elif key == curses.KEY_ENTER:
            #scr.addstr(2,0,str(m.curr_opt))
            if m.curr_opt == 0:
                menu_actions.login(panels)
            elif m.curr_opt == 1:
                menu_actions.add_user(panels)
            elif m.curr_opt == 2:
                menu_actions.create_user(panels)
            elif m.curr_opt == 3: break
        curses.doupdate()

# Main loop in curses wrapper
curses.wrapper(main)
