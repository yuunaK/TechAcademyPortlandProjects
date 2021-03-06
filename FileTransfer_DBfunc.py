#Item 62 PyDrill_DBfunctionality_34_IDLE (Add Database functionality
#to GUI File Transfer application.
#Python Course, The Tech Academy (Portland, OR)
#Yuuna Kaparti



from tkinter import *
import tkinter as tk
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

import sqlite3



#Create a class and accept a Tk object which is primary enclosing Tk frame that will
#hold all the other widgets.  So "Frame" is a parameter which will store the instance
#of Tk we created in the main function, root.
class File_Mover(Frame):

    #constructor function which will create an instance of the File_Mover Class. The
    #constructor function is always created using the def __init___ syntax.
    #This constructor function is an attribute method of the class File_Mover.
    #The first argument,'self', the constructor will take will be an instance of the
    #class File_Mover. The next argument, 'master', is a parameter that will accept
    #the Tk object ('root'), that has been passed to the class File_Mover. The last
    #two arguments allow the function to accept a variable length list of arguments.
    #The first parameter, '*args', allows us to accept non-keyworded arguments.
    #"**kwargs" allows us to accept keyworded arguments.
    def __init__(self, master, *args, **kwargs):

        #This is a constructor function for the Tk object passed into the class File_Mover.
        #We are inside of the class constructor function.  But before we can populate
        #the frame, we need to create it using the frame constructor function.
        Frame.__init__(self, master, *args, **kwargs)

        #we are configuring the Tk() object that has been passed to class File_Mover.
        master.title("Check for Newly Created and Modified Files")
        master.resizable(True, True)
        master.configure(background = '#ffffff')

        #configure the class object.  'self.' prefix is a reference to the object that
        #will have these characteristics and properties of class File_Mover.
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#ffffff')
        self.style.configure('TButton', background = '#ffffff')
        self.style.configure('TLabel', background = '#ffffff')



        #The root Tk() object will have three frames.  Each frame will be placed into
        #the Tk() master (parent) object using the pack geometry manager. The pack geometry
        #manager has the following options: fill (X, Y, BOTH), expand (True, False), side
        #(LEFT, RIGHT,TOP, BOTTOM, CENTER), anchor (like the grid and geometry manager's
        #sticky option; takes compass directios: n, s, e, w, ns, ew, ne, nw, se, sw, nsew),
        #padx/padyy (set pixel padding outside widget, ipadx/ipady(padding space in pixels
        #inside widget). The first frame contains one label widget, two entry widgets and
        #two button widgets.
        self.frame1 = ttk.Frame(master)
        self.frame1.pack(fill = X)

        self.label1 = ttk.Label(self.frame1, text = "Click on button to select the source and destination directory.")
        self.label1.grid(row = 0, column = 0, columnspan = 2, sticky = 'sw')

        self.entry1 = ttk.Entry(self.frame1, width = 50)
        self.entry1.grid(row = 1, column = 0)
        
        self.entry2 = ttk.Entry(self.frame1, width = 50)
        self.entry2.grid(row = 2, column = 0)
        
        #The two button widgets use a lambda function.  The option 'command' is typically used for
        #function calls.  But sometimes it is necessary to write a brief programming statement for
        #the command.  The keyword 'lambda' is used to facilitate this task.  The names / variables
        #for the entry widgets are passed in the function call.  When making the function call, it
        #is prefixed with the 'self.' so that the compiler knows to go to the function in the class
        #called Select_Directory.
        self.button_sourceDirectory = ttk.Button(self.frame1, text = "Source Directory", width = 15, command = lambda: self.Select_Directory(self.entry1))
        self.button_sourceDirectory.grid(row = 1, column = 1, sticky = 'w', padx = 40, pady = 5)
        
        self.button_destinationDirectory = ttk.Button(self.frame1, text = "Destination Dir..", width = 15, command = lambda: self.Select_Directory(self.entry2))
        self.button_destinationDirectory.grid(row = 2, column = 1, sticky = 'w', padx = 40, pady = 5)


        #Second Frame:The following code creates the second frame and the
        #widgets it contains: one label widget, one text widget (not themed
        #tkinter object, ttk), scrollbar.
        self.frame2 = ttk.Frame(master)
        self.frame2.pack(ipadx = 5, ipady = 10)
        
        self.label2 = ttk.Label(self.frame2, text = "Files that have been moved:")
        self.label2.grid(row = 0, column = 0, columnspan = 2, sticky = 'sw', pady = 5)

        self.text_display_filepath = Text(self.frame2, width = 70, height = 10)
        self.text_display_filepath.grid(row = 1, column = 0, columnspan = 2)

        self.text_scrollbar = ttk.Scrollbar(self.frame2, orient = VERTICAL)
        self.text_scrollbar.grid(row = 1, column = 2, sticky = 'w' + 'ns')

        self.text_display_filepath.config(yscrollcommand = self.text_scrollbar.set)
        self.text_scrollbar.config(command = self.text_display_filepath.yview)



        #Third Frame: The third frame contains one label widget, one entry widget, and two
        #button widgets.  The third frame contains the critical button that makes the
        #function call to the function CheckFiles_Button.
        self.frame3 = ttk.Frame(master)
        self.frame3.pack(ipady = 10, fill = X)

        self.label3 = ttk.Label(self.frame3, text = "Date and Time of Last File Check: ")
        self.label3.grid(row = 0, column = 0, sticky = 'w' + 'sw')

        self.entry3 = ttk.Entry(self.frame3, width = 30)
        self.entry3.grid(row = 1, column = 0, sticky = 'w')

        self.button_CloseWindow = ttk.Button(self.frame3, text = 'Close', width = 15, command = lambda: self.Close_Window(*args, **kwargs))
        self.button_CloseWindow.grid(row = 1, column = 3, sticky = 'e', padx = 50)

        self.button_checkFiles = ttk.Button(self.frame3, text = 'Check Files', width = 15, command = lambda: self.CheckFiles_Button())
        self.button_checkFiles.grid(row = 1, column = 4, sticky = 'w', padx = 10)




    #The Select_Directory function implements a popup filedialog box that allows users
    #to select a directory.  The Select_Directory function takes two arguments:
    #an instance of the class when module is run as well as a entry widget.  options is
    #first declared as an empty dictionary. It is then populated with the options and values
    #filedialog.askdirectory requires.  The function call for filedialog.askdirectory takes the
    #dictionary variable 'options' with two asterisk inside the parenthesis.  The value that is
    #generated by the filedialog is saved to a variable, 'directory'. We use this filepath
    #information to populate the entry widget. The first argument in the insert method is for
    #the index in the entry widget where the string should be inserted. The second argument is
    #the filepath for the directory.
    def Select_Directory(self, entryWidget):
        options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = True
        options['parent'] = self.frame1
        options['title'] = 'Select Directory'

        directory = filedialog.askdirectory(**options)
        entryWidget.insert(0, directory)


    def CheckFiles_Button(self):
        #get values stored in entry widgets: source directory and destination directory
        #replace the single forward slash with double forward slash for the python interpreter
        #The filepaths stored in variables 'dir1' and 'dir2' are exclusively a filepath to the
        #two directories.  They cannot be used to select text files from the source directory.
        dir1 = self.entry1.get()
        dir1 = dir1.replace("/", "//")
        dir2 = self.entry2.get()
        dir2 = dir2.replace("/", "//")
        #create a new variable that selects all the files with .txt extension in source directory
        #to select all the files with '.txt' extension, the filepath stored in "dir1" is concatenated
        #the string "//*.txt"
        #The two forward slashes are required by the interpreter. The slash separetes each directory level.
        #The asterisk (*) is a wildcard operator that will select all the files in source directory which
        #has the .txt extension.
        dirText = dir1 + "//*.txt"
        #create a list variable to store all the .txt files in the source directory using the glob module's
        #glob method.
        text_files = glob.glob(dirText)
        #create a variable to store the current date and time.  Note: date_now is an instance of
        #datetime class (that is, it is an object) and we can use methods on date_now such as
        #'date_now.hour', 'date_now.day' etc to return int values.
        date_now = datetime.datetime.now()
        Current_FileCheck = str(date_now)
        #function call to store current filecheck date and time
        self.Date_Time_DB(Current_FileCheck)
        Last_FileCheck = self.entry3.get()
       


        for i in text_files:
            #for each text file in text_files, get the time stamp.
            doc_time_stamp = os.path.getmtime(i)
            #convert time stamp into a string with date and time information. Use string slice method to retrieve
            #relevant portions of the string.
            time_stamp = time.ctime(doc_time_stamp)
            #use timedelta to set the time offset/difference.  We are setting timedelta to 1 day (24 hours).
            #d = timedelta(hours = 24)
            #create a variable to store yesterday's date. This is different from taking date_now.day - 1 since we may
            #get an inaccurate result.  If first day of month is 1, then date_now.day will be 1 and 1 minus 1 will give 0.
            #But, the correct result is last day of preceding month.
            #yesterday = date_now - d

            if ( int(time_stamp[8:10]) <= date_now.day and int(time_stamp[11:13]) <= date_now.hour and int(time_stamp[14:16]) <= date_now.minute) or  ( int(Last_FileCheck[9:11]) <= int(time_stamp[8:10]) and int(Last_FileCheck[12:14]) <= int(time_stamp[11:13]) and int(Last_FileCheck[15:17]) <= int(time_stamp[14:16])  ):
                shutil.move(i, dir2)
                #print to python shell
                print ('The following files were moved from FolderA to FolderB.')
                print (i)
                #print to GUI
                self.text_display_filepath.insert('1.0', 'The following file was moved from FolderA to FolderB.')
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




    def Date_Time_DB(self, dtInfo):
        conn = sqlite3.connect('db_DateTime.db')
        with conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS tbl_DateTime ( \
                        ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                        col_DateTime); ")
            #This statement inserts values into the table dynamically using a variable.
            #Use keywords INSERT INTO, provide table name and column name and after
            #keyword VALUES, use question marks as placeholder for a variable.
            #Enclose the SQL query in quotes, use a comma and provide teh variable that
            #will fill the question mark field in parenthesis, make sure to use a comma
            #to make sure that dtInfo is treated as a single unit instead of as a string
            #sequence with every element in the string representing a binding value.
            #From stackoverflow.com sqlite3.ProgrammingError:Incorrect number of bindings
            #"You need to pass in a sequence, but you forgot the
            #comma to make your parameters a tuple:
            #cursor.execute('INSERT INTO images VALUES(?)', (img,))
            #Without the comma, (img) is just a grouped expression, not a tuple and thus
            #the 'img' string is treated as the input sequence. If that string is 74
            #characters long, then Python sees that as 74 separate bind values, each
            #one character long.
            cur.execute("INSERT INTO tbl_DateTime (col_DateTime) VALUES (?) ", (dtInfo,))
            
            #for loop that inserts the row immediately preceding the last row.  Each row in
            #the table stores an id and a datetime string.
            for row in cur.execute("SELECT col_DateTime FROM tbl_DateTime \
                               WHERE ID = (SELECT MAX (ID) FROM tbl_DateTime) - 1; "):
                #assigns the datetime string in row to variable x
                x = row
                #prints the datetime string into the entry widget which notifies users
                #of date and time of last file check
                self.entry3.insert(0, x)
                print (x)

            #commits the changes to the table and closes the cursor connection
            conn.commit()
            cur.close()

        #closes the connection to the database.
        conn.close()
    



    #Closes the window of the File_Mover application. In order for this function to work propertly,
    #I had to import from tkinter the tk module.  The tk module is distinct from the ttk module.
    #Using *args allows a variable length for the list of arguments passed to the function.  Useful
    #because if you multiple objects that need to be closed.
    def Close_Window(self, *args):
        #This is a nice ready made popup box that asks the user for input. Depending on user selection
        #the application will return control to the File_Mover application or quit the application,
        #destroy the objects that were created when the program was executed and returns control to
        #the operating system.
        if messagebox.askokcancel("Exit program", "Okay to exit application?"):
            self.quit()
            self.destroy()
            os._exit(0)

        

#Main function.  Create a Tk object,an instance of the Tk class, and store it in the variable
#location identified by "root".  Create an instance of the File_Mover class and store it
#in the variable location called 'filemover'.  When creating a File_Mover object, pass it
#a Tk object, 'root'.  By doing this, we will be creating a composition of classes / objects:
#we make a Tk object and also a File_Mover object. We create a Tk object and pass it to the
#File_Mover class.
#Question: what is the relationship between the File_Mover object and the Tk object.  Does the
#File_Mover object encapsulate and contain the Tk object or is it the other way around - i.e.
#the Tk object contains and encapsulates the File_Mover object?
#Once the Tk object 'root' has been created we run the mainloop method on it so that the Python
#interpreter keeps repeating the steps in the main function until we exit out of the script using
#Close_Window function.
def main():

    root = Tk()
    filemover = File_Mover(root)
    root.mainloop()

#This if statement tells the Python interpreter that if there is a function named main in
#this script, start at that main function.
if __name__ == "__main__":
    main()

    

