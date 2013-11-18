#!/usr/bin/env python
import gtk, getpass, webbrowser, urllib, urlparse, os
from xml.dom.minidom import parse
from subprocess import Popen, PIPE, STDOUT
global activated
#############################
#############################

def select_folder(*arg):
	fol_dia = gtk.FileChooserDialog(title="Select folder")
	fol_dia.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
	fol_dia.set_select_multiple(False)
	fol_dia.set_show_hidden(False)
	fol_dia.add_button('OK', 1)
	fol_dia.add_button('Cancel', -1)
	###
	filter = gtk.FileFilter()
	filter.set_name("Folder")
	filter.add_pattern("*")
	fol_dia.add_filter(filter)
	###
	id = fol_dia.run()
	folder = fol_dia.get_uri()
	fol_dia.hide()
	if id == 1 and folder != None:
		folder = urllib.url2pathname(urlparse.urlparse(folder).path)
		ent1_section1_win1.set_text(folder)

def exit_save(*arg):
	global activated
	if len(ent1_section1_win1.get_text()) == 0:
		show_fol_err_win()
		pass
	print activated
	if activated == False:
		show_act_err_win()
		pass
	#write to file
	setting_file = ('/home/' + getpass.getuser() + '/.Repono_settings')
	file_filling = '<xml>\n<dir>' + ent1_section1_win1.get_text() + '</dir>\n<time>' + str(int(spi1_section2_win1.get_value())) + '</time>\n</xml>'
	print file_filling
	file = open(setting_file, 'w+')
	file.write(file_filling)
	gtk.main_quit()

