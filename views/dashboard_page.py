import customtkinter as ctk
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        from views.base_page import BasePage
        self.BG     = BasePage.BG
        self.CARD   = BasePage.CARD
        self.BORDER = BasePage.BORDER
        self.ACCENT = BasePage.ACCENT
        self.TEXT   = BasePage.TEXT
        self.MUTED  = BasePage.MUTED
        super().__init__(parent, fg_color=self.BG)
        self.controller = controller
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=self.BG)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self._build_header()
        self._build_stat_cards()
        self._build_charts()
        self._build_quick_actions()
        self._refresh()

    def _build_header(self):
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(
            row, text="📊  Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.ACCENT,
        ).pack(side="left")
        self.clock_label = ctk.CTkLabel(
            row, text="",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED,
        )
        self.clock_label.pack(side="right")
        ctk.CTkButton(
            row, text="🔄  Refresh",
            height=34, corner_radius=8,
            fg_color=self.CARD, hover_color=("#edeff5", "#252545"),
            border_width=1, border_color=self.BORDER,
            text_color=self.TEXT, font=ctk.CTkFont(size=13),
            command=self._refresh,
        ).pack(side="right", padx=(0, 10))
        ctk.CTkLabel(
            self.scroll,
            text="Welcome back! Here's your store overview.",
            font=ctk.CTkFont(size=14),
            text_color=self.MUTED,
            anchor="w",
        ).pack(fill="x", padx=15, pady=(4, 16))

    def _build_stat_cards(self):
        ctk.CTkLabel(
            self.scroll, text="Business Statistics",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.TEXT, anchor="w",
        ).pack(fill="x", padx=15, pady=(0, 10))
        self.cards_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=10)

    def _create_stat_card(self, col, icon, title, value, color):
        card = ctk.CTkFrame(
            self.cards_frame,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=14,
        )
        card.grid(row=0, column=col, padx=8, pady=8, sticky="ew")
        self.cards_frame.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=36)).pack(pady=(18, 4))
        ctk.CTkLabel(card, text=value,
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color=color).pack()
        ctk.CTkLabel(card, text=title,
                     font=ctk.CTkFont(size=12),
                     text_color=self.MUTED).pack(pady=(2, 16))

    def _build_charts(self):
        ctk.CTkLabel(
            self.scroll, text="Analytics & Insights",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.TEXT, anchor="w",
        ).pack(fill="x", padx=15, pady=(20, 10))
        self.charts_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.charts_frame.pack(fill="both", expand=True, padx=10)

    def _draw_charts(self):
        for w in self.charts_frame.winfo_children():
            w.destroy()
        plt.close("all")
        products   = self.controller.get_all_products() or []
        categories = self.controller.get_all_categories() or []
        mode = ctk.get_appearance_mode()
        chart_bg = "#f5f6fa" if mode == "Light" else "#1a1a2e"
        chart_fg = "#2f3640" if mode == "Light" else "#ccccdd"
        chart_muted = "#7f8c8d" if mode == "Light" else "#888899"
        chart_border = "#dcdde1" if mode == "Light" else "#3a3a6e"
        bar_container = ctk.CTkFrame(
            self.charts_frame,
            fg_color=self.CARD, border_width=1,
            border_color=self.BORDER, corner_radius=14,
        )
        bar_container.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        self.charts_frame.grid_columnconfigure(0, weight=1)
        if products:
            names  = [p["name"][:12] for p in products[:10]]
            stocks = [p["stock"] for p in products[:10]]
            fig1 = Figure(figsize=(5, 3.2), dpi=80, facecolor=chart_bg)
            ax1  = fig1.add_subplot(111, facecolor=chart_bg)
            ax1.bar(range(len(names)), stocks, color="#7c83fd",
                    edgecolor=chart_border, linewidth=1.2)
            ax1.set_xticks(range(len(names)))
            ax1.set_xticklabels(names, rotation=40, ha="right",
                                color=chart_muted, fontsize=8)
            ax1.set_ylabel("Stock", color=chart_muted, fontsize=9)
            ax1.set_title("Top Product Stock Levels", color=chart_fg,
                          fontsize=11, weight="bold", pad=10)
            ax1.tick_params(colors=chart_muted)
            ax1.grid(axis="y", alpha=0.2, color=chart_border, linestyle="--")
            for sp in ax1.spines.values():
                sp.set_color(chart_border)
            fig1.tight_layout()
            canvas1 = FigureCanvasTkAgg(fig1, master=bar_container)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        else:
            ctk.CTkLabel(bar_container, text="No product data yet.",
                         text_color=self.MUTED, font=ctk.CTkFont(size=13)).pack(pady=50)
        pie_container = ctk.CTkFrame(
            self.charts_frame,
            fg_color=self.CARD, border_width=1,
            border_color=self.BORDER, corner_radius=14,
        )
        pie_container.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        self.charts_frame.grid_columnconfigure(1, weight=1)
        valid_cats = [c for c in categories if c.get("product_count", 0) > 0]
        if valid_cats:
            names2  = [c["name"] for c in valid_cats]
            counts2 = [c["product_count"] for c in valid_cats]
            colors_scheme = ["#7c83fd", "#28a745", "#ffc107", "#dc3545",
                       "#17a2b8", "#fd7c83", "#a3fd7c"]
            fig2 = Figure(figsize=(5, 3.2), dpi=80, facecolor=chart_bg)
            ax2  = fig2.add_subplot(111, facecolor=chart_bg)
            ax2.pie(counts2, labels=names2, autopct="%1.0f%%",
                    colors=colors_scheme[:len(names2)], startangle=90,
                    textprops={"color": chart_fg, "fontsize": 9})
            ax2.set_title("Products by Category", color=chart_fg,
                          fontsize=11, weight="bold", pad=10)
            fig2.tight_layout()
            canvas2 = FigureCanvasTkAgg(fig2, master=pie_container)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        else:
            ctk.CTkLabel(pie_container, text="No category data yet.",
                         text_color=self.MUTED, font=ctk.CTkFont(size=13)).pack(pady=50)

    def _build_quick_actions(self):
        ctk.CTkLabel(
            self.scroll, text="Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.TEXT, anchor="w",
        ).pack(fill="x", padx=15, pady=(20, 10))
        actions_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        actions_frame.pack(fill="x", padx=10, pady=(0, 20))
        actions = [
            ("📦", "Manage Products",   "Products",   "#7c83fd"),
            ("📂", "Manage Categories", "Categories", "#28a745"),
            ("🛒", "View Orders",       "Orders",     "#ffc107"),
        ]
        for i, (icon, label, page, color) in enumerate(actions):
            btn = ctk.CTkButton(
                actions_frame,
                text=f"{icon}  {label}",
                height=54, corner_radius=12,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=self.CARD, hover_color=("#edeff5", "#252545"),
                border_width=1, border_color=color,
                text_color=color,
                command=lambda p=page: self._go_to(p),
            )
            btn.grid(row=0, column=i, padx=8, pady=8, sticky="ew")
            actions_frame.grid_columnconfigure(i, weight=1)

    def _go_to(self, page_name):
        w = self
        while w and not hasattr(w, "show_page"):
            w = w.master
        if w:
            w.show_page(page_name)

    def _refresh(self):
        self.clock_label.configure(
            text=datetime.now().strftime("%B %d, %Y  •  %I:%M %p")
        )
        stats = self.controller.get_dashboard_stats()
        for w in self.cards_frame.winfo_children():
            w.destroy()
        cards_data = [
            ("📦", "Total Products", str(stats.get("total_products", 0)), "#7c83fd"),
            ("📊", "Total Stock",    str(stats.get("total_stock", 0)),    "#28a745"),
            ("🛒", "Total Orders",   str(stats.get("total_orders", 0)),   "#ffc107"),
            ("💰", "Revenue",  f"{stats.get('total_revenue', 0):.2f} TND",   "#fd7c83"),
        ]
        for col, (icon, title, value, color) in enumerate(cards_data):
            self._create_stat_card(col, icon, title, value, color)
        self._draw_charts()
