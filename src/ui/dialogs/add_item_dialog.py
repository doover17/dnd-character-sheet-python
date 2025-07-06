"""
Dialog for adding a new item to the inventory.
"""
import tkinter as tk
from tkinter import ttk
from ...models.equipment.base import Equipment, EquipmentType

class AddItemDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add New Item")
        self.item = None

        self.name_var = tk.StringVar()
        self.type_var = tk.StringVar(value=EquipmentType.ADVENTURING_GEAR.value)
        self.quantity_var = tk.IntVar(value=1)
        self.weight_var = tk.DoubleVar(value=0.0)

        self.create_widgets()
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)

    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Name
        ttk.Label(frame, text="Item Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, sticky=tk.EW, pady=2)

        # Type
        ttk.Label(frame, text="Item Type:").grid(row=1, column=0, sticky=tk.W, pady=2)
        type_options = [e.value for e in EquipmentType]
        ttk.OptionMenu(frame, self.type_var, self.type_var.get(), *type_options).grid(row=1, column=1, sticky=tk.EW, pady=2)

        # Quantity
        ttk.Label(frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.quantity_var).grid(row=2, column=1, sticky=tk.EW, pady=2)

        # Weight
        ttk.Label(frame, text="Weight (lbs):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.weight_var).grid(row=3, column=1, sticky=tk.EW, pady=2)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, columnspan=2, pady=10)
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def on_ok(self):
        name = self.name_var.get()
        if not name:
            return # Or show an error

        self.item = Equipment(
            name=name,
            type=EquipmentType(self.type_var.get()),
            description="", # Placeholder
            weight=self.weight_var.get()
        )
        self.destroy()
