#!/usr/bin/env python
import curses
import curses.panel
import curses.textpad

curses.KEY_ENTER = 10
curses.KEY_ESCAPE = 27
from menu import Menu,Prompt,Notification

import msg

from client import UserClient

def main(scr):
    # Init curses
    #scr = curses.initscr()
    #scr.keypad(1)

    #curses.cbreak()
    #curses.noecho()
    curses.curs_set(0) #turn off the cursor

    max_y,max_x = scr.getmaxyx()

    #scr.addstr(0,0,str(max_x)+" "+str(max_y))
    m = Menu(max_y,max_x,["1. "+msg.Menu.login,
                          "2. "+msg.Menu.add_user,
                          "3. "+msg.Menu.create_user,
                          "4. "+msg.Menu.exit])
    prompt = Prompt(max_y,max_x)
    note   = Notification(max_y,max_x)
    ################################################3
    #tmp_win = curses.newwin(5, 60, 5, 10)
    #tb = curses.textpad.Textbox(tmp_win)
    #text = tb.edit()
    #curses.beep()
    #scr.addstr(1,1,text.encode('utf_8'))
    #scr.addstr(0,0,str(dir(entry)))
    ################################################
    p = []
    p.append(curses.panel.new_panel(scr))
    p.append(curses.panel.new_panel(prompt.win))
    p.append(curses.panel.new_panel(note.win))
    p.append(curses.panel.new_panel(m.win))
    # hide prompt and notification windows
    p[1].hide()
    p[2].hide()
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
            if p[3].hidden():
                p[3].show()
                curses.noecho()
                curses.curs_set(0)
            else:
                p[3].hide()
                curses.echo()
                curses.curs_set(1)
            curses.panel.update_panels()
        elif key == curses.KEY_ENTER:
            #scr.addstr(2,0,str(m.curr_opt))
            if m.curr_opt == 0: pass
            elif m.curr_opt == 1:
                p[1].top()
                p[1].show()
                curses.panel.update_panels()
                prompt.user_for("User ID",False)
                p[1].hide()
                curses.panel.update_panels()

                cli = UserClient("",int(prompt.content))
                cli.save_to_db()
                succ_msg = "Your account ID is: " + str(cli.usr_id)
                note.update_contents("Success!", succ_msg)
                p[2].top()
                p[2].show()
                curses.panel.update_panels()
                curses.doupdate()
                scr.getch()

                p[2].hide()
                p[3].top()
                curses.panel.update_panels()

            elif m.curr_opt == 2:
                # prompt user for password
                p[1].top()
                p[1].show()
                curses.panel.update_panels()
                prompt.user_for("Password",True)
                p[1].hide()
                curses.panel.update_panels()

                cli = UserClient(prompt.content)
                if cli.request_server_create():
                    cli.save_to_db()
                succ_msg = "Your account ID is: " + str(cli.usr_id)
                note.update_contents("Success!", succ_msg)
                p[2].top()
                p[2].show()
                curses.panel.update_panels()
                curses.doupdate()
                scr.getch()

                p[2].hide()
                p[3].top()
                curses.panel.update_panels()
            elif m.curr_opt == 3: break
        curses.doupdate()

curses.wrapper(main)
