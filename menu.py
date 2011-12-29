import curses

class Menu():
    # menu paddings
    h_pad = 2 + 1
    v_pad = 1 + 1
    def __init__(self, max_x=0,max_y=0, options = []):
        curses.initscr()
        #determining height and width
        self.width = 0
        for o in options:
            if len(o) > self.width: self.width = len(o)
        self.width  += Menu.h_pad*2
        self.height = len(options) + Menu.v_pad*2
        # get center coordinates
        x = (max_x - self.width)/2
        y = (max_y - self.height)/2
        # create menu window
        self.win = curses.newwin(self.height,self.width,y,x)
        self.win.box(0,0)
        # fill it with the given options
        self.curr_opt = 0
        self.last_opt = len(options)-1
        self.options  = options
        self.display()
    def next_opt(self):
        self.curr_opt = (self.curr_opt + 1) % len(self.options)
    def prev_opt(self):
        if self.curr_opt > 0: self.curr_opt -= 1
        else: self.curr_opt = self.last_opt
    def display(self):
        # create nice menu label
        x = (self.width-len(" MENU "))/2
        self.win.addstr(0,x," MENU ")
        # fill menu with supplied options
        i = 0
        for o in self.options:
            if (i == self.curr_opt):
                self.win.addstr(Menu.v_pad+i,Menu.h_pad,o,curses.A_STANDOUT)
            else:
                self.win.addstr(Menu.v_pad+i,Menu.h_pad,o)
            i+=1
        self.win.refresh()
