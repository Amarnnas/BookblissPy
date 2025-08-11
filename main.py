#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المبيعات والمصروفات مع تأجير الكتب
Sales Management System with Book Rental Feature
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
from datetime import datetime, timedelta
import uuid
from typing import Dict, List, Any, Optional
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المبيعات والمصروفات مع تأجير الكتب - نسخة مطورة
Developed by Ammar
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as b
from ttkbootstrap.constants import *
import json
import os
from datetime import datetime, timedelta
import uuid
from decimal import Decimal, getcontext
import csv
from typing import Dict, List, Any, Optional

# ضبط دقة الحسابات المالية
getcontext().prec = 10  # Precision for Decimal calculations

# --- واجهة وتصميم ---
# استخدام نفس الألوان المطلوبة في ثيم مخصص
THEME_NAME = 'bookbliss_theme'
COLORS = {
    'primary': '#060685',       # أزرق داكن للأجزاء الرئيسية
    'secondary': '#eeca11',    # أصفر ذهبي للأزرار والعناصر الثانوية
    'success': '#28a745',       # أخضر
    'info': '#17a2b8',          # سماوي
    'warning': '#ffc107',       # أصفر تحذيري
    'danger': '#dc3545',        # أحمر
    'light': '#f2f2f2',         # رمادي فاتح للخلفيات
    'dark': '#343a40',          # رمادي داكن للنصوص
    'bg': '#d4d2d2',            # خلفية النوافذ الرئيسية
    'fg': '#333333',            # لون الخط الأساسي
}

