import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from natsort import natsorted
from send2trash import send2trash

class FileMerge:
    def __init__(self, folder_paths):
        self.folder_paths = folder_paths
        self.folder_path = None
        self.index = 1

    def renamefiles_folder(self, folder_name, check_var):
        #Create a new folder named folder_name
        self.folder_name = folder_name
        parent_path = os.path.dirname(self.folder_paths[0])
        new_path = os.path.join(parent_path, self.folder_name)
        #Check if folder name was entered
        if not self.folder_name:
            messagebox.showwarning(
                "Warning",
                "Please enter a folder name"
            )
            return
        #Check if same name exists
        if os.path.exists(new_path):
            messagebox.showwarning(
                "Warning",
                "The folder already exists"
            )
            return
        else:
            os.makedirs(new_path)
        try:
            index = 1
            for folder_path in self.folder_paths:
                files = natsorted(os.listdir(folder_path))
                
                for file in files:
                    file_path = os.path.join(folder_path, file)
                    # Ignore if there is a folder
                    if os.path.isfile(file_path):
                        extension = os.path.splitext(file)[1]
                        new_file_path = os.path.join(new_path, f"{index}{extension}")
                        shutil.copy2(file_path , new_file_path)
                        index += 1
            if check_var:
                self.deletefolder()
            return True
        except Exception as e:
            #Error message
            print(e)
            return False
    
    def deletefolder(self):
            for folder_path in self.folder_paths:
                # Path name renamed for correct OS
                folder_path = os.path.normpath(folder_path)
                if os.path.exists(folder_path):
                    send2trash(folder_path)
    #Reset 
    def reset(self):
        self.folder_paths.clear()
        self.folder_name = None
        
folders2 = []
merge = FileMerge(folders2)

# UI implimentation with tk
appUI = tk.Tk()
appUI.title("Folder Merge and relist")
appUI.minsize(750, 70)

row2 = tk.Frame(appUI)
row2.pack(fill="x", padx=5, pady=5)

Name_entry = tk.Entry(row2, width = 50)
Name_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(5, 0)
)

check_var = tk.BooleanVar()

checkbox = tk.Checkbutton(
    row2,
    text="Delete original folders after merge",
    variable=check_var
)
checkbox.pack(
    side="left",
    padx=(5, 0)
)

def Merge_button():
    success = merge.renamefiles_folder(Name_entry.get(), check_var.get())
    if success:
        #If merge is success, reset all
        reset_ui()
        merge.reset()

#Reset UI
def reset_ui():
    check_var.set(False)
    Name_entry.delete(0, tk.END)
    for row in folder_entries:
        row.destroy()
    folder_entries.clear()
    folders2.clear()
    add_folder_row()

button = tk.Button(
    row2,
    text = "Merge",
    width=10,
    command = Merge_button
)
button.pack(side="left", padx=15)

button = tk.Button(
    row2,
    text = "Reset",
    width=10,
    # Both reset Methods
    command = lambda: (reset_ui(), merge.reset())
)
button.pack(side="left", padx=15)

folder_entries = []

def add_folder_row(folder_path = ""):
        #New row added
        row = tk.Frame(appUI)
        row.pack(fill="x", padx=3, pady=2, before=row2)
        #New Entry added 
        folder_entry = tk.Entry(row, width = 60)
        folder_entry.pack( side="right", fill="x", expand=True, padx=(5, 0))
        folder_entries.append(row)
        def select_folder():
            folder_path = filedialog.askdirectory()
            if folder_path:
                folder_entry.insert(0, folder_path)
                folders2.append(folder_path)
                add_folder_row(folder_path)
        #New Button added
        select_button = tk.Button(row,text="Select Folder",command= select_folder)
        select_button.pack(side="left")

# Initialize row
add_folder_row()

appUI.mainloop()

# Note: Below method modifies the original files directly.
# It does not create copies.

# def renamefiles(self):
#     files = natsorted(os.listdir(self.folder_path))
#     temp_files = []
#     for index,file in enumerate(files, start = 1):
#         old_path = os.path.join(self.folder_path, file)
#         if os.path.isfile(old_path):
#             extension = os.path.splitext(file)[1]
#             temp_name = f"__temp_{uuid.uuid4().hex}{extension}"
#             temp_path = os.path.join(self.folder_path, temp_name)
#             os.rename(old_path, temp_path)
#             temp_files.append(temp_path)
#     for index,file in enumerate(temp_files, start = 1):
#         extension = os.path.splitext(file)[1]
#         new_path = os.path.join(self.folder_path, f"{index}{extension}")
#         os.rename(file, new_path)