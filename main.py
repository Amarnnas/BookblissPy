#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المبيعات والمصروفات
Sales & Expense Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import uuid

class SalesManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("نظام إدارة المبيعات والمصروفات - Sales Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # تحديد مسار ملف البيانات
        self.data_file = "sales_data.json"
        
        # تهيئة البيانات
        self.data = self.load_data()
        self.cart = []
        
        # إعداد الواجهة
        self.setup_ui()
        
    def load_data(self) -> Dict[str, Any]:
        """تحميل البيانات من الملف"""
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
        """حفظ البيانات في الملف"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ البيانات: {str(e)}")
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # إعداد الخط
        self.font_large = ("Arial", 14, "bold")
        self.font_medium = ("Arial", 12)
        self.font_small = ("Arial", 10)
        
        # الشريط العلوي
        self.create_header()
        
        # الشريط الجانبي
        self.create_sidebar()
        
        # المنطقة الرئيسية
        self.create_main_area()
        
        # شريط الحالة
        self.create_status_bar()
        
        # عرض لوحة المبيعات افتراضياً
        self.show_sales_panel()
    
    def create_header(self):
        """إنشاء الشريط العلوي"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="نظام إدارة المبيعات والمصروفات",
            font=("Arial", 18, "bold"),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=20)
    
    def create_sidebar(self):
        """إنشاء الشريط الجانبي"""
        self.sidebar_frame = tk.Frame(self.root, bg='#34495e', width=250)
        self.sidebar_frame.pack(side='left', fill='y', padx=0, pady=0)
        self.sidebar_frame.pack_propagate(False)
        
        # أزرار القائمة
        buttons = [
            ("🛒 المبيعات", self.show_sales_panel),
            ("📦 المخزون", self.show_inventory_panel),
            ("💰 المصروفات", self.show_expenses_panel),
            ("📊 التقارير", self.show_reports_panel),
            ("⚙️ الإعدادات", self.show_settings_panel),
            ("💾 النسخ الاحتياطي", self.show_backup_panel)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                self.sidebar_frame,
                text=text,
                font=self.font_medium,
                bg='#3498db',
                fg='white',
                relief='flat',
                padx=20,
                pady=15,
                command=command,
                cursor='hand2'
            )
            btn.pack(fill='x', padx=10, pady=5)
            
            # تأثير hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#2980b9'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#3498db'))
    
    def create_main_area(self):
        """إنشاء المنطقة الرئيسية"""
        self.main_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.main_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
    
    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_bar = tk.Label(
            self.root,
            text="جاهز",
            relief='sunken',
            anchor='w',
            font=self.font_small,
            bg='#bdc3c7'
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def clear_main_frame(self):
        """مسح المحتوى الرئيسي"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_sales_panel(self):
        """عرض لوحة المبيعات"""
        self.clear_main_frame()
        self.status_bar.config(text="لوحة المبيعات")
        
        # إطار العنوان
        title_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🛒 إدارة المبيعات",
            font=self.font_large,
            bg='#ecf0f1'
        ).pack(side='left')
        
        # إطار السلة
        cart_frame = tk.LabelFrame(
            self.main_frame,
            text="سلة التسوق",
            font=self.font_medium,
            bg='#ecf0f1',
            padx=10,
            pady=10
        )
        cart_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # جدول السلة
        columns = ('المنتج', 'الكمية', 'السعر', 'الإجمالي')
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=150, anchor='center')
        
        # شريط التمرير
        cart_scrollbar = ttk.Scrollbar(cart_frame, orient='vertical', command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_tree.pack(side='left', fill='both', expand=True)
        cart_scrollbar.pack(side='right', fill='y')
        
        # إطار الأزرار والإجمالي
        bottom_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        bottom_frame.pack(fill='x', pady=10)
        
        # أزرار العمليات
        buttons_frame = tk.Frame(bottom_frame, bg='#ecf0f1')
        buttons_frame.pack(side='left')
        
        tk.Button(
            buttons_frame,
            text="إضافة منتج",
            font=self.font_medium,
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            command=self.add_to_cart
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="حذف من السلة",
            font=self.font_medium,
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.remove_from_cart
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="إتمام البيع",
            font=self.font_medium,
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.complete_sale
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="مسح السلة",
            font=self.font_medium,
            bg='#95a5a6',
            fg='white',
            padx=20,
            pady=10,
            command=self.clear_cart
        ).pack(side='left', padx=5)
        
        # إطار الإجمالي
        total_frame = tk.Frame(bottom_frame, bg='#ecf0f1')
        total_frame.pack(side='right')
        
        self.total_label = tk.Label(
            total_frame,
            text="الإجمالي: 0.00 جنيه",
            font=self.font_large,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.total_label.pack()
        
        self.update_cart_display()
    
    def show_inventory_panel(self):
        """عرض لوحة المخزون"""
        self.clear_main_frame()
        self.status_bar.config(text="لوحة المخزون")
        
        # إطار العنوان
        title_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="📦 إدارة المخزون",
            font=self.font_large,
            bg='#ecf0f1'
        ).pack(side='left')
        
        tk.Button(
            title_frame,
            text="إضافة منتج جديد",
            font=self.font_medium,
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            command=self.add_product
        ).pack(side='right')
        
        # جدول المنتجات
        columns = ('الرقم', 'اسم المنتج', 'السعر', 'الكمية المتاحة', 'الحالة')
        self.inventory_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=150, anchor='center')
        
        # شريط التمرير
        inventory_scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=inventory_scrollbar.set)
        
        self.inventory_tree.pack(side='left', fill='both', expand=True)
        inventory_scrollbar.pack(side='right', fill='y')
        
        # أزرار العمليات
        buttons_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        buttons_frame.pack(fill='x', pady=10)
        
        tk.Button(
            buttons_frame,
            text="تعديل منتج",
            font=self.font_medium,
            bg='#f39c12',
            fg='white',
            padx=20,
            pady=10,
            command=self.edit_product
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="حذف منتج",
            font=self.font_medium,
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.delete_product
        ).pack(side='left', padx=5)
        
        self.update_inventory_display()
    
    def show_expenses_panel(self):
        """عرض لوحة المصروفات"""
        self.clear_main_frame()
        self.status_bar.config(text="لوحة المصروفات")
        
        # إطار العنوان
        title_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="💰 إدارة المصروفات",
            font=self.font_large,
            bg='#ecf0f1'
        ).pack(side='left')
        
        tk.Button(
            title_frame,
            text="إضافة مصروف جديد",
            font=self.font_medium,
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.add_expense
        ).pack(side='right')
        
        # جدول المصروفات
        columns = ('التاريخ', 'الوصف', 'المبلغ', 'النوع')
        self.expenses_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        
        for col in columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, width=200, anchor='center')
        
        # شريط التمرير
        expenses_scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscrollcommand=expenses_scrollbar.set)
        
        self.expenses_tree.pack(side='left', fill='both', expand=True)
        expenses_scrollbar.pack(side='right', fill='y')
        
        # أزرار العمليات
        buttons_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        buttons_frame.pack(fill='x', pady=10)
        
        tk.Button(
            buttons_frame,
            text="حذف مصروف",
            font=self.font_medium,
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.delete_expense
        ).pack(side='left', padx=5)
        
        # إجمالي المصروفات
        total_expenses = sum(expense['amount'] for expense in self.data['expenses'])
        tk.Label(
            buttons_frame,
            text=f"إجمالي المصروفات: {total_expenses:.2f} جنيه",
            font=self.font_large,
            bg='#ecf0f1',
            fg='#e74c3c'
        ).pack(side='right')
        
        self.update_expenses_display()
    
    def show_reports_panel(self):
        """عرض لوحة التقارير"""
        self.clear_main_frame()
        self.status_bar.config(text="لوحة التقارير")
        
        tk.Label(
            self.main_frame,
            text="📊 التقارير والإحصائيات",
            font=self.font_large,
            bg='#ecf0f1'
        ).pack(pady=20)
        
        # إحصائيات سريعة
        stats_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        stats_frame.pack(fill='x', pady=20)
        
        # حساب الإحصائيات
        total_sales = sum(sale['total'] for sale in self.data['sales'])
        total_expenses = sum(expense['amount'] for expense in self.data['expenses'])
        profit = total_sales - total_expenses
        
        # بطاقات الإحصائيات
        self.create_stat_card(stats_frame, "إجمالي المبيعات", f"{total_sales:.2f} جنيه", "#27ae60")
        self.create_stat_card(stats_frame, "إجمالي المصروفات", f"{total_expenses:.2f} جنيه", "#e74c3c")
        self.create_stat_card(stats_frame, "صافي الربح", f"{profit:.2f} جنيه", "#3498db")
        self.create_stat_card(stats_frame, "عدد المنتجات", str(len(self.data['inventory'])), "#9b59b6")
    
    def create_stat_card(self, parent, title, value, color):
        """إنشاء بطاقة إحصائية"""
        card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            card_frame,
            text=title,
            font=self.font_medium,
            bg=color,
            fg='white'
        ).pack(pady=(10, 5))
        
        tk.Label(
            card_frame,
            text=value,
            font=self.font_large,
            bg=color,
            fg='white'
        ).pack(pady=(0, 10))
    
    def show_settings_panel(self):
        """عرض لوحة الإعدادات"""
        self.clear_main_frame()
        self.status_bar.config(text="لوحة الإعدادات")
        
        tk.Label(
            self.main_frame,
            text="⚙️ الإعدادات",
            font=self.font_large,
            bg='#ecf0f1'
        ).pack(pady=20)
        
        messagebox.showinfo("الإعدادات", "لوحة الإعدادات قيد التطوير")
    
    def show_backup_panel(self):
        """عرض لوحة النسخ الاحتياطي"""
        self.clear_main_frame()
        self.status_bar.config(text="لوحة النسخ الاحتياطي")
        
        tk.Label(
            self.main_frame,
            text="💾 النسخ الاحتياطي",
            font=self.font_large,
            bg='#ecf0f1'
        ).pack(pady=20)
        
        # أزرار النسخ الاحتياطي
        tk.Button(
            self.main_frame,
            text="إنشاء نسخة احتياطية",
            font=self.font_medium,
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            command=self.create_backup
        ).pack(pady=10)
        
        tk.Button(
            self.main_frame,
            text="استعادة من نسخة احتياطية",
            font=self.font_medium,
            bg='#3498db',
            fg='white',
            padx=30,
            pady=15,
            command=self.restore_backup
        ).pack(pady=10)
    
    def add_to_cart(self):
        """إضافة منتج إلى السلة"""
        if not self.data['inventory']:
            messagebox.showwarning("تحذير", "لا توجد منتجات في المخزون")
            return
        
        # نافذة اختيار المنتج
        product_window = tk.Toplevel(self.root)
        product_window.title("اختيار منتج")
        product_window.geometry("400x300")
        product_window.configure(bg='#ecf0f1')
        
        tk.Label(
            product_window,
            text="اختر المنتج:",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack(pady=10)
        
        # قائمة المنتجات
        products_listbox = tk.Listbox(product_window, font=self.font_medium)
        for product in self.data['inventory']:
            products_listbox.insert(tk.END, f"{product['name']} - {product['price']} جنيه")
        products_listbox.pack(fill='both', expand=True, padx=20, pady=10)
        
        # إدخال الكمية
        tk.Label(
            product_window,
            text="الكمية:",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack()
        
        quantity_entry = tk.Entry(product_window, font=self.font_medium, justify='center')
        quantity_entry.pack(pady=5)
        quantity_entry.insert(0, "1")
        
        def add_selected():
            selection = products_listbox.curselection()
            if not selection:
                messagebox.showwarning("تحذير", "يرجى اختيار منتج")
                return
            
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال كمية صحيحة")
                return
            
            product_index = selection[0]
            product = self.data['inventory'][product_index]
            
            if quantity > product['stock']:
                messagebox.showerror("خطأ", f"الكمية المطلوبة غير متوفرة. المتاح: {product['stock']}")
                return
            
            # إضافة إلى السلة
            cart_item = {
                'product_id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'total': product['price'] * quantity
            }
            
            # البحث عن المنتج في السلة
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
            product_window.destroy()
            messagebox.showinfo("نجح", "تم إضافة المنتج إلى السلة")
        
        tk.Button(
            product_window,
            text="إضافة",
            font=self.font_medium,
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=10,
            command=add_selected
        ).pack(pady=10)
    
    def remove_from_cart(self):
        """حذف منتج من السلة"""
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج من السلة")
            return
        
        item_index = self.cart_tree.index(selection[0])
        del self.cart[item_index]
        self.update_cart_display()
        messagebox.showinfo("نجح", "تم حذف المنتج من السلة")
    
    def complete_sale(self):
        """إتمام البيع"""
        if not self.cart:
            messagebox.showwarning("تحذير", "السلة فارغة")
            return
        
        # نافذة إتمام البيع
        sale_window = tk.Toplevel(self.root)
        sale_window.title("إتمام البيع")
        sale_window.geometry("400x300")
        sale_window.configure(bg='#ecf0f1')
        
        total = sum(item['total'] for item in self.cart)
        
        tk.Label(
            sale_window,
            text=f"إجمالي المبلغ: {total:.2f} جنيه",
            font=self.font_large,
            bg='#ecf0f1'
        ).pack(pady=20)
        
        # طريقة الدفع
        tk.Label(
            sale_window,
            text="طريقة الدفع:",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack()
        
        payment_var = tk.StringVar(value="نقدي")
        payment_frame = tk.Frame(sale_window, bg='#ecf0f1')
        payment_frame.pack(pady=10)
        
        tk.Radiobutton(
            payment_frame,
            text="نقدي",
            variable=payment_var,
            value="نقدي",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack(side='left', padx=10)
        
        tk.Radiobutton(
            payment_frame,
            text="آجل",
            variable=payment_var,
            value="آجل",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack(side='left', padx=10)
        
        # اسم العميل
        tk.Label(
            sale_window,
            text="اسم العميل (اختياري):",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack(pady=(20, 5))
        
        customer_entry = tk.Entry(sale_window, font=self.font_medium, width=30)
        customer_entry.pack()
        
        def confirm_sale():
            # إنشاء فاتورة
            sale = {
                'id': str(uuid.uuid4()),
                'date': datetime.now().isoformat(),
                'items': self.cart.copy(),
                'total': total,
                'payment_method': payment_var.get(),
                'customer': customer_entry.get() or "عميل عادي"
            }
            
            # إضافة البيع إلى البيانات
            self.data['sales'].append(sale)
            
            # تحديث المخزون
            for cart_item in self.cart:
                for product in self.data['inventory']:
                    if product['id'] == cart_item['product_id']:
                        product['stock'] -= cart_item['quantity']
                        break
            
            # مسح السلة
            self.cart.clear()
            
            # حفظ البيانات
            self.save_data()
            
            # تحديث العرض
            self.update_cart_display()
            
            sale_window.destroy()
            messagebox.showinfo("نجح", f"تم إتمام البيع بنجاح\nرقم الفاتورة: {sale['id'][:8]}")
        
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
    
    def clear_cart(self):
        """مسح السلة"""
        if messagebox.askyesno("تأكيد", "هل تريد مسح جميع المنتجات من السلة؟"):
            self.cart.clear()
            self.update_cart_display()
    
    def update_cart_display(self):
        """تحديث عرض السلة"""
        # مسح العرض الحالي
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # إضافة المنتجات
        total = 0
        for item in self.cart:
            self.cart_tree.insert('', 'end', values=(
                item['name'],
                item['quantity'],
                f"{item['price']:.2f}",
                f"{item['total']:.2f}"
            ))
            total += item['total']
        
        # تحديث الإجمالي
        if hasattr(self, 'total_label'):
            self.total_label.config(text=f"الإجمالي: {total:.2f} جنيه")
    
    def add_product(self):
        """إضافة منتج جديد"""
        product_window = tk.Toplevel(self.root)
        product_window.title("إضافة منتج جديد")
        product_window.geometry("400x350")
        product_window.configure(bg='#ecf0f1')
        
        # حقول الإدخال
        fields = [
            ("اسم المنتج:", "name"),
            ("السعر:", "price"),
            ("الكمية:", "stock"),
            ("الوصف:", "description")
        ]
        
        entries = {}
        
        for label_text, field_name in fields:
            tk.Label(
                product_window,
                text=label_text,
                font=self.font_medium,
                bg='#ecf0f1'
            ).pack(pady=(10, 5))
            
            entry = tk.Entry(product_window, font=self.font_medium, width=30)
            entry.pack()
            entries[field_name] = entry
        
        def save_product():
            try:
                name = entries['name'].get().strip()
                price = float(entries['price'].get())
                stock = int(entries['stock'].get())
                description = entries['description'].get().strip()
                
                if not name:
                    raise ValueError("اسم المنتج مطلوب")
                
                if price <= 0 or stock < 0:
                    raise ValueError("السعر والكمية يجب أن تكون أرقام موجبة")
                
                # إنشاء المنتج
                product = {
                    'id': len(self.data['inventory']) + 1,
                    'name': name,
                    'price': price,
                    'stock': stock,
                    'description': description,
                    'created_date': datetime.now().isoformat()
                }
                
                self.data['inventory'].append(product)
                self.save_data()
                self.update_inventory_display()
                
                product_window.destroy()
                messagebox.showinfo("نجح", "تم إضافة المنتج بنجاح")
                
            except ValueError as e:
                messagebox.showerror("خطأ", str(e))
        
        tk.Button(
            product_window,
            text="حفظ المنتج",
            font=self.font_medium,
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            command=save_product
        ).pack(pady=20)
    
    def edit_product(self):
        """تعديل منتج"""
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للتعديل")
            return
        
        item_index = self.inventory_tree.index(selection[0])
        product = self.data['inventory'][item_index]
        
        # نافذة التعديل
        edit_window = tk.Toplevel(self.root)
        edit_window.title("تعديل منتج")
        edit_window.geometry("400x350")
        edit_window.configure(bg='#ecf0f1')
        
        # حقول الإدخال مع القيم الحالية
        fields = [
            ("اسم المنتج:", "name", product['name']),
            ("السعر:", "price", str(product['price'])),
            ("الكمية:", "stock", str(product['stock'])),
            ("الوصف:", "description", product.get('description', ''))
        ]
        
        entries = {}
        
        for label_text, field_name, current_value in fields:
            tk.Label(
                edit_window,
                text=label_text,
                font=self.font_medium,
                bg='#ecf0f1'
            ).pack(pady=(10, 5))
            
            entry = tk.Entry(edit_window, font=self.font_medium, width=30)
            entry.pack()
            entry.insert(0, current_value)
            entries[field_name] = entry
        
        def save_changes():
            try:
                name = entries['name'].get().strip()
                price = float(entries['price'].get())
                stock = int(entries['stock'].get())
                description = entries['description'].get().strip()
                
                if not name:
                    raise ValueError("اسم المنتج مطلوب")
                
                if price <= 0 or stock < 0:
                    raise ValueError("السعر والكمية يجب أن تكون أرقام موجبة")
                
                # تحديث المنتج
                product['name'] = name
                product['price'] = price
                product['stock'] = stock
                product['description'] = description
                
                self.save_data()
                self.update_inventory_display()
                
                edit_window.destroy()
                messagebox.showinfo("نجح", "تم تحديث المنتج بنجاح")
                
            except ValueError as e:
                messagebox.showerror("خطأ", str(e))
        
        tk.Button(
            edit_window,
            text="حفظ التغييرات",
            font=self.font_medium,
            bg='#f39c12',
            fg='white',
            padx=30,
            pady=15,
            command=save_changes
        ).pack(pady=20)
    
    def delete_product(self):
        """حذف منتج"""
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للحذف")
            return
        
        item_index = self.inventory_tree.index(selection[0])
        product = self.data['inventory'][item_index]
        
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف المنتج '{product['name']}'؟"):
            del self.data['inventory'][item_index]
            self.save_data()
            self.update_inventory_display()
            messagebox.showinfo("نجح", "تم حذف المنتج بنجاح")
    
    def update_inventory_display(self):
        """تحديث عرض المخزون"""
        if not hasattr(self, 'inventory_tree'):
            return
        
        # مسح العرض الحالي
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # إضافة المنتجات
        for product in self.data['inventory']:
            status = "متوفر" if product['stock'] > 5 else "قليل" if product['stock'] > 0 else "نفد"
            self.inventory_tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                f"{product['price']:.2f}",
                product['stock'],
                status
            ))
    
    def add_expense(self):
        """إضافة مصروف جديد"""
        expense_window = tk.Toplevel(self.root)
        expense_window.title("إضافة مصروف جديد")
        expense_window.geometry("400x300")
        expense_window.configure(bg='#ecf0f1')
        
        # حقول الإدخال
        tk.Label(
            expense_window,
            text="وصف المصروف:",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack(pady=(20, 5))
        
        description_entry = tk.Entry(expense_window, font=self.font_medium, width=40)
        description_entry.pack()
        
        tk.Label(
            expense_window,
            text="المبلغ:",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack(pady=(20, 5))
        
        amount_entry = tk.Entry(expense_window, font=self.font_medium, width=20)
        amount_entry.pack()
        
        tk.Label(
            expense_window,
            text="نوع المصروف:",
            font=self.font_medium,
            bg='#ecf0f1'
        ).pack(pady=(20, 5))
        
        type_var = tk.StringVar(value="عام")
        type_frame = tk.Frame(expense_window, bg='#ecf0f1')
        type_frame.pack()
        
        types = ["عام", "مواد خام", "رواتب", "إيجار", "كهرباء", "صيانة", "أخرى"]
        type_combo = ttk.Combobox(type_frame, textvariable=type_var, values=types, font=self.font_medium)
        type_combo.pack()
        
        def save_expense():
            try:
                description = description_entry.get().strip()
                amount = float(amount_entry.get())
                expense_type = type_var.get()
                
                if not description:
                    raise ValueError("وصف المصروف مطلوب")
                
                if amount <= 0:
                    raise ValueError("المبلغ يجب أن يكون رقم موجب")
                
                # إنشاء المصروف
                expense = {
                    'id': str(uuid.uuid4()),
                    'date': datetime.now().isoformat(),
                    'description': description,
                    'amount': amount,
                    'type': expense_type
                }
                
                self.data['expenses'].append(expense)
                self.save_data()
                self.update_expenses_display()
                
                expense_window.destroy()
                messagebox.showinfo("نجح", "تم إضافة المصروف بنجاح")
                
            except ValueError as e:
                messagebox.showerror("خطأ", str(e))
        
        tk.Button(
            expense_window,
            text="حفظ المصروف",
            font=self.font_medium,
            bg='#e74c3c',
            fg='white',
            padx=30,
            pady=15,
            command=save_expense
        ).pack(pady=30)
    
    def delete_expense(self):
        """حذف مصروف"""
        selection = self.expenses_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار مصروف للحذف")
            return
        
        item_index = self.expenses_tree.index(selection[0])
        expense = self.data['expenses'][item_index]
        
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف المصروف '{expense['description']}'؟"):
            del self.data['expenses'][item_index]
            self.save_data()
            self.update_expenses_display()
            messagebox.showinfo("نجح", "تم حذف المصروف بنجاح")
    
    def update_expenses_display(self):
        """تحديث عرض المصروفات"""
        if not hasattr(self, 'expenses_tree'):
            return
        
        # مسح العرض الحالي
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        # إضافة المصروفات
        for expense in self.data['expenses']:
            date_str = datetime.fromisoformat(expense['date']).strftime('%Y-%m-%d %H:%M')
            self.expenses_tree.insert('', 'end', values=(
                date_str,
                expense['description'],
                f"{expense['amount']:.2f}",
                expense['type']
            ))
    
    def create_backup(self):
        """إنشاء نسخة احتياطية"""
        try:
            backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("نجح", f"تم إنشاء النسخة الاحتياطية: {backup_filename}")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في إنشاء النسخة الاحتياطية: {str(e)}")
    
    def restore_backup(self):
        """استعادة من نسخة احتياطية"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="اختر ملف النسخة الاحتياطية",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                self.save_data()
                messagebox.showinfo("نجح", "تم استعادة البيانات بنجاح")
                # إعادة تحميل العرض الحالي
                self.show_sales_panel()
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في استعادة البيانات: {str(e)}")
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SalesManagementSystem()
    app.run()