# --- الفئة الرئيسية للتطبيق ---
class SalesManagementSystem:
    def __init__(self, root: b.Window):
        self.root = root
        self.root.title("BookBliss - نظام إدارة المكتبة والمبيعات")
        self.root.geometry("1400x850")
        
        self.data_file = "bookbliss_data.json"
        self.load_data()

        self.cart = []
        self.cart_total = Decimal('0.00')
        
        self.create_widgets()
        self.update_dashboard()

        # الحفظ التلقائي عند الإغلاق
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """يتم استدعاؤها عند إغلاق النافذة الرئيسية."""
        if messagebox.askokcancel("إغلاق", "هل تريد إغلاق البرنامج؟ سيتم حفظ البيانات تلقائياً."):
            self.save_data()
            self.root.destroy()

    def load_data(self):
        """تحميل البيانات من ملف JSON وتحويل الأرقام إلى Decimal."""
        default_data = {"inventory": [], "sales": [], "expenses": [], "rentals": []}
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)
                
                self.data = default_data
                self.data['inventory'] = [
                    {**item, 'price': Decimal(item.get('price', '0'))} 
                    for item in raw_data.get('inventory', [])
                ]
                self.data['sales'] = [
                    {**sale, 'total': Decimal(sale.get('total', '0')), 
                     'items': [{**i, 'price': Decimal(i.get('price', '0')), 'total': Decimal(i.get('total', '0'))} for i in sale.get('items', [])]}
                    for sale in raw_data.get('sales', [])
                ]
                self.data['expenses'] = [
                    {**exp, 'amount': Decimal(exp.get('amount', '0'))} 
                    for exp in raw_data.get('expenses', [])
                ]
                self.data['rentals'] = [
                    {**rent, 'amount': Decimal(rent.get('amount', '0'))}
                    for rent in raw_data.get('rentals', [])
                ]

            except (json.JSONDecodeError, KeyError) as e:
                messagebox.showerror("خطأ في تحميل البيانات", f"الملف تالف أو غير متوافق. سيتم إنشاء ملف جديد.\n{e}")
                self.data = default_data
        else:
            self.data = default_data
        
        if not self.data['inventory']:
            self.data['inventory'].append({
                'id': str(uuid.uuid4()), 'name': 'منتج افتراضي', 'price': Decimal('500.00'), 
                'stock': 10, 'description': 'منتج للاختبار'
            })

    def save_data(self):
        """حفظ البيانات إلى ملف JSON مع تحويل Decimal إلى string."""
        try:
            data_to_save = {
                'inventory': [{**item, 'price': str(item['price'])} for item in self.data['inventory']],
                'sales': [
                    {**sale, 'total': str(sale['total']), 
                     'items': [{**i, 'price': str(i['price']), 'total': str(i['total'])} for i in sale['items']]}
                    for sale in self.data['sales']
                ],
                'expenses': [{**exp, 'amount': str(exp['amount'])} for exp in self.data['expenses']],
                'rentals': [{**rent, 'amount': str(rent['amount'])} for rent in self.data['rentals']]
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("خطأ في الحفظ", f"لم يتمكن من حفظ البيانات: {e}")

    def parse_datetime_flexible(self, date_string: str) -> Optional[datetime]:
        """تحليل سلسلة التاريخ بتنسيقات متعددة."""
        formats_to_try = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d"]
        for fmt in formats_to_try:
            try:
                return datetime.strptime(date_string, fmt)
            except (ValueError, TypeError):
                continue
        return None

    def create_widgets(self):
        """إنشاء الواجهة الرئيسية باستخدام نظام التبويبات."""
        main_pane = b.Frame(self.root, padding=10)
        main_pane.pack(fill=BOTH, expand=YES)

        self.notebook = b.Notebook(main_pane)
        self.notebook.pack(fill=BOTH, expand=YES)

        # إنشاء التبويبات
        self.dashboard_tab = b.Frame(self.notebook, padding=10)
        self.pos_tab = b.Frame(self.notebook, padding=10)
        self.inventory_tab = b.Frame(self.notebook, padding=10)
        self.rentals_tab = b.Frame(self.notebook, padding=10)
        self.expenses_tab = b.Frame(self.notebook, padding=10)
        self.reports_tab = b.Frame(self.notebook, padding=10)

        self.notebook.add(self.dashboard_tab, text='📊  لوحة التحكم  ')
        self.notebook.add(self.pos_tab, text='🛒  نقطة البيع  ')
        self.notebook.add(self.inventory_tab, text='📦  المخزون  ')
        self.notebook.add(self.rentals_tab, text='📚  الإيجارات  ')
        self.notebook.add(self.expenses_tab, text='💰  المصروفات  ')
        self.notebook.add(self.reports_tab, text='📈  التقارير والسجلات  ')

        # بناء محتوى كل تبويب
        self.create_dashboard_tab()
        self.create_pos_tab()
        self.create_inventory_tab()
        self.create_rentals_tab()
        self.create_expenses_tab()
        self.create_reports_tab()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        """تحديث البيانات عند تغيير التبويب."""
        try:
            selected_tab = self.notebook.tab(self.notebook.select(), "text")
            if "لوحة التحكم" in selected_tab:
                self.update_dashboard()
            elif "المخزون" in selected_tab:
                self.update_inventory_display()
            elif "الإيجارات" in selected_tab:
                self.update_rentals_display()
            elif "المصروفات" in selected_tab:
                self.update_expenses_display()
        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    # --- تبويب لوحة التحكم ---
    # ------------------------------------------------------------------
    def create_dashboard_tab(self):
        b.Label(self.dashboard_tab, text="ملخص الأداء", font=("Arial", 24, "bold"), bootstyle=DARK).pack(pady=10)
        
        stats_frame = b.Frame(self.dashboard_tab)
        stats_frame.pack(fill=BOTH, expand=YES, pady=20)
        
        sales_frame = b.Labelframe(stats_frame, text=" ملخص اليوم ", bootstyle=SUCCESS, padding=20)
        sales_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        stock_frame = b.Labelframe(stats_frame, text=" تنبيهات المخزون ", bootstyle=WARNING, padding=20)
        stock_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        rentals_frame = b.Labelframe(stats_frame, text=" الإيجارات المتأخرة ", bootstyle=DANGER, padding=20)
        rentals_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.daily_sales_label = b.Label(sales_frame, text="إجمالي المبيعات: 0.00 SDG", font=("Arial", 16))
        self.daily_sales_label.pack(pady=5)
        self.daily_expenses_label = b.Label(sales_frame, text="إجمالي المصروفات: 0.00 SDG", font=("Arial", 16))
        self.daily_expenses_label.pack(pady=5)
        self.daily_profit_label = b.Label(sales_frame, text="صافي الربح: 0.00 SDG", font=("Arial", 18, "bold"))
        self.daily_profit_label.pack(pady=10)

        self.low_stock_list = b.Treeview(stock_frame, columns=("product", "stock"), show="", height=8)
        self.low_stock_list.column("product", width=200)
        self.low_stock_list.pack(fill=BOTH, expand=YES)

        self.overdue_rentals_list = b.Treeview(rentals_frame, columns=("book", "renter"), show="", height=8)
        self.overdue_rentals_list.column("book", width=200)
        self.overdue_rentals_list.pack(fill=BOTH, expand=YES)
        
    def update_dashboard(self):
        today = datetime.now().date()
        
        daily_sales = sum(s['total'] for s in self.data['sales'] if (dt := self.parse_datetime_flexible(s['date'])) and dt.date() == today)
        daily_expenses = sum(e['amount'] for e in self.data['expenses'] if (dt := self.parse_datetime_flexible(e['date'])) and dt.date() == today)
        profit = daily_sales - daily_expenses
        
        self.daily_sales_label.config(text=f"إجمالي المبيعات: {daily_sales:.2f} SDG")
        self.daily_expenses_label.config(text=f"إجمالي المصروفات: {daily_expenses:.2f} SDG")
        self.daily_profit_label.config(text=f"صافي الربح: {profit:.2f} SDG", bootstyle=(SUCCESS if profit >= 0 else DANGER))

        for i in self.low_stock_list.get_children(): self.low_stock_list.delete(i)
        low_stock_items = [p for p in self.data['inventory'] if p['stock'] <= 5]
        for item in low_stock_items:
            self.low_stock_list.insert("", END, values=(f"{item['name']}", f"المتبقي: {item['stock']}"))

        for i in self.overdue_rentals_list.get_children(): self.overdue_rentals_list.delete(i)
        overdue_rentals = [r for r in self.data['rentals'] if r['status'] == 'مُعَار' and (dt := self.parse_datetime_flexible(r['due_date'])) and dt.date() < today]
        for rental in overdue_rentals:
            self.overdue_rentals_list.insert("", END, values=(f"{rental['book_name']}", f"المستأجر: {rental['renter_name']}"))

    # ------------------------------------------------------------------
    # --- تبويب نقطة البيع ---
    # ------------------------------------------------------------------
    def create_pos_tab(self):
        pos_pane = b.PanedWindow(self.pos_tab, orient=HORIZONTAL)
        pos_pane.pack(fill=BOTH, expand=YES)

        add_item_frame = b.Frame(pos_pane, padding=10)
        pos_pane.add(add_item_frame, weight=1)

        b.Label(add_item_frame, text="إضافة منتج للفاتورة", font=("Arial", 18, "bold")).pack(pady=10)
        
        form_frame = b.Frame(add_item_frame)
        form_frame.pack(pady=20)
        
        b.Label(form_frame, text="المنتج:", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=10, sticky='w')
        self.pos_product_var = b.StringVar()
        self.pos_product_combo = b.Combobox(form_frame, textvariable=self.pos_product_var, font=("Arial", 14), width=25)
        self.pos_product_combo.grid(row=0, column=1, padx=5, pady=10)
        
        b.Label(form_frame, text="الكمية:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=10, sticky='w')
        self.pos_quantity_var = b.StringVar(value="1")
        b.Entry(form_frame, textvariable=self.pos_quantity_var, font=("Arial", 14), width=10).grid(row=1, column=1, padx=5, pady=10, sticky='w')

        b.Button(form_frame, text="إضافة للسلة", command=self.add_to_cart, bootstyle=SUCCESS, width=20).grid(row=2, column=0, columnspan=2, pady=20)

        cart_frame = b.Frame(pos_pane, padding=10)
        pos_pane.add(cart_frame, weight=2)
        
        b.Label(cart_frame, text="الفاتورة الحالية", font=("Arial", 18, "bold")).pack(pady=10)
        
        cart_tree_frame = b.Frame(cart_frame)
        cart_tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        cart_cols = ("total", "price", "quantity", "product")
        self.cart_tree = b.Treeview(cart_tree_frame, columns=cart_cols, show='headings', height=10, bootstyle=PRIMARY)
        self.cart_tree.heading("product", text="المنتج")
        self.cart_tree.heading("quantity", text="الكمية")
        self.cart_tree.heading("price", text="السعر")
        self.cart_tree.heading("total", text="الإجمالي")
        self.cart_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        
        checkout_frame = b.Frame(cart_frame)
        checkout_frame.pack(fill=X, pady=10)
        
        self.cart_total_label = b.Label(checkout_frame, text="الإجمالي: 0.00 SDG", font=("Arial", 18, "bold"), bootstyle=SUCCESS)
        self.cart_total_label.pack(pady=10)
        
        payment_details_frame = b.Frame(checkout_frame)
        payment_details_frame.pack(pady=10)
        
        b.Label(payment_details_frame, text="العميل:", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
        self.pos_customer_var = b.StringVar()
        b.Entry(payment_details_frame, textvariable=self.pos_customer_var, font=("Arial", 14)).grid(row=0, column=1, padx=5, pady=5)
        
        b.Label(payment_details_frame, text="الدفع:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5)
        self.pos_payment_var = b.StringVar(value="نقداً")
        payment_combo = b.Combobox(payment_details_frame, textvariable=self.pos_payment_var, font=("Arial", 14), values=["نقداً", "آجل", "حساب بنكي"])
        payment_combo.grid(row=1, column=1, padx=5, pady=5)
        
        action_buttons_frame = b.Frame(checkout_frame)
        action_buttons_frame.pack(pady=20)
        b.Button(action_buttons_frame, text="إتمام البيع", command=self.checkout, bootstyle=SUCCESS, width=15).pack(side=LEFT, padx=10)
        b.Button(action_buttons_frame, text="مسح السلة", command=self.clear_cart, bootstyle=DANGER, width=15).pack(side=LEFT, padx=10)
    
    def add_to_cart(self):
        product_name = self.pos_product_var.get()
        quantity_str = self.pos_quantity_var.get()
        
        if not product_name or not quantity_str:
            messagebox.showwarning("نقص في المعلومات", "يرجى اختيار منتج وتحديد الكمية.")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("خطأ", "الكمية يجب أن تكون رقماً صحيحاً وأكبر من صفر.")
            return
        
        product = next((p for p in self.data['inventory'] if p['name'] == product_name), None)
        if not product:
            messagebox.showerror("خطأ", "المنتج المحدد غير موجود.")
            return
            
        if product['stock'] < quantity:
            messagebox.showwarning("المخزون لا يكفي", f"الكمية المطلوبة ({quantity}) أكبر من المتوفر ({product['stock']}).")
            return

        existing_item = next((item for item in self.cart if item['id'] == product['id']), None)
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            self.cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': quantity})
        
        self.update_cart_display()
        self.pos_product_var.set('')
        self.pos_quantity_var.set('1')

    def update_cart_display(self):
        for i in self.cart_tree.get_children(): self.cart_tree.delete(i)
        
        self.cart_total = Decimal('0.00')
        for item in self.cart:
            item_total = item['price'] * item['quantity']
            self.cart_tree.insert("", END, values=(f"{item_total:.2f}", f"{item['price']:.2f}", item['quantity'], item['name']))
            self.cart_total += item_total
            
        self.cart_total_label.config(text=f"الإجمالي: {self.cart_total:.2f} SDG")

    def clear_cart(self):
        if self.cart and messagebox.askyesno("تأكيد", "هل تريد بالتأكيد إفراغ السلة؟"):
            self.cart = []
            self.update_cart_display()

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("السلة فارغة", "لا يمكن إتمام البيع لأن السلة فارغة.")
            return

        payment_method = self.pos_payment_var.get()
        bank_details = None

        if payment_method == "حساب بنكي":
            bank_details = self.ask_bank_details()
            if not bank_details:
                return

        sale_record = {
            'id': str(uuid.uuid4()),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'customer': self.pos_customer_var.get().strip() or "عميل نقدي",
            'payment_method': payment_method,
            'status': 'مدفوعة' if payment_method != 'آجل' else 'آجل',
            'items': [{'id': i['id'], 'name': i['name'], 'price': i['price'], 'quantity': i['quantity'], 'total': i['price'] * i['quantity']} for i in self.cart],
            'total': self.cart_total,
            'bank_details': bank_details
        }

        for item in self.cart:
            product = next((p for p in self.data['inventory'] if p['id'] == item['id']), None)
            if product:
                product['stock'] -= item['quantity']
        
        self.data['sales'].append(sale_record)
        self.save_data()
        
        messagebox.showinfo("نجاح", f"تم تسجيل الفاتورة بنجاح برقم: {sale_record['id'][:8]}")

        self.cart = []
        self.update_cart_display()
        self.pos_customer_var.set('')
        self.update_dashboard()

    def ask_bank_details(self):
        dialog = b.Toplevel(self.root, title="تفاصيل الدفع البنكي")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = {}

        b.Label(dialog, text="اسم البنك:", font=("Arial", 12)).pack(pady=5)
        bank_name_var = b.StringVar()
        b.Entry(dialog, textvariable=bank_name_var, font=("Arial", 12)).pack(pady=5, padx=20, fill=X)
        
        b.Label(dialog, text="رقم العملية:", font=("Arial", 12)).pack(pady=5)
        trans_id_var = b.StringVar()
        b.Entry(dialog, textvariable=trans_id_var, font=("Arial", 12)).pack(pady=5, padx=20, fill=X)
        
        def on_ok():
            if not bank_name_var.get() or not trans_id_var.get():
                messagebox.showwarning("نقص", "يرجى ملء جميع الحقول.", parent=dialog)
                return
            result['bank_name'] = bank_name_var.get()
            result['transaction_id'] = trans_id_var.get()
            dialog.destroy()

        ok_button = b.Button(dialog, text="موافق", command=on_ok, bootstyle=SUCCESS)
        ok_button.pack(pady=20)
        
        self.root.wait_window(dialog)
        return result if 'bank_name' in result else None

    # ------------------------------------------------------------------
    # --- تبويب المخزون ---
    # ------------------------------------------------------------------
    def create_inventory_tab(self):
        b.Label(self.inventory_tab, text="إدارة المخزون", font=("Arial", 24, "bold"), bootstyle=DARK).pack(pady=10)
        
        control_frame = b.Frame(self.inventory_tab)
        control_frame.pack(fill=X, pady=10)
        b.Button(control_frame, text="إضافة منتج جديد", command=lambda: self.add_or_edit_product_dialog(), bootstyle=SUCCESS).pack(side=RIGHT, padx=5)
        b.Button(control_frame, text="تعديل المنتج المحدد", command=self.edit_selected_product, bootstyle=INFO).pack(side=RIGHT, padx=5)
        b.Button(control_frame, text="حذف المنتج المحدد", command=self.delete_selected_product, bootstyle=DANGER).pack(side=RIGHT, padx=5)
        
        tree_frame = b.Frame(self.inventory_tab)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        inv_cols = ('description', 'stock', 'price', 'name')
        self.inventory_tree = b.Treeview(tree_frame, columns=inv_cols, show='headings', bootstyle=PRIMARY)
        self.inventory_tree.heading('name', text='اسم المنتج')
        self.inventory_tree.heading('price', text='السعر (SDG)')
        self.inventory_tree.heading('stock', text='الكمية المتاحة')
        self.inventory_tree.heading('description', text='الوصف')
        self.inventory_tree.pack(fill=BOTH, expand=YES, side=LEFT)
        
        scrollbar = b.Scrollbar(tree_frame, orient=VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def update_inventory_display(self):
        for i in self.inventory_tree.get_children(): self.inventory_tree.delete(i)
        for item in sorted(self.data['inventory'], key=lambda x: x['name']):
            self.inventory_tree.insert("", END, iid=item['id'], values=(item.get('description', ''), item['stock'], f"{item['price']:.2f}", item['name']))
        
        product_names = [item['name'] for item in self.data['inventory'] if item['stock'] > 0]
        self.pos_product_combo['values'] = product_names

    def add_or_edit_product_dialog(self, product=None):
        is_edit = product is not None
        dialog = b.Toplevel(self.root, title="تعديل منتج" if is_edit else "إضافة منتج جديد")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = b.Frame(dialog, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        fields = {"اسم المنتج": b.StringVar(value=product['name'] if is_edit else ""),
                  "السعر": b.StringVar(value=str(product['price']) if is_edit else ""),
                  "الكمية": b.StringVar(value=str(product['stock']) if is_edit else ""),
                  "الوصف": b.StringVar(value=product.get('description', '') if is_edit else "")}

        for i, (label, var) in enumerate(fields.items()):
            b.Label(frame, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky='w')
            b.Entry(frame, textvariable=var, font=("Arial", 12)).grid(row=i, column=1, padx=10, pady=10, sticky='ew')
        
        frame.grid_columnconfigure(1, weight=1)

        def save():
            name = fields["اسم المنتج"].get().strip()
            price_str = fields["السعر"].get().strip()
            stock_str = fields["الكمية"].get().strip()
            
            if not all([name, price_str, stock_str]):
                messagebox.showerror("خطأ", "يجب ملء حقول الاسم والسعر والكمية.", parent=dialog)
                return
            
            try:
                price = Decimal(price_str)
                stock = int(stock_str)
            except Exception:
                messagebox.showerror("خطأ", "السعر والكمية يجب أن تكون أرقاماً صالحة.", parent=dialog)
                return

            name_lower = name.lower()
            for p in self.data['inventory']:
                if p['name'].lower() == name_lower and (not is_edit or p['id'] != product['id']):
                    messagebox.showerror("خطأ", "اسم المنتج موجود بالفعل.", parent=dialog)
                    return

            if is_edit:
                product.update({'name': name, 'price': price, 'stock': stock, 'description': fields["الوصف"].get().strip()})
            else:
                self.data['inventory'].append({'id': str(uuid.uuid4()), 'name': name, 'price': price, 'stock': stock, 'description': fields["الوصف"].get().strip()})
            
            self.save_data()
            self.update_inventory_display()
            self.update_dashboard()
            dialog.destroy()

        b.Button(frame, text="حفظ", command=save, bootstyle=SUCCESS).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def edit_selected_product(self):
        if not self.inventory_tree.selection():
            messagebox.showwarning("تنبيه", "يرجى تحديد منتج لتعديله.")
            return
        prod_id = self.inventory_tree.selection()[0]
        product = next((p for p in self.data['inventory'] if p['id'] == prod_id), None)
        if product:
            self.add_or_edit_product_dialog(product)

    def delete_selected_product(self):
        if not self.inventory_tree.selection():
            messagebox.showwarning("تنبيه", "يرجى تحديد منتج لحذفه.")
            return
        prod_id = self.inventory_tree.selection()[0]
        product = next((p for p in self.data['inventory'] if p['id'] == prod_id), None)
        if product and messagebox.askyesno("تأكيد الحذف", f"هل تريد بالتأكيد حذف المنتج '{product['name']}'؟"):
            self.data['inventory'] = [p for p in self.data['inventory'] if p['id'] != prod_id]
            self.save_data()
            self.update_inventory_display()
            self.update_dashboard()

    # ------------------------------------------------------------------
    # --- تبويب الإيجارات ---
    # ------------------------------------------------------------------
    def create_rentals_tab(self):
        b.Label(self.rentals_tab, text="إدارة إيجارات الكتب", font=("Arial", 24, "bold"), bootstyle=DARK).pack(pady=10)
        pass

    # ------------------------------------------------------------------
    # --- تبويب المصروفات ---
    # ------------------------------------------------------------------
    def create_expenses_tab(self):
        b.Label(self.expenses_tab, text="إدارة المصروفات", font=("Arial", 24, "bold"), bootstyle=DARK).pack(pady=10)
        pass

    # ------------------------------------------------------------------
    # --- تبويب التقارير ---
    # ------------------------------------------------------------------
    def create_reports_tab(self):
        b.Label(self.reports_tab, text="التقارير والسجلات", font=("Arial", 24, "bold"), bootstyle=DARK).pack(pady=10)
        
        export_frame = b.Frame(self.reports_tab)
        export_frame.pack(fill=X, pady=20)
        b.Button(export_frame, text="تصدير المبيعات إلى Excel", command=self.export_sales_to_csv, bootstyle=(INFO, OUTLINE)).pack(side=RIGHT, padx=10)
        b.Button(export_frame, text="تصدير المصروفات إلى Excel", command=self.export_expenses_to_csv, bootstyle=(INFO, OUTLINE)).pack(side=RIGHT, padx=10)
        pass

    def export_sales_to_csv(self):
        if not self.data['sales']:
            messagebox.showinfo("لا توجد بيانات", "سجل المبيعات فارغ.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="تصدير المبيعات")
        if not file_path: return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['رقم الفاتورة', 'التاريخ', 'العميل', 'طريقة الدفع', 'الحالة', 'اسم المنتج', 'الكمية', 'السعر', 'الإجمالي للمنتج', 'الإجمالي للفاتورة'])
                for sale in self.data['sales']:
                    for item in sale['items']:
                        writer.writerow([
                            sale['id'], sale['date'], sale['customer'], sale['payment_method'], sale['status'],
                            item['name'], item['quantity'], item['price'], item['total'], sale['total']
                        ])
            messagebox.showinfo("نجاح", f"تم تصدير المبيعات بنجاح إلى:\n{file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل تصدير البيانات: {e}")

    def export_expenses_to_csv(self):
        if not self.data['expenses']:
            messagebox.showinfo("لا توجد بيانات", "سجل المصروفات فارغ.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="تصدير المصروفات")
        if not file_path: return

        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['التاريخ', 'الوصف', 'المبلغ (SDG)'])
                for exp in self.data['expenses']:
                    writer.writerow([exp['date'], exp['description'], exp['amount']])
            messagebox.showinfo("نجاح", f"تم تصدير المصروفات بنجاح إلى:\n{file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل تصدير البيانات: {e}")
            
    def update_rentals_display(self): pass
    def update_expenses_display(self): pass


if __name__ == "__main__":
    # Create the main window first, using a standard theme as a base
    app = b.Window(themename="litera")
    
    # Get the style object associated with the window
    style = app.style
    
    # Define the custom theme using the COLORS dictionary
    # This registers the new theme name
    style.configure(THEME_NAME, colors=COLORS)
    
    # Now, explicitly switch the window's theme to our newly created theme
    style.theme_use(THEME_NAME)
    
    # Instantiate the main application class
    SalesManagementSystem(app)
    
    # Start the Tkinter main loop
    app.mainloop()

# الألوان والتصميم
COLORS = {
    'primary': '#eeca11',      # أصفر ذهبي
    'secondary': '#f2f2f2',    # رمادي فاتح
    'accent': '#060685',       # أزرق داكن
    'background': '#d4d2d2',     # أبيض
    'text': '#333333',          # رمادي داكن
    'success': '#28a745',       # أخضر
    'warning': '#ffc107',       # أصفر تحذيري
    'danger': '#dc3545',        # أحمر
    'light': '#f8f9fa',         # رمادي فاتح جداً
    'dark': '#343a40'           # رمادي داكن
}

FONT_SIZES = {
    'small': 10,
    'medium': 12,
    'large': 14,
    'xlarge': 16,
    'xxlarge': 18
}

class ModernButton(tk.Button):
    """زر حديث مع تصميم أنيق"""
    def __init__(self, parent, text="", command=None, style="primary", **kwargs):
        # تحديد الألوان حسب النمط
        if style == "primary":
            bg_color = COLORS['primary']
            fg_color = COLORS['accent']
            active_bg = COLORS['accent']
            active_fg = COLORS['background']
        elif style == "secondary":
            bg_color = COLORS['secondary']
            fg_color = COLORS['text']
            active_bg = COLORS['text']
            active_fg = COLORS['background']
        elif style == "success":
            bg_color = COLORS['success']
            fg_color = COLORS['background']
            active_bg = COLORS['background']
            active_fg = COLORS['success']
        elif style == "danger":
            bg_color = COLORS['danger']
            fg_color = COLORS['background']
            active_bg = COLORS['background']
            active_fg = COLORS['danger']
        else:
            bg_color = COLORS['light']
            fg_color = COLORS['text']
            active_bg = COLORS['text']
            active_fg = COLORS['background']
        
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            activebackground=active_bg,
            activeforeground=active_fg,
            relief='flat',
            borderwidth=0,
            font=('Arial', FONT_SIZES['medium'], 'bold'),
            cursor='hand2',
            padx=20,
            pady=10,
            **kwargs
        )
        
        # تأثيرات التفاعل
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self.default_bg = bg_color
        self.hover_bg = active_bg
        self.default_fg = fg_color
        self.hover_fg = active_fg
    
    def _on_enter(self, event):
        self.config(bg=self.hover_bg, fg=self.hover_fg)
    
    def _on_leave(self, event):
        self.config(bg=self.default_bg, fg=self.default_fg)

class SalesManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام إدارة المبيعات والمصروفات مع تأجير الكتب")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['background'])
        
        # تحميل البيانات
        self.data_file = "sales_data.json"
        self.load_data()
        
        # متغيرات السلة
        self.cart = []
        self.cart_total = 0.0
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحديث العرض
        self.update_displays()
    
    def load_data(self):
        """تحميل البيانات من الملف"""
        default_data = {
            "sales": [],
            "expenses": [],
            "inventory": [],
            "rentals": []
        }
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                for key in default_data:
                    if key not in self.data:
                        self.data[key] = default_data[key]
            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في تحميل البيانات: {str(e)}")
                self.data = default_data
        else:
            self.data = default_data

        # إضافة منتج افتراضي إذا كان المخزون فارغاً
        if not self.data['inventory']:
            self.data['inventory'].append({
                'id': str(uuid.uuid4()),
                'name': 'كتاب افتراضي',
                'price': 10.0,
                'stock': 5,
                'description': 'منتج افتراضي للاختبار'
            })
            self.save_data()
    
    def save_data(self):
        """حفظ البيانات في الملف"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ البيانات: {str(e)}")

    # =================================================================
    # == الدالة الجديدة لحل مشكلة التواريخ ==
    # =================================================================
    def parse_datetime_flexible(self, date_string: str) -> Optional[datetime]:
        """
        تحلل سلسلة نصية للتاريخ قد تكون بأحد التنسيقات المعروفة.
        Handles parsing a date string that might be in one of several formats.
        """
        # قائمة التنسيقات المحتملة بالترتيب
        formats_to_try = [
            "%Y-%m-%d %H:%M:%S",        # التنسيق القياسي الحالي
            "%Y-%m-%dT%H:%M:%S.%f",     # تنسيق ISO مع أجزاء الثانية (سبب الخطأ)
            "%Y-%m-%d",                # تنسيق التاريخ فقط (للإعارات)
        ]
        for fmt in formats_to_try:
            try:
                return datetime.strptime(date_string, fmt)
            except (ValueError, TypeError):
                continue
        
        # إذا فشلت كل المحاولات، يتم تسجيل تحذير وتجاهل السجل
        print(f"تحذير: لم يتمكن من تحليل التاريخ '{date_string}'.")
        return None
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            main_frame,
            text="نظام إدارة المبيعات والمصروفات مع تأجير الكتب",
            font=('Arial', FONT_SIZES['xxlarge'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=(0, 20))
        
        content_frame = tk.Frame(main_frame, bg=COLORS['background'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = tk.Frame(content_frame, bg=COLORS['background'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.create_sales_section(left_frame)
        
        right_frame = tk.Frame(content_frame, bg=COLORS['background'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.create_info_section(right_frame)
        
        self.create_bottom_bar(main_frame)
    
    def create_sales_section(self, parent):
        """إنشاء قسم المبيعات"""
        sales_title = tk.Label(parent, text="🛒 نقطة البيع", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['accent'])
        sales_title.pack(anchor='w', pady=(0, 10))
        
        add_frame = tk.Frame(parent, bg=COLORS['light'], relief='raised', bd=1)
        add_frame.pack(fill=tk.X, pady=(0, 10), padx=5, ipady=10)
        
        tk.Label(add_frame, text="المنتج:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(add_frame, textvariable=self.product_var, width=20, font=('Arial', FONT_SIZES['medium']))
        self.product_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="الكمية:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.quantity_var = tk.StringVar(value="1")
        tk.Entry(add_frame, textvariable=self.quantity_var, width=10, font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=3, padx=5, pady=5)
        
        ModernButton(add_frame, text="إضافة للسلة", command=self.add_to_cart).grid(row=0, column=4, padx=10, pady=5)
        
        cart_label = tk.Label(parent, text="🛍️ السلة", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['accent'])
        cart_label.pack(anchor='w', pady=(10, 5))
        
        cart_frame = tk.Frame(parent)
        cart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        columns = ('المنتج', 'الكمية', 'السعر', 'الإجمالي')
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show='headings', height=10)
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=120, anchor='center')
        
        cart_scrollbar = ttk.Scrollbar(cart_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        total_frame = tk.Frame(parent, bg=COLORS['light'], relief='raised', bd=1)
        total_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10)
        
        self.total_label = tk.Label(total_frame, text="الإجمالي: 0.00 ريال", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['light'], fg=COLORS['accent'])
        self.total_label.pack(pady=5)
        
        customer_frame = tk.Frame(total_frame, bg=COLORS['light'])
        customer_frame.pack(pady=5)
        tk.Label(customer_frame, text="اسم العميل:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(side=tk.LEFT, padx=5)
        self.customer_var = tk.StringVar()
        tk.Entry(customer_frame, textvariable=self.customer_var, width=20, font=('Arial', FONT_SIZES['medium'])).pack(side=tk.LEFT, padx=5)
        
        payment_frame = tk.Frame(total_frame, bg=COLORS['light'])
        payment_frame.pack(pady=5)
        tk.Label(payment_frame, text="طريقة الدفع:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(side=tk.LEFT, padx=5)
        self.payment_var = tk.StringVar(value="نقدي")
        ttk.Combobox(payment_frame, textvariable=self.payment_var, values=["نقدي", "آجل"], width=15, font=('Arial', FONT_SIZES['medium'])).pack(side=tk.LEFT, padx=5)
        
        buttons_frame = tk.Frame(total_frame, bg=COLORS['light'])
        buttons_frame.pack(pady=10)
        ModernButton(buttons_frame, text="مسح السلة", command=self.clear_cart, style="secondary").pack(side=tk.LEFT, padx=5)
        ModernButton(buttons_frame, text="إتمام البيع", command=self.checkout, style="success").pack(side=tk.LEFT, padx=5)
    
    def create_info_section(self, parent):
        """إنشاء قسم المعلومات والإحصائيات"""
        stats_frame = tk.LabelFrame(parent, text="📊 إحصائيات اليوم", font=('Arial', FONT_SIZES['medium'], 'bold'), bg=COLORS['background'], fg=COLORS['accent'], padx=10, pady=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        self.daily_sales_label = tk.Label(stats_frame, text="المبيعات: 0.00 ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium']))
        self.daily_sales_label.pack(anchor='w', pady=2)
        self.daily_expenses_label = tk.Label(stats_frame, text="المصروفات: 0.00 ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium']))
        self.daily_expenses_label.pack(anchor='w', pady=2)
        self.daily_profit_label = tk.Label(stats_frame, text="الربح: 0.00 ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium']))
        self.daily_profit_label.pack(anchor='w', pady=2)
        
        low_stock_frame = tk.LabelFrame(parent, text="⚠️ تنبيهات المخزون", font=('Arial', FONT_SIZES['medium'], 'bold'), bg=COLORS['background'], fg=COLORS['warning'], padx=10, pady=10)
        low_stock_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.low_stock_listbox = tk.Listbox(low_stock_frame, height=8, font=('Arial', FONT_SIZES['small']))
        self.low_stock_listbox.pack(fill=tk.BOTH, expand=True)
        
        recent_sales_frame = tk.LabelFrame(parent, text="🕒 آخر المبيعات", font=('Arial', FONT_SIZES['medium'], 'bold'), bg=COLORS['background'], fg=COLORS['accent'], padx=10, pady=10)
        recent_sales_frame.pack(fill=tk.BOTH, expand=True)
        self.recent_sales_listbox = tk.Listbox(recent_sales_frame, height=8, font=('Arial', FONT_SIZES['small']))
        self.recent_sales_listbox.pack(fill=tk.BOTH, expand=True)
    
    def create_bottom_bar(self, parent):
        """إنشاء الشريط السفلي مع أزرار الإدارة"""
        bottom_frame = tk.Frame(parent, bg=COLORS['secondary'], relief='raised', bd=1)
        bottom_frame.pack(fill=tk.X, pady=(10, 0), ipady=10)
        
        ModernButton(bottom_frame, text="📦 إدارة المخزون", command=self.show_inventory_window).pack(side=tk.LEFT, padx=10)
        ModernButton(bottom_frame, text="🧾 سجل المبيعات", command=self.show_sales_history_window).pack(side=tk.LEFT, padx=10)
        ModernButton(bottom_frame, text="💰 إدارة المصروفات", command=self.show_expenses_window).pack(side=tk.LEFT, padx=10)
        ModernButton(bottom_frame, text="📈 التقارير", command=self.show_reports_window).pack(side=tk.LEFT, padx=10)
        ModernButton(bottom_frame, text="📚 تأجير الكتب", command=self.show_rental_window).pack(side=tk.LEFT, padx=10)
        
        backup_frame = tk.Frame(bottom_frame, bg=COLORS['secondary'])
        backup_frame.pack(side=tk.RIGHT, padx=10)
        ModernButton(backup_frame, text="💾 نسخ احتياطي", command=self.backup_data, style="secondary").pack(side=tk.LEFT, padx=5)
        ModernButton(backup_frame, text="🔄 استعادة نسخة", command=self.restore_data, style="secondary").pack(side=tk.LEFT, padx=5)

    def add_to_cart(self):
        """إضافة منتج للسلة"""
        product_name = self.product_var.get()
        quantity_str = self.quantity_var.get()
        
        if not product_name or not quantity_str:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج وإدخال الكمية")
            return
        
        try:
            quantity = int(quantity_str)
            if quantity <= 0: raise ValueError()
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال كمية صحيحة")
            return
        
        product = next((item for item in self.data['inventory'] if item['name'] == product_name), None)
        
        if not product:
            messagebox.showerror("خطأ", "المنتج غير موجود في المخزون")
            return
        
        existing_item_in_cart = next((item for item in self.cart if item['id'] == product['id']), None)
        current_quantity_in_cart = existing_item_in_cart['quantity'] if existing_item_in_cart else 0
        
        if product['stock'] < current_quantity_in_cart + quantity:
            messagebox.showerror("خطأ", f"الكمية المطلوبة تتجاوز المتوفر. المتوفر: {product['stock']}")
            return
        
        if existing_item_in_cart:
            existing_item_in_cart['quantity'] += quantity
            existing_item_in_cart['total'] = existing_item_in_cart['price'] * existing_item_in_cart['quantity']
        else:
            self.cart.append({
                'id': product['id'], 'name': product['name'], 'price': product['price'],
                'quantity': quantity, 'total': product['price'] * quantity
            })
        
        self.update_cart_display()
        self.product_var.set("")
        self.quantity_var.set("1")

    def update_cart_display(self):
        """تحديث عرض السلة"""
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        self.cart_total = sum(item['total'] for item in self.cart)
        
        for item in self.cart:
            self.cart_tree.insert('', 'end', values=(item['name'], item['quantity'], f"{item['price']:.2f}", f"{item['total']:.2f}"))
        
        self.total_label.config(text=f"الإجمالي: {self.cart_total:.2f} ريال")

    def clear_cart(self):
        """مسح السلة"""
        if self.cart and messagebox.askyesno("تأكيد", "هل تريد مسح جميع عناصر السلة؟"):
            self.cart.clear()
            self.update_cart_display()

    def checkout(self):
        """إتمام البيع"""
        if not self.cart:
            messagebox.showwarning("تحذير", "السلة فارغة")
            return
        
        customer_name = self.customer_var.get().strip() or "عميل"
        
        sale_record = {
            'id': str(uuid.uuid4()),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'customer': customer_name,
            'payment_method': self.payment_var.get(),
            'items': self.cart.copy(),
            'total': self.cart_total
        }
        
        self.data['sales'].append(sale_record)
        
        for cart_item in self.cart:
            for inv_item in self.data['inventory']:
                if inv_item['id'] == cart_item['id']:
                    inv_item['stock'] -= cart_item['quantity']
                    break
        
        self.save_data()
        self.show_print_options(sale_record)
        
        self.cart.clear()
        self.customer_var.set("")
        self.payment_var.set("نقدي")
        self.update_cart_display()
        self.update_displays()

    def show_print_options(self, sale_record):
        """عرض نافذة تأكيد البيع"""
        win = tk.Toplevel(self.root)
        win.title("إتمام البيع")
        win.geometry("400x250")
        win.configure(bg=COLORS['background'])
        win.grab_set()
        
        tk.Label(win, text="✅ تم إتمام البيع بنجاح!", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['success']).pack(pady=20)
        
        details_frame = tk.Frame(win, bg=COLORS['background'])
        details_frame.pack(pady=10)
        
        tk.Label(details_frame, text=f"رقم الفاتورة: {sale_record['id'][:8]}...", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack()
        tk.Label(details_frame, text=f"العميل: {sale_record['customer']}", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack()
        tk.Label(details_frame, text=f"الإجمالي: {sale_record['total']:.2f} ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'], 'bold')).pack()
        
        ModernButton(win, text="إغلاق", command=win.destroy, style="primary").pack(pady=20)

    def show_inventory_window(self):
        """عرض نافذة إدارة المخزون"""
        win = tk.Toplevel(self.root)
        win.title("إدارة المخزون")
        win.geometry("800x600")
        win.configure(bg=COLORS['background'])
        win.grab_set()

        tk.Label(win, text="📦 إدارة المخزون", font=('Arial', FONT_SIZES['xlarge'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(pady=10)

        frame = tk.Frame(win, bg=COLORS['background'])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ('الاسم', 'السعر', 'المخزون', 'الوصف')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def update_display():
            for item in tree.get_children(): tree.delete(item)
            for item in sorted(self.data['inventory'], key=lambda x: x['name']):
                tree.insert('', 'end', iid=item['id'], values=(item['name'], f"{item['price']:.2f}", item['stock'], item.get('description', '')))
        update_display()

        buttons_frame = tk.Frame(win, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)

        def add_prod(): self.add_or_edit_product_dialog(callback=update_display, parent=win)
        def edit_prod():
            if not tree.selection():
                messagebox.showwarning("تحذير", "يرجى اختيار منتج لتعديله", parent=win)
                return
            prod_id = tree.selection()[0]
            prod = next((p for p in self.data['inventory'] if p['id'] == prod_id), None)
            if prod: self.add_or_edit_product_dialog(product=prod, callback=update_display, parent=win)
        
        def delete_prod():
            if not tree.selection():
                messagebox.showwarning("تحذير", "يرجى اختيار منتج لحذفه", parent=win)
                return
            prod_id = tree.selection()[0]
            prod = next((p for p in self.data['inventory'] if p['id'] == prod_id), None)
            if prod and messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف المنتج '{prod['name']}'؟", parent=win):
                self.data['inventory'] = [p for p in self.data['inventory'] if p['id'] != prod_id]
                self.save_data()
                update_display()
                self.update_displays()

        ModernButton(buttons_frame, text="إضافة منتج", command=add_prod, style="success").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="تعديل المنتج", command=edit_prod, style="primary").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="حذف المنتج", command=delete_prod, style="danger").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="إغلاق", command=win.destroy, style="secondary").pack(side=tk.RIGHT, padx=10)

    def add_or_edit_product_dialog(self, product=None, callback=None, parent=None):
        """حوار لإضافة أو تعديل منتج"""
        is_edit = product is not None
        win = tk.Toplevel(parent or self.root)
        win.title("تعديل منتج" if is_edit else "إضافة منتج جديد")
        win.geometry("400x350")
        win.configure(bg=COLORS['background'])
        win.grab_set()

        tk.Label(win, text=win.title(), font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(pady=10)

        frame = tk.Frame(win, bg=COLORS['background'], padx=20, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="اسم المنتج:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_var = tk.StringVar(value=product['name'] if is_edit else "")
        tk.Entry(frame, textvariable=name_var, width=30, font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="السعر:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        price_var = tk.StringVar(value=str(product['price']) if is_edit else "")
        tk.Entry(frame, textvariable=price_var, width=30, font=('Arial', FONT_SIZES['medium'])).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="الكمية:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        stock_var = tk.StringVar(value=str(product['stock']) if is_edit else "")
        tk.Entry(frame, textvariable=stock_var, width=30, font=('Arial', FONT_SIZES['medium'])).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="الوصف:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        desc_var = tk.StringVar(value=product.get('description', '') if is_edit else "")
        tk.Entry(frame, textvariable=desc_var, width=30, font=('Arial', FONT_SIZES['medium'])).grid(row=3, column=1, padx=5, pady=5)

        def save():
            name = name_var.get().strip()
            price_str = price_var.get().strip()
            stock_str = stock_var.get().strip()
            description = desc_var.get().strip()

            if not name or not price_str or not stock_str:
                messagebox.showerror("خطأ", "يرجى ملء جميع الحقول المطلوبة", parent=win)
                return
            
            try:
                price = float(price_str)
                stock = int(stock_str)
                if price < 0 or stock < 0: raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة للسعر والكمية", parent=win)
                return
            
            if not is_edit and any(p['name'].lower() == name.lower() for p in self.data['inventory']):
                 messagebox.showerror("خطأ", "اسم المنتج موجود بالفعل.", parent=win)
                 return
            if is_edit and any(p['name'].lower() == name.lower() and p['id'] != product['id'] for p in self.data['inventory']):
                messagebox.showerror("خطأ", "اسم المنتج موجود بالفعل.", parent=win)
                return

            if is_edit:
                product.update({'name': name, 'price': price, 'stock': stock, 'description': description})
            else:
                self.data['inventory'].append({
                    'id': str(uuid.uuid4()), 'name': name, 'price': price, 'stock': stock, 'description': description
                })
            
            self.save_data()
            self.update_displays()
            if callback: callback()
            win.destroy()

        buttons_frame = tk.Frame(win, bg=COLORS['background'])
        buttons_frame.pack(pady=20)
        ModernButton(buttons_frame, text="حفظ", command=save, style="success").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="إلغاء", command=win.destroy, style="secondary").pack(side=tk.LEFT, padx=10)

    def show_sales_history_window(self):
        """عرض نافذة سجل المبيعات"""
        win = tk.Toplevel(self.root)
        win.title("سجل المبيعات")
        win.geometry("900x600")
        win.configure(bg=COLORS['background'])
        win.grab_set()

        tk.Label(win, text="🧾 سجل المبيعات", font=('Arial', FONT_SIZES['xlarge'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(pady=10)
        
        search_frame = tk.Frame(win, bg=COLORS['background'])
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(search_frame, text="بحث:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=40, font=('Arial', FONT_SIZES['medium']))
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tree_frame = tk.Frame(win, bg=COLORS['background'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ('رقم الفاتورة', 'التاريخ', 'العميل', 'الإجمالي', 'طريقة الدفع')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def update_display(filter_term=""):
            for item in tree.get_children(): tree.delete(item)
            
            # Use the flexible parser for sorting
            sorted_sales = sorted(self.data['sales'], key=lambda s: self.parse_datetime_flexible(s['date']) or datetime.min, reverse=True)

            sales_to_display = sorted_sales
            if filter_term:
                sales_to_display = [s for s in sorted_sales if filter_term.lower() in s.get('customer', '').lower() or filter_term in s.get('id', '')]
            
            for sale in sales_to_display:
                tree.insert('', 'end', iid=sale['id'], values=(sale['id'][:8], sale['date'], sale['customer'], f"{sale['total']:.2f}", sale['payment_method']))
        
        search_var.trace_add("write", lambda *args: update_display(search_var.get()))
        update_display()

        def view_invoice_details():
            if not tree.selection():
                messagebox.showwarning("تحذير", "يرجى اختيار فاتورة لعرضها", parent=win)
                return
            sale_id = tree.selection()[0]
            sale = next((s for s in self.data['sales'] if s['id'] == sale_id), None)
            if sale: self.show_invoice_details_window(sale, parent=win)

        buttons_frame = tk.Frame(win, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        ModernButton(buttons_frame, text="عرض الفاتورة", command=view_invoice_details, style="primary").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="إغلاق", command=win.destroy, style="secondary").pack(side=tk.RIGHT, padx=10)

    def show_invoice_details_window(self, sale_record, parent):
        """عرض تفاصيل فاتورة محددة"""
        win = tk.Toplevel(parent)
        win.title(f"تفاصيل الفاتورة - {sale_record['id'][:8]}")
        win.geometry("600x400")
        win.configure(bg=COLORS['background'])
        win.grab_set()

        tk.Label(win, text=f"فاتورة رقم: {sale_record['id'][:8]}", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(pady=10)
        
        info_frame = tk.Frame(win, bg=COLORS['light'], padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(info_frame, text=f"التاريخ: {sale_record['date']}", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(info_frame, text=f"العميل: {sale_record['customer']}", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(info_frame, text=f"طريقة الدفع: {sale_record['payment_method']}", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')

        items_frame = tk.LabelFrame(win, text="المنتجات", font=('Arial', FONT_SIZES['medium']), bg=COLORS['background'], padx=10, pady=10)
        items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ('المنتج', 'الكمية', 'السعر', 'الإجمالي')
        tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=5)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        tree.pack(fill=tk.BOTH, expand=True)

        for item in sale_record['items']:
            tree.insert('', 'end', values=(item['name'], item['quantity'], f"{item['price']:.2f}", f"{item['total']:.2f}"))
        
        total_label = tk.Label(win, text=f"الإجمالي الكلي: {sale_record['total']:.2f} ريال", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['success'])
        total_label.pack(pady=10)

        ModernButton(win, text="إغلاق", command=win.destroy, style="secondary").pack(pady=10)

    def show_expenses_window(self):
        """عرض نافذة إدارة المصروفات"""
        win = tk.Toplevel(self.root)
        win.title("إدارة المصروفات")
        win.geometry("800x600")
        win.configure(bg=COLORS['background'])
        win.grab_set()

        tk.Label(win, text="💰 إدارة المصروفات", font=('Arial', FONT_SIZES['xlarge'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(pady=10)

        add_frame = tk.Frame(win, bg=COLORS['light'], relief='raised', bd=1, padx=10, pady=10)
        add_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(add_frame, text="الوصف:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        desc_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=desc_var, width=30, font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="المبلغ:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        amount_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=amount_var, width=15, font=('Arial', FONT_SIZES['medium'])).grid(row=1, column=1, padx=5, pady=5)
        
        def add_expense():
            desc = desc_var.get().strip()
            amount_str = amount_var.get().strip()
            if not desc or not amount_str:
                messagebox.showerror("خطأ", "يرجى ملء جميع الحقول", parent=win)
                return
            try:
                amount = float(amount_str)
                if amount <= 0: raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال مبلغ صحيح", parent=win)
                return
            
            self.data['expenses'].append({
                'id': str(uuid.uuid4()), 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'description': desc, 'amount': amount
            })
            self.save_data()
            update_display()
            self.update_displays()
            desc_var.set("")
            amount_var.set("")

        ModernButton(add_frame, text="إضافة مصروف", command=add_expense, style="success").grid(row=0, column=2, rowspan=2, padx=10, pady=5)

        tree_frame = tk.Frame(win, bg=COLORS['background'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        columns = ('التاريخ', 'الوصف', 'المبلغ')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def update_display():
            for item in tree.get_children(): tree.delete(item)
            sorted_expenses = sorted(self.data['expenses'], key=lambda e: self.parse_datetime_flexible(e['date']) or datetime.min, reverse=True)
            for expense in sorted_expenses:
                tree.insert('', 'end', iid=expense['id'], values=(expense['date'], expense['description'], f"{expense['amount']:.2f}"))
        update_display()

        buttons_frame = tk.Frame(win, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)

        def delete_expense():
            if not tree.selection():
                messagebox.showwarning("تحذير", "يرجى اختيار مصروف لحذفه", parent=win)
                return
            exp_id = tree.selection()[0]
            exp = next((e for e in self.data['expenses'] if e['id'] == exp_id), None)
            if exp and messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف المصروف '{exp['description']}'؟", parent=win):
                self.data['expenses'] = [e for e in self.data['expenses'] if e['id'] != exp_id]
                self.save_data()
                update_display()
                self.update_displays()
        
        ModernButton(buttons_frame, text="حذف المصروف", command=delete_expense, style="danger").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="إغلاق", command=win.destroy, style="secondary").pack(side=tk.RIGHT, padx=10)

    def show_reports_window(self):
        """عرض نافذة التقارير"""
        win = tk.Toplevel(self.root)
        win.title("التقارير والإحصائيات")
        win.geometry("700x500")
        win.configure(bg=COLORS['background'])
        win.grab_set()

        tk.Label(win, text="📈 التقارير والإحصائيات", font=('Arial', FONT_SIZES['xlarge'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(pady=10)

        notebook = ttk.Notebook(win)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        summary_tab = tk.Frame(notebook, bg=COLORS['background'], padx=10, pady=10)
        sales_tab = tk.Frame(notebook, bg=COLORS['background'], padx=10, pady=10)
        notebook.add(summary_tab, text="الملخص المالي")
        notebook.add(sales_tab, text="تحليل المبيعات")

        # --- تبويب الملخص ---
        today = datetime.now().date()
        
        daily_sales = sum(s['total'] for s in self.data['sales'] if (dt := self.parse_datetime_flexible(s['date'])) and dt.date() == today)
        daily_expenses = sum(e['amount'] for e in self.data['expenses'] if (dt := self.parse_datetime_flexible(e['date'])) and dt.date() == today)
        
        total_sales = sum(s['total'] for s in self.data['sales'])
        total_expenses = sum(e['amount'] for e in self.data['expenses'])

        tk.Label(summary_tab, text="ملخص اليوم", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(anchor='w', pady=5)
        tk.Label(summary_tab, text=f"إجمالي المبيعات: {daily_sales:.2f} ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(summary_tab, text=f"إجمالي المصروفات: {daily_expenses:.2f} ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        profit_color = COLORS['success'] if daily_sales - daily_expenses >= 0 else COLORS['danger']
        tk.Label(summary_tab, text=f"صافي الربح: {(daily_sales - daily_expenses):.2f} ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'], 'bold'), fg=profit_color).pack(anchor='w', pady=(0, 15))

        tk.Label(summary_tab, text="الملخص الإجمالي", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(anchor='w', pady=5)
        tk.Label(summary_tab, text=f"إجمالي المبيعات: {total_sales:.2f} ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(summary_tab, text=f"إجمالي المصروفات: {total_expenses:.2f} ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        total_profit_color = COLORS['success'] if total_sales - total_expenses >= 0 else COLORS['danger']
        tk.Label(summary_tab, text=f"صافي الربح الإجمالي: {(total_sales - total_expenses):.2f} ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'], 'bold'), fg=total_profit_color).pack(anchor='w')

        # --- تبويب تحليل المبيعات ---
        tk.Label(sales_tab, text="المنتجات الأكثر مبيعاً", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(anchor='w', pady=5)
        
        product_sales = {}
        for sale in self.data['sales']:
            for item in sale['items']:
                product_sales[item['name']] = product_sales.get(item['name'], 0) + item['quantity']
        
        best_selling = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for name, qty in best_selling:
            tk.Label(sales_tab, text=f"- {name}: {qty} قطعة", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')

    def show_rental_window(self):
        """عرض نافذة إدارة تأجير الكتب"""
        win = tk.Toplevel(self.root)
        win.title("إدارة تأجير الكتب")
        win.geometry("900x600")
        win.configure(bg=COLORS['background'])
        win.grab_set()

        tk.Label(win, text="📚 إدارة تأجير الكتب", font=('Arial', FONT_SIZES['xlarge'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(pady=10)

        frame = tk.Frame(win, bg=COLORS['background'])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ('اسم الكتاب', 'اسم المستعير', 'تاريخ التأجير', 'تاريخ الإرجاع', 'الحالة')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def update_display():
            for item in tree.get_children(): tree.delete(item)
            
            sorted_rentals = sorted(self.data['rentals'], key=lambda r: self.parse_datetime_flexible(r['rental_date']) or datetime.min, reverse=True)

            for rental in sorted_rentals:
                status = rental['status']
                due_date_dt = self.parse_datetime_flexible(rental['due_date'])
                if status == 'مُعَار' and due_date_dt and due_date_dt.date() < datetime.now().date():
                    status = "متأخر"
                
                tree.insert('', 'end', iid=rental['id'], values=(rental['book_name'], rental['renter_name'], rental['rental_date'], rental['due_date'], status))
                
                if status == "متأخر":
                    tree.item(rental['id'], tags=('late',))
            
            tree.tag_configure('late', background=COLORS['warning'], foreground=COLORS['dark'])

        update_display()

        buttons_frame = tk.Frame(win, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)

        def add_rental(): self.add_or_edit_rental_dialog(callback=update_display, parent=win)
        def return_book():
            if not tree.selection():
                messagebox.showwarning("تحذير", "يرجى اختيار إعارة لتسجيل إرجاعها", parent=win)
                return
            rental_id = tree.selection()[0]
            rental = next((r for r in self.data['rentals'] if r['id'] == rental_id), None)
            
            if rental and rental['status'] != 'تم إرجاعه' and messagebox.askyesno("تأكيد", f"هل تريد تسجيل إرجاع الكتاب '{rental['book_name']}'؟", parent=win):
                rental['status'] = 'تم إرجاعه'
                book = next((b for b in self.data['inventory'] if b['id'] == rental['book_id']), None)
                if book: book['stock'] += 1
                self.save_data()
                update_display()
                self.update_displays()

        ModernButton(buttons_frame, text="إضافة إعارة", command=add_rental, style="success").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="تسجيل إرجاع", command=return_book, style="primary").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="إغلاق", command=win.destroy, style="secondary").pack(side=tk.RIGHT, padx=10)

    def add_or_edit_rental_dialog(self, rental=None, callback=None, parent=None):
        """حوار لإضافة أو تعديل إعارة"""
        win = tk.Toplevel(parent or self.root)
        win.title("إضافة إعارة جديدة")
        win.geometry("400x300")
        win.configure(bg=COLORS['background'])
        win.grab_set()

        tk.Label(win, text=win.title(), font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['background'], fg=COLORS['accent']).pack(pady=10)

        frame = tk.Frame(win, bg=COLORS['background'], padx=20, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="الكتاب:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(frame, textvariable=book_var, width=30, font=('Arial', FONT_SIZES['medium']))
        available_books = [p['name'] for p in self.data['inventory'] if p['stock'] > 0]
        book_combo['values'] = available_books
        book_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="اسم المستعير:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        renter_var = tk.StringVar()
        tk.Entry(frame, textvariable=renter_var, width=30, font=('Arial', FONT_SIZES['medium'])).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="مدة الإعارة (أيام):", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        duration_var = tk.StringVar(value="14")
        tk.Entry(frame, textvariable=duration_var, width=30, font=('Arial', FONT_SIZES['medium'])).grid(row=2, column=1, padx=5, pady=5)

        def save():
            book_name = book_var.get()
            renter_name = renter_var.get().strip()
            duration_str = duration_var.get().strip()

            if not book_name or not renter_name or not duration_str:
                messagebox.showerror("خطأ", "يرجى ملء جميع الحقول", parent=win)
                return
            
            try:
                duration = int(duration_str)
                if duration <= 0: raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال مدة صحيحة", parent=win)
                return
            
            book = next((b for b in self.data['inventory'] if b['name'] == book_name), None)
            if not book:
                messagebox.showerror("خطأ", "الكتاب غير موجود", parent=win)
                return
            
            book['stock'] -= 1
            self.data['rentals'].append({
                'id': str(uuid.uuid4()), 'book_id': book['id'], 'book_name': book_name,
                'renter_name': renter_name, 'rental_date': datetime.now().strftime("%Y-%m-%d"),
                'due_date': (datetime.now() + timedelta(days=duration)).strftime("%Y-%m-%d"),
                'status': 'مُعَار'
            })
            
            self.save_data()
            self.update_displays()
            if callback: callback()
            win.destroy()

        buttons_frame = tk.Frame(win, bg=COLORS['background'])
        buttons_frame.pack(pady=20)
        ModernButton(buttons_frame, text="حفظ", command=save, style="success").pack(side=tk.LEFT, padx=10)
        ModernButton(buttons_frame, text="إلغاء", command=win.destroy, style="secondary").pack(side=tk.LEFT, padx=10)

    def backup_data(self):
        """إنشاء نسخة احتياطية من البيانات"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="حفظ نسخة احتياطية",
            initialfile=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("نجح", f"تم إنشاء النسخة الاحتياطية بنجاح في:\n{file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في إنشاء النسخة الاحتياطية: {str(e)}")
    
    def restore_data(self):
        """استعادة البيانات من نسخة احتياطية"""
        if not messagebox.askyesno(
            "تحذير خطير",
            "هل أنت متأكد من استعادة البيانات؟\nسيتم حذف جميع البيانات الحالية واستبدالها بالنسخة الاحتياطية."
        ):
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="اختر ملف النسخة الاحتياطية"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.save_data()
            self.update_displays()
            messagebox.showinfo("نجح", "تم استعادة البيانات بنجاح من النسخة الاحتياطية.")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في استعادة البيانات: {str(e)}")

    def update_displays(self):
        """تحديث جميع عناصر العرض في الواجهة"""
        # تحديث قائمة المنتجات في نقطة البيع
        product_names = [item['name'] for item in self.data['inventory'] if item['stock'] > 0]
        self.product_combo['values'] = product_names

        # تحديث إحصائيات اليوم
        today = datetime.now().date()
        daily_sales = sum(s['total'] for s in self.data['sales'] if (dt := self.parse_datetime_flexible(s['date'])) and dt.date() == today)
        daily_expenses = sum(e['amount'] for e in self.data['expenses'] if (dt := self.parse_datetime_flexible(e['date'])) and dt.date() == today)
        profit = daily_sales - daily_expenses
        self.daily_sales_label.config(text=f"المبيعات: {daily_sales:.2f} ريال")
        self.daily_expenses_label.config(text=f"المصروفات: {daily_expenses:.2f} ريال")
        self.daily_profit_label.config(text=f"الربح: {profit:.2f} ريال")

        # تحديث تنبيهات المخزون
        self.low_stock_listbox.delete(0, tk.END)
        for item in self.data['inventory']:
            if item['stock'] <= 3:
                self.low_stock_listbox.insert(tk.END, f"{item['name']} (المتبقي: {item['stock']})")

        # تحديث آخر المبيعات
        self.recent_sales_listbox.delete(0, tk.END)
        recent_sales = sorted(self.data['sales'], key=lambda s: self.parse_datetime_flexible(s['date']) or datetime.min, reverse=True)[:8]
        for sale in recent_sales:
            self.recent_sales_listbox.insert(tk.END, f"{sale['date']} - {sale['customer']} - {sale['total']:.2f} ريال")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesManagementSystem(root)
    root.mainloop()