def activate(*arg):
	if len(ent1_section1_win1.get_text()) == 0:
		show_fol_err_win()
		pass
	#starts grive and opens browser to input auth code
	global griveprocess
	global grivein
	global griveerr
	griveprocess = Popen("cd '" + ent1_section1_win1.get_text() + "/' && grive -a --dry-run",
	shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	griveout = griveprocess.stdout
	grivein = griveprocess.stdin
	griveerr = griveprocess.stderr

	#This is a mess!!!
	x = ''
	y = ''
	z = False
	while z == False:
		x = griveout.read(1)
		y = y + x
		if x == '\n':
			if y[:4] == 'http':
				z = True
			else:
				y = ''
	webbrowser.open(y)
	show_code_input_win()

def activate_two(*args):
	global activated
	authcode = entry_code_input_win.get_text()
	code_input_win.destroy()
	grivein.write(authcode + ' \n')
	griveprocess.wait()
	activated = True
	if griveprocess.returncode != 0:
		print 'Error, something went wrong'
		activated = False
		pass


#############################
#############################

#   main window
def win1(*arg):
	global win1
	win1 = gtk.Window()
	win1.set_title('Repono - Settings')
	win1.set_default_size(300, 280)
	win1.set_icon_from_file('/usr/share/pixmaps/gdrive.png')
	win1.set_position(gtk.WIN_POS_CENTER)
	win1.connect("delete-event", gtk.main_quit)
	global lay1_win1
	lay1_win1 = gtk.Layout()
	win1.add(lay1_win1)
	###########################
	###########################
	#Ok Button
	ok_button_win1 = gtk.Button()
	ok_button_win1.set_label('    OK    ')
	lay1_win1.put(ok_button_win1, 170, 250)
	ok_button_win1.connect("clicked", exit_save)
	#Cancel Button
	cancel_button_win1 = gtk.Button()
	cancel_button_win1.set_label('  Cancel  ')
	lay1_win1.put(cancel_button_win1, 230, 250)
	cancel_button_win1.connect("clicked", gtk.main_quit)
	############################
	win1.show_all()

def section1_win1(*arg):
##  lab1_section1_win1  ##
	lab1_section1_win1 = gtk.Label()
	lab1_section1_win1.set_label('Folder Settings')
	lay1_win1.put(lab1_section1_win1, 5, 5)
##  lab2_section1_win1  ##
	lab2_section1_win1 = gtk.Label()
	lab2_section1_win1.set_label('Folder to sync:')
	lay1_win1.put(lab2_section1_win1, 15, 25)
##  ent1_section1_win1
	global ent1_section1_win1
	ent1_section1_win1 = gtk.Entry()
	ent1_section1_win1.set_width_chars(21)
	ent1_section1_win1.set_property('editable', False)
	lay1_win1.put(ent1_section1_win1, 15, 45)
##  but1_section1_win1
	but1_section1_win1 = gtk.Button()
	but1_section1_win1.set_label('Select Folder')
	lay1_win1.put(but1_section1_win1, 198, 45)
	but1_section1_win1.connect("clicked", select_folder)
##  Show All
	win1.show_all()

def section2_win1(*arg):
##  lab1_section2_win1
	lab1_section2_win1 = gtk.Label()
	lab1_section2_win1.set_label('Time Settings')
	lay1_win1.put(lab1_section2_win1, 5, 80)
##  lab2_section2_win1
	lab2_section2_win1 = gtk.Label()
	lab2_section2_win1.set_label('Update Every')
	lay1_win1.put(lab2_section2_win1, 5, 110)
##  spi1_section2_win1
	global spi1_section2_win1
	spi1_section2_win1 = gtk.SpinButton(adjustment=gtk.Adjustment(value=300, lower=15, upper=100000, step_incr=30, page_incr=1, page_size=0), climb_rate=0.0, digits=0)
	lay1_win1.put(spi1_section2_win1, 100, 110)
##  lab3_section2_win1
	lab3_section2_win1 = gtk.Label()
	lab3_section2_win1.set_label('Sec')
	lay1_win1.put(lab3_section2_win1, 180, 110)
##  Show All
	win1.show_all()

def section3_win1(*arg):
##  lab1_section2_win1
	lab1_section2_win1 = gtk.Label()
	lab1_section2_win1.set_label('Other Settings')
	lay1_win1.put(lab1_section2_win1, 5, 150)
##  lab2_section2_win1
	lab2_section2_win1 = gtk.Label()
	lab2_section2_win1.set_label('Activate /  Reactivate Account')
	lay1_win1.put(lab2_section2_win1, 10, 175)
##  but1_section2_win1
	but1_section2_win1 = gtk.Button()
	but1_section2_win1.set_label('Activate')
	but1_section2_win1.connect("clicked", activate)
	lay1_win1.put(but1_section2_win1, 110, 200)
##  Show All
	win1.show_all()

#############################

#   folder error win
def show_fol_err_win(*arg):
	fol_err_win = gtk.Window()
	fol_err_win.set_title('Error')
	fol_err_win.set_default_size(200, 100)
	fol_err_win.set_position(gtk.WIN_POS_CENTER)
	####    Lay1    ####
	lay_fol_err_win = gtk.Layout()
	fol_err_win.add(lay_fol_err_win)
	#   lab_x
	lab1_lay_fol_err_win = gtk.Label()
	lab1_lay_fol_err_win.set_label('Input Folder to Finish Setup')
	lay_fol_err_win.put(lab1_lay_fol_err_win, 10, 5)
	fol_err_win.show_all()

#   Activate error win
def show_act_err_win(*arg):
	act_err_win = gtk.Window()
	act_err_win.set_title('Error')
	act_err_win.set_default_size(200, 100)
	act_err_win.set_position(gtk.WIN_POS_CENTER)
	####    Lay1    ####
	lay_act_err_win = gtk.Layout()
	act_err_win.add(lay_act_err_win)
	#   lab_x
	lab1_lay_act_err_win = gtk.Label()
	lab1_lay_act_err_win.set_label('Activate Account to Finish Setup')
	lay_act_err_win.put(lab1_lay_act_err_win, 10, 5)
	act_err_win.show_all()

def show_code_input_win(*arg):
	global code_input_win
	code_input_win = gtk.Window()
	code_input_win.set_title('Input Code:')
	code_input_win.set_default_size(200, 100)
	code_input_win.set_position(gtk.WIN_POS_CENTER)
	####    Lay1    ####
	lay1_code_input_win = gtk.Layout()
	code_input_win.add(lay1_code_input_win)
	#   lab_1
	lab1_code_input_win = gtk.Label()
	lab1_code_input_win.set_label('Input Code:')
	lay1_code_input_win.put(lab1_code_input_win, 5, 5)
	global entry_code_input_win
	entry_code_input_win = gtk.Entry()
	entry_code_input_win.set_width_chars(20)
	#entry_code_input_win.set_property('editable', True)
	lay1_code_input_win.put(entry_code_input_win, 15, 30)
	but_code_input_win = gtk.Button()
	but_code_input_win.set_label('   OK   ')
	lay1_code_input_win.put(but_code_input_win, 145, 60)
	but_code_input_win.connect("clicked", activate_two)
	code_input_win.show_all()

#############################
#############################

def main(*args):
	global activated
	win1()
	section1_win1()
	section2_win1()
	section3_win1()
	#############################
	#############################
	setting_file = ('/home/' + getpass.getuser() + '/.Repono_settings')
	try:
		with open(setting_file):
			setting_xml = parse(setting_file)
			activated = True
			drive_dir = setting_xml.getElementsByTagName('dir')[0].firstChild.nodeValue
			def_update_time = float(setting_xml.getElementsByTagName('time')[0].firstChild.nodeValue)
	except IOError:
		drive_dir = ''
		activated =  False
		def_update_time = 300
	ent1_section1_win1.set_text(drive_dir)
	spi1_section2_win1.set_value(def_update_time)


main()
gtk.main()
os.system('/usr/share/repono/main.py & exit')



