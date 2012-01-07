import curses
import locale
from client import UserClient

def login(panels):
    scr = panels['scr'].userptr()
    prompt = panels['prompt'].userptr()
    note = panels['note'].userptr()

    panels['prompt'].top()
    panels['prompt'].show()
    curses.panel.update_panels()
    prompt.user_for('User ID',False)
    try:
        usr_id = int(prompt.content)
    except:
        note.update_contents('Wrong User ID',locale.Login.invalid_uid)
        panels['note'].top()
        panels['note'].show()
        curses.panel.update_panels()
        curses.doupdate()
        scr.getch()

        panels['note'].hide()
        panels['menu'].top()
        curses.panel.update_panels()
        scr.refresh()
        curses.doupdate()
        return
    prompt.user_for('Password',True)
    usr_pass = prompt.content
    panels['prompt'].hide()
    cli = UserClient(usr_pass,usr_id)
    if cli.login():
        note.update_contents('Success!',locale.Login.succ)
    else:
        note.update_contents('Login failed',locale.Login.failed)
    panels['note'].top()
    panels['note'].show()
    curses.panel.update_panels()
    curses.doupdate()
    scr.getch()

    panels['note'].hide()
    panels['menu'].top()
    curses.panel.update_panels()
def add_user(panels):
    scr = panels['scr'].userptr()
    prompt = panels['prompt'].userptr()
    note = panels['note'].userptr()

    panels['prompt'].top()
    panels['prompt'].show()
    curses.panel.update_panels()
    prompt.user_for('User ID',False)
    panels['prompt'].hide()
    curses.panel.update_panels()
    # TODO validate num
    cli = UserClient('',int(prompt.content))
    cli.save_to_db()
    succ_msg = 'Your account ID is: ' + str(cli.usr_id)
    note.update_contents('Success!', succ_msg)
    panels['note'].top()
    panels['note'].show()
    curses.panel.update_panels()
    curses.doupdate()
    scr.getch()

    panels['note'].hide()
    panels['menu'].top()
    curses.panel.update_panels()
def create_user(panels):
    scr = panels['scr'].userptr()
    prompt = panels['prompt'].userptr()
    note = panels['note'].userptr()
    # prompt user for password
    panels['prompt'].top()
    panels['prompt'].show()
    curses.panel.update_panels()
    prompt.user_for('Password',True)
    panels['prompt'].hide()
    curses.panel.update_panels()

    cli = UserClient(prompt.content)
    if cli.request_server_create():
        cli.save_to_db()
    succ_msg = 'Your account ID is: ' + str(cli.usr_id)
    note.update_contents('Success!', succ_msg)
    panels['note'].top()
    panels['note'].show()
    curses.panel.update_panels()
    curses.doupdate()
    scr.getch()

    panels['note'].hide()
    panels['menu'].top()
    curses.panel.update_panels()
