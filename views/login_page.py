



import customtkinter as ctk



from tkinter import messagebox







                                               



             



                                



                                             



                                             



                                               







class LoginPage(ctk.CTkFrame):



    def __init__(self, parent, on_login_success, on_show_signup=None):



        super().__init__(parent)







                                      



        self.on_login_success = on_login_success



        self.on_show_signup = on_show_signup







                             



        self.BG = ("#f5f6fa", "#0d0d1a")



        self.CARD = ("#ffffff", "#1a1a2e")



        self.BORDER = ("#dcdde1", "#3a3a6e")



        self.TEXT = ("#2f3640", "#ccccdd")



        self.MUTED = ("#7f8c8d", "#888899")



        self.ACCENT = "#7c83fd"







        self.configure(fg_color=self.BG)







                                          



        self.card = ctk.CTkFrame(



            self,



            fg_color=self.CARD,



            border_width=1,



            border_color=self.BORDER,



            corner_radius=20,



            width=400,



            height=520,



        )



        self.card.place(relx=0.5, rely=0.5, anchor="center")



        self.card.pack_propagate(False)







        self._build_card()







    def _build_card(self):



                                                     







                                 



        ctk.CTkLabel(



            self.card,



            text="🛒",



            font=ctk.CTkFont(size=52),



        ).pack(pady=(35, 0))







        ctk.CTkLabel(



            self.card,



            text="ShopManager",



            font=ctk.CTkFont(size=26, weight="bold"),



            text_color=self.ACCENT,



        ).pack(pady=(6, 2))







        ctk.CTkLabel(



            self.card,



            text="Sign in to continue",



            font=ctk.CTkFont(size=13),



            text_color=self.MUTED,



        ).pack(pady=(0, 20))







                             



        self.role_var = ctk.StringVar(value="Client")



        self.role_switch = ctk.CTkSegmentedButton(



            self.card,



            values=["Client", "Admin"],



            variable=self.role_var,



            selected_color=self.ACCENT,



            unselected_color=("#edeff5", "#252540"),



            selected_hover_color="#5a60d0",



            font=ctk.CTkFont(size=12, weight="bold"),



            height=32,



        )



        self.role_switch.pack(pady=(0, 20))







                                



        ctk.CTkLabel(



            self.card,



            text="Username",



            font=ctk.CTkFont(size=13, weight="bold"),



            text_color=self.TEXT,



            anchor="w",



        ).pack(fill="x", padx=40)







        self.username_entry = ctk.CTkEntry(



            self.card,



            placeholder_text="Enter your username",



            height=42,



            corner_radius=10,



            border_color=self.BORDER,



            fg_color=("#f9fafb", "#252540"),



            text_color=("#2f3640", "#ffffff"),



            font=ctk.CTkFont(size=13),



        )



        self.username_entry.pack(fill="x", padx=40, pady=(4, 14))







                                



        ctk.CTkLabel(



            self.card,



            text="Password",



            font=ctk.CTkFont(size=13, weight="bold"),



            text_color=self.TEXT,



            anchor="w",



        ).pack(fill="x", padx=40)







        self.password_entry = ctk.CTkEntry(



            self.card,



            placeholder_text="Enter your password",



            show="●",



            height=42,



            corner_radius=10,



            border_color=self.BORDER,



            fg_color=("#f9fafb", "#252540"),



            text_color=("#2f3640", "#ffffff"),



            font=ctk.CTkFont(size=13),



        )



        self.password_entry.pack(fill="x", padx=40, pady=(4, 22))







                                



        self.login_btn = ctk.CTkButton(



            self.card,



            text="Sign In  →",



            height=44,



            corner_radius=10,



            font=ctk.CTkFont(size=14, weight="bold"),



            fg_color=self.ACCENT,



            hover_color="#5a60d0",



            command=self._do_login,



        )



        self.login_btn.pack(fill="x", padx=40)







                         



        ctk.CTkFrame(self.card, height=1, fg_color=self.BORDER).pack(



            fill="x", padx=40, pady=(22, 16)



        )







                             



        self.signup_row = ctk.CTkFrame(self.card, fg_color="transparent")



        self.signup_row.pack()







        ctk.CTkLabel(



            self.signup_row,



            text="No account yet?",



            font=ctk.CTkFont(size=13),



            text_color=self.MUTED,



        ).pack(side="left")







        ctk.CTkButton(



            self.signup_row,



            text="Create one",



            font=ctk.CTkFont(size=13, weight="bold"),



            fg_color="transparent",



            hover_color=("#edeff5", "#252540"),



            text_color=self.ACCENT,



            width=80,



            command=self.on_show_signup,



        ).pack(side="left")







                                                



        def _toggle_signup_vis(*args):



            if self.role_var.get() == "Admin":



                self.signup_row.pack_forget()



            else:



                self.signup_row.pack()







        self.role_var.trace_add("write", _toggle_signup_vis)







                                       



        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())



        self.password_entry.bind("<Return>", lambda e: self._do_login())







                                                        



    def _do_login(self):



                                                                    



        username = self.username_entry.get().strip()



        password = self.password_entry.get().strip()







                          



        if not username or not password:



            messagebox.showerror(



                "Missing Info",



                "Please enter both username and password.",



                parent=self.winfo_toplevel(),



            )



            return







                            



        self.login_btn.configure(text="Signing in...", state="disabled")



        self.update()







        def _complete_login():



            if not self.winfo_exists(): return



            try:



                selected_role = self.role_var.get().lower()



                self.on_login_success(username, password, selected_role)



            except Exception as err:



                if self.winfo_exists():



                    messagebox.showerror(



                        "Login Error",



                        f"Something went wrong:\n{err}",



                        parent=self.winfo_toplevel(),



                    )



            finally:



                                                                                                



                try:



                    if hasattr(self, 'login_btn') and self.login_btn.winfo_exists():



                        self.login_btn.configure(text="Sign In  →", state="normal")



                except Exception:



                    pass







                                                        



        _complete_login()



