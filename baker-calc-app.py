###
#   Baking/Cooking Calculator App
#   Written on stream @ twitch.tv/CodeNameTribbs

import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
    
class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.recipe_book = None
        
        # Main window configuration
        self.title('Recipe Calculator')
        self.geometry("800x500")
        self.iconbitmap('./py-app-icon.ico')
        
        # Creating the menu bar
        self.menubar = tk.Menu(self)
        
        # Create the main window frame
        self._frame = None
        self.switchFrame(FrameListRecipes)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # File menu
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New", command=lambda: self.menubarFileNew())
        filemenu.add_command(label="Open", command=lambda: self.menubarFileOpen())
        filemenu.add_command(label="Save", command=lambda: self.menubarFileSave())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=lambda: self.closeApp())
        self.menubar.add_cascade(label="File", menu=filemenu)
        
        self.config(menu=self.menubar)

        # Recipe Book
        self.recipe_book = None
        
    def switchFrame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky="nsew")  
        if isinstance(self._frame, FrameListRecipes):
            self._frame.updateRecipeBook(self.recipe_book)
            
    def menubarFileNew(self):
        print("File > New > Clicked")
        
    def menubarFileOpen(self):
        print("File > Open > Clicked")
        # Prompt user for an rbook file
        filepath = filedialog.askopenfilename(
            initialdir="./",
            filetypes=[("Recipe Book Files", "*.rbook")]
        )
        
        # if a file was selected, open and load file into memory
        if filepath:
            with open(filepath, 'r') as fo:
                self.recipe_book = json.load(fo)
        # switch frame view to Recipes View
        self.switchFrame(FrameListRecipes)
        
    def menubarFileSave(self):
        print("File > Save > Clicked")
    
    def  closeApp(self):
        self.destroy()
        
class FrameListRecipes(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title('Recipe List')
        
        self.recipe_book = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        # panel frames
        self.panel_recipe_list = tk.Frame(self)
        self.panel_recipe_text = tk.Frame(self)
        
        self.panel_recipe_list.grid_propagate(True)
        self.panel_recipe_text.grid_propagate(True)
        
        self.panel_controls = tk.Frame(self)
        self.panel_controls.grid_columnconfigure(0, weight=1)
        self.panel_controls.grid_columnconfigure(1, weight=1)
        self.panel_controls.grid_columnconfigure(2, weight=1)
        self.panel_controls.grid_columnconfigure(3, weight=1)
        self.panel_controls.grid_columnconfigure(4, weight=1)
        
        # widgets
        self.treeview_recipes_list = ttk.Treeview(self.panel_recipe_list, columns=("recipes"),
                                                       show="headings", selectmode="browse")
        self.treeview_recipes_list.heading("recipes", text="Recipes")
        
        self.treeview_selected_recipe = ttk.Treeview(self.panel_recipe_text,
                                                columns=("ingredient", "amount", "units", "cost"),
                                                show="headings", selectmode="none")
        self.treeview_selected_recipe.heading("ingredient", text="Ingredient")
        self.treeview_selected_recipe.heading("amount", text="Amount")
        self.treeview_selected_recipe.heading("units", text="Units")
        self.treeview_selected_recipe.heading("cost", text="Cost")
        self.treeview_selected_recipe.column('ingredient', width=80)
        self.treeview_selected_recipe.column('amount', width=10)
        self.treeview_selected_recipe.column('units', width=10)
        self.treeview_selected_recipe.column('cost', width=10)
        
        self.button_adj_yield = tk.Button(self.panel_controls, text="Adjust Yeild", width=20,
                                    command=lambda: self.btnAdjYield())  
        self.button_new_recipe = tk.Button(self.panel_controls, text="New Recipe", width=20, 
                                    command=lambda: self.btnNewRecipe())
        self.button_edit_recipe = tk.Button(self.panel_controls, text="Edit Recipe", width=20,
                                    command=lambda: self.btnEditRecipe())
        self.button_printout = tk.Button(self.panel_controls, text="Print to File", width=20,
                                    command=lambda: self.btnPrintToFile())
        self.button_remove_recipe = tk.Button(self.panel_controls, text="Remove Recipe", width=20,
                                    command=lambda: self.btnRemoveRecipe())
        
        # placeholder items
        items = [("Item 1",), ("Item 2",), ("Item 3",), ("Item 4",), ("Item 5",)]
        for item in items:
            self.treeview_recipes_list.insert("", tk.END, values=item)
        
        self.treeview_recipes_list.pack(fill=tk.BOTH, expand=True)
        self.treeview_selected_recipe.pack(fill=tk.BOTH, expand=True)
        
        self.button_adj_yield.grid(row=0, column=0)
        self.button_new_recipe.grid(row=0, column=1)
        self.button_edit_recipe.grid(row=0, column=2)
        self.button_printout.grid(row=0, column=3)
        self.button_remove_recipe.grid(row=0, column=4)
        
        # pack the panels into the main frame
        self.panel_recipe_list.grid(sticky='nsew', row=0, column=0, rowspan=2, padx=2, pady=2)
        self.panel_recipe_text.grid(sticky='nsew', row=0, column=1, padx=2, pady=2)
        self.panel_controls.grid(sticky='nsew', column=1, row=1, padx=2, pady=2)
        
        # Event Binds
        self.treeview_recipes_list.bind('<<TreeviewSelect>>', self.onRecipeSelected)
        
    def btnAdjYield(self):
        print("Button Click >> Adjust Yield")
        
    def btnNewRecipe(self):
        print("Button Click >> New Recipe")
    
    def btnEditRecipe(self):
        print("Button Click >> Edit Recipe")
    
    def btnPrintToFile(self):
        print("Button Click >> Print To File")
        
    def btnRemoveRecipe(self):
        print("Button Clicked >> Remove Recipe")
    
    def updateRecipeBook(self, rbook=None):
        self.recipe_book = rbook
        if self.recipe_book:
            self.treeview_recipes_list.delete(*self.treeview_recipes_list.get_children())
            for recipe in self.recipe_book:
                self.treeview_recipes_list.insert("", tk.END, values=(recipe,))
    
    def onRecipeSelected(self, event):
        selected_item = self.treeview_recipes_list.selection()[0]
        self.updateRecipeView(self.treeview_recipes_list.item(selected_item)['values'][0])
    
    def updateRecipeView(self, recipe):
        self.treeview_selected_recipe.delete(*self.treeview_selected_recipe.get_children())
        for ingredient in self.recipe_book[recipe]:
            print(ingredient)
            self.treeview_selected_recipe.insert("", tk.END, 
                values=(ingredient['name'], ingredient['amount'], ingredient['unit'], ingredient['cost'],)
            )
            
    
class FrameEditRecipe(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("Edit Recipe")
        

if __name__ == "__main__":
    app = Application()
    app.mainloop()