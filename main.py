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
