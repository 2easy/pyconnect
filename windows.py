import curses_wrapper as cs_wrap
cs = cs_wrap.CursesWrapper()

import locale

class Menu():
    # menu paddings
    h_pad = 2 + 1
    v_pad = 1 + 1
    def __init__(self, max_y=0,max_x=0, options = [], label = locale.Menu.menu):
        self.label = label
        self.max_y = max_y
        self.max_x = max_x
        # determining height and width
        self.width = 0
        for o in options:
            if len(o) > self.width: self.width = len(o)
        if len(self.label) > self.width: self.width = len(self.label)
        self.width  += Menu.h_pad*2
        self.height = len(options) + Menu.v_pad*2
        # get center coordinates
        x = (max_x - self.width)/2
        y = (max_y - self.height)/2
        # create menu window
        self.win = cs.create_window(self.height,self.width,y,x)
        self.win.keypad(1)
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
    def update_size(self,label):
        if len(label) > self.width:
            self.width = len(label)+Menu.h_pad*2
            self.win.resize(self.height,self.width)
        x = (self.max_x - self.width)/2
        y = (self.max_y - self.height)/2
        self.win.mvwin(y,x)
        self.win.clear()
        self.win.box(0,0)
        self.win.nooutrefresh()
    def display(self):
        # create nice menu label
        self.update_size(self.label+"  ")
        menu_label = " " + self.label + " "
        x = (self.width-len(menu_label))/2
#        if self.label == locale.Account.q_remember_pass: raise BaseException(self.width)
        self.win.addstr(0,x,menu_label)
        self.update()
        self.win.noutrefresh()
    def update(self):
        # fill menu with supplied options
        i = 0
        # for debuuging REMOVE LATER
        #self.win.addstr(1,1,str(curses.version),curses.A_REVERSE)
        for o in self.options:
            if (i == self.curr_opt):
                self.win.addstr(Menu.v_pad+i,Menu.h_pad,o,
                                cs_wrap.curses.A_REVERSE)
            else:
                self.win.addstr(Menu.v_pad+i,Menu.h_pad,o)
            i+=1
        self.win.refresh()

class WindowTooBigException(BaseException): pass
class LabeledWindow(object):
    padding = 4
    def __init__(self, max_y = 0, max_x = 0, label = "", content = ""):
        self.max_y = max_y
        self.max_x = max_x
        self.content = content
        self.height, self.width = self.get_size(content)
        # create window
        y,x = self.get_coords()
        self.win = cs.create_window(self.height,self.width,y,x)
        self.win.keypad(1)
        self.update_label(label)
    def get_size(self,content):
        width  = self.max_x / 2
        height = LabeledWindow.padding
        if len(self.content) == 0:
            height += 1
        else:
            height += len(content) / (width-LabeledWindow.padding)
        if height > self.max_y:
            raise WindowTooBigException("Too much content")
        else:
            return height,width
    def set_size(self,content):
        self.height, self.width = self.get_size(content)
        self.win.resize(self.height,self.width)
        self.win.nooutrefresh()
    def get_coords(self):
        return ( (self.max_y - self.height)/2 , (self.max_x - self.width)/2 )
    def update_coords(self):
        y,x = self.get_coords()
        self.win.mvwin(y,x)
        self.win.nooutrefresh()
    def update_label(self, label = ""):
        self.label = label
        self.win.box(0,0)
        # create nice menu label
        menu_label = " " + self.label + " "
        m_x = (self.width-len(menu_label))/2
        self.win.addstr(0,m_x,menu_label)
        self.win.noutrefresh()

class Notification(LabeledWindow):
    def __init__(self, max_y = 0, max_x = 0, label = "", message = ""):
        super(Notification,self).__init__(max_y,max_x,label, message)
        self.message = self.content
    def update_contents(self, label = "", msg = ""):
        self.set_size(msg)
        self.update_coords()
        self.win.clear()
        self.update_label(label)
        # update the notification message
        nrows = self.height - LabeledWindow.padding - 1
        for i in range(nrows):
            self.win.addstr(2,2+i,msg[i*self.width:(i+1)*self.width])
        i = nrows
        self.win.addstr(2,2+nrows, msg[(nrows)*self.width:])
        self.win.noutrefresh()

class Prompt(LabeledWindow):
    def __init__(self, max_x = 0, max_y = 0, label = "", content = ""):
        super(Prompt,self).__init__(max_x,max_y,label,content)
    def user_for(self, subject, obfucate = False):
        self.content = ""
        self.update_label(subject)
        self.win.move(2,2)
        c,i = '',0
        cs_wrap.curses.noecho()
        cs_wrap.curses.curs_set(1)
        while True:
            c = self.win.getch()
            if 32 < c < 126:
                self.content += chr(c)
                if obfucate: self.win.addch(2,2+i,'*')
                else: self.win.addch(2,2+i,chr(c))
                i += 1
                self.win.move(2,2+i)
                self.win.refresh()
            elif c == cs_wrap.curses.KEY_BACKSPACE and i > 0:
                self.content = self.content[:-1]
                i -= 1
                self.win.addch(2,2+i," ")
                self.win.move(2,2+i)
            elif c == cs_wrap.curses.KEY_ENTER:
                self.win.addstr(2,2," "*i)
                break
        cs_wrap.curses.curs_set(0)
        cs_wrap.curses.echo()
