#!usr/bin/env python
#-*-coding:utf-8-*-

Author='NZ'

n=30

try:
    from Tkinter import *
except:
    from tkinter import *

class soldier():
    soldiers = []
    def __init__(self,i,j,field):
        global n
        self.i=i; self.j=j; self.field=field
        self.alive = False
        self.sel = field.create_rectangle(n*self.j+2,n*self.i+2,n*self.j+n-2,n*self.i+n-2,width=1)
        self.kill()
        
    def born(self):
        self.field.itemconfig(self.sel, fill='red')
        self.alive = True

    def kill(self):
        if self.i > 4:
            self.field.itemconfig(self.sel, fill='#22ffff')
        else:
            self.field.itemconfig(self.sel, fill='white')
        self.alive = False

    def change(self):
        self.alive = not self.alive

    def highlight(self):
        if self.alive == True:
            self.field.itemconfig(self.sel, fill='orange')
    
class pos():
    last=(None,None)
    global n
    @staticmethod
    def get(event):
        j = event.x/n if ((2<event.x%n<(n-2)) and (0<=event.x/n<16)) else None
        i = event.y/n if ((2<event.y%n<(n-2)) and (0<=event.y/n<12)) else None
        pos.last = (i,j) if (i != None and j != None) else (None,None)
            
class put():
    @staticmethod
    def onPut(field):
        print 'Now, you can put your soldiers in the blue grids.'
        field.bind('<Button-1>',put.put)

    @staticmethod
    def put(event):
        pos.get(event)
        i,j = pos.last
        try:
            soldier_0 = soldier.soldiers[i][j]
        except TypeError:
            print 'Wrong Click'
            return -1
        soldier_0 = soldier.soldiers[i][j]
        if not(i>4 or soldier_0.alive):
            print 'You can\'t put the soldier there!'
            return -1
        if soldier_0.alive == False:
            print 'A soldier has been puted.'
            soldier_0.born()
        else:
            print 'A soldier has been removed.'
            soldier_0.kill()

class start():
    def __init__(self,field):
        self.field=field
        
    def onStart(self):
        self.field.bind('<Button-1>',start(self.field).start)
        print 'Select the soldier you want to move.'

    def start(self,event):
        pos.get(event)
        i,j = pos.last
        try:
            soldier_1 = soldier.soldiers[i][j]
        except TypeError:
            print 'Wrong click!'
            start(self.field).onStart()
            return -1
        if not soldier_1.alive:
            print 'You didn\'t select the rigrh soldier, select again!'
            start(self.field).onStart()
            return -1
        soldier_1.highlight()
        self.field.bind('<Button-1>',start(self.field).goto)
        print 'Select the grid the soldier will move to.'

    def goto(self,event):
        i,j = pos.last
        soldier_1 = soldier.soldiers[i][j]
        pos.get(event)
        i2,j2 = pos.last
        try:
            soldier_2 = soldier.soldiers[i2][j2]
        except TypeError:
            print 'Wrong click!'
            soldier_1.born()
            start(self.field).onStart()
            return -1
        if (abs(i2-i)==2 and j==j2) or (abs(j2-j)==2 and i==i2):
            soldier_3 = soldier.soldiers[(i2+i)/2][(j2+j)/2]
            if soldier_3.alive:
                soldier_1.kill()
                soldier_2.born()
                soldier_3.kill()
                
            else:
                print 'The soldier can\'t go there!'
                soldier_1.born()
                start(self.field).onStart()
                return -1
        else:
            print 'The soldier can\'t go there!'
            soldier_1.born()
            start(self.field).onStart()
            return -1
        start(self.field).onStart()

def onRestart():
    print 'Restart Game!'
    for i in range(12):
        for j in range(16):
            soldier.soldiers[i][j].kill()
    put().onPut(soldier.soldiers[0][0].field)


def main():
    win = Tk()
    win.title('Conway\'s Soldier')
    
    frame_title=Frame(win)
    frame_title.pack(side=TOP)
    Label(frame_title, text=' Conway\'s Soldier ', fg='red', font=('arial', 50, 'italic')).pack(side=TOP)
    Label(frame_title, text='By Group 3 ', font=('arial', 30, 'italic')).pack(side=RIGHT)

    frame_main = Frame(win)
    frame_main.pack()
    global n
    field = Canvas(frame_main, width=n*16, height=n*12)
    field.pack()
    field.create_rectangle(-4,150,n*16,n*16+4,fill='#22ffff',width=0)
    for i in range(12):
        soldier.soldiers.append([])
        for j in range(16):
            soldier.soldiers[i].append([])
            ins = soldier(i,j,field)
            soldier.soldiers[i][j] = ins
    
    frame_control = Frame(win)
    frame_control.pack(side=BOTTOM, fill=X)
    button_put = Button(frame_control, text='摆放士兵', command=lambda:put.onPut(field))
    button_start = Button(frame_control, text='开始前进', command=lambda:start(field).onStart())
    button_restart = Button(frame_control, text='重新开始', command=onRestart)
    button_put.pack(side=LEFT)
    button_start.pack(side=LEFT)
    button_restart.pack(side=RIGHT)   
    
    put().onPut(field)
    win.mainloop()

if __name__ =='__main__':
    main()
