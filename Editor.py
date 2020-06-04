import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog 


class MenuWidget:
	def __init__(self, pwindow):
		font_editex = ("ubuntu", 12)
		menuBar = tk.Menu(pwindow.window, font=font_editex)
		pwindow.window.config(menu=menuBar)

		listdown = tk.Menu(menuBar, font=font_editex, tearoff=0)

		listdown.add_command(label="New File", 
							command = pwindow.NewFile, 
							accelerator="Ctrl+N")
		listdown.add_command(label="Open File", 
							command = pwindow.OpenFile, 
							accelerator="Ctrl+O")
		listdown.add_command(label="Save", 
							command = pwindow.Save, 
							accelerator="Ctrl+S")
		listdown.add_command(label="Save As", 
							command = pwindow.SaveAs, 
							accelerator="Ctrl+Shift+S")

		listdown.add_separator()

		listdown.add_command(label="Exit", 
							command = pwindow.Exit, 
							accelerator="Ctrl+Q")

		aboutdown = tk.Menu(menuBar, font=font_editex, tearoff=0)
		aboutdown.add_command(label="Release Notes", 
							command = self.showReleaseNotesMessage)
		aboutdown.add_separator()
		aboutdown.add_command(label="About", 
							command = self.showAboutMessage)

		menuBar.add_cascade(label="File", menu=listdown)
		menuBar.add_cascade(label="About", menu=aboutdown)

	def showAboutMessage(self):
		boxTitle = "About Editext"
		boxMessage = "A simple Text Editor"
		messagebox.showinfo(boxTitle, boxMessage)
	
	def showReleaseNotesMessage(self):
		boxTitle = "Release Notes"
		boxMessage = "Version - 0.1"
		messagebox.showinfo(boxTitle, boxMessage)

class StatusWidget:
	def __init__(self, pwindow):
		
		font_editex = ("ubuntu", 14)
		self.status = tk.StringVar()
		self.status.set("Editext - 0.1")
		label = tk.Label(pwindow.textspace, fg="black", textvariable=self.status, 
						bg="lightgrey", font=font_editex, anchor='sw')
		label.pack(side=tk.BOTTOM, fill=tk.BOTH)

	def StatusWidgetUpdate(self, *args):
		if isinstance(args[0], bool):
			self.status.set("Your file has been saved!")
		else:
			self.status.set("Editext - 0.1")


class MainSource:
	
	def __init__(self, window):

		self.window = window
		self.filename = None
		window.title("Untitled - Editex")
		window.minsize(650, 500)
		window.geometry('1200x900')
		font_editex = ("ubuntu", 18)
		self.textspace = tk.Text(window, font=font_editex)
		self.scroll = tk.Scrollbar(window, command=self.textspace.yview)
		self.textspace.configure(yscrollcommand=self.scroll.set)
		self.textspace.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
		self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

		self.statusbar = StatusWidget(self)
		self.menubar = MenuWidget(self)

		self.ShortcutKeys()


	def NewFile(self, *args):
		self.textspace.delete(1.0, tk.END)
		self.filename = None
		self.Title_Name(self.filename)

	def Title_Name(self, name_file=None):
		if name_file:
			self.window.title(name_file + " - Editex")
		else:
			self.window.title("Untitled - Editex")

	def OpenFile(self, *args):
		self.filename = filedialog.askopenfilename(
			defaultextension=".txt",
			filetypes = [("All Files", "*.*"), 
						("Text Files", "*.txt"), 
						("CPP files", "*.cpp"),
						("Markdown documents", "*.md"),
						("Java Files", "*.java"),
						("Python Scripts", "*.py"),
						("JavaScript", "*.js"), 
						("C Files", "*.c"),
						("HTML Files", "*.html"),
						("CSS Files", "*.css")]
		)
		if self.filename:
			self.textspace.delete(1.0, tk.END)
			with open(self.filename, "r") as myfile:
				self.textspace.insert(1.0, myfile.read())
			self.Title_Name(self.filename)

	def Save(self, *args):
		if self.filename:
			try:
				textspace_buffer = self.textspace.get(1.0, tk.END)
				with open(self.filename, "w") as myfile:
					myfile.write(textspace_buffer)
		
				self.statusbar.StatusWidgetUpdate(True)
			except Exception as e:
				print(e)
		else:
			self.SaveAs()

	def SaveAs(self, *args):
		try:
			Newfile = filedialog.asksaveasfilename(
				initialfile="Untitled.txt", 
				defaultextension=".txt",
				filetypes = [("All Files", "*.*"), 
							("Text Files", "*.txt"), 
							("CPP files", "*.cpp"),
							("Markdown documents", "*.md"),
							("Java Files", "*.java"),
							("Python Scripts", "*.py"),
							("JavaScript", "*.js"), 
							("C Files", "*.c"),
							("HTML Files", "*.html"),
							("CSS Files", "*.css")]				
			)

			textspace_buffer = self.textspace.get(1.0, tk.END)
			with open(Newfile, "w") as myfile:
				myfile.write(textspace_buffer)
			
			self.statusbar.StatusWidgetUpdate(True)
			self.filename = Newfile
			self.Title_Name(self.filename)

		except Exception as e:
			print(e)

	def Exit(self):
		self.window.destroy()

	def ShortcutKeys(self):
		self.textspace.bind('<Control-n>', self.NewFile)
		self.textspace.bind('<Control-o>', self.OpenFile)
		self.textspace.bind('<Control-s>', self.Save)
		self.textspace.bind('<Control-S>', self.SaveAs)
		self.textspace.bind('<Control-q>', self.Exit)
		self.textspace.bind('<Key>', self.statusbar.StatusWidgetUpdate)


if __name__ == "__main__":
	window =  tk.Tk()
	#window.mi
	Editex = MainSource(window)
	window.mainloop()
	