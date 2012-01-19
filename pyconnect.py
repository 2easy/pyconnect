#!/usr/bin/env python
import curses_wrapper as cs_wrap
cs = cs_wrap.CursesWrapper()
cs_wrap.curses.KEY_ENTER = 10
cs_wrap.curses.KEY_ESCAPE = 27
from windows import Menu,Prompt,Notification

from twisted.internet import reactor
import menu_actions
from screen import Screen

import locale

def main():
    max_y,max_x = cs.scr.getmaxyx()

    #scr.addstr(0,0,str(max_x)+" "+str(max_y))
    m = Menu(max_y,max_x,["1. "+locale.Menu.login,
                          "2. "+locale.Menu.create_user,
                          "3. "+locale.Menu.exit])
    m_logged = Menu(max_y,max_x,["1. "+locale.Menu.send_msg,
                                 "2. "+locale.Menu.add_buddy,
                                 "3. "+locale.Menu.remove_buddy,
                                 "4. "+locale.Menu.logout,
                                 "5. "+locale.Menu.exit])
    bool_menu = Menu(max_y,max_x,[locale.General.no,locale.General.yes],
                     locale.Account.q_save)
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
              'bool_menu': cs_wrap.curses.panel.new_panel(bool_menu.win),
              'note'     : cs_wrap.curses.panel.new_panel(note.win),
              'm_logged' : cs_wrap.curses.panel.new_panel(m_logged.win),
              'menu'     : cs_wrap.curses.panel.new_panel(m.win)
             }
    panels['scr'].set_userptr(cs.scr)
    panels['prompt'].set_userptr(prompt)
    panels['bool_menu'].set_userptr(bool_menu)
    panels['note'].set_userptr(note)
    panels['m_logged'].set_userptr(m_logged)
    panels['menu'].set_userptr(m)
    screen = Screen(cs.scr,panels)
    # hide prompt and notification windows
    panels['prompt'].hide()
    panels['bool_menu'].hide()
    panels['note'].hide()
    panels['m_logged'].hide()
    cs_wrap.curses.panel.update_panels()
    cs.scr.refresh()
    m.display()

    reactor.addReader(screen)
    reactor.run()
    screen.close()
# Main loop in curses wrapper
try:     main()
except BaseException, msg: print(msg)
finally: cs_wrap.curses.endwin()
