#!/usr/bin/python
# -*- coding: utf8 -*-

from Tkinter import *
from ScrolledText import ScrolledText
from idlelib.WidgetRedirector import WidgetRedirector
from tkFileDialog import askopenfilename
import tkMessageBox

import Citra
from VerseTools import Verse



# text box that is read-only
# taken from http://tkinter.unpythonic.net/wiki/ReadOnlyText
class ReadOnlyText(Text):
  def __init__(self, *args, **kwargs):
     Text.__init__(self, *args, **kwargs)
     self.redirector = WidgetRedirector(self)
     self.insert = self.redirector.register("insert", lambda *args, **kw: "break")
     self.delete = self.redirector.register("delete", lambda *args, **kw: "break")



# called when the user presses the "Search" button
def search():
  if figure == None or len(figure.get()) == 0:
    tkMessageBox.showwarning('Error', 'No figure selected')
    return
  elif filename_box == None or len(filename_box.get()) == 0:
    tkMessageBox.showwarning('Error', 'No file selected')
    return

  # now we have a figure and a filename
  #if search_text.get(END) != None and search_text.get(END) != '':
  search_text.delete("1.0", END)

  # what we want to do is run the appropriate function to search for the verse
  verses = Citra.processRequest(figure.get(), filename_box.get())
  for verse in verses:
    search_text.insert(END, str(verse))



def loadFile():
  fname = askopenfilename(filetypes=(("Text Files", "*.txt"), ("All files", "*.*")) )
  if fname:
    try:
      print('File chosen: ' + fname)
    except:                     # <- naked except is a bad idea
      showerror("Open Source File", "Failed to read file\n'%s'" % fname)

  # put the filename into the textbox
  # focus on filename, not path
  filename_box.delete(0, END)
  filename_box.insert(0, fname)
  filename_box.xview(END)

  # enable the search button
  search_button.config(state = ACTIVE)




root = Tk()
root.title('Citra locator')

main = Frame(root)

#root.rowconfigure(5, weight=1)
#root.columnconfigure(5, weight=1)
#root.grid(sticky=W+E+N+S)

# figure label and dropdown menu
figure_frame = Frame(main)
figure_text = Label(figure_frame, text='Figure: ')
figure_text.grid(row=0, sticky=W)

figure = StringVar()
figure.set(Citra.FIGURES[0]) # default value
figure_list = OptionMenu(figure_frame, figure, *Citra.FIGURES)
figure_list.grid(row=0, column=1, sticky=W)

figure_frame.grid(row=0, sticky=W)



# filename to be searched
filename_frame = Frame(main)
filename_text = Label(filename_frame, text='File: ')
filename_text.grid(row=0, column=2, sticky=W)

filename_box = Entry(filename_frame)
filename_box.grid(row=0, column=3, sticky=W)

filename_button = Button(filename_frame, text="Browse", command=loadFile, width=10)
filename_button.grid(row=0, column=4, columnspan=2)

filename_frame.grid(row=0, column=1, sticky=W)



# button to start the action.
search_frame = Frame(main)
search_button = Button(search_frame, text="Search", command=search)
search_button.config(state = DISABLED)
search_button.grid(row=1, column=0, sticky=N+W)

# big textbox to display info
search_text = ReadOnlyText(search_frame, bg='white')
search_text.config(highlightbackground='black')
search_text.grid(row=1, column=1, columnspan=4, rowspan=10, sticky=W)

search_frame.grid(row=1, column=0, columnspan=2, rowspan=10, sticky=W)



main.grid()


root.mainloop()
