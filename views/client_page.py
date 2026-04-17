import customtkinter as ctk



from tkinter import messagebox



from views.payment_modal import PaymentModal



import urllib.request



import io



from PIL import Image



import threading



import hashlib



import os







class ClientPage(ctk.CTkFrame):



    BG     = ("#f5f6fa", "#0d0d1a")



    CARD   = ("#ffffff", "#1a1a2e")



    BORDER = ("#dcdde1", "#3a3a6e")



    ACCENT = ("#2ecc71", "#28a745")



    TEXT   = ("#2f3640", "#ccccdd")



    MUTED  = ("#7f8c8d", "#888899")







    def __init__(self, parent, controller, user, on_logout):



        super().__init__(parent, fg_color=self.BG)



        self.controller = controller



        self.user = user



        self.on_logout = on_logout



        



        self.cart = {}                                                                      



        self.all_products = []



        self.image_cache = {}                  



        self.cache_dir = os.path.join("assets", "cache")



        if not os.path.exists(self.cache_dir):



            os.makedirs(self.cache_dir)



            



        self.current_view = "Shop"                      



        



                                      



                                                                



                                                                       



        self._build_header()



        



        self.content_area = ctk.CTkFrame(self, fg_color="transparent")



        self.content_area.grid(row=1, column=0, columnspan=2, sticky="nsew")



        



                                                     



        self.grid_columnconfigure(0, weight=1)



        self.grid_rowconfigure(1, weight=1)







        self.content_area.grid_rowconfigure(0, weight=1)



        self.content_area.grid_columnconfigure(0, weight=1)







                                             



        self.shop_view = None



        self.orders_view = None



        



                                        



                                                 



        self.show_view("Shop")



        



                                               



        self.after(50, self._refresh_products)







                                                        



                              



                                                        



    def _build_header(self):



        header = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=0, height=60)



        header.grid(row=0, column=0, columnspan=2, sticky="ew")



        header.grid_propagate(False)







        ctk.CTkLabel(



            header,



            text="🛒  ShopManager Store",



            font=ctk.CTkFont(size=20, weight="bold"),



            text_color=self.ACCENT,



        ).pack(side="left", padx=25, pady=15)







                      



        ctk.CTkLabel(



            header,



            text=f"Welcome, {self.user.get('username', 'Client')}!",



            font=ctk.CTkFont(size=14),



            text_color=self.TEXT,



        ).pack(side="left", padx=20)







                              



        self.btn_switch = ctk.CTkButton(



            header, text="🔔  My Orders",



            height=34, corner_radius=8,



            fg_color=("#edeff5", "#252545"), hover_color=self.BORDER, text_color=self.TEXT,



            command=self._toggle_view, width=120



        )



        self.btn_switch.pack(side="right", padx=10)







                       



        ctk.CTkButton(



            header, text="🚪  Logout",



            height=34, corner_radius=8,



            fg_color="transparent", hover_color=("#fee2e2", "#3a1a1a"), text_color="#e05555",



            command=self.on_logout, width=80



        ).pack(side="right", padx=15)







    def _toggle_view(self):



        if self.current_view == "Shop":



            self.show_view("Orders")



        else:



            self.show_view("Shop")







    def show_view(self, view_name):



        self.current_view = view_name



        



                       



        if view_name == "Shop":



            if not self.shop_view:



                self._build_shop_view()



            



            if self.orders_view: self.orders_view.grid_remove()



            self.shop_view.grid(row=0, column=0, sticky="nsew")



            self.btn_switch.configure(text="🔔  My Orders", fg_color=("#edeff5", "#252545"))



        else:



            if not self.orders_view:



                self._build_orders_view()



            



            if self.shop_view: self.shop_view.grid_remove()



            self.orders_view.grid(row=0, column=0, sticky="nsew")



            self.btn_switch.configure(text="🛍️  Back to Shop", fg_color=self.ACCENT)



            self._refresh_orders()







                                                        



                



                                                        



    def _build_shop_view(self):



        self.shop_view = ctk.CTkFrame(self.content_area, fg_color="transparent")



        self.shop_view.grid_rowconfigure(0, weight=1)



        self.shop_view.grid_columnconfigure(0, weight=1)



        self.shop_view.grid_columnconfigure(1, weight=0)







        self._build_products_section(self.shop_view)



        self._build_cart_section(self.shop_view)







    def _build_products_section(self, parent):



        left_panel = ctk.CTkFrame(parent, fg_color="transparent")



        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)



        left_panel.grid_rowconfigure(1, weight=1)



        left_panel.grid_columnconfigure(0, weight=1)



        



        toolbar = ctk.CTkFrame(left_panel, fg_color="transparent")



        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 15))







        self.search_entry = ctk.CTkEntry(



            toolbar, placeholder_text="🔍  Search products…",



            height=38, corner_radius=10,



            border_color=self.BORDER, fg_color=self.CARD, text_color=self.TEXT, width=240,



        )



        self.search_entry.pack(side="left")



        self.search_entry.bind("<KeyRelease>", lambda e: self._filter_and_display())







        ctk.CTkLabel(toolbar, text="Tri (Sort by):", text_color=self.MUTED, font=ctk.CTkFont(size=13)).pack(side="left", padx=(20, 5))



        



        self.sort_var = ctk.StringVar(value="Default")



        ctk.CTkComboBox(



            toolbar, values=["Default", "Price: Low to High", "Price: High to Low", "A to Z"],



            variable=self.sort_var, command=lambda v: self._filter_and_display(),



            height=38, corner_radius=8,



            border_color=self.BORDER, fg_color=self.CARD, text_color=self.TEXT, button_color=self.ACCENT,



            dropdown_fg_color=self.CARD



        ).pack(side="left")







                                                                       



        self.products_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")



        self.products_scroll.grid(row=1, column=0, sticky="nsew")



        



                                     



        self.products_scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)







    def _build_cart_section(self, parent):



        self.cart_panel = ctk.CTkFrame(



            parent, fg_color=self.CARD, border_width=1, border_color=self.BORDER, corner_radius=16, width=320



        )



        self.cart_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)



        self.cart_panel.grid_propagate(False)



        self.cart_panel.grid_rowconfigure(1, weight=1)







        ctk.CTkLabel(



            self.cart_panel, text="🛍️  Your Cart", font=ctk.CTkFont(size=18, weight="bold"), text_color=self.ACCENT



        ).grid(row=0, column=0, pady=(20, 10), padx=20, sticky="w")







        self.cart_items_scroll = ctk.CTkScrollableFrame(self.cart_panel, fg_color="transparent", width=280)



        self.cart_items_scroll.grid(row=1, column=0, sticky="nsew", padx=10)







        footer = ctk.CTkFrame(self.cart_panel, fg_color="transparent")



        footer.grid(row=2, column=0, sticky="ew", pady=15, padx=20)







        self.total_label = ctk.CTkLabel(



            footer, text="Total: 0.00 TND", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.TEXT



        )



        self.total_label.pack(anchor="w", pady=(0, 10))







        ctk.CTkButton(



            footer, text="💳  Checkout Now", height=46, corner_radius=12,



            font=ctk.CTkFont(size=15, weight="bold"),



            fg_color=self.ACCENT, hover_color="#1e7e34",



            command=self._checkout



        ).pack(fill="x")







                                                        



                  



                                                        



    def _build_orders_view(self):



        self.orders_view = ctk.CTkFrame(self.content_area, fg_color="transparent")



        



                               



        self.orders_view.grid_columnconfigure(0, weight=1)



        self.orders_view.grid_rowconfigure(1, weight=1)



        



        ctk.CTkLabel(



            self.orders_view, text="📦  My Order History & Notifications",



            font=ctk.CTkFont(size=22, weight="bold"), text_color=self.TEXT



        ).pack(pady=(30, 10), padx=40, anchor="w")



        



        ctk.CTkLabel(



            self.orders_view, text="Track the status of your orders here. The admin will update them soon!",



            font=ctk.CTkFont(size=14), text_color=self.MUTED



        ).pack(pady=(0, 20), padx=40, anchor="w")







        self.orders_scroll = ctk.CTkScrollableFrame(self.orders_view, fg_color="transparent")



        self.orders_scroll.pack(fill="both", expand=True, padx=40, pady=(0, 30))



        



                                                                                    



                                                                    



                                                                       







    def _refresh_orders(self):



        for w in self.orders_scroll.winfo_children():



            w.destroy()







        username = self.user.get('username')



        orders = self.controller.get_customer_orders(username)







        if not orders:



            ctk.CTkLabel(self.orders_scroll, text="No orders found yet.", text_color=self.MUTED, font=ctk.CTkFont(size=16)).pack(pady=50)



            return







        for o in orders:



            card = ctk.CTkFrame(self.orders_scroll, fg_color=self.CARD, border_width=1, border_color=self.BORDER, corner_radius=12)



            card.pack(fill="x", pady=10)



            



            info = ctk.CTkFrame(card, fg_color="transparent")



            info.pack(side="left", padx=20, pady=15)



            



            ctk.CTkLabel(info, text=f"Order #{o['id']}: {o['product_name']}", font=ctk.CTkFont(size=15, weight="bold"), text_color=self.TEXT).pack(anchor="w")



            ctk.CTkLabel(info, text=f"Quantity: {o['quantity']}  |  Total: {o['total_price']:.2f} TND", text_color=self.MUTED).pack(anchor="w")



            ctk.CTkLabel(info, text=f"Date: {o['order_date']}", font=ctk.CTkFont(size=11), text_color=self.MUTED).pack(anchor="w")







            status_frame = ctk.CTkFrame(card, fg_color="transparent")



            status_frame.pack(side="right", padx=20)



            



            raw_status = o.get('status', 0)



            if raw_status == 0:



                s_text, s_color = "🕒 PENDING", "#ffc107"



            elif raw_status == 1:



                s_text, s_color = "✅ ACCEPTED", "#28a745"



            else:



                s_text, s_color = "❌ REJECTED", "#dc3545"



                



            ctk.CTkLabel(status_frame, text=s_text, font=ctk.CTkFont(size=13, weight="bold"), text_color=s_color).pack()







                                                        



                    



                                                        



    def _refresh_products(self):



        prods = self.controller.get_products()



        self.all_products = [p for p in prods if p.get('stock', 0) > 0] if prods else []



        self._filter_and_display()







    def _filter_and_display(self, products_list=None):



        term = self.search_entry.get().strip().lower()



        source = products_list if products_list else self.all_products



        filtered = [p for p in source if term in p['name'].lower() or term in p.get('category_name', '').lower()]



        



        sort_mode = self.sort_var.get()



        if sort_mode == "Price: Low to High":



            filtered.sort(key=lambda x: float(x['price']))



        elif sort_mode == "Price: High to Low":



            filtered.sort(key=lambda x: float(x['price']), reverse=True)



        elif sort_mode == "A to Z":



            filtered.sort(key=lambda x: x['name'].lower())







                                            



        self._display_products_lazy(filtered, 0)







    def _display_products_lazy(self, products, start_idx=0):



                                                                                        



                                                    



        if start_idx == 0:



            for w in self.products_scroll.winfo_children():



                w.destroy()



        



        if not products:



            if start_idx == 0:



                ctk.CTkLabel(self.products_scroll, text="No products found matching your criteria.", 



                             text_color=self.MUTED, font=ctk.CTkFont(size=14)).grid(row=0, column=0, pady=40, padx=20)



            return







                                                 



        batch_size = 16



        end_idx = min(start_idx + batch_size, len(products))



        cols = 4                       



        



        for idx in range(start_idx, end_idx):



            prod = products[idx]



            row = idx // cols



            col = idx % cols



            self._create_product_card(self.products_scroll, prod, row, col)







                                                                                      



        if end_idx < len(products):



                                                                                             



            if self.winfo_exists():



                self.after(20, lambda: self._display_products_lazy(products, end_idx))



    



    def _create_product_card(self, parent, prod, row, col):



                                                              



        card = ctk.CTkFrame(parent, fg_color=self.CARD, border_width=1, border_color=self.BORDER, corner_radius=12, width=220, height=240)



        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")



        card.grid_propagate(False)







                      



        img_url = prod.get('image_url')



        img_label = ctk.CTkLabel(card, text="🖼️", image=None, height=80)



        img_label.pack(pady=(10, 5), padx=10, fill="both")







                                   



        self._get_image_async(img_url, img_label)







        name = prod['name'] if len(prod['name']) <= 18 else prod['name'][:16] + ".."



        ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=14, weight="bold"), text_color=self.TEXT).pack(pady=(0, 2))



        



        cat = prod.get('category_name', 'Misc')



        ctk.CTkLabel(card, text=cat, font=ctk.CTkFont(size=11), text_color=self.MUTED).pack()







        price = float(prod['price'])



        ctk.CTkLabel(card, text=f"{price:.2f} TND", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.ACCENT).pack(pady=(5, 5))







        ctk.CTkButton(



            card, text="Add to Cart", height=30, corner_radius=8, font=ctk.CTkFont(size=12),



            fg_color=("#edeff5", "#252545"), hover_color=self.BORDER, text_color=self.TEXT,



            command=lambda p=prod: self._add_to_cart(p)



        ).pack(fill="x", padx=15, side="bottom", pady=(0, 15))







    def _get_image_async(self, url, label_widget):



                                                                                       



        if not url:



            return







                               



        if url in self.image_cache:



            ctk_img = self.image_cache[url]



            label_widget.configure(image=ctk_img, text="")



            return







                                                                             



        if not url.startswith("http"):



            if os.path.exists(url):



                try:



                    pil_img = Image.open(url)



                    pil_img = pil_img.resize((180, 80), Image.Resampling.LANCZOS)



                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(180, 80))



                    self.image_cache[url] = ctk_img



                    label_widget.configure(image=ctk_img, text="")



                    return



                except: pass



            return







                                                    



        url_hash = hashlib.md5(url.encode()).hexdigest()



        cache_path = os.path.join(self.cache_dir, f"{url_hash}.png")







        if os.path.exists(cache_path):



            try:



                pil_img = Image.open(cache_path)



                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(180, 80))



                self.image_cache[url] = ctk_img



                label_widget.configure(image=ctk_img, text="")



                return



            except: pass







                                                                



        threading.Thread(target=self._download_and_cache, args=(url, cache_path, label_widget), daemon=True).start()







    def _download_and_cache(self, url, cache_path, label_widget):



                                                            



        try:



            with urllib.request.urlopen(url, timeout=5) as response:



                img_data = response.read()



            



            pil_img = Image.open(io.BytesIO(img_data))



                                 



            pil_img = pil_img.resize((180, 80), Image.Resampling.LANCZOS)



            



                                 



            pil_img.save(cache_path)







                             



            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(180, 80))



            self.image_cache[url] = ctk_img



            



                                      



            if label_widget.winfo_exists():



                label_widget.after(0, lambda: label_widget.configure(image=ctk_img, text=""))



                



        except Exception as e:



                                                               



            pass







    def _add_to_cart(self, prod):



        pid = prod['id']



        current_stock = int(prod['stock'])



        in_cart = self.cart.get(pid, {}).get("qty", 0)



        if in_cart >= current_stock:



            messagebox.showwarning("Out of Stock", f"Only {current_stock} of {prod['name']} available.", parent=self.winfo_toplevel())



            return



        if pid in self.cart:



            self.cart[pid]["qty"] += 1



        else:



            self.cart[pid] = {"name": prod['name'], "price": float(prod['price']), "qty": 1}



        self._render_cart()







    def _remove_from_cart(self, pid):



        if pid in self.cart:



            self.cart[pid]["qty"] -= 1



            if self.cart[pid]["qty"] <= 0:



                del self.cart[pid]



            self._render_cart()







    def _render_cart(self):



        for w in self.cart_items_scroll.winfo_children():



            w.destroy()



        if not self.cart:



            ctk.CTkLabel(self.cart_items_scroll, text="Your cart is empty.", text_color=self.MUTED).pack(pady=30)



            self.total_label.configure(text="Total: 0.00 TND")



            return



        total = 0.0



        for pid, item in self.cart.items():



            subtotal = item["price"] * item["qty"]



            total += subtotal



            row = ctk.CTkFrame(self.cart_items_scroll, fg_color="transparent")



            row.pack(fill="x", pady=8)



            n = item['name'] if len(item['name']) <= 12 else item['name'][:10]+".."



            ctk.CTkLabel(row, text=f"{n}  (x{item['qty']})", font=ctk.CTkFont(size=13), text_color=self.TEXT).pack(side="left", anchor="w")



            ctk.CTkLabel(row, text=f"{subtotal:.2f} TND", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT).pack(side="right", padx=(0, 5))



            def _remove(p=pid): self._remove_from_cart(p)



            ctk.CTkButton(row, text="➖", width=25, height=25, corner_radius=6, fg_color=("#fee2e2", "#3a1a1a"), hover_color=("#7a2020", "#4a1e1e"), text_color=("#e05555", "#ff6b6b"), command=_remove).pack(side="right", padx=5)



        self.total_label.configure(text=f"Total: {total:.2f} TND")







    def _checkout(self):



        if not self.cart:



            messagebox.showwarning("Empty Cart", "Add some items to your cart first!", parent=self.winfo_toplevel())



            return



        confirm = messagebox.askyesno("Checkout", "Place order and proceed to Konnect Payment?", parent=self.winfo_toplevel())



        if not confirm: return



        total = sum(item['price'] * item['qty'] for item in self.cart.values())



        PaymentModal(self.winfo_toplevel(), self.cart, total, self._checkout_success, self.user)







    def _checkout_success(self):



        try:



            customer = self.user.get('username', 'Client')



            for pid, item in self.cart.items():



                qty = item['qty']



                total_price = item['price'] * qty



                self.controller.order_model.create(pid, customer, qty, total_price)



                for p in self.all_products:



                    if p['id'] == pid:



                        new_stock = int(p['stock']) - qty



                        self.controller.product_model.update(product_id=pid, category_id=p['category_id'], name=p['name'], price=p['price'], stock=new_stock)



                        break



            self.cart.clear()



            self._render_cart()



            self._refresh_products()



        except Exception as e:



            messagebox.showerror("Error", f"Failed to checkout:\n{e}", parent=self.winfo_toplevel())



