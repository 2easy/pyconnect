import curses_wrapper as cs_wrap
cs = cs_wrap.CursesWrapper()
import locale
from client import UserClient
from windows import Menu

def prompt_for(target,obfuscate,panels):
    prompt = panels['prompt'].userptr()
    # display prompt
    panels['prompt'].top()
    panels['prompt'].show()
    cs_wrap.curses.panel.update_panels()
    prompt.user_for(target,obfuscate)
    result = prompt.content
    # hide prompt window
    panels['prompt'].below().top()
    panels['prompt'].hide()
    cs_wrap.curses.panel.update_panels()
    return result
def notify_about(title,message,panels):
    note = panels['note'].userptr()
    scr = panels['scr'].userptr()
    # display notification
    panels['note'].top()
    panels['note'].show()
    note.update_contents(title,message)
    cs_wrap.curses.panel.update_panels()
    cs_wrap.curses.doupdate()
    scr.getch()
    # hide notification window
    panels['note'].below().top()
    panels['note'].hide()
    cs_wrap.curses.panel.update_panels()
def get_decision(menu_p):
    menu = menu_p.userptr()
    menu_p.top()
    menu_p.show()
    menu.display()
    # get answer
    while True:
        key = menu.win.getch()
        if   key == cs_wrap.curses.KEY_UP:   menu.prev_opt()
        elif key == cs_wrap.curses.KEY_DOWN: menu.next_opt()
        elif key == cs_wrap.curses.KEY_ESCAPE: return
        elif key == cs_wrap.curses.KEY_ENTER: break
        cs_wrap.curses.panel.update_panels()
        cs_wrap.curses.doupdate()
    # hide bool menu
    menu_p.below().top()
    menu_p.hide()
    cs_wrap.curses.panel.update_panels()
    # get result and reset menu
    opt_id = menu.curr_opt
    menu.curr_opt = 0
    return opt_id

def login(panels):
    scr = panels['scr'].userptr()
    bool_menu = panels['bool_menu'].userptr()
    prompt = panels['prompt'].userptr()
    note = panels['note'].userptr()
    # create login menu
    # contents must be dynamically created because of adding users
    user_list = UserClient.fetch_all()
    user_list.append((locale.Account.new,None,''))
    options = []
    for usr in user_list:
        options.append(usr[0])
    max_y,max_x = scr.getmaxyx()
    login_menu = Menu(max_y,max_x,options)
    panels['login_menu'] = cs_wrap.curses.panel.new_panel(login_menu.win)
    panels['login_menu'].set_userptr(login_menu)
    # display login menu
    panels['menu'].hide()
    opt_id = get_decision(panels['login_menu'])
    user_alias,user_id,user_password = user_list[opt_id]
    new_account = False
    # get credentials if necessary
    if user_alias == locale.Account.new:
        user_alias = prompt_for(locale.Login.alias,False,panels)
        new_account = True
    if not user_id:
        user_id = prompt_for(locale.Login.user_id,False,panels)
    if user_password == '':
        user_password = prompt_for(locale.Login.password,True,panels)
    # create User object
    try:
        cli = UserClient(user_password,user_id,user_alias)
    except ValueError:
        notify_about(locale.Login.error,locale.Login.wrong_uid,panels)
        # show main menu and exit
        panels['menu'].show()
        cs_wrap.curses.panel.update_panels()
        return
    # login user
    if cli.login():
        notify_about(locale.Login.success,locale.Login.succ_msg,panels)
    else:
        notify_about(locale.Login.failure,locale.Login.failed_msg,panels)
        panels['menu'].show()
        cs_wrap.curses.panel.update_panels()
        return
    # save account to local database?
    if new_account:
        bool_menu.label = locale.Account.q_save
        save = get_decision(panels['bool_menu'])
        # save if wanted
        if save:
            bool_menu.label = locale.Account.q_remember_pass
            remember_pass = get_decision(panels['bool_menu'])
            if remember_pass:
                cli.save_to_db(True)
            else:
                cli.save_to_db(False)
    # show menu for logged users
    panels['m_logged'].top()
    panels['m_logged'].show()
    cs_wrap.curses.panel.update_panels()

def create_user(panels):
    scr    = panels['scr'].userptr()
    prompt = panels['prompt'].userptr()
    note   = panels['note'].userptr()
    # prompt user for alias
    user_alias = prompt_for(locale.Login.alias,False,panels)
    # prompt user for password
    user_password = prompt_for(locale.Login.password,True,panels)
    try:
        cli = UserClient(user_password,0,user_alias)
    except ValueError:
        notify_about(locale.Login.error,locale.Login.wrong_uid,panels)
        # show main menu and exit
        panels['menu'].show()
        cs_wrap.curses.panel.update_panels()
        return

    if cli.request_server_create() and cli.save_to_db(False):
        succ_msg = locale.Account.your_acc_id_is +" "+ str(cli.usr_id)
        notify_about(locale.General.success,succ_msg,panels)
    else:
        notify_about(locale.Rgst.failure,locale.Rgst.failed,panels)

    panels['menu'].show()
    cs_wrap.curses.panel.update_panels()
