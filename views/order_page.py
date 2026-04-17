import customtkinter as ctk
from views.base_page import BasePage
from tkinter import messagebox

class OrderPage(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller, "🛒  Order Management")
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=20, pady=(12, 0))
        ctk.CTkLabel(
            toolbar,
            text="All customer orders are listed below.",
            font=ctk.CTkFont(size=13),
            text_color=self.MUTED,
        ).pack(side="left")
        ctk.CTkButton(
            toolbar, text="🔄  Refresh",
            height=36, corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color=self.CARD, hover_color=("#edeff5", "#252545"),
            border_width=1, border_color=self.BORDER,
            text_color=self.TEXT,
            command=self._refresh,
        ).pack(side="right", padx=(6, 0))
        ctk.CTkButton(
            toolbar, text="📤  Export CSV",
            height=36, corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color=("#dcfce7", "#1a3a2a"), hover_color="#1e4a33",
            text_color="#16a34a",
            command=self._export,
        ).pack(side="right", padx=(6, 0))
        self.setup_treeview(("ID", "Customer", "Product", "Qty", "Price", "Status", "Date"))
        actions = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=12, border_width=1, border_color=self.BORDER)
        actions.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(actions, text="Order Actions:", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT).pack(side="left", padx=20, pady=15)
        self.btn_accept = ctk.CTkButton(
            actions, text="✅  Accept Order",
            height=36, corner_radius=8,
            fg_color=("#dcfce7", "#1a3a2a"), hover_color="#1e4a33", text_color="#16a34a",
            command=lambda: self._update_status(1)
        )
        self.btn_accept.pack(side="left", padx=5)
        self.btn_reject = ctk.CTkButton(
            actions, text="❌  Reject Order",
            height=36, corner_radius=8,
            fg_color=("#fee2e2", "#3a1a1a"), hover_color="#4a1e1e", text_color="#ff6b6b",
            command=lambda: self._update_status(2)
        )
        self.btn_reject.pack(side="left", padx=5)
        self._refresh()

    def _update_status(self, status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select an order first.")
            return
        order_id = self.tree.item(selected[0])['values'][0]
        success, msg = self.controller.update_order_status(order_id, status)
        if success:
            self._refresh()
        else:
            messagebox.showerror("Error", msg)

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = []
        try:
            orders = self.controller.order_model.get_all_with_product() or []
        except Exception:
            pass
        self.tree.tag_configure("pending", foreground="#ffc107")         
        self.tree.tag_configure("accepted", foreground="#28a745")        
        self.tree.tag_configure("rejected", foreground="#dc3545")      
        for i, o in enumerate(orders):
            raw_status = o.get("status", 0)
            status_text = "Pending"
            tag = "pending"
            if raw_status == 1:
                status_text = "Accepted"
                tag = "accepted"
            elif raw_status == 2:
                status_text = "Rejected"
                tag = "rejected"
            self.tree.insert("", "end",
                             values=(
                                 o.get("id", ""),
                                 o.get("customer_name", ""),
                                 o.get("product_name", ""),
                                 o.get("quantity", ""),
                                 f"{o.get('total_price', 0):.2f} TND",
                                 status_text,
                                 o.get("order_date", "")
                             ),
                             tags=(tag,))

    def _export(self):
        try:
            orders = self.controller.order_model.get_all_with_product() or []
        except Exception:
            orders = []
        self.export_to_csv(orders, filename_hint="orders")
