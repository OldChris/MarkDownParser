#
#  system modules
#
import os
import tkinter as tk
import webbrowser
from tkinterweb import HtmlFrame
#
# my modules
#
import markdownhtml as mdhtml

def load_new_page(url):
    print("clicked on ", url)
    webbrowser.open(url)
#
# Create the main window
window = tk.Tk()
# place the HtmlFrame
thehtmlframe = HtmlFrame(window, on_link_click=load_new_page) 
thehtmlframe.pack(fill="both", expand=True)
#
# make full file paths
md_file=os.path.join(os.getcwd(), 'test.md')
html_file=os.path.join(os.getcwd(), 'test.html')
# convert md to html
mdhtml.markdown2html(md_file, html_file)
# display the result    
thehtmlframe.load_file(html_file) 
#
# Start the Tkinter event loop
window.mainloop()
#



