



import customtkinter as ctk



from tkinter import messagebox







                                                         



                                                 



 



                                



                                          



                                                       



                                                     



                   



                                        



                                                         







                                                          



from controllers.main_controller import MainController







                            



from views.login_page    import LoginPage



from views.signup_page   import SignupPage



from views.sidebar       import Sidebar



from views.dashboard_page import DashboardPage



from views.category_page  import CategoryPage



from views.product_page   import ProductPage



from views.order_page     import OrderPage











                                                         



class ShopManagerApp(ctk.CTk):



    



       







                  



    LOGIN_W, LOGIN_H   = 480, 560                       



    MAIN_W,  MAIN_H    = 1200, 700                   







    def __init__(self):



        super().__init__()







                                   



        ctk.set_appearance_mode("System")



        ctk.set_default_color_theme("blue")







        self.title("ShopManager")



        self.resizable(True, True)







                                                        



        self.controller = MainController()







                                       



        self.logged_in = False







                                                     



        self._show_login()







                                                        



                             



                                                        







    def _show_login(self):



                                                      



                                         



        self._set_window_size(self.LOGIN_W, self.LOGIN_H)



        self.title("ShopManager — Sign In")







                                    



        self._clear()







                                        



        page = LoginPage(



            self,



            on_login_success=self._handle_login,                                    



            on_show_signup=self._show_signup,                                             



        )



        page.pack(fill="both", expand=True)







    def _show_signup(self):



                                                       



        self._set_window_size(self.LOGIN_W, 640)



        self.title("ShopManager — Create Account")







        self._clear()







        page = SignupPage(



            self,



            on_signup_success=self._handle_signup,                                        



            on_back_to_login=self._show_login,                                          



        )



        page.pack(fill="both", expand=True)







                                                        



                    



                                                        







    def _handle_login(self, username, password, selected_role="client"):



        


           



        success, user = self.controller.login(username, password)







        if success:



            self.logged_in = True



            self.current_user = user



            



            if user.get('role') == 'admin':



                self._show_main_app()                                             



            else:



                self._show_client_app()                        



        else:



            messagebox.showerror(



                "Login Failed",



                "❌  Wrong username or password.\nPlease try again.",



                parent=self,



            )







    def _handle_signup(self, username, email, password, role="client"):



        


           



        success, message = self.controller.signup(username, email, password, role)







        if success:



            messagebox.showinfo(



                "Account Created! 🎉",



                f"{message}\n\nYou can now sign in with your new account.",



                parent=self,



            )



            self._show_login()                                  



        else:



            messagebox.showerror("Signup Failed", message, parent=self)







                                                        



                      



                                                        







    def _show_main_app(self):



        


           



                                     



        self.state("zoomed")



        self.title("ShopManager — Dashboard")







                             



        self._clear()







                                             



        self.grid_columnconfigure(0, weight=0)                      



        self.grid_columnconfigure(1, weight=1)                      



        self.grid_rowconfigure(0, weight=1)







                           



        self.sidebar = Sidebar(



            self,



            on_page_change=self.show_page,                                      



            on_logout=self._logout,                                         



        )



        self.sidebar.grid(row=0, column=0, sticky="nsew")







                                     



        self.page_area = ctk.CTkFrame(self, fg_color=CategoryPage.BG, corner_radius=0)



        self.page_area.grid(row=0, column=1, sticky="nsew")



        self.page_area.grid_columnconfigure(0, weight=1)



        self.page_area.grid_rowconfigure(0, weight=1)







                                   



        self.show_page("Dashboard")



        self.sidebar.highlight("Dashboard")







                                                        



                  



                                                        







    def show_page(self, page_name):



        


           



                                 



        for widget in self.page_area.winfo_children():



            widget.destroy()







                                           



        if page_name == "Dashboard":



            page = DashboardPage(self.page_area, self.controller)







        elif page_name == "Categories":



            page = CategoryPage(self.page_area, self.controller)







        elif page_name == "Products":



            page = ProductPage(self.page_area, self.controller)







        elif page_name == "Orders":



            page = OrderPage(self.page_area, self.controller)







        else:



                                             



            page = ctk.CTkLabel(



                self.page_area,



                text=f"🚧  '{page_name}' page coming soon…",



                font=ctk.CTkFont(size=20),



                text_color="#888899",



            )







                                                    



        page.grid(row=0, column=0, sticky="nsew")







                                 



        self.title(f"ShopManager — Admin — {page_name}")







                                                        



                         



                                                        







    def _show_client_app(self):



                                             



        self.state("zoomed")



        self.title("ShopManager — Store")



        self._clear()







                                                                          



        from views.client_page import ClientPage







                                              



                                                                                   



        self.grid_columnconfigure(0, weight=1)



        self.grid_columnconfigure(1, weight=0)



        self.grid_rowconfigure(0, weight=1)







        page = ClientPage(



            self,



            controller=self.controller,



            user=self.current_user,



            on_logout=self._logout



        )



        page.grid(row=0, column=0, sticky="nsew")







                                                        



             



                                                        







    def _logout(self):



        confirmed = messagebox.askyesno(



            "Logout",



            "Are you sure you want to log out?",



            parent=self,



        )



        if confirmed:



            self.logged_in = False



            self._show_login()







                                                        



              



                                                        







    def _clear(self):



                                                 



                                  



        self.grid_columnconfigure(0, weight=0)



        self.grid_columnconfigure(1, weight=0)







        for widget in self.winfo_children():



            widget.destroy()







    def _set_window_size(self, width, height):



                                                            



                               



        screen_w = self.winfo_screenwidth()



        screen_h = self.winfo_screenheight()







                                                 



        x = (screen_w - width) // 2



        y = (screen_h - height) // 2







        self.geometry(f"{width}x{height}+{x}+{y}")



        self.minsize(width, height)











                                                         



              



                                                 



                                                     



                                                         



if __name__ == "__main__":



    app = ShopManagerApp()



    app.mainloop()



