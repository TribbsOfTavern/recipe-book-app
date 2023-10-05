###
#   Digital Recipe Book
#   Written on stream @ twitch.tv/CodeNameTribbs

import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def app():
    # App Functions
    def menuNewBook():
        pass

    def menuOpenBook():
        nonlocal recipe_book
        filepath = filedialog.askopenfilename(
            initialdir="./",
            filetypes=[("Recipe Book File (.rbook)", "*.rbook")]
        )
        if filepath:
            with open(filepath, "r") as fo:
                recipe_book = json.load(fo)
            
            onRecipeLoaded()
    
    def menuSaveBook():
        pass

    def menuPrintToFile():
        pass

    def menuExitApp():
        root.destroy()
        
    def menuIngredientAdd():
        pass

    def menuIngredientEdit():
        pass

    def menuIngredientRemove():
        pass

    def menuRecipeNew():
        pass

    def menuRecipeRemove():
        pass

    def onRecipeLoaded():
        recipes_list.delete(*recipes_list.get_children())
        for recipe in recipe_book:
            recipes_list.insert("", tk.END, values=(recipe,))
    
    def onRecipeSelected(event):
        nonlocal recipe_book
        nonlocal recipes_list
        nonlocal current_recipe
        selected_recipe_id = recipes_list.selection()[0]
        recipe = recipes_list.item(selected_recipe_id)['values'][0]
        current_recipe.delete(*current_recipe.get_children())
        for ingredient in recipe_book[recipe]:
            current_recipe.insert("", tk.END,
                value=(ingredient["name"], ingredient["amount"], ingredient["unit"], ingredient["cost"],)                      
            )
    
    # App variables
    recipe_book = None
    selected_recipe = None
    
    # Main Window
    root = tk.Tk()
    root.title("Recipe Book")
    root.geometry("800x500")
    root.iconbitmap("./py-app-icon.ico")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=4)
    
    # Menubar
    menubar = tk.Menu()
    
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New Book", command=menuNewBook)
    filemenu.add_command(label="Open Book", command=menuOpenBook)
    filemenu.add_command(label="Save Book", command=menuSaveBook)
    filemenu.add_separator()
    filemenu.add_command(label="Print To File", command=menuPrintToFile)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=menuExitApp)
    
    recipemenu = tk.Menu(menubar, tearoff=0)
    recipemenu.add_command(label="Add Ingredient", command=menuIngredientAdd)
    recipemenu.add_command(label="Edit Ingredient", command=menuIngredientEdit)
    recipemenu.add_command(label="Remove Ingredient", command=menuIngredientRemove)
    recipemenu.add_separator()
    recipemenu.add_command(label="New Recipe", command=menuRecipeNew)
    recipemenu.add_command(label="Remove Recipe", command=menuRecipeRemove)
    
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Recipe", menu=recipemenu)
    
    root.config(menu=menubar)
    
    # panel frames
    panel_recipes_list = tk.Frame(root)
    panel_recipes_list.grid_propagate(True)
    
    panel_current_recipe = tk.Frame(root)
    panel_current_recipe.grid_propagate(True)
    
    # widgets
    recipes_list = ttk.Treeview(
        panel_recipes_list, 
        columns=("recipes"), 
        show="headings", 
        selectmode="browse"
    )
    recipes_list.heading("recipes", text="Recipes")
    
    current_recipe = ttk.Treeview(
        panel_current_recipe, 
        columns=("ingredients", "amount", "units", "cost"),
        show="headings",
        selectmode="browse"
    )
    current_recipe.heading("ingredients", text="Ingredient")
    current_recipe.heading("amount", text="Amount")
    current_recipe.heading("units", text="Units")
    current_recipe.heading("cost", text="Cost")
    current_recipe.column("ingredients", width=80)
    current_recipe.column("amount", width=10)
    current_recipe.column("units", width=10)
    current_recipe.column("cost", width=10)
    
    # Widget Event Binds
    recipes_list.bind("<<TreeviewSelect>>", onRecipeSelected)
    
    # placeholder items for startup
    items = [("Item 1"), ("Item 2"), ("Item 3"), ("Item 4"), ("Item 5")]
    for item in items:
        recipes_list.insert("", tk.END, values=item)
    
    # Pack widgets to their panels    
    recipes_list.pack(fill=tk.BOTH, expand=True)
    current_recipe.pack(fill=tk.BOTH, expand=True)
    
    # Pack panels to main window
    panel_recipes_list.grid(sticky="nsew", row=0, column=0, padx=2, pady=2)
    panel_current_recipe.grid(sticky="nsew", row=0, column=1, padx=2, pady=2)
    
    root.mainloop()
    
    
if __name__ == "__main__":
    app()