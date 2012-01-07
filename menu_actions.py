import curses
import locale

def login(panels):
    scr = panels["scr"].userptr()
    prompt = panels["prompt"].userptr()
    note = panels["note"].userptr()

    panels["prompt"].top()
    panels["prompt"].show()
    curses.panel.update_panels()
    prompt.user_for("User ID",False)
    try:
        usr_id = int(prompt.content)
    except:
        note.update_contents("Wrong User ID",locale.Login.invalid_uid)
        panels["note"].top()
        panels["note"].show()
        curses.panel.update_panels()
        curses.doupdate()
        scr.getch()

        panels["note"].hide()
        panels["menu"].top()
        curses.panel.update_panels()
        scr.refresh()
        curses.doupdate()
        return
    prompt.user_for("Password",True)
    usr_pass = prompt.content
    panels["prompt"].hide()
    cli = UserClient(usr_pass,usr_id)
    if cli.login():
        note.update_contents("Success!",locale.Login.succ)
    else:
        note.update_contents("Login failed",locale.Login.failed)
    panels["note"].top()
    panels["note"].show()
    curses.panel.update_panels()
    curses.doupdate()
    scr.getch()

    panels["note"].hide()
    panels["menu"].top()
    curses.panel.update_panels()
