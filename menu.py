import curses

class Menu():
    def __init__(self, max_x=0,max_y=0, options = []):
        curses.initscr()
        #determining height and width
        self.width = 0
        for o in options:
            if len(o) > self.width: self.width = len(o)
        # +2 for up/bottom, left/right borders
        self.width  += 2
        self.height = len(options) + 2
        # get center coordinates
        x = (max_x - self.width)/2
        y = (max_y - self.height)/2
        # create menu window
        self.win = curses.newwin(self.height,self.width,y,x)
        self.win.box(0,0)
        # fill it with the given options
        self.curr_opt = 0
        self.last     = len(options)-1
        i = 1
        for o in options:
            if (i-1 == self.curr_opt):
                self.win.addstr(i,1,o,curses.A_STANDOUT)
            else:
                self.win.addstr(i,1,o)
            i+=1
        self.options  = options
    def display(self):
        self.win.refresh()
