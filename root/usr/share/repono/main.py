#!/usr/bin/env python
import os, gtk, appindicator, getpass, glib, threading, time, webbrowser
from xml.dom.minidom import parse
global def_update_time
def_update_time = 300

setting_file = ('/home/' + getpass.getuser() + '/.Repono_settings')
try:
	with open(setting_file):
		pass
except IOError:
	os.system('/usr/share/repono/settings.py & exit')
	exit()

setting_xml = parse(setting_file)
drive_dir = "'" + setting_xml.getElementsByTagName('dir')[0].firstChild.nodeValue + "'"
def_update_time = setting_xml.getElementsByTagName('time')[0].firstChild.nodeValue
def_update_time = int(def_update_time)

global update_time
update_time = def_update_time


#########################
#########################


def settings(*arg):
	os.system('/usr/share/repono/settings.py & exit')
	gtk.main_quit()
	exit()


def time_update(*arg):
	call_update()
	glib.timeout_add_seconds(update_time, time_update)

def update(*arg):
	global ind
	global update_time
	global def_update_time
	#####################
	glib.idle_add(ind.set_icon, 'gdrive_sync')
	#####################
	grive_stat = os.system('cd ' + drive_dir + ' && grive')
	#####################
	if grive_stat != 0:
		glib.idle_add(ind.set_icon, 'gdrive_error')
		update_time = 5
		return
	if grive_stat == 0 and update_time != def_update_time:
		glib.idle_add(ind.set_icon, 'gdrive')
		update_time = def_update_time
		return
	######################
	glib.idle_add(ind.set_icon, 'gdrive')

def call_update(*arg):
	threading.Thread(target=update).start()

#########################
#########################

def open_folder(*args):#opens google drive folder
	os.system('xdg-open ' + drive_dir)
	return

def open_online(*args):#opens google drive online
	webbrowser.open('http://drive.google.com')
	return

#########################
#########################

def menu_item_one(*arg):
	global menu
	global item1
	item1 = gtk.MenuItem("Update Google Drive")
	item1.connect("activate", call_update)
	item1.show()
	menu.append(item1)

def menu_item_two(*arg):
	global menu
	global item2
	item2 = gtk.MenuItem("Open Folder")
	item2.connect("activate", open_folder)
	item2.show()
	menu.append(item2)

def menu_item_three(*arg):
	global menu
	global item3
	item3 = gtk.MenuItem("Open Online")
	item3.connect("activate", open_online)
	item3.show()
	menu.append(item3)

def menu_item_four(*arg):
	global menu
	global item4
	item4 = gtk.MenuItem("Settings")
	item4.connect("activate", settings)
	item4.show()
	menu.append(item4)

def menu_item_five(*arg):
	global menu
	global item5
	item5 = gtk.MenuItem("Quit")
	item5.connect("activate", gtk.main_quit)
	item5.show()
	menu.append(item5)

#########################
#########################

def ind(*arg):
	global ind
	ind = appindicator.Indicator("google-drive-panel", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
	ind.set_status(appindicator.STATUS_ACTIVE)
	ind.set_icon('gdrive')

def menu(*arg):
	global menu
	global ind
	menu = gtk.Menu()
	ind.set_menu(menu)

def menu_item_spacer(*arg):
	spacer = gtk.SeparatorMenuItem()
	spacer.show()
	menu.append(spacer)


#################
ind()
menu()
#################
menu_item_one()
menu_item_spacer()
menu_item_two()
menu_item_three()
menu_item_spacer()
menu_item_four()
menu_item_five()
################
glib.threads_init()
time_update()
gtk.main()
#'''