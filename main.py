#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المبيعات والمصروفات مع تأجير الكتب
Sales Management System with Book Rental Feature
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import uuid
from typing import Dict, List, Any

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
            "rentals": []  # إضافة قسم التأجير
        }
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                # التأكد من وجود جميع الأقسام المطلوبة
                for key in default_data:
                    if key not in self.data:
                        self.data[key] = default_data[key]
            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في تحميل البيانات: {str(e)}")
                self.data = default_data
        else:
            self.data = default_data
    
    def save_data(self):
        """حفظ البيانات في الملف"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ البيانات: {str(e)}")
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # العنوان
        title_label = tk.Label(
            main_frame,
            text="نظام إدارة المبيعات والمصروفات مع تأجير الكتب",
            font=('Arial', FONT_SIZES['xxlarge'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=(0, 20))
        
        # إطار المحتوى الرئيسي
        content_frame = tk.Frame(main_frame, bg=COLORS['background'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # الجانب الأيسر - السلة والمبيعات
        left_frame = tk.Frame(content_frame, bg=COLORS['background'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_sales_section(left_frame)
        
        # الجانب الأيمن - المعلومات والإحصائيات
        right_frame = tk.Frame(content_frame, bg=COLORS['background'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        self.create_info_section(right_frame)
        
        # الشريط السفلي
        self.create_bottom_bar(main_frame)
    
    def create_sales_section(self, parent):
        """إنشاء قسم المبيعات"""
        # عنوان القسم
        sales_title = tk.Label(
            parent,
            text="🛒 نقطة البيع",
            font=('Arial', FONT_SIZES['large'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        sales_title.pack(anchor='w', pady=(0, 10))
        
        # إطار إضافة المنتجات
        add_frame = tk.Frame(parent, bg=COLORS['light'], relief='raised', bd=1)
        add_frame.pack(fill=tk.X, pady=(0, 10), padx=5, ipady=10)
        
        # اختيار المنتج
        tk.Label(add_frame, text="المنتج:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(add_frame, textvariable=self.product_var, width=20, font=('Arial', FONT_SIZES['medium']))
        self.product_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # الكمية
        tk.Label(add_frame, text="الكمية:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = tk.Entry(add_frame, textvariable=self.quantity_var, width=10, font=('Arial', FONT_SIZES['medium']))
        quantity_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # زر الإضافة
        add_btn = ModernButton(add_frame, text="إضافة للسلة", command=self.add_to_cart)
        add_btn.grid(row=0, column=4, padx=10, pady=5)
        
        # السلة
        cart_label = tk.Label(
            parent,
            text="🛍️ السلة",
            font=('Arial', FONT_SIZES['large'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        cart_label.pack(anchor='w', pady=(10, 5))
        
        # جدول السلة
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
        
        # إطار الإجمالي والدفع
        total_frame = tk.Frame(parent, bg=COLORS['light'], relief='raised', bd=1)
        total_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10)
        
        # الإجمالي
        self.total_label = tk.Label(
            total_frame,
            text="الإجمالي: 0.00 ريال",
            font=('Arial', FONT_SIZES['large'], 'bold'),
            bg=COLORS['light'],
            fg=COLORS['accent']
        )
        self.total_label.pack(pady=5)
        
        # اسم العميل
        customer_frame = tk.Frame(total_frame, bg=COLORS['light'])
        customer_frame.pack(pady=5)
        
        tk.Label(customer_frame, text="اسم العميل:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(side=tk.LEFT, padx=5)
        self.customer_var = tk.StringVar()
        customer_entry = tk.Entry(customer_frame, textvariable=self.customer_var, width=20, font=('Arial', FONT_SIZES['medium']))
        customer_entry.pack(side=tk.LEFT, padx=5)
        
        # طريقة الدفع
        payment_frame = tk.Frame(total_frame, bg=COLORS['light'])
        payment_frame.pack(pady=5)
        
        tk.Label(payment_frame, text="طريقة الدفع:", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(side=tk.LEFT, padx=5)
        self.payment_var = tk.StringVar(value="نقدي")
        payment_combo = ttk.Combobox(payment_frame, textvariable=self.payment_var, values=["نقدي", "آجل"], width=15, font=('Arial', FONT_SIZES['medium']))
        payment_combo.pack(side=tk.LEFT, padx=5)
        
        # أزرار العمليات
        buttons_frame = tk.Frame(total_frame, bg=COLORS['light'])
        buttons_frame.pack(pady=10)
        
        clear_btn = ModernButton(buttons_frame, text="مسح السلة", command=self.clear_cart, style="secondary")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        checkout_btn = ModernButton(buttons_frame, text="إتمام البيع", command=self.checkout, style="success")
        checkout_btn.pack(side=tk.LEFT, padx=5)
    
    def create_info_section(self, parent):
        """إنشاء قسم المعلومات والإحصائيات"""
        # الإحصائيات اليومية
        stats_frame = tk.LabelFrame(
            parent,
            text="📊 إحصائيات اليوم",
            font=('Arial', FONT_SIZES['medium'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent'],
            padx=10,
            pady=10
        )
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.daily_sales_label = tk.Label(stats_frame, text="المبيعات: 0.00 ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium']))
        self.daily_sales_label.pack(anchor='w', pady=2)
        
        self.daily_expenses_label = tk.Label(stats_frame, text="المصروفات: 0.00 ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium']))
        self.daily_expenses_label.pack(anchor='w', pady=2)
        
        self.daily_profit_label = tk.Label(stats_frame, text="الربح: 0.00 ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium']))
        self.daily_profit_label.pack(anchor='w', pady=2)
        
        # المنتجات منخفضة المخزون
        low_stock_frame = tk.LabelFrame(
            parent,
            text="⚠️ تنبيهات المخزون",
            font=('Arial', FONT_SIZES['medium'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['warning'],
            padx=10,
            pady=10
        )
        low_stock_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.low_stock_listbox = tk.Listbox(low_stock_frame, height=8, font=('Arial', FONT_SIZES['small']))
        self.low_stock_listbox.pack(fill=tk.BOTH, expand=True)
        
        # آخر المبيعات
        recent_sales_frame = tk.LabelFrame(
            parent,
            text="🕒 آخر المبيعات",
            font=('Arial', FONT_SIZES['medium'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent'],
            padx=10,
            pady=10
        )
        recent_sales_frame.pack(fill=tk.BOTH, expand=True)
        
        self.recent_sales_listbox = tk.Listbox(recent_sales_frame, height=8, font=('Arial', FONT_SIZES['small']))
        self.recent_sales_listbox.pack(fill=tk.BOTH, expand=True)
    
    def create_bottom_bar(self, parent):
        """إنشاء الشريط السفلي مع أزرار الإدارة"""
        bottom_frame = tk.Frame(parent, bg=COLORS['secondary'], relief='raised', bd=1)
        bottom_frame.pack(fill=tk.X, pady=(10, 0), ipady=10)
        
        # أزرار الإدارة
        inventory_btn = ModernButton(bottom_frame, text="📦 إدارة المخزون", command=self.show_inventory_window)
        inventory_btn.pack(side=tk.LEFT, padx=10)
        
        expenses_btn = ModernButton(bottom_frame, text="💰 إدارة المصروفات", command=self.show_expenses_window)
        expenses_btn.pack(side=tk.LEFT, padx=10)
        
        reports_btn = ModernButton(bottom_frame, text="📈 التقارير", command=self.show_reports_window)
        reports_btn.pack(side=tk.LEFT, padx=10)
        
        # زر تأجير الكتب الجديد
        rental_btn = ModernButton(bottom_frame, text="📚 تأجير الكتب", command=self.show_rental_window)
        rental_btn.pack(side=tk.LEFT, padx=10)
        
        backup_btn = ModernButton(bottom_frame, text="💾 نسخ احتياطي", command=self.backup_data, style="secondary")
        backup_btn.pack(side=tk.RIGHT, padx=10)
    
    def show_rental_window(self):
        """عرض نافذة إدارة تأجير الكتب"""
        rental_window = tk.Toplevel(self.root)
        rental_window.title("إدارة تأجير الكتب")
        rental_window.geometry("900x600")
        rental_window.configure(bg=COLORS['background'])
        
        # العنوان
        title_label = tk.Label(
            rental_window,
            text="📚 إدارة تأجير الكتب",
            font=('Arial', FONT_SIZES['xlarge'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=10)
        
        # جدول الإعارات
        rentals_frame = tk.Frame(rental_window)
        rentals_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ('اسم الكتاب', 'اسم المستعير', 'تاريخ التأجير', 'تاريخ الإرجاع المتوقع', 'الحالة')
        self.rentals_tree = ttk.Treeview(rentals_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.rentals_tree.heading(col, text=col)
            self.rentals_tree.column(col, width=150, anchor='center')
        
        rentals_scrollbar = ttk.Scrollbar(rentals_frame, orient=tk.VERTICAL, command=self.rentals_tree.yview)
        self.rentals_tree.configure(yscrollcommand=rentals_scrollbar.set)
        
        self.rentals_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        rentals_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # أزرار العمليات
        buttons_frame = tk.Frame(rental_window, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        add_rental_btn = ModernButton(buttons_frame, text="إضافة إعارة جديدة", command=self.add_new_rental, style="success")
        add_rental_btn.pack(side=tk.LEFT, padx=10)
        
        return_book_btn = ModernButton(buttons_frame, text="تسجيل إرجاع كتاب", command=self.return_book, style="primary")
        return_book_btn.pack(side=tk.LEFT, padx=10)
        
        close_btn = ModernButton(buttons_frame, text="إغلاق", command=rental_window.destroy, style="secondary")
        close_btn.pack(side=tk.RIGHT, padx=10)
        
        # تحديث عرض الإعارات
        self.update_rentals_display()
    
    def add_new_rental(self):
        """إضافة إعارة جديدة"""
        # نافذة حوار لإضافة الإعارة
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة إعارة جديدة")
        dialog.geometry("400x300")
        dialog.configure(bg=COLORS['background'])
        dialog.grab_set()  # جعل النافذة modal
        
        # العنوان
        title_label = tk.Label(
            dialog,
            text="إضافة إعارة جديدة",
            font=('Arial', FONT_SIZES['large'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=10)
        
        # إطار الحقول
        fields_frame = tk.Frame(dialog, bg=COLORS['background'])
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # اختيار الكتاب
        tk.Label(fields_frame, text="اختر الكتاب:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(fields_frame, textvariable=book_var, width=30, font=('Arial', FONT_SIZES['medium']))
        
        # ملء قائمة الكتب المتاحة (التي لديها مخزون > 0)
        available_books = [f"{item['name']} (متوفر: {item['stock']})" for item in self.data['inventory'] if item['stock'] > 0]
        book_combo['values'] = available_books
        book_combo.pack(fill=tk.X, pady=(0, 10))
        
        # اسم المستعير
        tk.Label(fields_frame, text="اسم المستعير:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        renter_var = tk.StringVar()
        renter_entry = tk.Entry(fields_frame, textvariable=renter_var, width=30, font=('Arial', FONT_SIZES['medium']))
        renter_entry.pack(fill=tk.X, pady=(0, 10))
        
        # مدة الإعارة
        tk.Label(fields_frame, text="مدة الإعارة (بالأيام):", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        duration_var = tk.StringVar(value="7")
        duration_entry = tk.Entry(fields_frame, textvariable=duration_var, width=30, font=('Arial', FONT_SIZES['medium']))
        duration_entry.pack(fill=tk.X, pady=(0, 20))
        
        # أزرار العمليات
        buttons_frame = tk.Frame(fields_frame, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X)
        
        def save_rental():
            book_selection = book_var.get()
            renter_name = renter_var.get().strip()
            duration_str = duration_var.get().strip()
            
            if not book_selection or not renter_name or not duration_str:
                messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
                return
            
            try:
                duration = int(duration_str)
                if duration <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال مدة صحيحة بالأيام")
                return
            
            # استخراج اسم الكتاب من الاختيار
            book_name = book_selection.split(" (متوفر:")[0]
            
            # البحث عن الكتاب في المخزون
            book_item = None
            for item in self.data['inventory']:
                if item['name'] == book_name:
                    book_item = item
                    break
            
            if not book_item or book_item['stock'] <= 0:
                messagebox.showerror("خطأ", "الكتاب غير متوفر في المخزون")
                return
            
            # إنشاء سجل الإعارة
            rental_date = datetime.now().strftime("%Y-%m-%d")
            due_date = (datetime.now() + timedelta(days=duration)).strftime("%Y-%m-%d")
            
            rental_record = {
                'id': str(uuid.uuid4()),
                'book_id': book_item['id'],
                'book_name': book_name,
                'renter_name': renter_name,
                'rental_date': rental_date,
                'due_date': due_date,
                'status': 'مُعَار'
            }
            
            # إضافة الإعارة إلى البيانات
            self.data['rentals'].append(rental_record)
            
            # تقليل المخزون
            book_item['stock'] -= 1
            
            # حفظ البيانات
            self.save_data()
            
            # تحديث العروض
            self.update_displays()
            self.update_rentals_display()
            
            messagebox.showinfo("نجح", f"تم تسجيل إعارة الكتاب '{book_name}' للمستعير '{renter_name}' بنجاح")
            dialog.destroy()
        
        save_btn = ModernButton(buttons_frame, text="حفظ", command=save_rental, style="success")
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = ModernButton(buttons_frame, text="إلغاء", command=dialog.destroy, style="secondary")
        cancel_btn.pack(side=tk.LEFT)
    
    def return_book(self):
        """تسجيل إرجاع كتاب"""
        selected_item = self.rentals_tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "يرجى اختيار إعارة من القائمة")
            return
        
        # الحصول على بيانات الإعارة المحددة
        item_values = self.rentals_tree.item(selected_item[0])['values']
        book_name = item_values[0]
        renter_name = item_values[1]
        status = item_values[4]
        
        if status == "تم إرجاعه":
            messagebox.showinfo("معلومة", "هذا الكتاب تم إرجاعه بالفعل")
            return
        
        # البحث عن سجل الإعارة
        rental_record = None
        for rental in self.data['rentals']:
            if rental['book_name'] == book_name and rental['renter_name'] == renter_name and rental['status'] == 'مُعَار':
                rental_record = rental
                break
        
        if not rental_record:
            messagebox.showerror("خطأ", "لم يتم العثور على سجل الإعارة")
            return
        
        # تأكيد الإرجاع
        confirm = messagebox.askyesno("تأكيد", f"هل تريد تسجيل إرجاع الكتاب '{book_name}' من المستعير '{renter_name}'؟")
        if not confirm:
            return
        
        # تحديث حالة الإعارة
        rental_record['status'] = 'تم إرجاعه'
        rental_record['return_date'] = datetime.now().strftime("%Y-%m-%d")
        
        # زيادة المخزون
        for item in self.data['inventory']:
            if item['id'] == rental_record['book_id']:
                item['stock'] += 1
                break
        
        # حفظ البيانات
        self.save_data()
        
        # تحديث العروض
        self.update_displays()
        self.update_rentals_display()
        
        messagebox.showinfo("نجح", f"تم تسجيل إرجاع الكتاب '{book_name}' بنجاح")
    
    def update_rentals_display(self):
        """تحديث عرض الإعارات"""
        if hasattr(self, 'rentals_tree'):
            # مسح العرض الحالي
            for item in self.rentals_tree.get_children():
                self.rentals_tree.delete(item)
            
            # إضافة الإعارات
            for rental in self.data['rentals']:
                self.rentals_tree.insert('', 'end', values=(
                    rental['book_name'],
                    rental['renter_name'],
                    rental['rental_date'],
                    rental['due_date'],
                    rental['status']
                ))
    
    def add_to_cart(self):
        """إضافة منتج للسلة"""
        product_name = self.product_var.get()
        quantity_str = self.quantity_var.get()
        
        if not product_name or not quantity_str:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج وإدخال الكمية")
            return
        
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال كمية صحيحة")
            return
        
        # البحث عن المنتج في المخزون
        product = None
        for item in self.data['inventory']:
            if item['name'] == product_name:
                product = item
                break
        
        if not product:
            messagebox.showerror("خطأ", "المنتج غير موجود في المخزون")
            return
        
        if product['stock'] < quantity:
            messagebox.showerror("خطأ", f"الكمية المطلوبة غير متوفرة. المتوفر: {product['stock']}")
            return
        
        # إضافة للسلة
        cart_item = {
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'total': product['price'] * quantity
        }
        
        # التحقق من وجود المنتج في السلة
        existing_item = None
        for item in self.cart:
            if item['id'] == product['id']:
                existing_item = item
                break
        
        if existing_item:
            new_quantity = existing_item['quantity'] + quantity
            if product['stock'] < new_quantity:
                messagebox.showerror("خطأ", f"الكمية الإجمالية تتجاوز المتوفر. المتوفر: {product['stock']}")
                return
            existing_item['quantity'] = new_quantity
            existing_item['total'] = existing_item['price'] * new_quantity
        else:
            self.cart.append(cart_item)
        
        self.update_cart_display()
        
        # مسح الحقول
        self.product_var.set("")
        self.quantity_var.set("1")
    
    def update_cart_display(self):
        """تحديث عرض السلة"""
        # مسح العرض الحالي
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # حساب الإجمالي
        self.cart_total = 0
        
        # إضافة العناصر
        for item in self.cart:
            self.cart_tree.insert('', 'end', values=(
                item['name'],
                item['quantity'],
                f"{item['price']:.2f}",
                f"{item['total']:.2f}"
            ))
            self.cart_total += item['total']
        
        # تحديث الإجمالي
        self.total_label.config(text=f"الإجمالي: {self.cart_total:.2f} ريال")
    
    def clear_cart(self):
        """مسح السلة"""
        if self.cart:
            confirm = messagebox.askyesno("تأكيد", "هل تريد مسح جميع عناصر السلة؟")
            if confirm:
                self.cart.clear()
                self.update_cart_display()
    
    def checkout(self):
        """إتمام البيع"""
        if not self.cart:
            messagebox.showwarning("تحذير", "السلة فارغة")
            return
        
        customer_name = self.customer_var.get().strip()
        payment_method = self.payment_var.get()
        
        if not customer_name:
            customer_name = "عميل"
        
        # إنشاء فاتورة
        sale_id = str(uuid.uuid4())
        sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        sale_record = {
            'id': sale_id,
            'date': sale_date,
            'customer': customer_name,
            'payment_method': payment_method,
            'items': self.cart.copy(),
            'total': self.cart_total
        }
        
        # إضافة البيع للبيانات
        self.data['sales'].append(sale_record)
        
        # تحديث المخزون
        for cart_item in self.cart:
            for inventory_item in self.data['inventory']:
                if inventory_item['id'] == cart_item['id']:
                    inventory_item['stock'] -= cart_item['quantity']
                    break
        
        # حفظ البيانات
        self.save_data()
        
        # عرض خيارات الطباعة (مبسطة)
        self.show_print_options(sale_record)
        
        # مسح السلة
        self.cart.clear()
        self.customer_var.set("")
        self.payment_var.set("نقدي")
        self.update_cart_display()
        self.update_displays()
    
    def show_print_options(self, sale_record):
        """عرض خيارات الطباعة المبسطة"""
        print_window = tk.Toplevel(self.root)
        print_window.title("إتمام البيع")
        print_window.geometry("400x200")
        print_window.configure(bg=COLORS['background'])
        print_window.grab_set()
        
        # رسالة النجاح
        success_label = tk.Label(
            print_window,
            text="✅ تم إتمام البيع بنجاح!",
            font=('Arial', FONT_SIZES['large'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['success']
        )
        success_label.pack(pady=20)
        
        # تفاصيل البيع
        details_frame = tk.Frame(print_window, bg=COLORS['background'])
        details_frame.pack(pady=10)
        
        tk.Label(details_frame, text=f"رقم الفاتورة: {sale_record['id'][:8]}", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack()
        tk.Label(details_frame, text=f"العميل: {sale_record['customer']}", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack()
        tk.Label(details_frame, text=f"الإجمالي: {sale_record['total']:.2f} ريال", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'], 'bold')).pack()
        
        # زر الإغلاق
        close_btn = ModernButton(print_window, text="إغلاق", command=print_window.destroy, style="primary")
        close_btn.pack(pady=20)
    
    def show_inventory_window(self):
        """عرض نافذة إدارة المخزون"""
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("إدارة المخزون")
        inventory_window.geometry("800x600")
        inventory_window.configure(bg=COLORS['background'])
        inventory_window.grab_set()

        # العنوان
        title_label = tk.Label(
            inventory_window,
            text="📦 إدارة المخزون",
            font=('Arial', FONT_SIZES['xlarge'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=10)

        # جدول المخزون
        inventory_frame = tk.Frame(inventory_window)
        inventory_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ('الاسم', 'السعر', 'المخزون', 'الوصف')
        inventory_tree = ttk.Treeview(inventory_frame, columns=columns, show='headings', height=15)

        for col in columns:
            inventory_tree.heading(col, text=col)
            inventory_tree.column(col, width=150, anchor='center')

        inventory_scrollbar = ttk.Scrollbar(inventory_frame, orient=tk.VERTICAL, command=inventory_tree.yview)
        inventory_tree.configure(yscrollcommand=inventory_scrollbar.set)

        inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inventory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # تحديث عرض المخزون
        def update_inventory_display():
            selected_iid = inventory_tree.selection()
            
            for item in inventory_tree.get_children():
                inventory_tree.delete(item)

            for item in sorted(self.data['inventory'], key=lambda x: x['name']):
                inventory_tree.insert('', 'end', iid=item['id'], values=(
                    item['name'],
                    f"{item['price']:.2f}",
                    item['stock'],
                    item.get('description', '')
                ))
            
            if selected_iid and inventory_tree.exists(selected_iid[0]):
                inventory_tree.selection_set(selected_iid[0])

        update_inventory_display()

        # أزرار العمليات
        buttons_frame = tk.Frame(inventory_window, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)

        def add_product():
            self.add_product_dialog(update_inventory_display)

        def edit_product():
            selected_iid = inventory_tree.selection()
            if not selected_iid:
                messagebox.showwarning("تحذير", "يرجى اختيار منتج لتعديله", parent=inventory_window)
                return
            
            product_id = selected_iid[0]
            product_to_edit = next((p for p in self.data['inventory'] if p['id'] == product_id), None)
            
            if product_to_edit:
                self.edit_product_dialog(product_to_edit, update_inventory_display)

        def delete_product():
            selected_iid = inventory_tree.selection()
            if not selected_iid:
                messagebox.showwarning("تحذير", "يرجى اختيار منتج لحذفه", parent=inventory_window)
                return
            
            product_id = selected_iid[0]
            product_to_delete = next((p for p in self.data['inventory'] if p['id'] == product_id), None)
            
            if product_to_delete:
                product_name = product_to_delete['name']
                confirm = messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد أنك تريد حذف المنتج '{product_name}'؟\nلا يمكن التراجع عن هذا الإجراء.", parent=inventory_window)
                if confirm:
                    self.data['inventory'].remove(product_to_delete)
                    self.save_data()
                    update_inventory_display()
                    self.update_displays()
                    messagebox.showinfo("نجح", f"تم حذف المنتج '{product_name}' بنجاح.", parent=inventory_window)

        add_btn = ModernButton(buttons_frame, text="إضافة منتج", command=add_product, style="success")
        add_btn.pack(side=tk.LEFT, padx=10)

        edit_btn = ModernButton(buttons_frame, text="تعديل المنتج", command=edit_product, style="primary")
        edit_btn.pack(side=tk.LEFT, padx=10)

        delete_btn = ModernButton(buttons_frame, text="حذف المنتج", command=delete_product, style="danger")
        delete_btn.pack(side=tk.LEFT, padx=10)

        close_btn = ModernButton(buttons_frame, text="إغلاق", command=inventory_window.destroy, style="secondary")
        close_btn.pack(side=tk.RIGHT, padx=10)
    
    def add_product_dialog(self, callback=None):
        """حوار إضافة منتج جديد"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة منتج جديد")
        dialog.geometry("400x350")
        dialog.configure(bg=COLORS['background'])
        dialog.grab_set()
        
        # العنوان
        title_label = tk.Label(
            dialog,
            text="إضافة منتج جديد",
            font=('Arial', FONT_SIZES['large'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=10)
        
        # إطار الحقول
        fields_frame = tk.Frame(dialog, bg=COLORS['background'])
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # اسم المنتج
        tk.Label(fields_frame, text="اسم المنتج:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        name_var = tk.StringVar()
        name_entry = tk.Entry(fields_frame, textvariable=name_var, width=30, font=('Arial', FONT_SIZES['medium']))
        name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # السعر
        tk.Label(fields_frame, text="السعر:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        price_var = tk.StringVar()
        price_entry = tk.Entry(fields_frame, textvariable=price_var, width=30, font=('Arial', FONT_SIZES['medium']))
        price_entry.pack(fill=tk.X, pady=(0, 10))
        
        # الكمية
        tk.Label(fields_frame, text="الكمية:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        stock_var = tk.StringVar()
        stock_entry = tk.Entry(fields_frame, textvariable=stock_var, width=30, font=('Arial', FONT_SIZES['medium']))
        stock_entry.pack(fill=tk.X, pady=(0, 10))
        
        # الوصف
        tk.Label(fields_frame, text="الوصف (اختياري):", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        desc_var = tk.StringVar()
        desc_entry = tk.Entry(fields_frame, textvariable=desc_var, width=30, font=('Arial', FONT_SIZES['medium']))
        desc_entry.pack(fill=tk.X, pady=(0, 20))
        
        # أزرار العمليات
        buttons_frame = tk.Frame(fields_frame, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X)
        
        def save_product():
            name = name_var.get().strip()
            price_str = price_var.get().strip()
            stock_str = stock_var.get().strip()
            description = desc_var.get().strip()
            
            if not name or not price_str or not stock_str:
                messagebox.showerror("خطأ", "يرجى ملء جميع الحقول المطلوبة", parent=dialog)
                return
            
            if any(p['name'].lower() == name.lower() for p in self.data['inventory']):
                messagebox.showerror("خطأ", "اسم المنتج موجود بالفعل.", parent=dialog)
                return

            try:
                price = float(price_str)
                stock = int(stock_str)
                if price < 0 or stock < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة للسعر والكمية", parent=dialog)
                return
            
            # إنشاء المنتج الجديد
            product = {
                'id': str(uuid.uuid4()),
                'name': name,
                'price': price,
                'stock': stock,
                'description': description
            }
            
            # إضافة للمخزون
            self.data['inventory'].append(product)
            self.save_data()
            
            # تحديث العروض
            self.update_displays()
            if callback:
                callback()
            
            messagebox.showinfo("نجح", f"تم إضافة المنتج '{name}' بنجاح", parent=dialog)
            dialog.destroy()
        
        save_btn = ModernButton(buttons_frame, text="حفظ", command=save_product, style="success")
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = ModernButton(buttons_frame, text="إلغاء", command=dialog.destroy, style="secondary")
        cancel_btn.pack(side=tk.LEFT)

    def edit_product_dialog(self, product, callback=None):
        """حوار تعديل منتج موجود"""
        dialog = tk.Toplevel(self.root)
        dialog.title("تعديل منتج")
        dialog.geometry("400x350")
        dialog.configure(bg=COLORS['background'])
        dialog.grab_set()

        # العنوان
        title_label = tk.Label(
            dialog,
            text="تعديل منتج",
            font=('Arial', FONT_SIZES['large'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=10)

        # إطار الحقول
        fields_frame = tk.Frame(dialog, bg=COLORS['background'])
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # اسم المنتج
        tk.Label(fields_frame, text="اسم المنتج:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        name_var = tk.StringVar(value=product['name'])
        name_entry = tk.Entry(fields_frame, textvariable=name_var, width=30, font=('Arial', FONT_SIZES['medium']))
        name_entry.pack(fill=tk.X, pady=(0, 10))

        # السعر
        tk.Label(fields_frame, text="السعر:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        price_var = tk.StringVar(value=str(product['price']))
        price_entry = tk.Entry(fields_frame, textvariable=price_var, width=30, font=('Arial', FONT_SIZES['medium']))
        price_entry.pack(fill=tk.X, pady=(0, 10))

        # الكمية
        tk.Label(fields_frame, text="الكمية:", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        stock_var = tk.StringVar(value=str(product['stock']))
        stock_entry = tk.Entry(fields_frame, textvariable=stock_var, width=30, font=('Arial', FONT_SIZES['medium']))
        stock_entry.pack(fill=tk.X, pady=(0, 10))

        # الوصف
        tk.Label(fields_frame, text="الوصف (اختياري):", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w', pady=(0, 5))
        desc_var = tk.StringVar(value=product.get('description', ''))
        desc_entry = tk.Entry(fields_frame, textvariable=desc_var, width=30, font=('Arial', FONT_SIZES['medium']))
        desc_entry.pack(fill=tk.X, pady=(0, 20))

        # أزرار العمليات
        buttons_frame = tk.Frame(fields_frame, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X)

        def save_changes():
            name = name_var.get().strip()
            price_str = price_var.get().strip()
            stock_str = stock_var.get().strip()
            description = desc_var.get().strip()

            if not name or not price_str or not stock_str:
                messagebox.showerror("خطأ", "يرجى ملء جميع الحقول المطلوبة", parent=dialog)
                return

            try:
                price = float(price_str)
                stock = int(stock_str)
                if price < 0 or stock < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة للسعر والكمية", parent=dialog)
                return
            
            if any(p['name'].lower() == name.lower() and p['id'] != product['id'] for p in self.data['inventory']):
                messagebox.showerror("خطأ", "اسم المنتج مستخدم بالفعل.", parent=dialog)
                return

            # تحديث المنتج
            product['name'] = name
            product['price'] = price
            product['stock'] = stock
            product['description'] = description
            
            self.save_data()

            # تحديث العروض
            self.update_displays()
            if callback:
                callback()

            dialog.destroy()

        save_btn = ModernButton(buttons_frame, text="حفظ التعديلات", command=save_changes, style="success")
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        cancel_btn = ModernButton(buttons_frame, text="إلغاء", command=dialog.destroy, style="secondary")
        cancel_btn.pack(side=tk.LEFT)

    def show_expenses_window(self):
        """عرض نافذة إدارة المصروفات"""
        expenses_window = tk.Toplevel(self.root)
        expenses_window.title("إدارة المصروفات")
        expenses_window.geometry("700x500")
        expenses_window.configure(bg=COLORS['background'])
        
        # العنوان
        title_label = tk.Label(
            expenses_window,
            text="💰 إدارة المصروفات",
            font=('Arial', FONT_SIZES['xlarge'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=10)
        
        # إطار إضافة مصروف
        add_frame = tk.Frame(expenses_window, bg=COLORS['light'], relief='raised', bd=1)
        add_frame.pack(fill=tk.X, padx=20, pady=10, ipady=10)
        
        tk.Label(add_frame, text="إضافة مصروف جديد", font=('Arial', FONT_SIZES['medium'], 'bold'), bg=COLORS['light']).pack(pady=5)
        
        fields_frame = tk.Frame(add_frame, bg=COLORS['light'])
        fields_frame.pack(pady=5)
        
        # الوصف
        tk.Label(fields_frame, text="الوصف:", bg=COLORS['light']).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        desc_var = tk.StringVar()
        desc_entry = tk.Entry(fields_frame, textvariable=desc_var, width=20)
        desc_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # المبلغ
        tk.Label(fields_frame, text="المبلغ:", bg=COLORS['light']).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        amount_var = tk.StringVar()
        amount_entry = tk.Entry(fields_frame, textvariable=amount_var, width=15)
        amount_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # النوع
        tk.Label(fields_frame, text="النوع:", bg=COLORS['light']).grid(row=0, column=4, padx=5, pady=5, sticky='w')
        type_var = tk.StringVar(value="عام")
        type_combo = ttk.Combobox(fields_frame, textvariable=type_var, values=["عام", "مكتب", "نقل", "صيانة", "أخرى"], width=12)
        type_combo.grid(row=0, column=5, padx=5, pady=5)
        
        def add_expense():
            desc = desc_var.get().strip()
            amount_str = amount_var.get().strip()
            expense_type = type_var.get()
            
            if not desc or not amount_str:
                messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال مبلغ صحيح")
                return
            
            expense = {
                'id': str(uuid.uuid4()),
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'description': desc,
                'amount': amount,
                'type': expense_type
            }
            
            self.data['expenses'].append(expense)
            self.save_data()
            self.update_displays()
            update_expenses_display()
            
            # مسح الحقول
            desc_var.set("")
            amount_var.set("")
            type_var.set("عام")
            
            messagebox.showinfo("نجح", "تم إضافة المصروف بنجاح")
        
        add_btn = ModernButton(add_frame, text="إضافة", command=add_expense, style="success")
        add_btn.pack(pady=5)
        
        # جدول المصروفات
        expenses_frame = tk.Frame(expenses_window)
        expenses_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ('التاريخ', 'الوصف', 'المبلغ', 'النوع')
        expenses_tree = ttk.Treeview(expenses_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            expenses_tree.heading(col, text=col)
            expenses_tree.column(col, width=150, anchor='center')
        
        expenses_scrollbar = ttk.Scrollbar(expenses_frame, orient=tk.VERTICAL, command=expenses_tree.yview)
        expenses_tree.configure(yscrollcommand=expenses_scrollbar.set)
        
        expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        expenses_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def update_expenses_display():
            for item in expenses_tree.get_children():
                expenses_tree.delete(item)
            
            for expense in reversed(self.data['expenses']):
                expenses_tree.insert('', 'end', values=(
                    expense['date'],
                    expense['description'],
                    f"{expense['amount']:.2f}",
                    expense['type']
                ))
        
        update_expenses_display()
        
        # زر الإغلاق
        close_btn = ModernButton(expenses_window, text="إغلاق", command=expenses_window.destroy, style="secondary")
        close_btn.pack(pady=10)
    
    def show_reports_window(self):
        """عرض نافذة التقارير"""
        reports_window = tk.Toplevel(self.root)
        reports_window.title("التقارير والإحصائيات")
        reports_window.geometry("600x500")
        reports_window.configure(bg=COLORS['background'])
        
        # العنوان
        title_label = tk.Label(
            reports_window,
            text="📈 التقارير والإحصائيات",
            font=('Arial', FONT_SIZES['xlarge'], 'bold'),
            bg=COLORS['background'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=10)
        
        # حساب الإحصائيات
        today = datetime.now().strftime("%Y-%m-%d")
        
        # المبيعات اليومية
        daily_sales = sum(sale['total'] for sale in self.data['sales'] if sale['date'].startswith(today))
        
        # المصروفات اليومية
        daily_expenses = sum(expense['amount'] for expense in self.data['expenses'] if expense['date'].startswith(today))
        
        # الربح اليومي
        daily_profit = daily_sales - daily_expenses
        
        # إجمالي المبيعات
        total_sales = sum(sale['total'] for sale in self.data['sales'])
        
        # إجمالي المصروفات
        total_expenses = sum(expense['amount'] for expense in self.data['expenses'])
        
        # الربح الإجمالي
        total_profit = total_sales - total_expenses
        
        # عرض الإحصائيات
        stats_frame = tk.Frame(reports_window, bg=COLORS['light'], relief='raised', bd=1)
        stats_frame.pack(fill=tk.X, padx=20, pady=10, ipady=15)
        
        tk.Label(stats_frame, text="الإحصائيات اليومية", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['light'], fg=COLORS['accent']).pack(pady=5)
        
        daily_frame = tk.Frame(stats_frame, bg=COLORS['light'])
        daily_frame.pack(pady=5)
        
        tk.Label(daily_frame, text=f"المبيعات اليوم: {daily_sales:.2f} ريال", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(daily_frame, text=f"المصروفات اليوم: {daily_expenses:.2f} ريال", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        
        profit_color = COLORS['success'] if daily_profit >= 0 else COLORS['danger']
        tk.Label(daily_frame, text=f"الربح اليوم: {daily_profit:.2f} ريال", bg=COLORS['light'], font=('Arial', FONT_SIZES['medium'], 'bold'), fg=profit_color).pack(anchor='w')
        
        # الإحصائيات الإجمالية
        total_stats_frame = tk.Frame(reports_window, bg=COLORS['secondary'], relief='raised', bd=1)
        total_stats_frame.pack(fill=tk.X, padx=20, pady=10, ipady=15)
        
        tk.Label(total_stats_frame, text="الإحصائيات الإجمالية", font=('Arial', FONT_SIZES['large'], 'bold'), bg=COLORS['secondary'], fg=COLORS['accent']).pack(pady=5)
        
        total_frame = tk.Frame(total_stats_frame, bg=COLORS['secondary'])
        total_frame.pack(pady=5)
        
        tk.Label(total_frame, text=f"إجمالي المبيعات: {total_sales:.2f} ريال", bg=COLORS['secondary'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(total_frame, text=f"إجمالي المصروفات: {total_expenses:.2f} ريال", bg=COLORS['secondary'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        
        total_profit_color = COLORS['success'] if total_profit >= 0 else COLORS['danger']
        tk.Label(total_frame, text=f"الربح الإجمالي: {total_profit:.2f} ريال", bg=COLORS['secondary'], font=('Arial', FONT_SIZES['medium'], 'bold'), fg=total_profit_color).pack(anchor='w')
        
        # معلومات إضافية
        info_frame = tk.Frame(reports_window, bg=COLORS['background'])
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(info_frame, text=f"عدد المنتجات في المخزون: {len(self.data['inventory'])}", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(info_frame, text=f"عدد المبيعات: {len(self.data['sales'])}", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(info_frame, text=f"عدد المصروفات: {len(self.data['expenses'])}", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        tk.Label(info_frame, text=f"عدد الإعارات: {len(self.data['rentals'])}", bg=COLORS['background'], font=('Arial', FONT_SIZES['medium'])).pack(anchor='w')
        
        # زر الإغلاق
        close_btn = ModernButton(reports_window, text="إغلاق", command=reports_window.destroy, style="secondary")
        close_btn.pack(pady=20)
    
    def backup_data(self):
        """إنشاء نسخة احتياطية من البيانات"""
        try:
            backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("نجح", f"تم إنشاء النسخة الاحتياطية: {backup_filename}")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في إنشاء النسخة الاحتياطية: {str(e)}")
    
    def update_displays(self):
        """تحديث جميع العروض"""
        # تحديث قائمة المنتجات
        products = [item['name'] for item in self.data['inventory'] if item['stock'] > 0]
        self.product_combo['values'] = products
        
        # تحديث الإحصائيات اليومية
        today = datetime.now().strftime("%Y-%m-%d")
        daily_sales = sum(sale['total'] for sale in self.data['sales'] if sale['date'].startswith(today))
        daily_expenses = sum(expense['amount'] for expense in self.data['expenses'] if expense['date'].startswith(today))
        daily_profit = daily_sales - daily_expenses
        
        self.daily_sales_label.config(text=f"المبيعات: {daily_sales:.2f} ريال")
        self.daily_expenses_label.config(text=f"المصروفات: {daily_expenses:.2f} ريال")
        
        profit_color = COLORS['success'] if daily_profit >= 0 else COLORS['danger']
        self.daily_profit_label.config(text=f"الربح: {daily_profit:.2f} ريال", fg=profit_color)
        
        # تحديث تنبيهات المخزون المنخفض
        self.low_stock_listbox.delete(0, tk.END)
        for item in self.data['inventory']:
            if item['stock'] <= 5:  # تنبيه عند 5 قطع أو أقل
                self.low_stock_listbox.insert(tk.END, f"{item['name']}: {item['stock']} قطعة")
        
        # تحديث آخر المبيعات
        self.recent_sales_listbox.delete(0, tk.END)
        recent_sales = sorted(self.data['sales'], key=lambda x: x['date'], reverse=True)[:10]
        for sale in recent_sales:
            sale_date = sale['date'].split()[0]  # التاريخ فقط
            self.recent_sales_listbox.insert(tk.END, f"{sale_date} - {sale['customer']}: {sale['total']:.2f} ريال")

def main():
    """الدالة الرئيسية"""
    root = tk.Tk()
    app = SalesManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
