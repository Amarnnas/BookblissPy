#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sales & Expense Management System
"""

"""
Windows Installation & Packaging Instructions:

1. Install Python 3.9+ 64-bit from https://www.python.org/downloads/windows/
2. Install dependencies:
   pip install -r requirements.txt

3. To create a standalone .exe (no Python needed for end user):
   pip install pyinstaller
   pyinstaller --onefile --noconsole main.py

   The .exe will be in the 'dist' folder.

4. Double-click the generated main.exe to run the application.

If you see errors about missing DLLs or fonts, install Cairo and the required fonts on Windows.
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
except ImportError:
    print("Error: tkinter is not available on this system.")
    print("\nTo fix this issue:")
    print("1. On Ubuntu/Debian: sudo apt-get install python3-tk")
    print("2. On Fedora/RHEL: sudo dnf install python3-tkinter")
    print("3. On macOS: tkinter should be included with Python")
    print("4. On Windows: tkinter should be included with Python")
    print("\nIf you're using a virtual environment, you may need to:")
    print("- Deactivate the virtual environment")
    print("- Install tkinter system-wide")
    print("- Recreate the virtual environment")
    exit(1)

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import uuid
import arabic_reshaper
from bidi.algorithm import get_display

class SalesManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("نظام إدارة المبيعات والمنصرفات")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f3f4f6')
        self.lang = "ar"
        self.texts = {
            "ar": {
                "title": "نظام إدارة المبيعات والمنصرفات",
                "sales": "المبيعات",
                "all_sales": "كل المبيعات",
                "inventory": "المخزون",
                "expenses": "المنصرفات",
                "reports": "التقارير",
                "settings": "الإعدادات",
                "backup": "نسخ احتياطي",
                "add_product": "إضافة صنف",
                "remove_cart": "حذف من السلة",
                "complete_sale": "إتمام البيع",
                "clear_cart": "إفراغ السلة",
                "cart": "سلة المشتريات",
                "total": "الإجمالي",
                "ready": "جاهز",
                "add_new_product": "إضافة صنف جديد",
                "edit_product": "تعديل الصنف",
                "delete_product": "حذف الصنف",
                "inventory_panel": "لوحة المخزون",
                "sales_panel": "لوحة المبيعات",
                "expenses_panel": "لوحة المنصرفات",
                "reports_panel": "لوحة التقارير",
                "settings_panel": "لوحة الإعدادات",
                "backup_panel": "لوحة النسخ الاحتياطي",
                "add_expense": "إضافة منصرف",
                "delete_expense": "حذف المنصرف",
                "total_expenses": "إجمالي المنصرفات",
                "stat_sales": "إجمالي المبيعات",
                "stat_profit": "صافي الربح",
                "stat_products": "عدد الأصناف",
                "stat_expenses": "إجمالي المنصرفات",
                "modern": "واجهة حديثة",
                "currency": "جنيه",
                "product_type": "نوع المنتج",
                "filter_type": "تصفية حسب النوع",
                "login": "تسجيل الدخول",
                "username": "اسم المستخدم",
                "password": "كلمة المرور",
                "login_btn": "دخول",
                "logout": "تسجيل خروج",
                "language": "اللغة",
                "choose_folder": "اختر مجلد الحفظ",
                "save_folder": "حفظ المجلد",
                "invoice_image": "حفظ الفاتورة كصورة",
                "invoice_pdf": "حفظ الفاتورة PDF"
            },
            "en": {
                "title": "Sales & Expense Management System",
                "sales": "Sales",
                "all_sales": "All Sales",
                "inventory": "Inventory",
                "expenses": "Expenses",
                "reports": "Reports",
                "settings": "Settings",
                "backup": "Backup",
                "add_product": "Add Product",
                "remove_cart": "Remove from Cart",
                "complete_sale": "Complete Sale",
                "clear_cart": "Clear Cart",
                "cart": "Cart",
                "total": "Total",
                "ready": "Ready",
                "add_new_product": "Add New Product",
                "edit_product": "Edit Product",
                "delete_product": "Delete Product",
                "inventory_panel": "Inventory Panel",
                "sales_panel": "Sales Panel",
                "expenses_panel": "Expenses Panel",
                "reports_panel": "Reports Panel",
                "settings_panel": "Settings Panel",
                "backup_panel": "Backup Panel",
                "add_expense": "Add Expense",
                "delete_expense": "Delete Expense",
                "total_expenses": "Total Expenses",
                "stat_sales": "Total Sales",
                "stat_profit": "Net Profit",
                "stat_products": "Products Count",
                "stat_expenses": "Total Expenses",
                "modern": "Modern UI",
                "currency": "EGP",
                "product_type": "Product Type",
                "filter_type": "Filter by Type",
                "login": "Login",
                "username": "Username",
                "password": "Password",
                "login_btn": "Login",
                "logout": "Logout",
                "language": "Language",
                "choose_folder": "Choose Save Folder",
                "save_folder": "Save Folder",
                "invoice_image": "Save Invoice as Image",
                "invoice_pdf": "Save Invoice as PDF"
            }
        }
        self.data_file = "sales_data.json"
        self.save_folder = os.getcwd()
        self.data = self.load_data()
        self.cart = []
        self.current_panel = self.show_sales_panel
        self.logged_in = False
        self.login_screen()
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from file"""
        default_data = {
            "inventory": [],
            "sales": [],
            "expenses": [],
            "customers": [],
            "settings": {
                "currency": "EGP",
                "tax_rate": 0.0,
                "low_stock_threshold": 5
            }
        }
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default_data
        return default_data
    
    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def login_screen(self):
        """واجهة تسجيل الدخول"""
        self.root.withdraw()
        login_win = tk.Toplevel()
        login_win.title(self.texts[self.lang]["login"])
        login_win.geometry("350x250")
        login_win.resizable(False, False)
        login_win.configure(bg="#f3f4f6")
        tk.Label(login_win, text=self.texts[self.lang]["login"], font=("Cairo", 20, "bold"), bg="#f3f4f6").pack(pady=20)
        tk.Label(login_win, text=self.texts[self.lang]["username"], font=self.font_medium, bg="#f3f4f6").pack()
        username_entry = tk.Entry(login_win, font=self.font_medium)
        username_entry.pack()
        tk.Label(login_win, text=self.texts[self.lang]["password"], font=self.font_medium, bg="#f3f4f6").pack()
        password_entry = tk.Entry(login_win, font=self.font_medium, show="*")
        password_entry.pack()
        def do_login():
            # اسم المستخدم: admin، كلمة المرور: 1234
            if username_entry.get() == "admin" and password_entry.get() == "1234":
                self.logged_in = True
                login_win.destroy()
                self.root.deiconify()
                self.setup_ui()
            else:
                messagebox.showerror(self.texts[self.lang]["login"], "بيانات الدخول غير صحيحة")
        tk.Button(login_win, text=self.texts[self.lang]["login_btn"], font=self.font_medium, bg="#2563eb", fg="white", command=do_login).pack(pady=20)
        login_win.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def switch_language(self):
        self.lang = "en" if self.lang == "ar" else "ar"
        self.setup_ui()

    def setup_ui(self):
        # Use Cairo font for Arabic, fallback to Segoe UI for English
        self.font_large = ("Cairo", 22, "bold")
        self.font_medium = ("Cairo", 15, "bold")
        self.font_small = ("Cairo", 12)
        self.justify = 'right' if self.lang == "ar" else 'left'
        self.anchor = 'e' if self.lang == "ar" else 'w'
        # Redraw all parts of the interface
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_header()
        self.create_navbar()
        self.create_main_area()
        self.create_status_bar()
        self.current_panel()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#fff', height=90, bd=0, highlightthickness=0)
        header_frame.pack(fill='x', padx=30, pady=20)
        header_frame.pack_propagate(False)
        # Rounded corners and shadow (simulate with padding and border)
        header_frame.config(highlightbackground='#e5e7eb', highlightcolor='#e5e7eb', highlightthickness=1)
        title_label = tk.Label(
            header_frame,
            text=self.texts["title"],
            font=("Cairo", 28, "bold"),
            fg='#2563eb',
            bg='#fff',
            anchor='center',
            justify='center'
        )
        title_label.pack(expand=True)

    def create_navbar(self):
        nav_frame = tk.Frame(self.root, bg='#fff', height=60)
        nav_frame.pack(fill='x', padx=30, pady=(0, 20))
        nav_frame.pack_propagate(False)
        tabs = [
            ("backup_panel", self.show_backup_panel, "#64748b"),
            ("settings_panel", self.show_settings_panel, "#64748b"),
            ("reports_panel", self.show_reports_panel, "#2563eb"),
            ("expenses_panel", self.show_expenses_panel, "#dc2626"),
            ("inventory_panel", self.show_inventory_panel, "#2563eb"),
            ("sales_panel", self.show_sales_panel, "#2563eb"),
            ("all_sales", self.show_all_sales_panel, "#16a34a"),
        ]
        self.active_tab = getattr(self, "active_tab", "sales_panel")
        for idx, (key, func, color) in enumerate(tabs):
            is_active = self.active_tab == key
            btn_color = color if is_active else "#e5e7eb"
            fg_color = "#fff" if is_active else "#2563eb"
            btn = tk.Button(
                nav_frame,
                text=self.texts[self.lang].get(key, key),
                font=self.font_medium,
                bg=btn_color,
                fg=fg_color,
                bd=0,
                padx=24,
                pady=10,
                relief='flat',
                highlightthickness=0,
                cursor='hand2',
                activebackground="#1e40af" if is_active else "#cbd5e1",
                activeforeground="#fff",
                command=lambda f=func, k=key: self.switch_tab(f, k)
            )
            btn.pack(side='right', padx=(0 if idx == 0 else 12, 0))
            btn.configure(borderwidth=0)
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=c if not is_active else c))
            btn.bind("<Leave>", lambda e, b=btn, c=btn_color: b.config(bg=c))

    def switch_tab(self, func, key):
        self.active_tab = key
        self.current_panel = func
        self.setup_ui()

    def create_main_area(self):
        self.main_frame = tk.Frame(self.root, bg='#f3f4f6')
        self.main_frame.pack(fill='both', expand=True, padx=30, pady=10)

    def create_status_bar(self):
        self.status_bar = tk.Label(
            self.root,
            text=self.texts["ready"],
            relief='flat',
            anchor=self.anchor,
            font=self.font_small,
            bg='#e5e7eb',
            fg='#2563eb',
            justify=self.justify
        )
        self.status_bar.pack(side='bottom', fill='x', padx=30, pady=(0, 10))

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def reshape_arabic(self, text):
        """Reshape Arabic text for correct display in Tkinter."""
        if not text:
            return ""
        try:
            reshaped = arabic_reshaper.reshape(text)
            return get_display(reshaped)
        except Exception:
            return text

    def show_sales_panel(self):
        self.clear_main_frame()
        self.status_bar.config(text=self.texts["sales_panel"])
        # Layout: right (add product), left (cart/invoice)
        content = tk.Frame(self.main_frame, bg='#f3f4f6')
        content.pack(fill='both', expand=True)
        # Right: Add product card
        right = tk.Frame(content, bg='#fff', bd=0, highlightthickness=0)
        right.pack(side='right', fill='y', padx=(20, 0), pady=10, ipadx=10, ipady=10)
        right.config(highlightbackground='#e5e7eb', highlightcolor='#e5e7eb', highlightthickness=1)
        right.grid_propagate(False)
        right.config(relief='groove')
        tk.Label(
            right,
            text="إضافة صنف للفاتورة",
            font=("Cairo", 18, "bold"),
            fg='#16a34a',
            bg='#fff'
        ).pack(pady=(10, 20))

        # --- New: Product selection and quantity entry ---
        product_names = [f"{p['name']} - {p['price']} {self.texts['currency']}" for p in self.data['inventory']]
        selected_product = tk.StringVar(value=product_names[0] if product_names else "")
        product_dropdown = ttk.Combobox(
            right,
            values=product_names,
            textvariable=selected_product,
            font=self.font_medium,
            state="readonly"
        )
        product_dropdown.pack(fill='x', padx=10, pady=(0, 10))

        tk.Label(
            right,
            text="الكمية:",
            font=self.font_medium,
            bg='#fff'
        ).pack(pady=(0, 5))
        quantity_entry = tk.Entry(right, font=self.font_medium, justify='center')
        quantity_entry.pack(fill='x', padx=10)
        quantity_entry.insert(0, "1")

        def add_selected_direct():
            if not self.data['inventory']:
                messagebox.showwarning("Warning", "No products in inventory")
                return
            idx = product_dropdown.current()
            if idx == -1:
                messagebox.showwarning("Warning", "Please select a product")
                return
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid quantity")
                return
            product = self.data['inventory'][idx]
            if quantity > product['stock']:
                messagebox.showerror("Error", f"Requested quantity not available. Available: {product['stock']}")
                return
            # Add to cart
            cart_item = {
                'product_id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'total': product['price'] * quantity
            }
            found = False
            for item in self.cart:
                if item['product_id'] == product['id']:
                    item['quantity'] += quantity
                    item['total'] = item['price'] * item['quantity']
                    found = True
                    break
            if not found:
                self.cart.append(cart_item)
            self.update_cart_display()
            messagebox.showinfo("نجاح", "تمت إضافة الصنف للسلة")

        tk.Button(
            right,
            text="إضافة الصنف المحدد",
            font=self.font_medium,
            bg='#27ae60',
            fg='#fff',
            activebackground='#15803d',
            activeforeground='#fff',
            bd=0,
            relief='flat',
            padx=20,
            pady=12,
            command=add_selected_direct
        ).pack(fill='x', padx=10, pady=(10, 10))

        # --- Existing Add Product button (opens modal) ---
        tk.Button(
            right,
            text="إضافة صنف",
            font=self.font_medium,
            bg='#16a34a',
            fg='#fff',
            activebackground='#15803d',
            activeforeground='#fff',
            bd=0,
            relief='flat',
            padx=20,
            pady=12,
            command=self.add_to_cart
        ).pack(fill='x', padx=10, pady=(0, 10))
        # Left: Cart/Invoice card
        left = tk.Frame(content, bg='#fff', bd=0, highlightthickness=0)
        left.pack(side='left', fill='both', expand=True, padx=(0, 20), pady=10, ipadx=10, ipady=10)
        left.config(highlightbackground='#e5e7eb', highlightcolor='#e5e7eb', highlightthickness=1)
        left.config(relief='groove')
        tk.Label(
            left,
            text="الفاتورة الحالية",
            font=("Cairo", 18, "bold"),
            fg='#2563eb',
            bg='#fff'
        ).pack(pady=(10, 10))
        # Cart table
        columns = ('الصنف', 'الكمية', 'السعر', 'الإجمالي')
        self.cart_tree = ttk.Treeview(left, columns=columns, show='headings', height=10)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.font_medium, background="#f1f5f9", foreground="#2563eb")
        style.configure("Treeview", font=self.font_small, rowheight=28, background="#fff", fieldbackground="#fff")
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=120, anchor='center')
        self.cart_tree.pack(fill='both', expand=True, padx=10, pady=10)
        # زر حذف من السلة
        tk.Button(
            left,
            text="حذف من السلة",
            font=self.font_medium,
            bg='#e74c3c',
            fg='#fff',
            activebackground='#c0392b',
            activeforeground='#fff',
            bd=0,
            relief='flat',
            padx=20,
            pady=10,
            command=self.remove_from_cart
        ).pack(fill='x', padx=10, pady=(0, 10))
        # Total
        self.total_label = tk.Label(
            left,
            text="الإجمالي: 0.00 " + self.texts["currency"],
            font=("Cairo", 18, "bold"),
            fg='#2563eb',
            bg='#fff'
        )
        self.total_label.pack(pady=(10, 0))
        # Complete sale button
        tk.Button(
            left,
            text="إتمام البيع",
            font=self.font_medium,
            bg='#2563eb',
            fg='#fff',
            activebackground='#1e40af',
            activeforeground='#fff',
            bd=0,
            relief='flat',
            padx=20,
            pady=15,
            command=self.complete_sale,
            state='normal' if self.cart else 'disabled'
        ).pack(fill='x', padx=10, pady=(20, 10))
        self.update_cart_display()
    
    def show_all_sales_panel(self):
        """عرض كل المبيعات مع التاريخ وحالة الدفع واسم العميل"""
        self.clear_main_frame()
        self.status_bar.config(text=self.texts[self.lang]["all_sales"])
        columns = (self.texts[self.lang]["total"], "التاريخ", "طريقة الدفع", "اسم العميل", "رقم الفاتورة")
        sales_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        for col in columns:
            sales_tree.heading(col, text=col)
            sales_tree.column(col, width=150, anchor='center')
        sales_tree.pack(fill='both', expand=True, padx=10, pady=10)
        for sale in self.data.get('sales', []):
            date_str = datetime.fromisoformat(sale['date']).strftime('%Y-%m-%d %H:%M')
            sales_tree.insert('', 'end', values=(
                f"{sale['total']:.2f} {self.texts[self.lang]['currency']}",
                date_str,
                sale.get('payment_method', ''),
                sale.get('customer', ''),
                sale['id'][:8]
            ))

    def show_inventory_panel(self):
        """Show inventory panel with type filter"""
        self.clear_main_frame()
        self.status_bar.config(text=self.texts[self.lang]["inventory_panel"])
        title_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        title_frame.pack(fill='x', pady=(0, 20))
        tk.Label(
            title_frame,
            text=self.texts[self.lang]["inventory_panel"],
            font=self.font_large,
            bg='#ecf0f1',
            anchor=self.anchor,
            justify=self.justify
        ).pack(side='right')
        tk.Button(
            title_frame,
            text=self.texts[self.lang]["add_new_product"],
            font=self.font_medium,
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            command=self.add_product
        ).pack(side='left')
        # نوع المنتج - تصفية
        filter_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        filter_frame.pack(fill='x', pady=(0, 10))
        tk.Label(
            filter_frame,
            text=self.texts[self.lang]["filter_type"],
            font=self.font_small,
            bg='#ecf0f1'
        ).pack(side='right')
        types = list({p.get('type', '') for p in self.data['inventory'] if p.get('type', '')})
        type_var = tk.StringVar(value="")
        type_combo = ttk.Combobox(filter_frame, textvariable=type_var, values=[""] + types, font=self.font_small, width=15)
        type_combo.pack(side='right', padx=10)
        def filter_inventory(*_):
            self.update_inventory_display(type_filter=type_var.get())
        type_combo.bind("<<ComboboxSelected>>", filter_inventory)
        columns = ('ID', self.texts[self.lang]["add_product"], self.texts[self.lang]["product_type"], 'Price', 'Available Stock', 'Status')
        self.inventory_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=120, anchor='center')
        inventory_scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=inventory_scrollbar.set)
        self.inventory_tree.pack(side='left', fill='both', expand=True)
        inventory_scrollbar.pack(side='right', fill='y')
        buttons_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        buttons_frame.pack(fill='x', pady=10)
        tk.Button(
            buttons_frame,
            text=self.texts[self.lang]["edit_product"],
            font=self.font_medium,
            bg='#f39c12',
            fg='white',
            padx=20,
            pady=10,
            command=self.edit_product
        ).pack(side='right', padx=5)
        tk.Button(
            buttons_frame,
            text=self.texts[self.lang]["delete_product"],
            font=self.font_medium,
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.delete_product
        ).pack(side='right', padx=5)
        self.update_inventory_display()

    def update_inventory_display(self, type_filter=None):
        """Update inventory display with type filter"""
        if not hasattr(self, 'inventory_tree'):
            return
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        for product in self.data['inventory']:
            if type_filter and product.get('type', '') != type_filter:
                continue
            name = product['name']
            try:
                if any('\u0600' <= c <= '\u06FF' for c in name):
                    name = self.reshape_arabic(name)
            except Exception:
                pass
            status = "Available" if product['stock'] > 5 else "Low" if product['stock'] > 0 else "Out of Stock"
            self.inventory_tree.insert('', 'end', values=(
                product['id'],
                name,
                product.get('type', ''),
                f"{product['price']:.2f}",
                product['stock'],
                status
            ))

    def add_product(self):
        """Add new product with type"""
        product_window = tk.Toplevel(self.root)
        product_window.title(self.texts[self.lang]["add_new_product"])
        product_window.geometry("400x400")
        product_window.configure(bg='#ecf0f1')
        fields = [
            (self.texts[self.lang]["add_product"] + ":", "name"),
            ("السعر:", "price"),
            ("الكمية:", "stock"),
            ("الوصف:", "description"),
            (self.texts[self.lang]["product_type"] + ":", "type")
        ]
        entries = {}
        for label_text, field_name in fields:
            tk.Label(
                product_window,
                text=label_text,
                font=self.font_medium,
                bg='#ecf0f1',
                anchor='e',
                justify='right'
            ).pack(pady=(10, 5), fill='x')
            entry = tk.Entry(product_window, font=self.font_medium, width=30, justify='right')
            entry.pack(fill='x', padx=10)
            entries[field_name] = entry
        def save_product():
            try:
                name = entries['name'].get().strip()
                price = float(entries['price'].get())
                stock = int(entries['stock'].get())
                description = entries['description'].get().strip()
                ptype = entries['type'].get().strip()
                if not name:
                    raise ValueError("اسم الصنف مطلوب")
                if price <= 0 or stock < 0:
                    raise ValueError("السعر والكمية يجب أن تكون أرقام موجبة")
                product = {
                    'id': len(self.data['inventory']) + 1,
                    'name': name,
                    'price': price,
                    'stock': stock,
                    'description': description,
                    'type': ptype,
                    'created_date': datetime.now().isoformat()
                }
                self.data['inventory'].append(product)
                self.save_data()
                self.update_inventory_display()
                product_window.destroy()
                messagebox.showinfo("نجاح", "تمت إضافة الصنف بنجاح")
            except ValueError as e:
                messagebox.showerror("خطأ", str(e))
        tk.Button(
            product_window,
            text="حفظ الصنف",
            font=self.font_medium,
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            command=save_product
        ).pack(pady=20)

    def show_reports_panel(self):
        """Show reports panel with most sold products stats."""
        self.clear_main_frame()
        self.status_bar.config(text=self.texts["reports_panel"])

        tk.Label(
            self.main_frame,
            text=self.reshape_arabic("📊 Reports and Statistics"),
            font=self.font_large,
            bg='#ecf0f1',
            anchor=self.anchor,
            justify=self.justify
        ).pack(pady=20)

        stats_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        stats_frame.pack(fill='x', pady=20)

        total_sales = sum(sale['total'] for sale in self.data['sales'])
        total_expenses = sum(expense['amount'] for expense in self.data['expenses'])
        profit = total_sales - total_expenses

        self.create_stat_card(stats_frame, self.texts["stat_sales"], f"{total_sales:.2f} {self.texts['currency']}", "#27ae60")
        self.create_stat_card(stats_frame, self.texts["stat_expenses"], f"{total_expenses:.2f} {self.texts['currency']}", "#e74c3c")
        self.create_stat_card(stats_frame, self.texts["stat_profit"], f"{profit:.2f} {self.texts['currency']}", "#3498db")
        self.create_stat_card(stats_frame, self.texts["stat_products"], str(len(self.data['inventory'])), "#9b59b6")

        # --- Most Sold Products Section ---
        from collections import Counter
        import datetime

        def get_most_sold_products(period_days=None, specific_date=None):
            now = datetime.datetime.now()
            counter = Counter()
            for sale in self.data['sales']:
                sale_date = datetime.datetime.fromisoformat(sale['date'])
                if specific_date:
                    if sale_date.date() != specific_date:
                        continue
                elif period_days is not None:
                    if (now - sale_date).days >= period_days:
                        continue
                for item in sale['items']:
                    counter[item['name']] += item['quantity']
            return counter.most_common(5)

        # Helper to create a section
        def create_most_sold_section(parent, title, items):
            frame = tk.Frame(parent, bg='#fff', bd=1, relief='groove')
            frame.pack(side='right', fill='y', expand=True, padx=10, pady=10)
            tk.Label(
                frame,
                text=self.reshape_arabic(title),
                font=self.font_medium,
                bg='#fff',
                fg='#2563eb'
            ).pack(pady=(10, 5))
            for name, qty in items:
                tk.Label(
                    frame,
                    text=f"{self.reshape_arabic(name)}: {qty}",
                    font=self.font_small,
                    bg='#fff'
                ).pack(anchor='w', padx=10)

        # Periods: today, week, month, year, custom
        now = datetime.datetime.now()
        today = now.date()
        most_today = get_most_sold_products(specific_date=today)
        most_week = get_most_sold_products(period_days=7)
        most_month = get_most_sold_products(period_days=30)
        most_year = get_most_sold_products(period_days=365)

        most_frame = tk.Frame(self.main_frame, bg='#f3f4f6')
        most_frame.pack(fill='x', pady=10)

        create_most_sold_section(most_frame, "Most Sold Today", most_today)
        create_most_sold_section(most_frame, "Most Sold This Week", most_week)
        create_most_sold_section(most_frame, "Most Sold This Month", most_month)
        create_most_sold_section(most_frame, "Most Sold This Year", most_year)

        # Custom date picker
        def show_custom_date():
            import tkinter.simpledialog
            date_str = tkinter.simpledialog.askstring("Custom Date", "Enter date (YYYY-MM-DD):")
            try:
                custom_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                most_custom = get_most_sold_products(specific_date=custom_date)
                custom_win = tk.Toplevel(self.root)
                custom_win.title("Most Sold on " + date_str)
                custom_win.configure(bg='#fff')
                create_most_sold_section(custom_win, f"Most Sold on {date_str}", most_custom)
            except Exception:
                messagebox.showerror("Error", "Invalid date format.")

        tk.Button(
            most_frame,
            text="Show Most Sold on Date",
            font=self.font_small,
            bg='#2563eb',
            fg='#fff',
            command=show_custom_date
        ).pack(side='right', padx=10, pady=10)

    def create_stat_card(self, parent, title, value, color):
        """Create a statistic card"""
        card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            card_frame,
            text=title,
            font=self.font_medium,
            bg=color,
            fg='white',
            anchor=self.anchor,
            justify=self.justify
        ).pack(pady=(10, 5))
        
        tk.Label(
            card_frame,
            text=value,
            font=self.font_large,
            bg=color,
            fg='white',
            anchor=self.anchor,
            justify=self.justify
        ).pack(pady=(0, 10))
    
    def show_settings_panel(self):
        """Show settings panel with language and folder options"""
        self.clear_main_frame()
        self.status_bar.config(text=self.texts[self.lang]["settings_panel"])
        tk.Label(
            self.main_frame,
            text=self.texts[self.lang]["settings"],
            font=self.font_large,
            bg='#f8fafc',
            anchor=self.anchor,
            justify=self.justify
        ).pack(pady=20)
        # لغة التطبيق
        lang_frame = tk.Frame(self.main_frame, bg='#f8fafc')
        lang_frame.pack(pady=10)
        tk.Label(lang_frame, text=self.texts[self.lang]["language"], font=self.font_medium, bg='#f8fafc').pack(side='right')
        tk.Button(lang_frame, text="عربي/English", font=self.font_medium, command=self.switch_language).pack(side='right', padx=10)
        # اختيار مجلد الحفظ
        folder_frame = tk.Frame(self.main_frame, bg='#f8fafc')
        folder_frame.pack(pady=10)
        tk.Label(folder_frame, text=self.texts[self.lang]["choose_folder"], font=self.font_medium, bg='#f8fafc').pack(side='right')
        tk.Button(folder_frame, text=self.texts[self.lang]["save_folder"], font=self.font_medium, command=self.choose_save_folder).pack(side='right', padx=10)
        tk.Label(folder_frame, text=self.save_folder, font=self.font_small, bg='#f8fafc', fg='#64748b').pack(side='right', padx=10)
        messagebox.showinfo(self.texts[self.lang]["settings"], self.texts[self.lang]["modern"])

    def choose_save_folder(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory(title=self.texts[self.lang]["choose_folder"])
        if folder:
            self.save_folder = folder
            self.data_file = os.path.join(self.save_folder, "sales_data.json")
            self.save_data()
            messagebox.showinfo("تم", f"تم اختيار مجلد الحفظ: {self.save_folder}")

    def complete_sale(self):
        """Complete the sale with invoice export"""
        if not self.cart:
            messagebox.showwarning("تنبيه", "السلة فارغة")
            return
        sale_window = tk.Toplevel(self.root)
        sale_window.title(self.texts[self.lang]["complete_sale"])
        sale_window.geometry("400x400")
        sale_window.configure(bg='#ecf0f1')
        total = sum(item['total'] for item in self.cart)
        tk.Label(
            sale_window,
            text=f"{self.texts[self.lang]['total']}: {total:.2f} {self.texts[self.lang]['currency']}",
            font=self.font_large,
            bg='#ecf0f1',
            anchor=self.anchor,
            justify=self.justify
        ).pack(pady=20)
        tk.Label(
            sale_window,
            text="طريقة الدفع:",
            font=self.font_medium,
            bg='#ecf0f1',
            anchor=self.anchor,
            justify=self.justify
        ).pack()
        payment_var = tk.StringVar(value="نقداً")
        payment_frame = tk.Frame(sale_window, bg='#ecf0f1')
        payment_frame.pack(pady=10)
        tk.Radiobutton(
            payment_frame,
            text="نقداً",
            variable=payment_var,
            value="نقداً",
            font=self.font_medium,
            bg='#ecf0f1',
            anchor=self.anchor,
            justify=self.justify
        ).pack(side='right', padx=10)
        tk.Radiobutton(
            payment_frame,
            text="آجل",
            variable=payment_var,
            value="آجل",
            font=self.font_medium,
            bg='#ecf0f1',
            anchor=self.anchor,
            justify=self.justify
        ).pack(side='right', padx=10)
        tk.Label(
            sale_window,
            text="اسم العميل (سيظهر في الفاتورة):",
            font=self.font_medium,
            bg='#ecf0f1',
            anchor=self.anchor,
            justify=self.justify
        ).pack(pady=(20, 5))
        customer_entry = tk.Entry(sale_window, font=self.font_medium, width=30)
        customer_entry.pack()
        def confirm_sale():
            sale = {
                'id': str(uuid.uuid4()),
                'date': datetime.now().isoformat(),
                'items': self.cart.copy(),
                'total': total,
                'payment_method': payment_var.get(),
                'customer': customer_entry.get() or "Guest"
            }
            self.data['sales'].append(sale)
            for cart_item in self.cart:
                for product in self.data['inventory']:
                    if product['id'] == cart_item['product_id']:
                        product['stock'] -= cart_item['quantity']
                        break
            self.cart.clear()
            self.save_data()
            self.update_cart_display()
            sale_window.destroy()
            messagebox.showinfo("نجاح", f"تمت عملية البيع بنجاح\nرقم الفاتورة: {sale['id'][:8]}\nالعميل: {sale['customer']}")
            self.export_invoice_dialog(sale)
        tk.Button(
            sale_window,
            text="تأكيد البيع",
            font=self.font_medium,
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            command=confirm_sale
        ).pack(pady=20)

    def export_invoice_dialog(self, sale):
        """نافذة تصدير الفاتورة كصورة أو PDF"""
        win = tk.Toplevel(self.root)
        win.title("تصدير الفاتورة")
        win.geometry("300x200")
        win.configure(bg="#f3f4f6")
        tk.Label(win, text="تصدير الفاتورة", font=self.font_large, bg="#f3f4f6").pack(pady=10)
        tk.Button(win, text=self.texts[self.lang]["invoice_image"], font=self.font_medium, command=lambda: self.export_invoice_image(sale)).pack(pady=10)
        tk.Button(win, text=self.texts[self.lang]["invoice_pdf"], font=self.font_medium, command=lambda: self.export_invoice_pdf(sale)).pack(pady=10)

    def export_invoice_image(self, sale):
        """حفظ الفاتورة كصورة (PNG)"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            width, height = 400, 60 + 40 * len(sale['items'])
            img = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            y = 10
            draw.text((10, y), f"فاتورة رقم: {sale['id'][:8]}", fill="black", font=font)
            y += 20
            draw.text((10, y), f"العميل: {sale['customer']}", fill="black", font=font)
            y += 20
            draw.text((10, y), f"التاريخ: {datetime.fromisoformat(sale['date']).strftime('%Y-%m-%d %H:%M')}", fill="black", font=font)
            y += 20
            for item in sale['items']:
                draw.text((10, y), f"{item['name']} x{item['quantity']} = {item['total']:.2f}", fill="black", font=font)
                y += 20
            draw.text((10, y), f"الإجمالي: {sale['total']:.2f}", fill="black", font=font)
            filename = os.path.join(self.save_folder, f"فاتورة_{sale['id'][:8]}.png")
            img.save(filename)
            messagebox.showinfo("تم", f"تم حفظ الفاتورة كصورة: {filename}")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    def export_invoice_pdf(self, sale):
        """حفظ الفاتورة كملف PDF"""
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"فاتورة رقم: {sale['id'][:8]}", ln=1)
            pdf.cell(200, 10, txt=f"العميل: {sale['customer']}", ln=1)
            pdf.cell(200, 10, txt=f"التاريخ: {datetime.fromisoformat(sale['date']).strftime('%Y-%m-%d %H:%M')}", ln=1)
            for item in sale['items']:
                pdf.cell(200, 10, txt=f"{item['name']} x{item['quantity']} = {item['total']:.2f}", ln=1)
            pdf.cell(200, 10, txt=f"الإجمالي: {sale['total']:.2f}", ln=1)
            filename = os.path.join(self.save_folder, f"فاتورة_{sale['id'][:8]}.pdf")
            pdf.output(filename)
            messagebox.showinfo("تم", f"تم حفظ الفاتورة PDF: {filename}")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

# ...existing code...fpdf
