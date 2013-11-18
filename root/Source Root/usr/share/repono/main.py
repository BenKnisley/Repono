#!/usr/bin/env python
# Repono authored by Ben Knisley
# Main.py - Creates an applet with simple command to control how Google drive is updated.

# Imports 
import os, time, webbrowser, getpass # Import Basic moduals
import gtk, appindicator # Import Gtk moduals
import glib, threading # Import Mutithreading Moduals
from xml.dom.minidom import parse # Import Xml moduals

# Creates backup for update_time
global backup_update_time
backup_update_time = 300

# Test to see if settings file exists
settings_file = ('/home/' + getpass.getuser() + '/.Repono_settings')
try:
	with open(settings_file):
		pass
except IOError: # If settings file does to exist, open setting diolog and exit
	os.system('/usr/share/repono/settings.py & exit')
	exit()

# Retrives settings from file
setting_xml = parse(settings_file)
drive_dir = "'" + setting_xml.getElementsByTagName('dir')[0].firstChild.nodeValue + "'"
backup_update_time = setting_xml.getElementsByTagName('time')[0].firstChild.nodeValue
backup_update_time = int(backup_update_time)

# sets update time to defalt seting 
global update_time
update_time = backup_update_time

# Time update functions

def time_update(*arg): # Starts the time update loop
	call_update()
	glib.timeout_add_seconds(update_time, time_update)

def update(*arg): # Does the update, changes icons, and all other update hevey lifting
	global applet
	global update_time
	global backup_update_time
	# Label Me
	glib.idle_add(applet.set_icon, 'gdrive_sync')
	# Label Me
	grive_stat = os.system('cd ' + drive_dir + ' && grive')
	# Label Me
	if grive_stat != 0: # Add Descrip
		glib.idle_add(applet.set_icon, 'gdrive_error')
		update_time = 5
		return
	if grive_stat == 0 and update_time != backup_update_time: # Add Descrip
		glib.idle_add(applet.set_icon, 'gdrive')
		update_time = backup_update_time
		return
	# Label Me
	glib.idle_add(applet.set_icon, 'gdrive')


# Menu Item Functions

def call_update(*arg): # Calls an update without time loop
	threading.Thread(target=update).start()

def settings(*arg): # opens the setting Dialog
	os.system('/usr/share/repono/settings.py & exit')
	gtk.main_quit()
	exit()

def open_folder(*args): # opens google drive folder
	os.system('xdg-open ' + drive_dir)
	return

def open_online(*args): # opens google drive online
	webbrowser.open('http://drive.google.com')
	return

# Add Menu Items to menu Functions

def add_update_gdrive_item(*arg):
	global menu
	item = gtk.MenuItem("Update Google Drive")
	item.connect("activate", call_update)
	item.show()
	menu.append(item)

def add_open_dir_item(*arg):
	global menu
	item = gtk.MenuItem("Open Folder")
	item.connect("activate", open_folder)
	item.show()
	menu.append(item)

def add_open_online_item(*arg):
	global menu
	item = gtk.MenuItem("Open Online")
	item.connect("activate", open_online)
	item.show()
	menu.append(item)

def add_open_setting_item(*arg):
	global menu
	item = gtk.MenuItem("Settings")
	item.connect("activate", settings)
	item.show()
	menu.append(item)

def add_quit_item(*arg):
	global menu
	item = gtk.MenuItem("Quit")
	item.connect("activate", gtk.main_quit)
	item.show()
	menu.append(item)
	
def add_spacer_item(*arg):
	spacer = gtk.SeparatorMenuItem()
	spacer.show()
	menu.append(spacer)

# Basic Applet objects

def applet(*arg):
	global applet
	applet = appindicator.Indicator("repono", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
	applet.set_status(appindicator.STATUS_ACTIVE)
	applet.set_icon('gdrive')

def menu(*arg):
	global menu
	global applet
	menu = gtk.Menu()
	applet.set_menu(menu)

# Starting Basic applet objects
applet()
menu()

# Adding menu Items to menu
add_update_gdrive_item()
add_spacer_item()
add_open_dir_item()
add_open_online_item()
add_spacer_item()
add_open_setting_item()
add_spacer_item()
add_quit_item()

# Starting Program
glib.threads_init()
time_update()
gtk.main()
