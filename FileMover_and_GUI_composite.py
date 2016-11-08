#Item 60 PyDril_GUI_34_IDLE
#Python Course, The Tech Academy (Portland, OR)
#Yuuna Kaparti


from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import os
import sys

from datetime import *
from datetime import date
import datetime
import time
import shutil
import glob
from pprint import pprint




class File_Mover:

    def __init__(self, master):

    
        source_Directory = StringVar()
        destination_Directory = StringVar()
        directory = StringVar()


        master.title("Check for Newly Created and Modified Files")
        master.resizable(True, True)
        master.configure(background = '#ffffff')

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#ffffff')
        self.style.configure('TButton', background = '#ffffff')
        self.style.configure('TLabel', background = '#ffffff')




        self.frame1 = ttk.Frame(master)
        self.frame1.pack()

        self.label1 = ttk.Label(self.frame1, text = "Click on button to select the source and destination directory.")
        self.label1.grid(row = 0, column = 0, columnspan = 2, sticky = 'sw')

        self.entry1 = ttk.Entry(self.frame1, width = 47)
        self.entry1.grid(row = 1, column = 0)
        
        self.entry2 = ttk.Entry(self.frame1, width = 47)
        self.entry2.grid(row = 2, column = 0)
        
        self.button_sourceDirectory = ttk.Button(self.frame1, text = "Source Directory", width = 15, command = lambda: self.Select_Directory(self.entry1))
        self.button_sourceDirectory.grid(row = 1, column = 1, sticky = 'w', padx = 20, pady = 5)
        
        self.button_destinationDirectory = ttk.Button(self.frame1, text = "Destination Dir..", width = 15, command = lambda: self.Select_Directory(self.entry2))
        self.button_destinationDirectory.grid(row = 2, column = 1, sticky = 'w', padx = 20, pady = 5)





        self.frame2 = ttk.Frame(master)
        self.frame2.pack(ipadx = 5, ipady = 10)
        
        self.label2 = ttk.Label(self.frame2, text = "Files that have been moved:")
        self.label2.grid(row = 0, column = 0, columnspan = 2, sticky = 'sw', pady = 5)

        self.text_display_filepath = Text(self.frame2, width = 60, height = 10)
        self.text_display_filepath.grid(row = 1, column = 0, columnspan = 2)

        self.text_scrollbar = ttk.Scrollbar(self.frame2, orient = VERTICAL)
        self.text_scrollbar.grid(row = 1, column = 2, sticky = 'w' + 'ns')

        self.text_display_filepath.config(yscrollcommand = self.text_scrollbar.set)
        self.text_scrollbar.config(command = self.text_display_filepath.yview)

        self.button_checkFiles = ttk.Button(self.frame2, text = 'Check Files', width = 15,
                                            command = lambda: self.CheckFiles_Button())
        self.button_checkFiles.grid(row = 2, column = 3, sticky = 'w', padx = 10)


    def Select_Directory(self, pick_directory):
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = True
        options['parent'] = self.frame1
        options['title'] = 'Select Directory'

        directory = filedialog.askdirectory(**options)
        pick_directory.insert(0, directory)



    def CheckFiles_Button(self):
        #get values stored in entry widgets: source directory and destination directory
        #replace the single forward slash with double forward slash for the python interpreter
        dir1 = self.entry1.get()
        dir1 = dir1.replace("/", "//")
        dir2 = self.entry2.get()
        dir2 = dir2.replace("/", "//")
        #create a new variable that selects all the files with .txt extension in source directory
        dirText = dir1 + "//*.txt"
        #create a variable to store the current date and time.  Note: date_now is an instance of
        #datetime class and we can use methods on date_now such as date_now.hour, etc to return int values.
        date_now = datetime.datetime.now()
        #create a list variable to store all the .txt files in the source directory using the glob module's
        #glob method.
        text_files = glob.glob(dirText)


        for i in text_files:
            #for each text file in text_files, get the time stamp.
            doc_time_stamp = os.path.getmtime(i)
            #convert time stamp into a string with date and time information. Use string slice method to retrieve
            #relevant portions of the string.
            time_stamp = time.ctime(doc_time_stamp)
            #use timedelta to set the time offset/difference.  We are setting timedelta to 1 day (24 hours).
            d = timedelta(hours = 24)
            #create a variable to store yesterday's date. This is different from taking date_now.day - 1 since we may
            #get an inaccurate result.  If first day of month is 1, then date_now.day will be 1 and 1 minus 1 will give 0.
            #But, the correct result is last day of preceding month.
            yesterday = date_now - d

            if ( date_now.day == int(time_stamp[8:10]) and int(time_stamp[11:13]) <= date_now.hour ) or  ( yesterday == int(time_stamp[8:10]) and int(time_stamp[11:13]) >= date_now.hour):
                shutil.move(i, dir2)
                #print to python shell
                print ('The following files were moved from FolderA to FolderB.')
                for y in range(len(text_files)):
                    print (i)
                #print to GUI
                self.text_display_filepath.insert('1.0', 'The following file was moved from FolderA to FolderB.')
                for x in range(len(text_files)):
                    self.text_display_filepath.insert('end + 1 lines', ('\n', i))

        dirlistA = os.listdir(dir1)
        print('Source Directory: ', dir1)
        pprint (dirlistA)

        self.text_display_filepath.insert('end + 1 lines', ('\nSource Directory: ', dir1))
        for x in range(len(dirlistA)):
            self.text_display_filepath.insert('end + 1 lines', ('\n', dirlistA[x]))

        dirlistB = os.listdir(dir2)
        print('Destination Directory: ', dir2)
        pprint(dirlistB)

        self.text_display_filepath.insert('end + 1 lines', ('\nDestination Directory: ', dir2))
        for y in range(len(dirlistB)):
            self.text_display_filepath.insert('end + 1 lines', ('\n', dirlistB[y]))


  


    def CloseWindow(self):
        root.quit()


def main():

    root = Tk()
    filemover = File_Mover(root)
    root.mainloop()


if __name__ == "__main__":
    main()

    

