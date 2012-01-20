import curses_wrapper as cs_wrap
cs = cs_wrap.CursesWrapper()
import menu_actions

class CursesStdIO:
    def fileno(self):
        return 0
    def doRead(self):
        """Called when input is ready"""
    def logPrefix(self): return 'Curses Client'

class Screen(CursesStdIO):
    def __init__(self, scr, panels):
        self.scr = scr
        self.panels = panels
        # curses initialization
        self.scr.nodelay(1)
        cs_wrap.curses.cbreak()
        self.scr.keypad(1)
        cs_wrap.curses.curs_set(0)

        self.max_y,self.max_x = self.scr.getmaxyx()
    def connectionLost(self,reason):
        self.close()
    def close(self):
        cs_wrap.curses.nocbreak()
        self.scr.keypad(0)
        cs_wrap.curses.echo()
        cs_wrap.curses.endwin()
    def doRead(self):
        cs_wrap.curses.noecho()

        opt_id = menu_actions.get_decision(self.panels['menu'])

        if   opt_id == 0: menu_actions.login(self.panels)
        elif opt_id == 1: menu_actions.create_user(self.panels)
        elif opt_id == 2: self.close()
