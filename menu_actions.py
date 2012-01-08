import curses_wrapper as cs_wrap
import locale
from client import UserClient

def login(panels):
    scr = panels['scr'].userptr()
    prompt = panels['prompt'].userptr()
    note = panels['note'].userptr()

    panels['prompt'].top()
    panels['prompt'].show()
    cs_wrap.curses.panel.update_panels()
    prompt.user_for(locale.Login.user_id,False)
    try:
        usr_id = int(prompt.content)
    except:
        note.update_contents(locale.Login.wrong_uid,locale.Login.invalid_uid)
        panels['note'].top()
        panels['note'].show()
        cs_wrap.curses.panel.update_panels()
        cs_wrap.curses.doupdate()
        scr.getch()

        panels['note'].hide()
        panels['menu'].top()
        cs_wrap.curses.panel.update_panels()
        scr.refresh()
        cs_wrap.curses.doupdate()
        return
    prompt.user_for('Password',True)
    usr_pass = prompt.content
    panels['prompt'].hide()
    cli = UserClient(usr_pass,usr_id)
    if cli.login():
        note.update_contents(locale.Login.success,locale.Login.succ_msg)
    else:
        note.update_contents(failure,locale.Login.failed_msg)
    panels['note'].top()
    panels['note'].show()
    cs_wrap.curses.panel.update_panels()
    cs_wrap.curses.doupdate()
    scr.getch()

    panels['note'].hide()
    panels['menu'].top()
    cs_wrap.curses.panel.update_panels()

def add_user(panels):
    scr = panels['scr'].userptr()
    prompt = panels['prompt'].userptr()
    note = panels['note'].userptr()

    panels['prompt'].top()
    panels['prompt'].show()
    cs_wrap.curses.panel.update_panels()
    prompt.user_for(user_id,False)
    panels['prompt'].hide()
    cs_wrap.curses.panel.update_panels()
    # TODO validate num
    cli = UserClient('',int(prompt.content))
    if cli.save_to_db():
        succ_msg = locale.AddAcc.your_acc_id_is +" "+ str(cli.usr_id)
        note.update_contents(locale.AddAcc.success, succ_msg)
    else:
        note.update_contents(locale.AddAcc.failure, locale.AddAcc.db_error)
    panels['note'].top()
    panels['note'].show()
    cs_wrap.curses.panel.update_panels()
    cs_wrap.curses.doupdate()
    scr.getch()

    panels['note'].hide()
    panels['menu'].top()
    cs_wrap.curses.panel.update_panels()

def create_user(panels):
    scr = panels['scr'].userptr()
    prompt = panels['prompt'].userptr()
    note = panels['note'].userptr()
    # prompt user for password
    panels['prompt'].top()
    panels['prompt'].show()
    cs_wrap.curses.panel.update_panels()
    prompt.user_for('Password',True)
    panels['prompt'].hide()
    cs_wrap.curses.panel.update_panels()

    cli = UserClient(prompt.content)
    if cli.request_server_create() and cli.save_to_db():
        succ_msg = locale.AddAcc.your_acc_id_is +" "+ str(cli.usr_id)
        note.update_contents(locale.AddAcc.success, succ_msg)
    else:
        note.update_contents(locale.AddAcc.failure, locale.AddAcc.error)
    panels['note'].top()
    panels['note'].show()
    cs_wrap.curses.panel.update_panels()
    cs_wrap.curses.doupdate()
    scr.getch()

    panels['note'].hide()
    panels['menu'].top()
    cs_wrap.curses.panel.update_panels()
