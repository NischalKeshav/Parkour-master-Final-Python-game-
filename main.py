from tkinter import *
import random
import time 

class Game:
  def __init__(self):
    i = 0
    self.tk = Tk()
    self.tk.title("Agent Stickman races for the exit!")
    self.tk.resizable(0,0)
    self.tk.wm_attributes("-topmost",1)
    self.canvas = Canvas(self.tk,width =500,height=500,    highlightthickness=0)
    self.canvas.pack()
    self.tk.update()
    self.canvas_height = 500
    self.canvas_width = 500
    self.bg = PhotoImage(file= "background.png")
    self.bg2 = PhotoImage(file= "background2.png")
    h = self.bg.height()
    w = self.bg.height()
    for x in range (0,5):
      i += 1
      for y in range (0,5):
        if (y + i) % 2 == 0:
          self.canvas.create_image((x*w),y*h,image= self.bg,anchor= 'nw') 
        else:
          self.canvas.create_image((x*w),y*h,image= self.bg2,anchor= 'nw') 
    self.sprites =[]
    self.running = True 
  def mainloop(self):
    while 1:
      if self.running == True :
        for sprite in self.sprites:
          sprite.move()
      self.tk.update_idletasks() 
      self.tk.update()
      time.sleep(.01)  
class Coords:
  def __init__(self,x1=0,y1=0,x2=0,y2=0):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
def within_x(co1, co2):
  if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
    or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
    or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
    or (co2.x2 > co1.x1 and co2.x2 < co1.x1):
        return True
  else:
    return False
def within_y(co1, co2):
  if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
    or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
    or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
    or (co2.y2 > co1.y1 and co2.y2 < co1.y1):
      return True
  else:
    return False
def collided_left(co1,co2):
    if within_y(co1,co2):
      if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
        return True 
    else:
      return False 
def collided_right(co1,co2):
    if within_y(co1,co2):
      if co1.x2 >= co2.x1 and co1.x2 <= co2.x2 :
        return True
    else:
      return False 
def collided_top(co1,co2):
    if within_x(co1,co2):
      if co1.y1 <= co2.y2 and co1.y1 >= co2.y1 :
        return True
    else:
      return False
def collided_bottom(y,co1,co2):
    if within_x(co1,co2):
      y_calc = co1.y2 +y
      if y_calc >= co2.y1 and y_calc <= co2.y2 :
        return True
    return False 
class Sprite:
  def __init__(self, game):
    self.game = game
    self.endgame = False
    self.coordinates = None
  def move(self):
    pass
  def coords(self):
    return self.coordinates

class PlateformSprite(Sprite):
  def __init__(self, game, photo_image, x, y, width, height):
    Sprite.__init__(self, game)
    self.photo_image = photo_image
    self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
    self.coordinates = Coords(x, y, x + width, y + height)
class stickFigure(Sprite):
  def __init__(self,game):
    Sprite.__init__(self,game)
    self.images_left = [
      PhotoImage(file = "left1.png"),
      PhotoImage(file = "left2.png"),
      PhotoImage(file  ="left3.png")
    ]
    self.images_right= [
      PhotoImage(file = "1.png"),
      PhotoImage(file = "2.png"),
      PhotoImage(file = "3.png")
    ]
    self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
    self.x = -2
    self.y = 0
    self.current_image = 0
    self.current_image_add = 1
    self.jump_count = 0
    self.last_time = time.time()
    self.coordinates = Coords()
    game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
    game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
    game.canvas.bind_all('<space>', self.jump)
    game.canvas.bind_all('<KeyPress-Up>', self.jump)
    game.canvas.bind('<KeyRelease>',self.stop)
  def turn_left(self,evt):
    if self.y == 0:
      self.x = -2
  def stop(self,evt):
    self.x=  0 
  def turn_right(self,evt):
    if self.y == 0:
      self.x = 2
  def jump (self,evt):
    if self.y == 0:
      self.y = -4
      self.jump_count = 0
  def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image]) 
  def coords(self):
    xy = self.game.canvas.coords(self.image)
    self.coordinates.x1 = xy[0]
    self.coordinates.y1 = xy[1]
    self.coordinates.x2 = xy [0] + 27
    self.coordinates.y2 = xy[1] + 30
    return self.coordinates
  def move(self):
    self.animate()
    if self.y < 0:
      self.jump_count +=1
      if self.jump_count > 20:
        self.y = 4
    if self.y > 0:
      self.jump_count -= 1
    co = self.coords()
    left = True
    right = True
    top = True
    bottom = True
    falling = True 
    if self.y > 0 and co.y2 >= self.game.canvas_height:
      self.y = 0
      bottom = False
    elif self.y < 0  and co.y1 <= 0:
      self.y  = 0 
      top = False
    if co.x1 <= 0 and self.x<0:
      self.x = 0  
    if self.x > 0 and co.x2 >= self.game.canvas_width:
      self.x = 0 
      right = False
    elif self.x < 0  and co.x2 <= 0:
      self.x = 0
      left = False 
    for sprite in self.game.sprites:
      if sprite == self:
        continue
      sprite_co = sprite.coords()
      if top and self.y < 0 and collided_top(co, sprite_co):
        self.y = -self.y
        top = False
                
      if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
        self.y = sprite_co.y1 - co.y2
        if self.y < 0:
          self.y = 0
        bottom = False
        top = False

      if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(1, co, sprite_co):
        falling = False
                
      if left and self.x < 0 and collided_left(co, sprite_co):
        self.x = 0
        left = False
        if sprite.endgame:
          self.game.running = False

      if right and self.x > 0 and collided_right(co, sprite_co):
        self.x = 0
        right = False
        if sprite.endgame:
          self.game.running = False
        if falling and bottom and self.y == True and co.y2 < self.game.canvas_height:
          self.y = 4
        self.game.canvas.move(self.image,self.x,self.y)
    if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
      self.y = 4

    self.game.canvas.move(self.image,self.x,self.y)
g = Game()
plateform1 = PlateformSprite (g,PhotoImage(file='platform100x10.png'),0,480,100,10)

plateform2 = PlateformSprite (g,PhotoImage(file='platform100x10.png'),150,440,100,10)

plateform3 = PlateformSprite (g,PhotoImage(file='platform100x10.png'),300,400,100,10)

plateform4 = PlateformSprite (g,PhotoImage(file='platform100x10.png'),300,160,100,10)

plateform5 = PlateformSprite (g,PhotoImage(file='platform66x10.png'),175,350,66,10)

plateform6 = PlateformSprite (g,PhotoImage(file='platform66x10.png'),50,300,66,10)

plateform7 = PlateformSprite (g,PhotoImage(file='platform100x10.png'),170,120,66,10)

plateform8 = PlateformSprite (g,PhotoImage(file='platform100x10.png'),45,60,66,10)

plateform9 = PlateformSprite (g,PhotoImage(file='plateform10x32.png'),170,250,32,10)

plateform10 = PlateformSprite (g,PhotoImage(file='plateform10x32.png'),230,200,32,10)
g.sprites.append(plateform1)
g.sprites.append(plateform2)
g.sprites.append(plateform3)
g.sprites.append(plateform4)
g.sprites.append(plateform5)
g.sprites.append(plateform6)
g.sprites.append(plateform7)
g.sprites.append(plateform8)
g.sprites.append(plateform9)
g.sprites.append(plateform10)
sf = stickFigure(g)
g.sprites.append(sf)
g.mainloop()

