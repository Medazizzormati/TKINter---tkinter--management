



import customtkinter as ctk



from tkinter import messagebox



import re







                                               



              



                             



                                       



                                               







class SignupPage(ctk.CTkFrame):



    def __init__(self, parent, on_signup_success, on_back_to_login):



        super().__init__(parent)







        self.on_signup_success = on_signup_success



        self.on_back_to_login = on_back_to_login







                             



        self.BG = ("#f5f6fa", "#0d0d1a")



        self.CARD = ("#ffffff", "#1a1a2e")



        self.BORDER = ("#dcdde1", "#3a3a6e")



        self.TEXT = ("#2f3640", "#ccccdd")



        self.MUTED = ("#7f8c8d", "#888899")



        self.ACCENT = "#7c83fd"



        self.SUCCESS = "#28a745"







        self.configure(fg_color=self.BG)







                                           



        self.card = ctk.CTkFrame(



            self,



            fg_color=self.CARD,



            border_width=1,



            border_color=self.BORDER,



            corner_radius=20,



            width=420,



            height=600,



        )



        self.card.place(relx=0.5, rely=0.5, anchor="center")



        self.card.pack_propagate(False)







        self._build_card()







    def _build_card(self):



                                                    







                        



        ctk.CTkLabel(



            self.card,



            text="📝",



            font=ctk.CTkFont(size=44),



        ).pack(pady=(28, 0))







        ctk.CTkLabel(



            self.card,



            text="Create Account",



            font=ctk.CTkFont(size=24, weight="bold"),



            text_color=self.ACCENT,



        ).pack(pady=(6, 2))







        ctk.CTkLabel(



            self.card,



            text="Join ShopManager today",



            font=ctk.CTkFont(size=13),



            text_color=self.MUTED,



        ).pack(pady=(0, 18))







                          



        ctk.CTkLabel(



            self.card, text="Username",



            font=ctk.CTkFont(size=13, weight="bold"),



            text_color=self.TEXT, anchor="w",



        ).pack(fill="x", padx=40)



        self.username_entry = ctk.CTkEntry(



            self.card, placeholder_text="Choose a username",



            height=40, corner_radius=10,



            border_color=self.BORDER, fg_color=("#f9fafb", "#252540"), text_color=("#2f3640", "#ffffff"),



        )



        self.username_entry.pack(fill="x", padx=40, pady=(4, 12))







                       



        ctk.CTkLabel(



            self.card, text="Email",



            font=ctk.CTkFont(size=13, weight="bold"),



            text_color=self.TEXT, anchor="w",



        ).pack(fill="x", padx=40)



        self.email_entry = ctk.CTkEntry(



            self.card, placeholder_text="Enter your email address",



            height=40, corner_radius=10,



            border_color=self.BORDER, fg_color=("#f9fafb", "#252540"), text_color=("#2f3640", "#ffffff"),



        )



        self.email_entry.pack(fill="x", padx=40, pady=(4, 12))







                          



        ctk.CTkLabel(



            self.card, text="Password  (min 8 characters)",



            font=ctk.CTkFont(size=13, weight="bold"),



            text_color=self.TEXT, anchor="w",



        ).pack(fill="x", padx=40)



        self.password_entry = ctk.CTkEntry(



            self.card, placeholder_text="Create a password",



            show="●", height=40, corner_radius=10,



            border_color=self.BORDER, fg_color=("#f9fafb", "#252540"), text_color=("#2f3640", "#ffffff"),



        )



        self.password_entry.pack(fill="x", padx=40, pady=(4, 12))







                                  



        ctk.CTkLabel(



            self.card, text="Confirm Password",



            font=ctk.CTkFont(size=13, weight="bold"),



            text_color=self.TEXT, anchor="w",



        ).pack(fill="x", padx=40)



        self.confirm_entry = ctk.CTkEntry(



            self.card, placeholder_text="Repeat your password",



            show="●", height=40, corner_radius=10,



            border_color=self.BORDER, fg_color=("#f9fafb", "#252540"), text_color=("#2f3640", "#ffffff"),



        )



        self.confirm_entry.pack(fill="x", padx=40, pady=(4, 20))







                               



        self.signup_btn = ctk.CTkButton(



            self.card,



            text="Create Account  →",



            height=44,



            corner_radius=10,



            font=ctk.CTkFont(size=14, weight="bold"),



            fg_color=self.SUCCESS,



            hover_color="#1e7e34",



            command=self._do_signup,



        )



        self.signup_btn.pack(fill="x", padx=40)







                               



        ctk.CTkFrame(self.card, height=1, fg_color=self.BORDER).pack(



            fill="x", padx=40, pady=(20, 12)



        )







        back_row = ctk.CTkFrame(self.card, fg_color="transparent")



        back_row.pack()







        ctk.CTkLabel(



            back_row, text="Already have an account?",



            font=ctk.CTkFont(size=13), text_color=self.MUTED,



        ).pack(side="left")







        ctk.CTkButton(



            back_row, text="Sign in",



            font=ctk.CTkFont(size=13, weight="bold"),



            fg_color="transparent", hover_color=("#edeff5", "#252540"),



            text_color=self.ACCENT, width=70,



            command=self.on_back_to_login,



        ).pack(side="left")







                                       



        self.confirm_entry.bind("<Return>", lambda e: self._do_signup())







                                                        



    def _do_signup(self):



                                                           



        username = self.username_entry.get().strip()



        email    = self.email_entry.get().strip()



        password = self.password_entry.get()



        confirm  = self.confirm_entry.get()







                                                                



        if not username:



            messagebox.showerror("Missing Field", "Please enter a username.", parent=self.winfo_toplevel())



            self.username_entry.focus()



            return







        if not email:



            messagebox.showerror("Missing Field", "Please enter your email.", parent=self.winfo_toplevel())



            self.email_entry.focus()



            return







                           



        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):



            messagebox.showerror("Bad Email", "Please enter a valid email address.", parent=self.winfo_toplevel())



            self.email_entry.focus()



            return







        if not password:



            messagebox.showerror("Missing Field", "Please enter a password.", parent=self.winfo_toplevel())



            self.password_entry.focus()



            return







        if len(password) < 6:



            messagebox.showerror("Weak Password", "Password must be at least 6 characters.", parent=self.winfo_toplevel())



            self.password_entry.focus()



            return







        if password != confirm:



            messagebox.showerror("Mismatch", "Passwords do not match. Please try again.", parent=self.winfo_toplevel())



            self.confirm_entry.focus()



            return







                            



        self.signup_btn.configure(text="Creating account…", state="disabled")



        self.update()







        try:



            self.on_signup_success(username, email, password, "client")



        except Exception as err:



            if self.winfo_exists():



                messagebox.showerror("Error", f"Something went wrong:\n{err}", parent=self.winfo_toplevel())



        finally:



            try:



                if hasattr(self, 'signup_btn') and self.signup_btn.winfo_exists():



                    self.signup_btn.configure(text="Create Account  →", state="normal")



            except Exception:



                pass

