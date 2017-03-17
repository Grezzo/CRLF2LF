#!/usr/bin/env python3

class LF2CRLF:
    
    def __init__(self, file_name):

        self.file_name = file_name
        
        #Open the text file
        with open(self.file_name, "rb") as file:
            self.content = file.read()

        #Check for BOM
        if self.content.startswith(b"\xFF\xFE"): #UTF-16 Little Endian
            self.win_line_end = b"\r\0\n\0"
            self.unix_line_end = b"\n\0"
        elif self.content.startswith(b"\xFE\xFF"): #UTF-16 Big Endian
            self.win_line_end = b"\0\r\0\n"
            self.unix_line_end = b"\0\n"
        else: #UTF-8
            self.win_line_end = b"\r\n"
            self.unix_line_end = b"\n"

        #Check whether content has new line and doesn't contain windows style line ending
        self.unix_endings = (
            self.unix_line_end in self.content and #Check that there is a new line at all
            self.win_line_end not in self.content #Check whether there is not a windows style line ending
        )
        
    def convert(self):
        #Replace line endings if they need to be
        if self.unix_endings:
            self.content = self.content.replace(self.unix_line_end, self.win_line_end)
            self.unix_endings = False

    def save(self):
        with open(self.file_name, "wb") as file:
            file.write(self.content)



if __name__ == '__main__':

    import sys
    import tkinter, tkinter.messagebox
    import subprocess

    #Fire up tkinter, but hide main window
    root = tkinter.Tk()
    root.withdraw()

    converter = LF2CRLF(sys.argv[1])
    
    if converter.unix_endings:
        #Ask user whether to change line endings to windows style
        if tkinter.messagebox.askyesno(
            "Unix line endings detected",
            "Do you want to convert the line endings before opening?",
        ):
            converter.convert()
            try:
                converter.save()
            except PermissionError:
                tkinter.messagebox.showerror(
                    "Could not save file",
                    "Permission Denied",
                )

    #Open file
    subprocess.Popen('Notepad.exe ' + sys.argv[1])

    #Close tkinter
    root.destroy()
