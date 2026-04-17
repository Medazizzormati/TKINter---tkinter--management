
import customtkinter as ctk
from tkinter import ttk, messagebox
import csv
from tkinter import filedialog

# =============================================
#  BASE PAGE
#  Every admin page (Categories, Products…)
#  inherits from this class.
#  It provides:
#   • A page title header
#   • A styled Treeview (data table)
#   • Helper methods for sorting columns
# =============================================

class BasePage(ctk.CTkFrame):

    # Color palette used across all pages (Light, Dark)
    BG       = ("#f5f6fa", "#0d0d1a")   # Main background
    CARD     = ("#ffffff", "#1a1a2e")   # Card / panel color
    BORDER   = ("#dcdde1", "#3a3a6e")   # Border color
    ACCENT   = ("#4a4ae6", "#7c83fd")   # Highlight / accent blue
    TEXT     = ("#2f3640", "#ccccdd")   # Normal text
    MUTED    = ("#7f8c8d", "#888899")   # Gray / muted text

    def __init__(self, parent, controller, title):
        super().__init__(parent, fg_color=self.BG)
        self.controller = controller  # MainController instance

        # --- PAGE TITLE HEADER ---
        header = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.ACCENT,
        )
        self.title_label.pack(side="left", padx=25, pady=15)

    # --------------------------------------------------
    def setup_treeview(self, columns):
        """
        Create a styled data table (Treeview).
        """
        self.tree_frame = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=12)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        # We'll use a dynamic approach for Treeview colors
        style = ttk.Style()
        style.theme_use("clam")

        self._update_treeview_style()

        # --- TREEVIEW WIDGET ---
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
        )

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _c=col: self._sort_column(_c, False))
            self.tree.column(col, width=130, anchor="center")

        sb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y", padx=(0, 5), pady=10)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self._update_row_colors()

    def _update_treeview_style(self):
        """Update the global Custom.Treeview style based on current appearance mode."""
        style = ttk.Style()
        mode = ctk.get_appearance_mode()
        
        if mode == "Light":
            bg, fg, field, hdr_bg, hdr_fg, sel_bg = "#ffffff", "#2f3640", "#ffffff", "#f5f6fa", "#4a4ae6", "#dcdde1"
        else:
            bg, fg, field, hdr_bg, hdr_fg, sel_bg = "#1a1a2e", "#ccccdd", "#1a1a2e", "#252545", "#7c83fd", "#3a3a6e"

        style.configure("Custom.Treeview",
            background=bg, foreground=fg, fieldbackground=field,
            rowheight=34, font=("Segoe UI", 12), borderwidth=0)
        
        style.configure("Custom.Treeview.Heading",
            background=hdr_bg, foreground=hdr_fg,
            font=("Segoe UI", 12, "bold"), relief="flat")
        
        style.map("Custom.Treeview",
            background=[("selected", sel_bg)],
            foreground=[("selected", "#ffffff" if mode=="Dark" else "#000000")])

    def _update_row_colors(self):
        """Apply alternating row colors based on current mode."""
        mode = ctk.get_appearance_mode()
        if mode == "Light":
            self.tree.tag_configure("odd",  background="#f9f9fb")
            self.tree.tag_configure("even", background="#ffffff")
        else:
            self.tree.tag_configure("odd",  background="#1e1e38")
            self.tree.tag_configure("even", background="#1a1a2e")

    # --------------------------------------------------
    def insert_row(self, values):
        """Insert a row with alternating color tags."""
        count = len(self.tree.get_children())
        tag = "odd" if count % 2 == 0 else "even"
        self.tree.insert("", "end", values=values, tags=(tag,))

    # --------------------------------------------------
    def _sort_column(self, col, reverse):
        """Sort the treeview table when a column header is clicked."""
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        data.sort(reverse=reverse)
        for index, (_, k) in enumerate(data):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self._sort_column(col, not reverse))

    # --------------------------------------------------
    def export_to_csv(self, rows, filename_hint="export"):
        """
        Open a Save-file dialog and write `rows` (list of dicts) to CSV.
        Call this from child pages.
        """
        if not rows:
            messagebox.showwarning("No Data", "There is nothing to export.", parent=self.winfo_toplevel())
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=filename_hint,
        )
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            messagebox.showinfo("Exported!", f"File saved to:\n{path}", parent=self.winfo_toplevel())
