import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import subprocess
import webbrowser

home_dir =os.getenv("HOME") + "/wellnessapp/" 
  
window = tk.Tk()
 
window.title("AkaTracker")
window.minsize(250,250)
 
def clickMe():
   #status, output = os.system("python3 "+ script)
   if os.system("python3 "+ home_dir+"plot_chart.py") == 0:
   	stat = webbrowser.get('open -a /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome %s').open_new_tab(home_dir+'index2.html')
   	if stat:
   		exit(0)
   	else :
   		messagebox.showerror("ERROR", "Could not open webpage")
   else:
   	messagebox.showerror("ERROR", "Plot graph did not run succeessfully")

output = subprocess.check_output("id -F", shell=True)
#print(output.decode("utf-8"))
l = Label(window, text = "Hello "+output.decode("utf-8").strip() + "!")
l.config(font =("Courier", 24))
l.pack() 
   
button = Button(window, text = "Show me some stats", command = clickMe,height = 5, width = 15)
#button.grid(column= 0, row = 2)
button.pack()
 
window.mainloop()