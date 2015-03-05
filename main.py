#!/usr/bin/env python

import pygtk
import gtk
import sys
import gtk.gdk
import math
import requests
from  config import *

class CredFrame(gtk.Window):
	
	def __init__(self):
		super(CredFrame, self).__init__()

		logger = Static()
		info = logger.load()

		self.show()
		self.connect("destroy", self.destroy)
	
		self.set_title("Schulnetz")
		self.resize(350, 100)
		self.set_border_width(10)
		self.set_position(gtk.WIN_POS_CENTER)

		self.login = gtk.Button(label = "Login")
		self.user = gtk.Entry()
		self.secure = gtk.Entry()

		label = gtk.Label("Benutzername")
		label_pass = gtk.Label("Passwort")

		if info is not None:
			self.user.set_text(info["user"])
			self.secure.set_text(info["passw"])

		logger.save("yo", "bitch")

		self.secure.set_visibility(False)
		box = gtk.HBox()
		self.add(box)

		# login info
		container = gtk.Fixed()
		table = gtk.Table(2, 5, False)
		table.attach(label, 0, 1, 0, 1)
		table.attach(label_pass, 0, 1, 1, 2)
		table.attach(self.user, 1, 3, 0, 1)
		table.attach(self.secure, 1, 3, 1, 2)
		table.attach(self.login, 3, 5, 1, 3)
		container.put(table, 0, 0)

		box.add(container)
		self.show_all()

	def destroy(self, event):
		gtk.main_quit()
		sys.exit()
	
	def response(self):
		gtk.main()
		print("lol")
	
class Uploader():

	def __init__(self):
		self.session = requests.session()

	def login(username, password):
		request = session.post("http://aeg-schulnetz.de/login/index.php", {"username":username, "password":password})
		##todo: validate

	def upload(self, startX, startY, endX, endY):
		self.save_screen(startX, startY, endX, endY)
		data = CredFrame().response()

	def save_screen(self, startX, startY, endX, endY):
		width = int(math.fabs(endX - startX))
		height = int(math.fabs(endY - startY))
		w = gtk.gdk.get_default_root_window()
		sz = w.get_size()
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,width,height)
		pb = pb.get_from_drawable(w,w.get_colormap(), int(startX), int(startY), 0, 0, width, height)
		if (pb != None):
    			pb.save("screenshot.png","png")
   			print "Screenshot saved to screenshot.png."
		else:
    			print "Unable to get the screenshot."


class CacheWindow:
	def __init__(self):
		self.hit = False
		self.window = gtk.Window()
		self.window.set_opacity(0.1)
		self.window.fullscreen()
		self.window.show()

		self.drawer = gtk.DrawingArea()
		self.drawer.connect("expose-event", self.expose)
		self.window.add(self.drawer)
		self.drawer.show()

		self.window.add_events(gtk.gdk.KEY_PRESS_MASK | gtk.gdk.BUTTON_PRESS_MASK |  gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK)
		self.window.connect("key-press-event", self.key_press)
		self.window.connect("button-press-event", self.button_down)
		self.window.connect("motion-notify-event", self.motion)

		self.release_id = self.window.connect("button-release-event", self.button_up)

	def expose(self, widget, event):
		cr = widget.window.cairo_create()

		if self.hit:
			cr.set_source_rgb(0.2, 0.2, 0.2)
			cr.rectangle(self.X, self.Y, self.curX - self.X, self.curY - self.Y)
			cr.fill()
			
	def key_press(self, widget, event):
		if event.keyval == 65307:
			sys.exit()

	def button_down(self, widget, event):
		if event.button == 1:
			self.hit = True
			self.X = event.x
			self.Y = event.y					
			self.curX = event.x
			self.curY = event.y

	def motion(self, widget, event):
		if self.hit:
			self.curX = event.x
			self.curY = event.y
			self.drawer.queue_draw()
						
	def button_up(self, widget, event):
		if event.button == 1 and self.hit:
			self.hit = False
			self.window.disconnect(self.release_id)
			gtk.main_quit()
			self.window.hide()
			Uploader().upload(self.X, self.Y, event.x, event.y)
			sys.exit()

	def main(self):
		gtk.main()

base = CacheWindow()
base.main()
