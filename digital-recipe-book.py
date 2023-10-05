###
#   Digital Recipe Book
#   Written on stream @ twitch.tv/CodeNameTribbs

import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def app():
    # App Functions
    def  getRootPos():
        nonlocal root
        return {
            "x": root.winfo_x(),
            "y": root.winfo_y(),
            "width": root.winfo_width(),
            "height": root.winfo_height()
        }
    
    def menuNewBook():
        nonlocal recipe_book
        nonlocal selected_ingredient
        nonlocal selected_recipe
        recipe_book = {}
        selected_recipe = None
        selected_ingredient = None
        
        updateRecipeList()
        updateCurrentRecipe()

    def menuOpenBook():
        nonlocal recipe_book
        filepath = filedialog.askopenfilename(
            initialdir="./",
            filetypes=[("Recipe Book File (.rbook)", "*.rbook")]
        )
        if filepath:
            with open(filepath, "r") as fo:
                recipe_book = json.load(fo)
            
            updateRecipeList()
    
    def menuSaveBook():
        # TODO test saving funcationality
        nonlocal recipe_book
        filepath = filedialog.asksaveasfilename(
            initialdir="./",
            filetypes=[("Recipe Book File (*.rbook)", "*.rbook")]
        )
        if filepath:
            with open(filepath, "w") as fo:
                json.dump(recipe_book, fo, indent=4)

    def menuPrintToFile():
        pass

    def menuExitApp():
        root.destroy()
        
    def menuIngredientAdd():
        nonlocal root
        window = tk.Toplevel(root)
        window.title("Add Ingredient...")
        r_pos = getRootPos()
        size = f"400x100+{int(r_pos['x'] + r_pos['width']/2) - 200}+{int(r_pos['y'] + r_pos['height']/2) - 50}"
        window.geometry(size)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.grid_columnconfigure(2, weight=1)
        window.grid_columnconfigure(3, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.grid_rowconfigure(2, weight=1)

        # Ingredient
        lbl_ingredient = tk.Label(window, text="Ingrdient")
        lbl_ingredient.grid_propagate(True)
        ent_ingredient = tk.Entry(window)
        ent_ingredient.grid_propagate(True)
        # Amount
        lbl_amount = tk.Label(window, text="Amount")
        lbl_amount.grid_propagate(True)
        ent_amount = tk.Entry(window)
        ent_amount.grid_propagate(True)
        # Units
        lbl_units = tk.Label(window, text="Unit")
        lbl_units.grid_propagate(True)
        ent_units = tk.Entry(window)
        ent_units.grid_propagate(True)
        # Cost
        lbl_cost = tk.Label(window, text="Cost")
        lbl_cost.grid_propagate(True)
        ent_cost = tk.Entry(window)
        ent_cost.grid_propagate(True)
        # Controls Panel
        panel_controls = tk.Frame(window)
        panel_controls.grid_columnconfigure(0, weight=2)
        panel_controls.grid_columnconfigure(1, weight=1)
        panel_controls.grid_rowconfigure(0, weight=1)
        panel_controls.grid_propagate(True)
        # Add Button (Submit)
        btn_add = tk.Button(panel_controls, text="Add Ingredient",
            command=lambda: _addIngredient(window, {"name": ent_ingredient.get(), "amount": ent_amount.get(),
                                            "unit": ent_units.get(), "cost": ent_cost.get()})
        )
        btn_add.grid_propagate(True)
        # Cancel Button
        btn_cancel = tk.Button(panel_controls, text="Cancel", command=window.destroy)
        btn_cancel.grid_propagate(True)

        # pack widgets to window
        lbl_ingredient.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        lbl_amount.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        lbl_units.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
        lbl_cost.grid(row=0, column=3, sticky="nsew", padx=2, pady=2)
        ent_ingredient.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        ent_amount.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
        ent_units.grid(row=1, column=2, sticky="nsew", padx=2, pady=2)
        ent_cost.grid(row=1, column=3, sticky="nsew", padx=2, pady=2)
        btn_add.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        btn_cancel.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        panel_controls.grid(row=2, column=0, columnspan=4, sticky="nsew")
        
    def menuIngredientEdit():
        nonlocal root
        nonlocal selected_ingredient
        
        ingredient_values = current_recipe.item(selected_ingredient[0])['values']
        
        window = tk.Toplevel(root)
        window.title("Edit Ingredient...")
        r_pos = getRootPos()
        size = f"400x100+{int(r_pos['x'] + r_pos['width']/2) - 200}+{int(r_pos['y'] + r_pos['height']/2) - 50}"
        window.geometry(size)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.grid_columnconfigure(2, weight=1)
        window.grid_columnconfigure(3, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.grid_rowconfigure(2, weight=1)

        # Ingredient
        lbl_ingredient = tk.Label(window, text="Ingrdient")
        lbl_ingredient.grid_propagate(True)
        ent_ingredient = tk.Entry(window)
        ent_ingredient.grid_propagate(True)
        ent_ingredient.insert(0, ingredient_values[0])
        # Amount
        lbl_amount = tk.Label(window, text="Amount")
        lbl_amount.grid_propagate(True)
        ent_amount = tk.Entry(window)
        ent_amount.grid_propagate(True)
        ent_amount.insert(0, ingredient_values[1])
        # Units
        lbl_units = tk.Label(window, text="Unit")
        lbl_units.grid_propagate(True)
        ent_units = tk.Entry(window)
        ent_units.grid_propagate(True)
        ent_units.insert(0, ingredient_values[2])
        # Cost
        lbl_cost = tk.Label(window, text="Cost")
        lbl_cost.grid_propagate(True)
        ent_cost = tk.Entry(window)
        ent_cost.grid_propagate(True)
        ent_cost.insert(0, ingredient_values[3])
        # Controls Panel
        panel_controls = tk.Frame(window)
        panel_controls.grid_columnconfigure(0, weight=2)
        panel_controls.grid_columnconfigure(1, weight=1)
        panel_controls.grid_rowconfigure(0, weight=1)
        panel_controls.grid_propagate(True)
        # Add Button (Submit)
        btn_add = tk.Button(panel_controls, text="Update Ingredient",
            command=lambda: _updateIngredient(window, {"name": ent_ingredient.get(), "amount": ent_amount.get(),
                                            "unit": ent_units.get(), "cost": ent_cost.get()})
        )
        btn_add.grid_propagate(True)
        # Cancel Button
        btn_cancel = tk.Button(panel_controls, text="Cancel", command=window.destroy)
        btn_cancel.grid_propagate(True)

        # pack widgets to window
        lbl_ingredient.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        lbl_amount.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        lbl_units.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
        lbl_cost.grid(row=0, column=3, sticky="nsew", padx=2, pady=2)
        ent_ingredient.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        ent_amount.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
        ent_units.grid(row=1, column=2, sticky="nsew", padx=2, pady=2)
        ent_cost.grid(row=1, column=3, sticky="nsew", padx=2, pady=2)
        btn_add.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        btn_cancel.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        panel_controls.grid(row=2, column=0, columnspan=4, sticky="nsew")
        
    def menuIngredientRemove():
        nonlocal selected_ingredient
        nonlocal current_recipe
        nonlocal recipe_book
        nonlocal selected_recipe
        
        #remove the ingredient from the recipe in recipe_book
        index_search = {
            "name": current_recipe.item(selected_ingredient[0])['values'][0],
            "amount": current_recipe.item(selected_ingredient[0])['values'][1],
            "unit": current_recipe.item(selected_ingredient[0])['values'][2],
            "cost": current_recipe.item(selected_ingredient[0])['values'][3]
        }
        ingredient_index = recipe_book[selected_recipe].index(index_search)
        del recipe_book[selected_recipe][ingredient_index]
        
         # delete from treeview
        current_recipe.delete(selected_ingredient)
        
        # set and update
        selected_ingredient = None
        updateCurrentRecipe()

    def menuRecipeNew():
        nonlocal root
        window = tk.Toplevel(root)
        window.title("Add Ingredient...")
        r_pos = getRootPos()
        size = f"250x50+{int(r_pos['x'] + r_pos['width']/2) - 125}+{int(r_pos['y'] + r_pos['height']/2) - 25}"
        window.geometry(size)
        window.geometry("250x50")
        window.resizable(False, False)
        
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=2)
        window.grid_columnconfigure(2, weight=1)
        window.grid_rowconfigure(0, weight=2)
        window.grid_rowconfigure(1, weight=2)
        window.grid_rowconfigure(2, weight=2)
        
        lbl_name = tk.Label(window, text="Recipe Name:")
        ent_name = tk.Entry(window)
        btn_submit = tk.Button(window, text="Submit", command=lambda: _addRecipe(window, ent_name.get()))
        
        lbl_name.grid(row=1, column=0, sticky="nsew", padx=2, pady=5)
        ent_name.grid(row=1, column=1, sticky="nsew", padx=2, pady=5)
        btn_submit.grid(row=1, column=2, sticky="nsew", padx=2, pady=5)

    def menuRecipeRemove():
        nonlocal recipe_book
        nonlocal selected_recipe
        if selected_recipe:
            del recipe_book[selected_recipe]
            selected_recipe = None
            updateRecipeList()

    def updateRecipeList():
        recipes_list.delete(*recipes_list.get_children())
        for recipe in recipe_book:
            recipes_list.insert("", tk.END, values=(recipe,))
    
    def updateCurrentRecipe():
        nonlocal selected_recipe
        nonlocal recipe_book
        nonlocal current_recipe
        nonlocal lbl_current_recipe
        
        current_recipe.delete(*current_recipe.get_children())
        for ingredient in recipe_book[selected_recipe]:
            current_recipe.insert("", tk.END,
                value=(ingredient["name"], ingredient["amount"], ingredient["unit"], ingredient["cost"],)                      
            )
        text = f"Current Recipe: {selected_recipe}"
        lbl_current_recipe.config(text=text)
            
    def onRecipeSelected(event):
        nonlocal selected_recipe
        nonlocal recipe_book
        nonlocal recipes_list
        
        if recipes_list.selection():
            selected_recipe = recipes_list.item(recipes_list.selection()[0])['values'][0]
            updateCurrentRecipe()
            
    def onIngredientSelected(event):
        nonlocal selected_ingredient
        nonlocal recipe_book
        nonlocal current_recipe

        if current_recipe.selection():
            selected_ingredient = current_recipe.selection()
            updateRecipeList()
    
    def _addRecipe(window, recipe):
        nonlocal recipe_book
        recipe_book[recipe] = []
        window.destroy()
        
        updateRecipeList()
    
    def _addIngredient(window, ingredient):
        nonlocal current_recipe
        nonlocal recipe_book
        nonlocal selected_recipe
        
        if ingredient:
            recipe_book[selected_recipe].append(ingredient)
            current_recipe.insert("", tk.END,
                value=(ingredient["name"], ingredient["amount"], ingredient["unit"], ingredient["cost"],)                      
            )
            window.destroy()
    
    def _updateIngredient(window, ingredient):
        nonlocal current_recipe
        nonlocal recipe_book
        nonlocal selected_ingredient
        nonlocal selected_recipe
        
        index_search = {
            "name": current_recipe.item(selected_ingredient[0])['values'][0],
            "amount": current_recipe.item(selected_ingredient[0])['values'][1],
            "unit": current_recipe.item(selected_ingredient[0])['values'][2],
            "cost": current_recipe.item(selected_ingredient[0])['values'][3]
        }
        ingredient_index = recipe_book[selected_recipe].index(index_search)
        
        recipe_book[selected_recipe][ingredient_index] = constructIngredent(
            ingredient["name"],
            ingredient["amount"],
            ingredient["unit"],
            ingredient["cost"]
        )
        
        window.destroy()
        updateCurrentRecipe()
    
    def constructIngredent(name, amount, unit, cost) -> dict:
        ingredient = {
            "name": str(name),
            "amount": str(amount),
            "unit": str(unit),
            "cost": str(cost)
        }
        return ingredient
    
    def setMenuStates():
        #TODO hanfling menu states based on states of app
        pass
        
    # App variables
    recipe_book = {}
    selected_recipe = None
    selected_ingredient = None

    # Main Window
    root = tk.Tk()
    root.title("Recipe Book")
    root.geometry("800x500")
    root.iconbitmap("./py-app-icon.ico")
    root.grid_rowconfigure(1, weight=1)
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
    lbl_current_recipe = tk.Label(root, text="Selected Recipe:")
    lbl_current_recipe.grid_propagate(True)
    
    recipes_list = ttk.Treeview(
        panel_recipes_list, 
        columns=("recipes"), 
        show="headings", 
        selectmode="browse"
    )
    recipes_list.heading("recipes", text="Recipe Book")
    
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
    current_recipe.bind("<<TreeviewSelect>>", onIngredientSelected)
    
    # Pack widgets to their panels    
    recipes_list.pack(fill=tk.BOTH, expand=True)
    current_recipe.pack(fill=tk.BOTH, expand=True)
    
    # Pack panels to main window
    lbl_current_recipe.grid(sticky="sw", row=0, column=1, padx=2, pady=2)
    panel_recipes_list.grid(sticky="nsew", row=1, column=0, padx=2, pady=2)
    panel_current_recipe.grid(sticky="nsew", row=1, column=1, padx=2, pady=2)
    
    setMenuStates()
    root.mainloop()
    
    
if __name__ == "__main__":
    app()