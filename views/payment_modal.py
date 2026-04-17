import customtkinter as ctk
from tkinter import messagebox
import random
import os
import datetime
import requests
import webbrowser
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class PaymentModal(ctk.CTkToplevel):
    BG     = ("#f5f6fa", "#0d0d1a")
    CARD   = ("#ffffff", "#1a1a2e")
    BORDER = ("#dcdde1", "#3a3a6e")
    TEXT   = ("#2f3640", "#ccccdd")
    MUTED  = ("#7f8c8d", "#888899")
    ACCENT = ("#db2777")                                

    def __init__(self, parent, cart_items, total_price, on_success, user):
        super().__init__(parent)
        self.cart_items = cart_items
        self.total_price = total_price
        self.on_success = on_success
        self.user = user
        self.title("Konnect Payment Gateway - Sandbox")
        self.geometry("750x500")
        self.resizable(False, False)
        self.configure(fg_color=self.BG)
        self.transient(parent)
        self.grab_set()
        self.has_card = False
        self.card_balance = 0.0
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)               
        self.grid_columnconfigure(1, weight=1)               
        self._build_invoice_side()
        self._build_payment_side()

    def _build_invoice_side(self):
        frame = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=16, border_width=1, border_color=self.BORDER)
        frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        frame.grid_propagate(False)
        ctk.CTkLabel(
            frame, text="🧾  Invoice Summary", 
            font=ctk.CTkFont(size=18, weight="bold"), text_color=self.TEXT
        ).pack(pady=(20, 10))
        ctk.CTkFrame(frame, height=1, fg_color=self.BORDER).pack(fill="x", padx=15, pady=(0, 15))
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10)
        for _pid, item in self.cart_items.items():
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=4)
            name = item['name']
            if len(name) > 15: name = name[:13] + ".."
            subtotal = item['price'] * item['qty']
            ctk.CTkLabel(row, text=f"{item['qty']}x {name}", font=ctk.CTkFont(size=13), text_color=self.TEXT).pack(side="left")
            ctk.CTkLabel(row, text=f"{subtotal:.2f} TND", font=ctk.CTkFont(size=13), text_color=self.MUTED).pack(side="right")
        ctk.CTkFrame(frame, height=1, fg_color=self.BORDER).pack(fill="x", padx=15, pady=(10, 10))
        total_lbl = ctk.CTkLabel(
            frame, text=f"Total: {self.total_price:.2f} TND", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color=self.ACCENT
        )
        total_lbl.pack(pady=(0, 20))

    def _build_payment_side(self):
        frame = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=16, border_width=1, border_color=self.BORDER)
        frame.grid(row=0, column=1, sticky="nsew", padx=(0,15), pady=15)
        ctk.CTkLabel(
            frame, text="💳  Konnect Payment Gateway", 
            font=ctk.CTkFont(size=18, weight="bold"), text_color=self.TEXT
        ).pack(pady=(20, 5))
        ctk.CTkLabel(
            frame, text="Complete your details to proceed to payment.", 
            font=ctk.CTkFont(size=12), text_color=self.MUTED
        ).pack(pady=(0, 15))
        form = ctk.CTkFrame(frame, fg_color="transparent")
        form.pack(fill="x", padx=20)
        ctk.CTkLabel(form, text="Full Name:", font=ctk.CTkFont(size=12), text_color=self.TEXT, anchor="w").pack(fill="x")
        self.name_entry = ctk.CTkEntry(form, height=36, corner_radius=8, fg_color=("#f9fafb", "#1f2937"), border_color=self.BORDER, text_color=self.TEXT)
        self.name_entry.pack(fill="x", pady=(2, 10))
        self.name_entry.insert(0, self.user.get('username', ''))
        ctk.CTkLabel(form, text="Email Address:", font=ctk.CTkFont(size=12), text_color=self.TEXT, anchor="w").pack(fill="x")
        self.email_entry = ctk.CTkEntry(form, height=36, corner_radius=8, fg_color=("#f9fafb", "#1f2937"), border_color=self.BORDER, text_color=self.TEXT)
        self.email_entry.pack(fill="x", pady=(2, 10))
        self.email_entry.insert(0, self.user.get('email', ''))
        ctk.CTkLabel(form, text="Phone Number (Required):", font=ctk.CTkFont(size=12), text_color=self.TEXT, anchor="w").pack(fill="x")
        self.phone_entry = ctk.CTkEntry(form, placeholder_text="e.g. 55123456", height=36, corner_radius=8, fg_color=("#f9fafb", "#1f2937"), border_color=self.BORDER, text_color=self.TEXT)
        self.phone_entry.pack(fill="x", pady=(2, 15))
        self.pay_btn = ctk.CTkButton(
            frame, text="🔒  Initiate Payment", 
            height=46, corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.ACCENT, hover_color="#be185d",
            command=self._initiate_konnect_payment
        )
        self.pay_btn.pack(fill="x", padx=20, pady=(10, 5))
        self.complete_btn = ctk.CTkButton(
            frame, text="✅  Confirm Payment Complete", 
            height=46, corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#28a745", hover_color="#1e7e34",
            state="disabled",
            command=self._process_payment
        )
        self.complete_btn.pack(fill="x", padx=20, pady=5)

    def _initiate_konnect_payment(self):
        first_name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not first_name or not email or not phone:
            messagebox.showwarning("Missing Info", "Please provide name, email, and phone number.", parent=self)
            return
        url = "https://api.sandbox.konnect.network/api/v2/payments/init-payment"
        headers = {
            "x-api-key": "68036ba4c4f4ab1d9ffb00e7:JRU7VYZeHEYHbWKw",
            "Content-Type": "application/json"
        }
        payload = {
            "receiverWalletId": "68036ba4c4f4ab1d9ffb00ef",
            "amount": int(self.total_price * 1000),                         
            "token": "TND",
            "firstName": first_name,
            "lastName": "Customer",
            "phoneNumber": phone,
            "email": email,
            "orderId": f"ORDER-{random.randint(1000, 9999)}",
            "add_fields": {"app": "ShopManager-Desktop"}
        }
        try:
            self.pay_btn.configure(text="⌛  Connecting...", state="disabled")
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()
            if not self.winfo_exists(): return
            if response.status_code == 200 and "payUrl" in data:
                pay_url = data["payUrl"]
                webbrowser.open(pay_url)
                if self.winfo_exists():
                    messagebox.showinfo(
                        "Payment Initiated", 
                        "Payment link opened in your browser.\n\nPlease complete the payment there, then return to this app and click 'Confirm Payment Complete'.",
                        parent=self
                    )
                if self.winfo_exists():
                    self.pay_btn.configure(text="🔗  Opened in Browser", fg_color="#333333")
                    self.complete_btn.configure(state="normal")
            else:
                error_msg = data.get("errors", ["Unknown error"])[0] if "errors" in data else str(data)
                if self.winfo_exists():
                    messagebox.showerror("API Error", f"Konnect API Error: {error_msg}", parent=self)
                if self.winfo_exists():
                    self.pay_btn.configure(text="🔒  Retry Initiation", state="normal")
        except Exception as e:
            if self.winfo_exists():
                messagebox.showerror("Connection Error", f"Could not reach Konnect API:\n{e}", parent=self)
                self.pay_btn.configure(text="🔒  Retry Initiation", state="normal")

    def _process_payment(self):
        confirm = messagebox.askyesno(
            "Finalize Order", 
            "Did you successfully complete the payment in the browser?\n\n(Click 'Yes' only if the browser shows Success)", 
            parent=self
        )
        if confirm:
            self._show_success_view()

    def _show_success_view(self):
        for w in self.grid_slaves(column=1):
            w.destroy()
        success_frame = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=16, border_width=1, border_color="#28a745")
        success_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        ctk.CTkLabel(
            success_frame, text="🎉  Payment Successful!", 
            font=ctk.CTkFont(size=22, weight="bold"), text_color="#28a745"
        ).pack(pady=(60, 10))
        ctk.CTkLabel(
            success_frame, text="Your order has been placed successfully.", 
            font=ctk.CTkFont(size=14), text_color=self.TEXT
        ).pack(pady=(0, 40))
        ctk.CTkButton(
            success_frame, text="📄  Print Receipt (PDF)", 
            height=46, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3b3b5c", hover_color="#4b4b7c",
            command=self._print_receipt
        ).pack(fill="x", padx=40, pady=10)
        ctk.CTkButton(
            success_frame, text="Done & Back to Store", 
            height=46, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.ACCENT, hover_color="#be185d",
            command=lambda: [self.destroy(), self.on_success()]
        ).pack(fill="x", padx=40, pady=10)

    def _print_receipt(self):
        try:
            order_id = random.randint(10000, 99999)
            filename = f"invoice_order_{order_id}.pdf"
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            c.setFillColor(colors.HexColor("#0d0d1a"))
            c.rect(0, height - 100, width, 100, fill=1)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 24)
            c.drawString(50, height - 60, "SHOPMANAGER")
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 80, "Your Smart Supermarket Partner")
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 130, f"INVOICE #{order_id}")
            c.setFont("Helvetica", 10)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.drawString(50, height - 150, f"Date: {now}")
            c.drawString(50, height - 165, f"Customer: {self.user.get('username', 'Guest')}")
            c.setStrokeColor(colors.HexColor("#3a3a6e"))
            c.line(50, height - 190, width - 50, height - 190)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(60, height - 205, "ITEM")
            c.drawString(350, height - 205, "QTY")
            c.drawString(450, height - 205, "TOTAL")
            c.line(50, height - 215, width - 50, height - 215)
            c.setFont("Helvetica", 10)
            y = height - 235
            for _pid, item in self.cart_items.items():
                c.drawString(60, y, item['name'])
                c.drawString(350, y, str(item['qty']))
                subtotal = item['price'] * item['qty']
                c.drawRightString(width - 60, y, f"{subtotal:.2f} TND")
                y -= 25
                if y < 100:                        
                    c.showPage()
                    y = height - 50
            c.line(50, y, width - 50, y)
            y -= 30
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(colors.HexColor("#db2777"))
            c.drawString(60, y, "GRAND TOTAL")
            c.drawRightString(width - 60, y, f"{self.total_price:.2f} TND")
            c.setFillColor(colors.grey)
            c.setFont("Helvetica-Oblique", 10)
            c.drawCentredString(width / 2, 50, "Thank you for shopping with ShopManager!")
            c.save()
            if hasattr(os, 'startfile'):
                os.startfile(filename)
            else:
                import subprocess
                subprocess.run(['xdg-open' if os.name == 'posix' else 'open', filename])
            messagebox.showinfo("Receipt Printed", f"Invoice has been generated in PDF: {filename}", parent=self)
        except Exception as e:
            messagebox.showerror("Error Printing", f"Could not print invoice: {e}", parent=self)
