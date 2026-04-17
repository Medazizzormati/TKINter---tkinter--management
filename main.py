
import customtkinter as ctk
from tkinter import messagebox

# =======================================================
#  MAIN.PY  —  Entry point of the ShopManager app
#
#  HOW IT WORKS (for beginners):
#  1. The app starts small (login window).
#  2. After a successful login it EXPANDS to full size.
#  3. It shows a sidebar on the left and page content
#     on the right.
#  4. The sidebar lets you switch pages.
# =======================================================

# ---- Import the controller (handles database logic) ----
from controllers.main_controller import MainController

# ---- Import all pages ----
from views.login_page    import LoginPage
from views.signup_page   import SignupPage
from views.sidebar       import Sidebar
from views.dashboard_page import DashboardPage
from views.category_page  import CategoryPage
from views.product_page   import ProductPage
from views.order_page     import OrderPage


# -------------------------------------------------------
class ShopManagerApp(ctk.CTk):
    """
    The main application window.
    It manages switching between the login screen
    and the main admin interface.
    """

    # Window sizes
    LOGIN_W, LOGIN_H   = 480, 560   # Small login window
    MAIN_W,  MAIN_H    = 1200, 700  # Full app window

    def __init__(self):
        super().__init__()

        # --- Global appearance ---
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("ShopManager")
        self.resizable(True, True)

        # --- Set up the controller (connects to DB) ---
        self.controller = MainController()

        # --- Track logged-in state ---
        self.logged_in = False

        # --- Start with the login window (small) ---
        self._show_login()

    # ==================================================
    #  LOGIN / SIGNUP SCREENS
    # ==================================================

    def _show_login(self):
        """Resize to small and show the login page."""
        # Make window small and center it
        self._set_window_size(self.LOGIN_W, self.LOGIN_H)
        self.title("ShopManager — Sign In")

        # Clear any existing content
        self._clear()

        # Create and fill the login page
        page = LoginPage(
            self,
            on_login_success=self._handle_login,   # called when user clicks Sign In
            on_show_signup=self._show_signup,       # called when user clicks "Create one"
        )
        page.pack(fill="both", expand=True)

    def _show_signup(self):
        """Resize slightly and show the signup page."""
        self._set_window_size(self.LOGIN_W, 640)
        self.title("ShopManager — Create Account")

        self._clear()

        page = SignupPage(
            self,
            on_signup_success=self._handle_signup,  # called when user submits signup form
            on_back_to_login=self._show_login,       # called when user clicks "Sign in"
        )
        page.pack(fill="both", expand=True)

    # ==================================================
    #  AUTH HANDLERS
    # ==================================================

    def _handle_login(self, username, password, selected_role="client"):
        """
        Called by LoginPage with the typed username & password.
        Asks the controller to check if they are correct.
        """
        success, user = self.controller.login(username, password)

        if success:
            self.logged_in = True
            self.current_user = user
            
            if user.get('role') == 'admin':
                self._show_main_app()         # Expand and show the full admin app
            else:
                self._show_client_app()       # Show client app
        else:
            messagebox.showerror(
                "Login Failed",
                "❌  Wrong username or password.\nPlease try again.",
                parent=self,
            )

    def _handle_signup(self, username, email, password, role="client"):
        """
        Called by SignupPage with the typed user details.
        Asks the controller to create the account.
        """
        success, message = self.controller.signup(username, email, password, role)

        if success:
            messagebox.showinfo(
                "Account Created! 🎉",
                f"{message}\n\nYou can now sign in with your new account.",
                parent=self,
            )
            self._show_login()   # Go back to login after signup
        else:
            messagebox.showerror("Signup Failed", message, parent=self)

    # ==================================================
    #  MAIN APP LAYOUT
    # ==================================================

    def _show_main_app(self):
        """
        Expand the window to full size and build the
        sidebar + page area layout.
        """
        # Animate window to full size
        self.state("zoomed")
        self.title("ShopManager — Dashboard")

        # Clear login content
        self._clear()

        # ---- TWO-COLUMN LAYOUT (Admin) ----
        self.grid_columnconfigure(0, weight=0) # Sidebar stays fixed
        self.grid_columnconfigure(1, weight=1) # Page area stretches
        self.grid_rowconfigure(0, weight=1)

        # ---- SIDEBAR ----
        self.sidebar = Sidebar(
            self,
            on_page_change=self.show_page,   # called when nav button is clicked
            on_logout=self._logout,          # called when Logout is clicked
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # ---- PAGE CONTENT AREA ----
        self.page_area = ctk.CTkFrame(self, fg_color=CategoryPage.BG, corner_radius=0)
        self.page_area.grid(row=0, column=1, sticky="nsew")
        self.page_area.grid_columnconfigure(0, weight=1)
        self.page_area.grid_rowconfigure(0, weight=1)

        # Show dashboard by default
        self.show_page("Dashboard")
        self.sidebar.highlight("Dashboard")

    # ==================================================
    #  PAGE ROUTER
    # ==================================================

    def show_page(self, page_name):
        """
        Destroy the current page and load the new one.
        Called by the sidebar or by dashboard quick-action buttons.
        """
        # Remove the current page
        for widget in self.page_area.winfo_children():
            widget.destroy()

        # Choose which page class to create
        if page_name == "Dashboard":
            page = DashboardPage(self.page_area, self.controller)

        elif page_name == "Categories":
            page = CategoryPage(self.page_area, self.controller)

        elif page_name == "Products":
            page = ProductPage(self.page_area, self.controller)

        elif page_name == "Orders":
            page = OrderPage(self.page_area, self.controller)

        else:
            # Fallback for unknown page names
            page = ctk.CTkLabel(
                self.page_area,
                text=f"🚧  '{page_name}' page coming soon…",
                font=ctk.CTkFont(size=20),
                text_color="#888899",
            )

        # Pack the page so it fills the content area
        page.grid(row=0, column=0, sticky="nsew")

        # Update the window title
        self.title(f"ShopManager — Admin — {page_name}")

    # ==================================================
    #  CLIENT APP LAYOUT 
    # ==================================================

    def _show_client_app(self):
        """Load the Client storefront view"""
        self.state("zoomed")
        self.title("ShopManager — Store")
        self._clear()

        # Import locally to avoid circular imports if client_page is large
        from views.client_page import ClientPage

        # ---- ONE-COLUMN LAYOUT (Client) ----
        # Reset column 1 so it doesn't take space if it was an admin session before
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

    # ==================================================
    #  LOGOUT
    # ==================================================

    def _logout(self):
        confirmed = messagebox.askyesno(
            "Logout",
            "Are you sure you want to log out?",
            parent=self,
        )
        if confirmed:
            self.logged_in = False
            self._show_login()

    # ==================================================
    #  HELPERS
    # ==================================================

    def _clear(self):
        """Remove all widgets from the window."""
        # Reset grid configuration
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        for widget in self.winfo_children():
            widget.destroy()

    def _set_window_size(self, width, height):
        """Resize the window and center it on the screen."""
        # Get screen dimensions
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # Calculate position to center the window
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(width, height)


# =======================================================
#  RUN THE APP
#  This block only runs when you execute  main.py
#  directly (not when it's imported by another file).
# =======================================================
if __name__ == "__main__":
    app = ShopManagerApp()
    app.mainloop()
