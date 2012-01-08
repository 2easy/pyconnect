import curses, curses.panel
curses.KEY_ENTER = 10
curses.KEY_ESCAPE = 27

class CursesWrapper():
    __shared_state = { 'scr' : curses.initscr() }
    def __init__(self):
        self.__dict__ = self.__shared_state
    def create_window(self,height,width,y,x):
        return curses.newwin(height,width,y,x)
