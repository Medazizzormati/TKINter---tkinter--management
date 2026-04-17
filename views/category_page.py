import customtkinter as ctk
from tkinter import messagebox
from views.base_page import BasePage
CATEGORY_ICONS = {
    "Bakery": "🥖",
    "Beveranges": "🥤",
    "Clothing": "👕",
    "Dairy & Eggs": "🥛",
    "Electronics": "💻",
    "Frozen Foods": "🧊",
    "Fruits & Vegetables": "🥦",
    "Home & Kitchen": "🏠",
    "Household Items": "🧹",
    "juices": "🍹",
    "Meat & Seafood": "🥩",
    "Pantry Staples": "🥫",
    "Personal Care": "🧴",
    "Snacks & Sweets": "🍩",
    "Default": "📂"
}

class CategoryPage(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller, "📂  Category Management")
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=20, pady=(12, 0))
        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="🔍  Search categories…",
            height=38,
            corner_radius=10,
            border_color=self.BORDER,
            fg_color=self.CARD,
            text_color=self.TEXT,
            font=ctk.CTkFont(size=13),
            width=260,
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self._on_search)
        btn_cfg = dict(height=38, corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"))
        ctk.CTkButton(
            toolbar, text="➕  Add Category",
            fg_color=self.ACCENT, hover_color="#5a60d0",
            command=self._open_add_dialog, **btn_cfg,
        ).pack(side="right", padx=(6, 0))
        ctk.CTkButton(
            toolbar, text="✏️  Edit",
            fg_color=("#edeff5", "#252545"), hover_color=self.BORDER,
            text_color=self.TEXT, command=self._edit_selected, **btn_cfg,
        ).pack(side="right", padx=(6, 0))
        ctk.CTkButton(
            toolbar, text="🗑️  Delete",
            fg_color=("#fee2e2", "#4a1a1a"), hover_color="#7a2020", text_color="#ff6b6b",
            command=self._delete_selected, **btn_cfg,
        ).pack(side="right", padx=(6, 0))
        ctk.CTkButton(
            toolbar, text="📤  Export CSV",
            fg_color=("#dcfce7", "#1a3a2a"), hover_color="#1e4a33", text_color="#16a34a",
            command=self._export, **btn_cfg,
        ).pack(side="right", padx=(6, 0))
        ctk.CTkLabel(
            self,
            text="Category Overview",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.MUTED,
            anchor="w",
        ).pack(fill="x", padx=25, pady=(16, 6))
        self.card_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=200,
        )
        self.card_scroll.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(
            self,
            text="All Categories (table view — click a column to sort)",
            font=ctk.CTkFont(size=13),
            text_color=self.MUTED,
            anchor="w",
        ).pack(fill="x", padx=25, pady=(4, 2))
        self.setup_treeview(("ID", "Name", "Description"))
        self._refresh()

    def _refresh(self, data=None):
        categories = data if data is not None else self.controller.get_categories() or []
        for w in self.card_scroll.winfo_children():
            w.destroy()
        if categories:
            for idx, cat in enumerate(categories):
                self._create_category_card(idx, cat)
        else:
            ctk.CTkLabel(
                self.card_scroll,
                text="No categories yet. Click  ➕ Add Category  to create one.",
                text_color=self.MUTED,
                font=ctk.CTkFont(size=13),
            ).pack(pady=20)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for cat in categories:
            self.insert_row((cat["id"], cat["name"], cat.get("description", "")))

    def _create_category_card(self, idx, cat):
        name_key = cat["name"]
        icon = CATEGORY_ICONS.get(name_key, CATEGORY_ICONS["Default"])
        card = ctk.CTkFrame(
            self.card_scroll,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=14,
            width=160,
            height=110,
        )
        card.grid(row=0, column=idx, padx=8, pady=8, sticky="n")
        card.grid_propagate(False)
        ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=30)).pack(pady=(14, 4))
        name = cat["name"] if len(cat["name"]) <= 14 else cat["name"][:14] + "…"
        ctk.CTkLabel(
            card,
            text=name,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.ACCENT,
        ).pack()

    def _on_search(self, _event=None):
        term = self.search_entry.get().strip()
        results = self.controller.category_model.search(term)
        self._refresh(results)

    def _open_add_dialog(self):
        self._open_dialog()

    def _edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select a row", "Please click on a category in the table first.", parent=self.winfo_toplevel())
            return
        vals = self.tree.item(selected[0])["values"]
        self._open_dialog(item_id=vals[0], old_name=str(vals[1]), old_desc=str(vals[2]))

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select a row", "Please click on a category in the table first.", parent=self.winfo_toplevel())
            return
        vals = self.tree.item(selected[0])["values"]
        confirmed = messagebox.askyesno(
            "Delete Category",
            f"Are you sure you want to delete  '{vals[1]}'?\n\nAll products in this category will also be deleted!",
            parent=self.winfo_toplevel(),
        )
        if confirmed:
            try:
                self.controller.category_model.delete(vals[0])
                self._refresh()
            except Exception as err:
                messagebox.showerror("Error", str(err), parent=self.winfo_toplevel())

    def _export(self):
        self.export_to_csv(self.controller.get_categories() or [], filename_hint="categories")

    def _open_dialog(self, item_id=None, old_name="", old_desc=""):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Category" if item_id else "Add New Category")
        dialog.geometry("420x350")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=self.BG)
        ctk.CTkLabel(
            dialog,
            text="Edit Category" if item_id else "Add New Category",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.ACCENT,
        ).pack(pady=(24, 16))
        ctk.CTkLabel(dialog, text="Category Name:", font=ctk.CTkFont(size=13), text_color=self.TEXT, anchor="w").pack(fill="x", padx=40)
        name_entry = ctk.CTkEntry(dialog, placeholder_text="e.g. Beverages", height=40, corner_radius=10,
                                  border_color=self.BORDER, fg_color=("#f9fafb", "#252545"), text_color=self.TEXT)
        name_entry.pack(fill="x", padx=40, pady=(4, 14))
        if old_name:
            name_entry.insert(0, old_name)
        ctk.CTkLabel(dialog, text="Description:", font=ctk.CTkFont(size=13), text_color=self.TEXT, anchor="w").pack(fill="x", padx=40)
        desc_entry = ctk.CTkEntry(dialog, placeholder_text="Short description (optional)", height=40, corner_radius=10,
                                  border_color=self.BORDER, fg_color=("#f9fafb", "#252545"), text_color=self.TEXT)
        desc_entry.pack(fill="x", padx=40, pady=(4, 20))
        if old_desc:
            desc_entry.insert(0, old_desc)

        def _save():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip() or "No description"
            if not name:
                messagebox.showwarning("Missing Name", "Please enter a category name.", parent=dialog)
                return
            try:
                if item_id:
                    self.controller.category_model.update(item_id, name, desc)
                    messagebox.showinfo("Updated", "Category updated successfully!", parent=dialog)
                else:
                    ok, msg = self.controller.add_category(name, desc)
                    if not ok:
                        messagebox.showerror("Error", msg, parent=dialog)
                        return
                    messagebox.showinfo("Added", msg, parent=dialog)
                self._refresh()
                dialog.destroy()
            except Exception as err:
                messagebox.showerror("Error", str(err), parent=dialog)
        ctk.CTkButton(
            dialog, text="  💾  Save", height=42, corner_radius=10,
            fg_color=self.ACCENT, hover_color="#5a60d0",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=_save,
        ).pack(fill="x", padx=40)
