"""
Equipment and Inventory UI component
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from ...models.character.base import Character
from ...models.equipment.base import InventoryItem
from ..dialogs.add_item_dialog import AddItemDialog

class EquipmentWidget(ttk.Frame):
    """Widget for managing equipment and inventory"""

    def __init__(self, parent, character: Character, on_change: Optional[Callable] = None):
        super().__init__(parent)
        self.character = character
        self.on_change = on_change
        self.setup_ui()

    def setup_ui(self):
        """Set up the equipment and inventory UI"""
        # Title
        title_label = ttk.Label(self, text="Equipment & Inventory", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))

        # Currency
        self.create_currency_frame()

        # Inventory
        self.create_inventory_frame()
        self.update_inventory_list()

    def create_currency_frame(self):
        """Create the frame for currency management"""
        currency_frame = ttk.LabelFrame(self, text="Currency")
        currency_frame.pack(fill=tk.X, pady=5)

        # Gold (GP)
        gp_frame = ttk.Frame(currency_frame)
        gp_frame.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(gp_frame, text="GP:").pack(side=tk.LEFT)
        self.gp_var = tk.IntVar(value=0) # Placeholder
        gp_entry = ttk.Entry(gp_frame, textvariable=self.gp_var, width=8)
        gp_entry.pack(side=tk.LEFT)

        # Silver (SP)
        sp_frame = ttk.Frame(currency_frame)
        sp_frame.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(sp_frame, text="SP:").pack(side=tk.LEFT)
        self.sp_var = tk.IntVar(value=0) # Placeholder
        sp_entry = ttk.Entry(sp_frame, textvariable=self.sp_var, width=8)
        sp_entry.pack(side=tk.LEFT)

        # Copper (CP)
        cp_frame = ttk.Frame(currency_frame)
        cp_frame.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(cp_frame, text="CP:").pack(side=tk.LEFT)
        self.cp_var = tk.IntVar(value=0) # Placeholder
        cp_entry = ttk.Entry(cp_frame, textvariable=self.cp_var, width=8)
        cp_entry.pack(side=tk.LEFT)

    def create_inventory_frame(self):
        """Create the frame for the inventory list"""
        inventory_frame = ttk.LabelFrame(self, text="Inventory")
        inventory_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("name", "quantity", "weight")
        self.inventory_tree = ttk.Treeview(inventory_frame, columns=columns, show="headings")
        self.inventory_tree.heading("name", text="Item")
        self.inventory_tree.heading("quantity", text="Qty")
        self.inventory_tree.heading("weight", text="Weight (lbs)")
        self.inventory_tree.column("quantity", width=50, anchor=tk.CENTER)
        self.inventory_tree.column("weight", width=80, anchor=tk.E)

        self.inventory_tree.pack(fill=tk.BOTH, expand=True)

        # Add/Remove buttons
        button_frame = ttk.Frame(inventory_frame)
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Add Item", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Item", command=self.remove_item).pack(side=tk.LEFT, padx=5)

    def add_item(self):
        dialog = AddItemDialog(self)
        if dialog.item:
            inventory_item = InventoryItem(equipment=dialog.item, quantity=dialog.quantity_var.get())
            self.character.equipment.append(inventory_item)
            self.update_inventory_list()

    def remove_item(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            return

        item_name = self.inventory_tree.item(selected_item, "values")[0]
        
        # Find and remove the item from the character's equipment list
        for item in self.character.equipment:
            if item.equipment.name == item_name:
                self.character.equipment.remove(item)
                break
        
        self.update_inventory_list()

    def update_inventory_list(self):
        # Clear existing items
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)

        # Add items from character data
        for item in self.character.equipment:
            self.inventory_tree.insert("", tk.END, values=(
                item.equipment.name,
                item.quantity,
                item.total_weight
            ))
