import curses, curses.panel
curses.KEY_ENTER = 10
curses.KEY_ESCAPE = 27

class CursesWrapper():
    __shared_state = { 'scr' : curses.initscr() }
    def __init__(self):
        self.__dict__ = self.__shared_state
    def create_window(self,height,width,y,x):
        return curses.newwin(height,width,y,x)

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

        self.scr.nodelay(1)
        curses.cbreak()
        self.scr.keypad(1)
        curses.curs_set(0)

        self.max_y,self.max_x = self.scr.getmaxyx()
    def connectionLost(self,reason):
        self.close()
    def close(self):
        curses.nocbreak()
        self.scr.keypad(0)
        curses.echo()
        curses.endwin()
    def doRead(self):
        curses.noecho()
        m = self.panels['menu'].userptr()

        key = self.scr.getch()
        if   key == curses.KEY_UP:   m.prev_opt()
        elif key == curses.KEY_DOWN: m.next_opt()
        elif key == curses.KEY_ESCAPE: pass
        elif key == curses.KEY_ENTER:
            if   m.curr_opt == 0: menu_actions.login(self.panels)
            elif m.curr_opt == 1: menu_actions.create_user(self.panels)
            elif m.curr_opt == 2: self.close()
        curses.doupdate()
        self.scr.refresh()
