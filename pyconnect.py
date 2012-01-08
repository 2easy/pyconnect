#!/usr/bin/env python
import curses_wrapper as cs_wrap
cs = cs_wrap.CursesWrapper()

cs_wrap.curses.KEY_ENTER = 10
cs_wrap.curses.KEY_ESCAPE = 27
from windows import Menu,Prompt,Notification
import menu_actions

import locale

def main():
    cs_wrap.curses.curs_set(0) #turn off the cursor

    max_y,max_x = cs.scr.getmaxyx()

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
    panels = {'scr'      : cs_wrap.curses.panel.new_panel(cs.scr),
              'prompt'   : cs_wrap.curses.panel.new_panel(prompt.win),
              'note'     : cs_wrap.curses.panel.new_panel(note.win),
              'm_logged' : cs_wrap.curses.panel.new_panel(m_logged.win),
              'menu'     : cs_wrap.curses.panel.new_panel(m.win)
             }
    panels['scr'].set_userptr(cs.scr)
    panels['prompt'].set_userptr(prompt)
    panels['note'].set_userptr(note)
    panels['m_logged'].set_userptr(m_logged)
    panels['menu'].set_userptr(m)
    # hide prompt and notification windows
    panels['prompt'].hide()
    panels['note'].hide()
    panels['m_logged'].hide()
    cs_wrap.curses.panel.update_panels()
    cs.scr.refresh()
    m.display()
    key = None
    while True:
        key = cs.scr.getch()
        #scr.addstr(1,0,str("ble"))
        #scr.addstr(2,0,str(key))
        if   key == cs_wrap.curses.KEY_UP:   m.prev_opt()
        elif key == cs_wrap.curses.KEY_DOWN: m.next_opt()
        elif key == cs_wrap.curses.KEY_ESCAPE: pass
        elif key == cs_wrap.curses.KEY_ENTER:
            #scr.addstr(2,0,str(m.curr_opt))
            if m.curr_opt == 0:   menu_actions.login(panels)
            elif m.curr_opt == 1: menu_actions.add_user(panels)
            elif m.curr_opt == 2: menu_actions.create_user(panels)
            elif m.curr_opt == 3: break
        cs_wrap.curses.doupdate()
        cs.scr.refresh()

# Main loop in curses wrapper
try:
    cs_wrap.curses.cbreak()
    cs.scr.keypad(1)
    main()
except BaseException, msg:
    print(msg)
finally:
    cs_wrap.curses.endwin()
