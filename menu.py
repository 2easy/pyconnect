import curses
import msg

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
        self.update()
    def prev_opt(self):
        if self.curr_opt > 0: self.curr_opt -= 1
        else: self.curr_opt = self.last_opt
        self.update()
    def display(self):
        # create nice menu label
        menu_label = " " + msg.Menu.menu + " "
        x = (self.width-len(menu_label))/2
        self.win.addstr(0,x,menu_label)
        self.update()
        self.win.noutrefresh()
    def update(self):
        # fill menu with supplied options
        i = 0
        for o in self.options:
            if (i == self.curr_opt):
                self.win.addstr(Menu.v_pad+i,Menu.h_pad,o,curses.A_STANDOUT)
            else:
                self.win.addstr(Menu.v_pad+i,Menu.h_pad,o)
            i+=1
        self.win.refresh()

class WindowTooBigException(BaseException): pass
class LabeledWindow(object):
    padding = 4
    def __init__(self, max_x = 0, max_y = 0, label = "", content = ""):
        curses.initscr()
        self.content = content
        self.width   = max_x / 2
        self.height  = LabeledWindow.padding
        if len(self.content) == 0:
            self.height += 1
        else:
            self.height  += len(content) / (self.width-LabeledWindow.padding)
        if self.height > max_y: raise WindowTooBigException("Too much content")
        # create window
        x = (max_x - self.width)/2
        y = (max_y - self.height)/2
        self.win    = curses.newwin(self.height,self.width,y,x)
        self.win.keypad(1)
        self.update_label(label)
    def update_label(self, label = ""):
        self.label = label
        self.win.box(0,0)
        # create nice menu label
        menu_label = " " + self.label + " "
        m_x = (self.width-len(menu_label))/2
        self.win.addstr(0,m_x,menu_label)
        self.win.noutrefresh()

class Prompt(LabeledWindow):
    def __init__(self, max_x = 0, max_y = 0, label = "", val = ""):
        super(type(self),self).__init__(max_x,max_y,label,val)
    def user_for(self, subject, obfucate = False):
        self.val = ""
        self.update_label(subject)
        self.win.move(2,2)
        c,i = '',0
        curses.noecho()
        curses.curs_set(1)
        while True:
            c = self.win.getch()
            if 32 < c < 126:
                self.val += chr(c)
                if obfucate: self.win.addch(2,2+i,'*')
                else: self.win.addch(2,2+i,chr(c))
                i += 1
                self.win.move(2,2+i)
                self.win.refresh()
            elif c == curses.KEY_BACKSPACE and i > 0:
                self.val = self.val[:-1]
                i -= 1
                self.win.addch(2,2+i," ")
                self.win.move(2,2+i)
            elif c == curses.KEY_ENTER:
                self.win.addstr(2,2," "*i)
                break
        curses.curs_set(0)
        curses.echo()
