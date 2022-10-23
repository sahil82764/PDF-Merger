import DragDropListbox
import tkinter as tk 
from tkinter import filedialog
import os
from os import listdir, mkdir
from pikepdf import Pdf 

pdfFiles = []

class pdfMergeApp():

    def __init__(self):
        
        self.window = tk.Tk()
        self.window.title("PDF MERGER")
        self.window.geometry("1000x400")

        self.myFrame = tk.Frame(self.window).place(x=100, y=100)
        tk.Label(self.window, text="PDF Merger", font=('Arial', 40, 'bold')).pack()

        self.folderSelectButton = tk.Button(self.window, text="Choose Folder", command= self.folderSelect)
        self.folderSelectButton.pack()

        self.pdfListBox = DragDropListbox.DragDropListbox(self.window, width=60, font=('Arial',15))
        self.pdfListBox.pack()

        self.pdfMergerButton = tk.Button(self.window, text="Merge", command=self.pdfMergeFunction, height=4)
        self.pdfMergerButton.pack()

        self.window.mainloop()

    def pdfMerge(self):
        itemAmount = self.pdfListBox.size()
        fileList = self.pdfListBox.get(0, itemAmount-1)

        fileList = list(fileList)
        files = [self.pdfFolder + "/" + fileName for fileName in fileList]

        pdf = Pdf.new()

        for file in files:
            source = Pdf.open(file)
            pdf.pages.extend(source.pages)

        try:
            os.remove(self.pdfFolder + "/merged/output.pdf")
        except:
            pass

        try:
            mkdir(self.pdfFolder + "/merged")
        except:
            pass

        pdf.save(self.pdfFolder + '/merged/output.pdf')

        tk.Label(self.window, text=f"Successfully Merged at {self.pdfFolder}/merged/output.pdf").pack()

        itemNumber = self.pdfListBox.size()
        self.pdfListBox.delete(0, itemNumber)
        self.pdfListBox.insert('end', 'Merge Successful!')
        self.pdfFolder = ""

    def folderSelect(self):
        self.pdfFolder = filedialog.askdirectory()

        for filename in listdir(self.pdfFolder):
            if filename.endswith('.pdf'):
                pdfFiles.append(filename)

        itemNumber = self.pdfListBox.size()
        self.pdfListBox.delete(0, itemNumber)
        self.pdfListBox.insert('end', *pdfFiles)

        newItemNumber = len(pdfFiles)
        if newItemNumber <=20:
            self.pdfListBox.config(height=newItemNumber)
        else:
            self.pdfListBox.config(height=20)

        tk.Label(self.window, text = f"Listbox updated with pdf files in folder {self.pdfFolder}").pack()

    def pdfMergeFunction(self):
        if len(pdfFiles) == 0:
            itemNumber = self.pdfListBox.size()
            self.pdfListBox.delete(0, itemNumber)
            self.pdfListBox.insert('end', f"No PDF files are present in folder {self.pdfFolder}")
            tk.Label(self.window, text = f"No PDF files are present in folder {self.pdfFolder}").pack()
        else:
            self.pdfMerge()


    