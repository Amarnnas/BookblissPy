#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المبيعات والمصروفات المطور - Book Bliss
Enhanced Sales & Expense Management System - Book Bliss
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog, filedialog
except ImportError:
    print("Error: tkinter is not available on this system.")
    exit(1)

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid
import hashlib
from PIL import Image, ImageDraw, ImageFont, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import threading
import time

# ألوان Book Bliss
COLORS = {
    'primary': '#0A0C63',      # أزرق داكن
    'secondary': '#FFD633',    # أصفر ذهبي
    'background': '#FAFAFA',   # خلفية فاتحة
    'white': '#FFFFFF',
    'success': '#28A745',      # أخضر
    'warning': '#FFC107',      # برتقالي
    'danger': '#DC3545',       # أحمر
    'dark': '#343A40',
    'light': '#F8F9FA'
}

class LoginWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.root = tk.Toplevel()
        self.root.title("Book Bliss - تسجيل الدخول")
        self.root.geometry("450x350")
        self.root.configure(bg=COLORS['background'])
        self.root.resizable(False, False)
        
        # جعل النافذة في المقدمة
        self.root.transient(parent_app.root)
        self.root.grab_set()
        
        # توسيط النافذة
        self.center_window()
        
        self.setup_ui()
        
    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.root.winfo_screenheight() // 2) - (350 // 2)
        self.root.geometry(f"450x350+{x}+{y}")
        
    def setup_ui(self):
        # الشعار والعنوان
        header_frame = tk.Frame(self.root, bg=COLORS['primary'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📚 Book Bliss",
            font=("Cairo", 24, "bold"),
            fg=COLORS['secondary'],
            bg=COLORS['primary']
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="نظام إدارة المبيعات",
            font=("Cairo", 12),
            fg=COLORS['white'],
            bg=COLORS['primary']
        )
        subtitle_label.pack()
        
        # إطار تسجيل الدخول
        login_frame = tk.Frame(self.root, bg=COLORS['white'], padx=40, pady=30)
        login_frame.pack(pady=30, padx=40, fill='both', expand=True)
        
        # اسم المستخدم
        tk.Label(
            login_frame,
            text="اسم المستخدم:",
            font=("Cairo", 12, "bold"),
            fg=COLORS['dark'],
            bg=COLORS['white']
        ).pack(pady=(0, 5), anchor='w')
        
        self.username_entry = tk.Entry(
            login_frame, 
            font=("Cairo", 12), 
            width=25,
            relief='flat',
            bd=10,
            bg=COLORS['light']
        )
        self.username_entry.pack(pady=(0, 15), ipady=8)
        self.username_entry.insert(0, "admin")
        
        # كلمة المرور
        tk.Label(
            login_frame,
            text="كلمة المرور:",
            font=("Cairo", 12, "bold"),
            fg=COLORS['dark'],
            bg=COLORS['white']
        ).pack(pady=(0, 5), anchor='w')
        
        self.password_entry = tk.Entry(
            login_frame, 
            font=("Cairo", 12), 
            width=25, 
            show="*",
            relief='flat',
            bd=10,
            bg=COLORS['light']
        )
        self.password_entry.pack(pady=(0, 20), ipady=8)
        self.password_entry.insert(0, "admin")
        
        # زر تسجيل الدخول
        login_btn = tk.Button(
            login_frame,
            text="تسجيل الدخول",
            font=("Cairo", 14, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white'],
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            command=self.login
        )
        login_btn.pack(pady=10)
        
        # تأثير hover للزر
        def on_enter(e):
            login_btn.configure(bg=COLORS['secondary'], fg=COLORS['primary'])
        def on_leave(e):
            login_btn.configure(bg=COLORS['primary'], fg=COLORS['white'])
            
        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)
        
        # ربط Enter بتسجيل الدخول
        self.root.bind('<Return>', lambda e: self.login())
        
        # تركيز على حقل اسم المستخدم
        self.username_entry.focus()
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # تشفير كلمة المرور
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # التحقق من بيانات تسجيل الدخول
        users = self.parent_app.data.get('users', {})
        
        if not users:  # إنشاء مستخدم افتراضي
            default_user = {
                'admin': {
                    'password': hashlib.sha256('admin'.encode()).hexdigest(),
                    'role': 'admin',
                    'name': 'المدير'
                }
            }
            self.parent_app.data['users'] = default_user
            users = default_user
        
        if username in users and users[username]['password'] == hashed_password:
            self.parent_app.current_user = {
                'username': username,
                'role': users[username]['role'],
                'name': users[username]['name']
            }
            self.root.destroy()
            self.parent_app.show_main_window()
        else:
            messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")

class ModernButton(tk.Button):
    """زر حديث مخصص"""
    def __init__(self, parent, text, command=None, bg_color=COLORS['primary'], 
                 fg_color=COLORS['white'], hover_bg=COLORS['secondary'], 
                 hover_fg=COLORS['primary'], **kwargs):
        
        super().__init__(
            parent,
            text=text,
            command=command,
            font=("Cairo", 11, "bold"),
            bg=bg_color,
            fg=fg_color,
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            **kwargs
        )
        
        self.default_bg = bg_color
        self.default_fg = fg_color
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self.configure(bg=self.hover_bg, fg=self.hover_fg)
        
    def on_leave(self, e):
        self.configure(bg=self.default_bg, fg=self.default_fg)

class ProductCard(tk.Frame):
    """بطاقة منتج حديثة"""
    def __init__(self, parent, product, add_to_cart_callback):
        super().__init__(parent, bg=COLORS['white'], relief='flat', bd=1)
        
        self.product = product
        self.add_to_cart_callback = add_to_cart_callback
        
        # إطار الصورة
        image_frame = tk.Frame(self, bg=COLORS['light'], height=80)
        image_frame.pack(fill='x', padx=5, pady=5)
        image_frame.pack_propagate(False)
        
        # أيقونة المنتج (يمكن استبدالها بصورة حقيقية)
        icon_label = tk.Label(
            image_frame,
            text="📚" if "كتاب" in product.get('category', '') else "📦",
            font=("Arial", 24),
            bg=COLORS['light'],
            fg=COLORS['primary']
        )
        icon_label.pack(expand=True)
        
        # اسم المنتج
        name_label = tk.Label(
            self,
            text=product['name'][:20] + "..." if len(product['name']) > 20 else product['name'],
            font=("Cairo", 10, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark'],
            wraplength=120
        )
        name_label.pack(pady=(5, 2))
        
        # السعر
        price_label = tk.Label(
            self,
            text=f"{product['price']:.2f} جنيه",
            font=("Cairo", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        price_label.pack(pady=2)
        
        # حالة المخزون
        stock_color = COLORS['success'] if product['stock'] > 10 else COLORS['warning'] if product['stock'] > 0 else COLORS['danger']
        stock_text = "متوفر" if product['stock'] > 10 else "قليل" if product['stock'] > 0 else "نفد"
        
        stock_label = tk.Label(
            self,
            text=f"المخزون: {stock_text}",
            font=("Cairo", 8),
            bg=COLORS['white'],
            fg=stock_color
        )
        stock_label.pack(pady=2)
        
        # زر الإضافة
        if product['stock'] > 0:
            add_btn = ModernButton(
                self,
                text="إضافة",
                command=lambda: self.add_to_cart_callback(product),
                bg_color=COLORS['secondary'],
                fg_color=COLORS['primary']
            )
            add_btn.pack(pady=5, padx=5, fill='x')
        
        # تأثير hover للبطاقة
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        # ربط الأحداث لجميع العناصر الفرعية
        for child in self.winfo_children():
            child.bind("<Enter>", self.on_enter)
            child.bind("<Leave>", self.on_leave)
            for grandchild in child.winfo_children():
                grandchild.bind("<Enter>", self.on_enter)
                grandchild.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.configure(relief='raised', bd=2)
        
    def on_leave(self, e):
        self.configure(relief='flat', bd=1)

class SalesManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # إخفاء النافذة الرئيسية حتى تسجيل الدخول
        
        # تحديد مسار ملف البيانات
        self.data_file = "sales_data.json"
        self.backup_path = os.path.join(os.getcwd(), "backups")
        
        # تهيئة البيانات
        self.data = self.load_data()
        self.cart = []
        self.current_user = None
        self.current_language = self.data.get('settings', {}).get('language', 'ar')
        
        # تحميل النصوص
        self.load_translations()
        
        # إنشاء مجلد النسخ الاحتياطية
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)
        
        # متغيرات البحث والفلترة
        self.search_var = tk.StringVar()
        self.category_filter_var = tk.StringVar()
        
        # عرض نافذة تسجيل الدخول
        self.login_window = LoginWindow(self)
        
    def show_main_window(self):
        """عرض النافذة الرئيسية بعد تسجيل الدخول"""
        self.root.deiconify()
        self.root.title(f"Book Bliss - {self.current_user['name']}")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['background'])
        self.root.state('zoomed')  # ملء الشاشة
        
        # إعداد الواجهة
        self.setup_modern_ui()
        
    def load_translations(self):
        """تحميل النصوص حسب اللغة"""
        if self.current_language == 'ar':
            self.texts = {
                'app_title': 'Book Bliss - نظام إدارة المبيعات',
                'sales': '🛒 المبيعات',
                'inventory': '📦 المخزون',
                'expenses': '💰 المصروفات',
                'reports': '📊 التقارير',
                'settings': '⚙️ الإعدادات',
                'backup': '💾 النسخ الاحتياطي',
                'all_sales': '📋 جميع المبيعات',
                'search_placeholder': 'البحث عن منتج...',
                'scan_barcode': '📷 مسح باركود',
                'total': 'الإجمالي',
                'pay_now': 'الدفع الآن',
                'cash': 'كاش',
                'card': 'بطاقة',
                'wallet': 'محفظة',
                'save_invoice': 'حفظ الفاتورة',
                'cancel': 'إلغاء',
                'daily_report': 'تقرير يومي',
                'currency': 'جنيه'
            }
        else:  # English
            self.texts = {
                'app_title': 'Book Bliss - Sales Management System',
                'sales': '🛒 Sales',
                'inventory': '📦 Inventory',
                'expenses': '💰 Expenses',
                'reports': '📊 Reports',
                'settings': '⚙️ Settings',
                'backup': '💾 Backup',
                'all_sales': '📋 All Sales',
                'search_placeholder': 'Search for product...',
                'scan_barcode': '📷 Scan Barcode',
                'total': 'Total',
                'pay_now': 'Pay Now',
                'cash': 'Cash',
                'card': 'Card',
                'wallet': 'Wallet',
                'save_invoice': 'Save Invoice',
                'cancel': 'Cancel',
                'daily_report': 'Daily Report',
                'currency': 'EGP'
            }
        
    def load_data(self) -> Dict[str, Any]:
        """تحميل البيانات من الملف"""
        default_data = {
            "inventory": [
                {
                    'id': 1,
                    'name': 'كتاب الأسود يليق بك',
                    'price': 85.0,
                    'stock': 25,
                    'category': 'كتب تطوير الذات',
                    'description': 'كتاب رائع في تطوير الذات',
                    'barcode': '1234567890123'
                },
                {
                    'id': 2,
                    'name': 'رواية مئة عام من العزلة',
                    'price': 120.0,
                    'stock': 15,
                    'category': 'روايات',
                    'description': 'رواية كلاسيكية',
                    'barcode': '1234567890124'
                },
                {
                    'id': 3,
                    'name': 'كتاب البرمجة بـ Python',
                    'price': 200.0,
                    'stock': 8,
                    'category': 'كتب تقنية',
                    'description': 'تعلم البرمجة',
                    'barcode': '1234567890125'
                }
            ],
            "sales": [],
            "expenses": [],
            "customers": [],
            "users": {},
            "product_categories": ["كتب تطوير الذات", "روايات", "كتب تقنية", "كتب أطفال", "مجلات", "قرطاسية"],
            "settings": {
                "currency": "EGP",
                "tax_rate": 0.14,
                "low_stock_threshold": 5,
                "language": "ar",
                "backup_path": os.path.join(os.getcwd(), "backups"),
                "data_path": os.getcwd(),
                "store_name": "Book Bliss",
                "store_address": "شارع الكتب، القاهرة",
                "store_phone": "01234567890"
            }
        }
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    # دمج البيانات الافتراضية مع البيانات المحملة
                    for key, value in default_data.items():
                        if key not in loaded_data:
                            loaded_data[key] = value
                    return loaded_data
            except:
                return default_data
        return default_data
    
    def save_data(self):
        """حفظ البيانات في الملف"""
        try:
            data_path = self.data.get('settings', {}).get('data_path', os.getcwd())
            file_path = os.path.join(data_path, "sales_data.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ البيانات: {str(e)}")
    
    def setup_modern_ui(self):
        """إعداد الواجهة الحديثة"""
        # الشريط العلوي
        self.create_top_bar()
        
        # المحتوى الرئيسي
        self.create_main_content()
        
        # الشريط السفلي
        self.create_bottom_bar()
        
        # تحديث العرض
        self.update_products_display()
        self.update_cart_display()
        
        # بدء النسخ الاحتياطي التلقائي
        self.start_auto_backup()
    
    def create_top_bar(self):
        """إنشاء الشريط العلوي"""
        top_bar = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        top_bar.pack(fill='x')
        top_bar.pack_propagate(False)
        
        # الشعار
        logo_frame = tk.Frame(top_bar, bg=COLORS['primary'])
        logo_frame.pack(side='left', padx=20, pady=15)
        
        logo_label = tk.Label(
            logo_frame,
            text="📚 Book Bliss",
            font=("Cairo", 20, "bold"),
            fg=COLORS['secondary'],
            bg=COLORS['primary']
        )
        logo_label.pack()
        
        # أدوات البحث
        search_frame = tk.Frame(top_bar, bg=COLORS['primary'])
        search_frame.pack(side='right', padx=20, pady=15)
        
        # حقل البحث
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Cairo", 12),
            width=25,
            relief='flat',
            bd=5,
            bg=COLORS['white']
        )
        search_entry.pack(side='left', padx=5, ipady=8)
        search_entry.insert(0, self.texts['search_placeholder'])
        
        # ربط البحث
        self.search_var.trace('w', self.on_search_change)
        
        # زر مسح الباركود
        barcode_btn = ModernButton(
            search_frame,
            text=self.texts['scan_barcode'],
            command=self.scan_barcode,
            bg_color=COLORS['secondary'],
            fg_color=COLORS['primary']
        )
        barcode_btn.pack(side='left', padx=5)
        
        # معلومات المستخدم والوقت
        info_frame = tk.Frame(top_bar, bg=COLORS['primary'])
        info_frame.pack(side='right', padx=20, pady=15)
        
        user_label = tk.Label(
            info_frame,
            text=f"المستخدم: {self.current_user['name']}",
            font=("Cairo", 10),
            fg=COLORS['white'],
            bg=COLORS['primary']
        )
        user_label.pack()
        
        time_label = tk.Label(
            info_frame,
            text=datetime.now().strftime('%Y-%m-%d %H:%M'),
            font=("Cairo", 10),
            fg=COLORS['secondary'],
            bg=COLORS['primary']
        )
        time_label.pack()
        
        # تحديث الوقت كل دقيقة
        def update_time():
            time_label.config(text=datetime.now().strftime('%Y-%m-%d %H:%M'))
            self.root.after(60000, update_time)
        update_time()
    
    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # القسم الأيسر - المنتجات
        left_frame = tk.Frame(main_frame, bg=COLORS['white'], relief='flat', bd=1)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # عنوان وفلتر المنتجات
        products_header = tk.Frame(left_frame, bg=COLORS['white'], height=50)
        products_header.pack(fill='x', padx=10, pady=10)
        products_header.pack_propagate(False)
        
        tk.Label(
            products_header,
            text="المنتجات",
            font=("Cairo", 16, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(side='left', pady=10)
        
        # فلتر الفئات
        tk.Label(
            products_header,
            text="الفئة:",
            font=("Cairo", 10),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(side='right', padx=(0, 5))
        
        category_combo = ttk.Combobox(
            products_header,
            textvariable=self.category_filter_var,
            values=["الكل"] + self.data['product_categories'],
            font=("Cairo", 10),
            state="readonly",
            width=15
        )
        category_combo.set("الكل")
        category_combo.pack(side='right', padx=5)
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.update_products_display())
        
        # إطار المنتجات مع التمرير
        products_container = tk.Frame(left_frame, bg=COLORS['white'])
        products_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Canvas للتمرير
        self.products_canvas = tk.Canvas(products_container, bg=COLORS['white'], highlightthickness=0)
        products_scrollbar = ttk.Scrollbar(products_container, orient="vertical", command=self.products_canvas.yview)
        self.products_scrollable_frame = tk.Frame(self.products_canvas, bg=COLORS['white'])
        
        self.products_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.products_canvas.configure(scrollregion=self.products_canvas.bbox("all"))
        )
        
        self.products_canvas.create_window((0, 0), window=self.products_scrollable_frame, anchor="nw")
        self.products_canvas.configure(yscrollcommand=products_scrollbar.set)
        
        self.products_canvas.pack(side="left", fill="both", expand=True)
        products_scrollbar.pack(side="right", fill="y")
        
        # ربط عجلة الماوس بالتمرير
        def on_mousewheel(event):
            self.products_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.products_canvas.bind("<MouseWheel>", on_mousewheel)
        
        # القسم الأيمن - سلة المشتريات
        right_frame = tk.Frame(main_frame, bg=COLORS['white'], relief='flat', bd=1, width=400)
        right_frame.pack(side='right', fill='y', padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # عنوان السلة
        cart_header = tk.Frame(right_frame, bg=COLORS['primary'], height=60)
        cart_header.pack(fill='x')
        cart_header.pack_propagate(False)
        
        tk.Label(
            cart_header,
            text="🛒 سلة المشتريات",
            font=("Cairo", 16, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        # قائمة المنتجات في السلة
        cart_container = tk.Frame(right_frame, bg=COLORS['white'])
        cart_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas للسلة
        self.cart_canvas = tk.Canvas(cart_container, bg=COLORS['white'], highlightthickness=0)
        cart_scrollbar = ttk.Scrollbar(cart_container, orient="vertical", command=self.cart_canvas.yview)
        self.cart_scrollable_frame = tk.Frame(self.cart_canvas, bg=COLORS['white'])
        
        self.cart_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))
        )
        
        self.cart_canvas.create_window((0, 0), window=self.cart_scrollable_frame, anchor="nw")
        self.cart_canvas.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_canvas.pack(side="left", fill="both", expand=True)
        cart_scrollbar.pack(side="right", fill="y")
        
        # الإجمالي وزر الدفع
        payment_frame = tk.Frame(right_frame, bg=COLORS['light'], height=120)
        payment_frame.pack(fill='x', side='bottom')
        payment_frame.pack_propagate(False)
        
        # الإجمالي
        self.total_label = tk.Label(
            payment_frame,
            text="الإجمالي: 0.00 جنيه",
            font=("Cairo", 18, "bold"),
            bg=COLORS['light'],
            fg=COLORS['primary']
        )
        self.total_label.pack(pady=10)
        
        # زر الدفع الكبير
        self.pay_button = ModernButton(
            payment_frame,
            text=self.texts['pay_now'],
            command=self.show_payment_dialog,
            bg_color=COLORS['secondary'],
            fg_color=COLORS['primary']
        )
        self.pay_button.pack(pady=10, padx=20, fill='x', ipady=10)
        self.pay_button.configure(font=("Cairo", 16, "bold"))
    
    def create_bottom_bar(self):
        """إنشاء الشريط السفلي"""
        bottom_bar = tk.Frame(self.root, bg=COLORS['primary'], height=60)
        bottom_bar.pack(fill='x', side='bottom')
        bottom_bar.pack_propagate(False)
        
        # الأزرار اليسرى
        left_buttons = tk.Frame(bottom_bar, bg=COLORS['primary'])
        left_buttons.pack(side='left', padx=20, pady=10)
        
        ModernButton(
            left_buttons,
            text=self.texts['save_invoice'],
            command=self.save_current_invoice,
            bg_color=COLORS['success'],
            hover_bg=COLORS['light']
        ).pack(side='left', padx=5)
        
        ModernButton(
            left_buttons,
            text=self.texts['cancel'],
            command=self.clear_cart,
            bg_color=COLORS['danger'],
            hover_bg=COLORS['light']
        ).pack(side='left', padx=5)
        
        ModernButton(
            left_buttons,
            text=self.texts['daily_report'],
            command=self.show_daily_report,
            bg_color=COLORS['warning'],
            fg_color=COLORS['dark'],
            hover_bg=COLORS['light']
        ).pack(side='left', padx=5)
        
        # مؤشر حالة المخزون
        status_frame = tk.Frame(bottom_bar, bg=COLORS['primary'])
        status_frame.pack(side='right', padx=20, pady=10)
        
        # حساب إحصائيات المخزون
        available = len([p for p in self.data['inventory'] if p['stock'] > 10])
        low = len([p for p in self.data['inventory'] if 0 < p['stock'] <= 10])
        out = len([p for p in self.data['inventory'] if p['stock'] == 0])
        
        tk.Label(
            status_frame,
            text=f"🟢 متوفر: {available}",
            font=("Cairo", 10),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(side='left', padx=10)
        
        tk.Label(
            status_frame,
            text=f"🟡 قليل: {low}",
            font=("Cairo", 10),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(side='left', padx=10)
        
        tk.Label(
            status_frame,
            text=f"🔴 نفد: {out}",
            font=("Cairo", 10),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(side='left', padx=10)
        
        # أزرار الإدارة
        admin_buttons = tk.Frame(bottom_bar, bg=COLORS['primary'])
        admin_buttons.pack(side='right', padx=20, pady=10)
        
        ModernButton(
            admin_buttons,
            text="📦 المخزون",
            command=self.show_inventory_window,
            bg_color=COLORS['secondary'],
            fg_color=COLORS['primary']
        ).pack(side='left', padx=2)
        
        ModernButton(
            admin_buttons,
            text="📊 التقارير",
            command=self.show_reports_window,
            bg_color=COLORS['secondary'],
            fg_color=COLORS['primary']
        ).pack(side='left', padx=2)
        
        ModernButton(
            admin_buttons,
            text="⚙️ الإعدادات",
            command=self.show_settings_window,
            bg_color=COLORS['secondary'],
            fg_color=COLORS['primary']
        ).pack(side='left', padx=2)
    
    def update_products_display(self):
        """تحديث عرض المنتجات"""
        # مسح المنتجات الحالية
        for widget in self.products_scrollable_frame.winfo_children():
            widget.destroy()
        
        # فلترة المنتجات
        search_term = self.search_var.get().lower()
        if search_term == self.texts['search_placeholder'].lower():
            search_term = ""
        
        category_filter = self.category_filter_var.get()
        
        filtered_products = []
        for product in self.data['inventory']:
            # فلتر البحث
            if search_term and search_term not in product['name'].lower():
                continue
            
            # فلتر الفئة
            if category_filter != "الكل" and product.get('category', '') != category_filter:
                continue
            
            filtered_products.append(product)
        
        # عرض المنتجات في شبكة
        row = 0
        col = 0
        max_cols = 4
        
        for product in filtered_products:
            card = ProductCard(self.products_scrollable_frame, product, self.add_to_cart)
            card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # تكوين الأعمدة للتوسيط
        for i in range(max_cols):
            self.products_scrollable_frame.grid_columnconfigure(i, weight=1)
    
    def update_cart_display(self):
        """تحديث عرض السلة"""
        # مسح السلة الحالية
        for widget in self.cart_scrollable_frame.winfo_children():
            widget.destroy()
        
        total = 0
        
        for i, item in enumerate(self.cart):
            # إطار المنتج في السلة
            item_frame = tk.Frame(self.cart_scrollable_frame, bg=COLORS['light'], relief='flat', bd=1)
            item_frame.pack(fill='x', pady=2, padx=5)
            
            # اسم المنتج
            name_label = tk.Label(
                item_frame,
                text=item['name'][:25] + "..." if len(item['name']) > 25 else item['name'],
                font=("Cairo", 10, "bold"),
                bg=COLORS['light'],
                fg=COLORS['dark']
            )
            name_label.pack(anchor='w', padx=5, pady=2)
            
            # السعر والكمية
            details_frame = tk.Frame(item_frame, bg=COLORS['light'])
            details_frame.pack(fill='x', padx=5, pady=2)
            
            tk.Label(
                details_frame,
                text=f"{item['price']:.2f} × {item['quantity']}",
                font=("Cairo", 9),
                bg=COLORS['light'],
                fg=COLORS['dark']
            ).pack(side='left')
            
            tk.Label(
                details_frame,
                text=f"{item['total']:.2f} جنيه",
                font=("Cairo", 10, "bold"),
                bg=COLORS['light'],
                fg=COLORS['primary']
            ).pack(side='right')
            
            # أزرار التحكم
            controls_frame = tk.Frame(item_frame, bg=COLORS['light'])
            controls_frame.pack(fill='x', padx=5, pady=2)
            
            # زر تقليل الكمية
            tk.Button(
                controls_frame,
                text="-",
                font=("Cairo", 12, "bold"),
                bg=COLORS['danger'],
                fg=COLORS['white'],
                relief='flat',
                width=3,
                command=lambda idx=i: self.decrease_quantity(idx)
            ).pack(side='left', padx=2)
            
            # عرض الكمية
            tk.Label(
                controls_frame,
                text=str(item['quantity']),
                font=("Cairo", 10, "bold"),
                bg=COLORS['light'],
                fg=COLORS['dark'],
                width=3
            ).pack(side='left', padx=5)
            
            # زر زيادة الكمية
            tk.Button(
                controls_frame,
                text="+",
                font=("Cairo", 12, "bold"),
                bg=COLORS['success'],
                fg=COLORS['white'],
                relief='flat',
                width=3,
                command=lambda idx=i: self.increase_quantity(idx)
            ).pack(side='left', padx=2)
            
            # زر الحذف
            tk.Button(
                controls_frame,
                text="🗑️",
                font=("Arial", 10),
                bg=COLORS['danger'],
                fg=COLORS['white'],
                relief='flat',
                command=lambda idx=i: self.remove_from_cart(idx)
            ).pack(side='right', padx=2)
            
            total += item['total']
        
        # تحديث الإجمالي
        self.total_label.config(text=f"الإجمالي: {total:.2f} جنيه")
        
        # تفعيل/تعطيل زر الدفع
        if self.cart:
            self.pay_button.configure(state='normal')
        else:
            self.pay_button.configure(state='disabled')
    
    def add_to_cart(self, product):
        """إضافة منتج إلى السلة"""
        # البحث عن المنتج في السلة
        for item in self.cart:
            if item['product_id'] == product['id']:
                if item['quantity'] < product['stock']:
                    item['quantity'] += 1
                    item['total'] = item['price'] * item['quantity']
                    self.update_cart_display()
                    return
                else:
                    messagebox.showwarning("تحذير", "الكمية المطلوبة غير متوفرة في المخزون")
                    return
        
        # إضافة منتج جديد للسلة
        if product['stock'] > 0:
            cart_item = {
                'product_id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': 1,
                'total': product['price']
            }
            self.cart.append(cart_item)
            self.update_cart_display()
        else:
            messagebox.showwarning("تحذير", "هذا المنتج غير متوفر في المخزون")
    
    def increase_quantity(self, index):
        """زيادة كمية منتج في السلة"""
        item = self.cart[index]
        product = next((p for p in self.data['inventory'] if p['id'] == item['product_id']), None)
        
        if product and item['quantity'] < product['stock']:
            item['quantity'] += 1
            item['total'] = item['price'] * item['quantity']
            self.update_cart_display()
        else:
            messagebox.showwarning("تحذير", "الكمية المطلوبة غير متوفرة في المخزون")
    
    def decrease_quantity(self, index):
        """تقليل كمية منتج في السلة"""
        item = self.cart[index]
        if item['quantity'] > 1:
            item['quantity'] -= 1
            item['total'] = item['price'] * item['quantity']
            self.update_cart_display()
        else:
            self.remove_from_cart(index)
    
    def remove_from_cart(self, index):
        """حذف منتج من السلة"""
        del self.cart[index]
        self.update_cart_display()
    
    def clear_cart(self):
        """مسح السلة"""
        if self.cart and messagebox.askyesno("تأكيد", "هل تريد مسح جميع المنتجات من السلة؟"):
            self.cart.clear()
            self.update_cart_display()
    
    def show_payment_dialog(self):
        """عرض نافذة الدفع"""
        if not self.cart:
            messagebox.showwarning("تحذير", "السلة فارغة")
            return
        
        # نافذة الدفع
        payment_window = tk.Toplevel(self.root)
        payment_window.title("الدفع")
        payment_window.geometry("500x600")
        payment_window.configure(bg=COLORS['background'])
        payment_window.resizable(False, False)
        
        # توسيط النافذة
        payment_window.transient(self.root)
        payment_window.grab_set()
        
        # حساب الإجمالي
        subtotal = sum(item['total'] for item in self.cart)
        tax_rate = self.data.get('settings', {}).get('tax_rate', 0.14)
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount
        
        # العنوان
        header_frame = tk.Frame(payment_window, bg=COLORS['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="💳 إتمام الدفع",
            font=("Cairo", 20, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=20)
        
        # تفاصيل الفاتورة
        details_frame = tk.Frame(payment_window, bg=COLORS['white'], padx=30, pady=20)
        details_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            details_frame,
            text=f"المجموع الفرعي: {subtotal:.2f} جنيه",
            font=("Cairo", 12),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w', pady=2)
        
        tk.Label(
            details_frame,
            text=f"الضريبة ({tax_rate*100:.0f}%): {tax_amount:.2f} جنيه",
            font=("Cairo", 12),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w', pady=2)
        
        tk.Frame(details_frame, bg=COLORS['dark'], height=1).pack(fill='x', pady=10)
        
        tk.Label(
            details_frame,
            text=f"الإجمالي: {total:.2f} جنيه",
            font=("Cairo", 18, "bold"),
            bg=COLORS['white'],
            fg=COLORS['secondary']
        ).pack(anchor='w', pady=5)
        
        # معلومات العميل
        customer_frame = tk.LabelFrame(
            payment_window, 
            text="معلومات العميل", 
            font=("Cairo", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        customer_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            customer_frame,
            text="اسم العميل:",
            font=("Cairo", 10),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w', padx=10, pady=(10, 2))
        
        customer_entry = tk.Entry(
            customer_frame,
            font=("Cairo", 12),
            bg=COLORS['light'],
            relief='flat',
            bd=5
        )
        customer_entry.pack(fill='x', padx=10, pady=(0, 5), ipady=5)
        
        tk.Label(
            customer_frame,
            text="رقم الهاتف:",
            font=("Cairo", 10),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w', padx=10, pady=(5, 2))
        
        phone_entry = tk.Entry(
            customer_frame,
            font=("Cairo", 12),
            bg=COLORS['light'],
            relief='flat',
            bd=5
        )
        phone_entry.pack(fill='x', padx=10, pady=(0, 10), ipady=5)
        
        # طرق الدفع
        payment_frame = tk.LabelFrame(
            payment_window,
            text="طريقة الدفع",
            font=("Cairo", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        payment_frame.pack(fill='x', padx=20, pady=10)
        
        payment_method = tk.StringVar(value="cash")
        
        methods_frame = tk.Frame(payment_frame, bg=COLORS['white'])
        methods_frame.pack(pady=10)
        
        # أزرار طرق الدفع
        cash_btn = tk.Radiobutton(
            methods_frame,
            text="💵 " + self.texts['cash'],
            variable=payment_method,
            value="cash",
            font=("Cairo", 14, "bold"),
            bg=COLORS['success'],
            fg=COLORS['white'],
            selectcolor=COLORS['success'],
            relief='flat',
            padx=20,
            pady=10
        )
        cash_btn.pack(side='left', padx=5, fill='x', expand=True)
        
        card_btn = tk.Radiobutton(
            methods_frame,
            text="💳 " + self.texts['card'],
            variable=payment_method,
            value="card",
            font=("Cairo", 14, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white'],
            selectcolor=COLORS['primary'],
            relief='flat',
            padx=20,
            pady=10
        )
        card_btn.pack(side='left', padx=5, fill='x', expand=True)
        
        wallet_btn = tk.Radiobutton(
            methods_frame,
            text="📱 " + self.texts['wallet'],
            variable=payment_method,
            value="wallet",
            font=("Cairo", 14, "bold"),
            bg=COLORS['warning'],
            fg=COLORS['dark'],
            selectcolor=COLORS['warning'],
            relief='flat',
            padx=20,
            pady=10
        )
        wallet_btn.pack(side='left', padx=5, fill='x', expand=True)
        
        # أزرار الإجراءات
        actions_frame = tk.Frame(payment_window, bg=COLORS['background'])
        actions_frame.pack(fill='x', padx=20, pady=20)
        
        def complete_payment():
            customer_name = customer_entry.get().strip() or "عميل عادي"
            phone = phone_entry.get().strip()
            method = payment_method.get()
            
            # إنشاء الفاتورة
            sale = {
                'id': str(uuid.uuid4()),
                'invoice_number': len(self.data['sales']) + 1,
                'date': datetime.now().isoformat(),
                'items': self.cart.copy(),
                'subtotal': subtotal,
                'tax_amount': tax_amount,
                'total': total,
                'payment_method': method,
                'customer': customer_name,
                'phone': phone,
                'status': 'مكتمل',
                'cashier': self.current_user['name']
            }
            
            # إضافة البيع
            self.data['sales'].append(sale)
            
            # تحديث المخزون
            for cart_item in self.cart:
                for product in self.data['inventory']:
                    if product['id'] == cart_item['product_id']:
                        product['stock'] -= cart_item['quantity']
                        break
            
            # حفظ البيانات
            self.save_data()
            
            # مسح السلة
            self.cart.clear()
            self.update_cart_display()
            self.update_products_display()
            
            payment_window.destroy()
            
            # عرض خيارات الطباعة
            self.show_print_options(sale)
        
        ModernButton(
            actions_frame,
            text="✅ تأكيد الدفع",
            command=complete_payment,
            bg_color=COLORS['success'],
            fg_color=COLORS['white']
        ).pack(side='left', padx=5, fill='x', expand=True, ipady=10)
        
        ModernButton(
            actions_frame,
            text="❌ إلغاء",
            command=payment_window.destroy,
            bg_color=COLORS['danger'],
            fg_color=COLORS['white']
        ).pack(side='right', padx=5, fill='x', expand=True, ipady=10)
    
    def show_print_options(self, sale):
        """عرض خيارات الطباعة"""
        print_window = tk.Toplevel(self.root)
        print_window.title("طباعة الفاتورة")
        print_window.geometry("400x300")
        print_window.configure(bg=COLORS['background'])
        print_window.resizable(False, False)
        
        # توسيط النافذة
        print_window.transient(self.root)
        print_window.grab_set()
        
        tk.Label(
            print_window,
            text=f"✅ تم إتمام البيع بنجاح\nرقم الفاتورة: {sale['invoice_number']}",
            font=("Cairo", 14, "bold"),
            bg=COLORS['background'],
            fg=COLORS['success']
        ).pack(pady=30)
        
        ModernButton(
            print_window,
            text="📄 طباعة PDF",
            command=lambda: self.generate_invoice_pdf(sale),
            bg_color=COLORS['danger']
        ).pack(pady=5, padx=50, fill='x', ipady=8)
        
        ModernButton(
            print_window,
            text="🖼️ حفظ كصورة",
            command=lambda: self.generate_invoice_image(sale),
            bg_color=COLORS['success']
        ).pack(pady=5, padx=50, fill='x', ipady=8)
        
        ModernButton(
            print_window,
            text="📧 إرسال بالإيميل",
            command=lambda: self.send_invoice_email(sale),
            bg_color=COLORS['primary']
        ).pack(pady=5, padx=50, fill='x', ipady=8)
        
        ModernButton(
            print_window,
            text="إغلاق",
            command=print_window.destroy,
            bg_color=COLORS['dark']
        ).pack(pady=20, padx=50, fill='x', ipady=8)
    
    def generate_invoice_pdf(self, sale):
        """إنشاء فاتورة PDF"""
        try:
            filename = f"invoice_{sale['invoice_number']}_{sale['customer'].replace(' ', '_')}.pdf"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialname=filename
            )
            
            if not filepath:
                return
            
            c = canvas.Canvas(filepath, pagesize=A4)
            width, height = A4
            
            # الشعار والعنوان
            c.setFillColor(COLORS['primary'])
            c.rect(0, height-100, width, 100, fill=1)
            
            c.setFillColor(COLORS['secondary'])
            c.setFont("Helvetica-Bold", 24)
            c.drawString(50, height-50, "Book Bliss")
            
            c.setFillColor(COLORS['white'])
            c.setFont("Helvetica", 12)
            c.drawString(50, height-70, self.data['settings']['store_address'])
            c.drawString(50, height-85, f"Tel: {self.data['settings']['store_phone']}")
            
            # معلومات الفاتورة
            c.setFillColor(COLORS['dark'])
            c.setFont("Helvetica-Bold", 16)
            c.drawString(400, height-50, "INVOICE")
            
            c.setFont("Helvetica", 10)
            y = height - 130
            
            invoice_info = [
                f"Invoice Number: {sale['invoice_number']}",
                f"Date: {datetime.fromisoformat(sale['date']).strftime('%Y-%m-%d %H:%M')}",
                f"Customer: {sale['customer']}",
                f"Phone: {sale.get('phone', 'N/A')}",
                f"Payment Method: {sale['payment_method']}",
                f"Cashier: {sale['cashier']}"
            ]
            
            for info in invoice_info:
                c.drawString(50, y, info)
                y -= 15
            
            # جدول المنتجات
            y -= 30
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, "Product")
            c.drawString(250, y, "Qty")
            c.drawString(300, y, "Price")
            c.drawString(400, y, "Total")
            
            y -= 15
            c.line(50, y, 500, y)
            y -= 10
            
            c.setFont("Helvetica", 9)
            for item in sale['items']:
                c.drawString(50, y, item['name'][:30])
                c.drawString(250, y, str(item['quantity']))
                c.drawString(300, y, f"{item['price']:.2f}")
                c.drawString(400, y, f"{item['total']:.2f}")
                y -= 15
            
            # الإجماليات
            y -= 20
            c.line(50, y, 500, y)
            y -= 20
            
            c.setFont("Helvetica", 10)
            c.drawString(300, y, f"Subtotal: {sale['subtotal']:.2f} EGP")
            y -= 15
            c.drawString(300, y, f"Tax: {sale['tax_amount']:.2f} EGP")
            y -= 15
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(300, y, f"Total: {sale['total']:.2f} EGP")
            
            # شكر العميل
            y -= 40
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(50, y, "Thank you for your business!")
            c.drawString(50, y-15, "شكراً لتسوقكم معنا!")
            
            c.save()
            messagebox.showinfo("نجح", f"تم حفظ الفاتورة: {filepath}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في إنشاء PDF: {str(e)}")
    
    def generate_invoice_image(self, sale):
        """إنشاء فاتورة كصورة"""
        try:
            filename = f"invoice_{sale['invoice_number']}_{sale['customer'].replace(' ', '_')}.png"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialname=filename
            )
            
            if not filepath:
                return
            
            # إنشاء صورة
            img_width, img_height = 600, 800
            img = Image.new('RGB', (img_width, img_height), 'white')
            draw = ImageDraw.Draw(img)
            
            try:
                font_large = ImageFont.truetype("arial.ttf", 20)
                font_medium = ImageFont.truetype("arial.ttf", 14)
                font_small = ImageFont.truetype("arial.ttf", 12)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # الخلفية العلوية
            draw.rectangle([0, 0, img_width, 100], fill=COLORS['primary'])
            
            # الشعار
            draw.text((30, 30), "📚 Book Bliss", fill=COLORS['secondary'], font=font_large)
            draw.text((30, 60), self.data['settings']['store_address'], fill='white', font=font_small)
            
            y = 130
            
            # معلومات الفاتورة
            draw.text((30, y), "INVOICE / فاتورة", fill=COLORS['primary'], font=font_large)
            y += 40
            
            invoice_info = [
                f"Invoice Number: {sale['invoice_number']}",
                f"Date: {datetime.fromisoformat(sale['date']).strftime('%Y-%m-%d %H:%M')}",
                f"Customer: {sale['customer']}",
                f"Phone: {sale.get('phone', 'N/A')}",
                f"Payment: {sale['payment_method']}",
                f"Cashier: {sale['cashier']}"
            ]
            
            for info in invoice_info:
                draw.text((30, y), info, fill='black', font=font_medium)
                y += 20
            
            # جدول المنتجات
            y += 20
            draw.text((30, y), "Product", fill='black', font=font_medium)
            draw.text((250, y), "Qty", fill='black', font=font_medium)
            draw.text((320, y), "Price", fill='black', font=font_medium)
            draw.text((420, y), "Total", fill='black', font=font_medium)
            y += 25
            
            draw.line([(30, y), (550, y)], fill='black', width=2)
            y += 15
            
            for item in sale['items']:
                draw.text((30, y), item['name'][:25], fill='black', font=font_small)
                draw.text((250, y), str(item['quantity']), fill='black', font=font_small)
                draw.text((320, y), f"{item['price']:.2f}", fill='black', font=font_small)
                draw.text((420, y), f"{item['total']:.2f}", fill='black', font=font_small)
                y += 20
            
            # الإجماليات
            y += 20
            draw.line([(30, y), (550, y)], fill='black', width=2)
            y += 20
            
            draw.text((320, y), f"Subtotal: {sale['subtotal']:.2f} EGP", fill='black', font=font_medium)
            y += 20
            draw.text((320, y), f"Tax: {sale['tax_amount']:.2f} EGP", fill='black', font=font_medium)
            y += 25
            draw.text((320, y), f"Total: {sale['total']:.2f} EGP", fill=COLORS['primary'], font=font_large)
            
            # شكر العميل
            y += 50
            draw.text((30, y), "Thank you for your business!", fill=COLORS['success'], font=font_medium)
            draw.text((30, y+20), "شكراً لتسوقكم معنا!", fill=COLORS['success'], font=font_medium)
            
            img.save(filepath)
            messagebox.showinfo("نجح", f"تم حفظ الفاتورة: {filepath}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في إنشاء الصورة: {str(e)}")
    
    def send_invoice_email(self, sale):
        """إرسال الفاتورة بالإيميل (وهمي)"""
        messagebox.showinfo("قريباً", "ميزة الإرسال بالإيميل قيد التطوير")
    
    def on_search_change(self, *args):
        """تحديث البحث عند تغيير النص"""
        self.update_products_display()
    
    def scan_barcode(self):
        """مسح الباركود (وهمي)"""
        barcode = simpledialog.askstring("مسح الباركود", "أدخل رقم الباركود:")
        if barcode:
            # البحث عن المنتج بالباركود
            product = next((p for p in self.data['inventory'] if p.get('barcode') == barcode), None)
            if product:
                self.add_to_cart(product)
                messagebox.showinfo("نجح", f"تم إضافة {product['name']} إلى السلة")
            else:
                messagebox.showwarning("غير موجود", "المنتج غير موجود")
    
    def save_current_invoice(self):
        """حفظ الفاتورة الحالية"""
        if not self.cart:
            messagebox.showwarning("تحذير", "السلة فارغة")
            return
        
        # حفظ كمسودة
        draft = {
            'id': str(uuid.uuid4()),
            'date': datetime.now().isoformat(),
            'items': self.cart.copy(),
            'total': sum(item['total'] for item in self.cart),
            'status': 'مسودة',
            'cashier': self.current_user['name']
        }
        
        if 'drafts' not in self.data:
            self.data['drafts'] = []
        
        self.data['drafts'].append(draft)
        self.save_data()
        
        messagebox.showinfo("نجح", "تم حفظ الفاتورة كمسودة")
    
    def show_daily_report(self):
        """عرض التقرير اليومي"""
        today = datetime.now().date()
        today_sales = [s for s in self.data['sales'] 
                      if datetime.fromisoformat(s['date']).date() == today]
        
        total_sales = sum(s['total'] for s in today_sales)
        total_items = sum(len(s['items']) for s in today_sales)
        
        report_text = f"""
📊 التقرير اليومي - {today.strftime('%Y-%m-%d')}

💰 إجمالي المبيعات: {total_sales:.2f} جنيه
🛒 عدد الفواتير: {len(today_sales)}
📦 عدد المنتجات المباعة: {total_items}

💵 المبيعات النقدية: {sum(s['total'] for s in today_sales if s['payment_method'] == 'cash'):.2f} جنيه
💳 مبيعات البطاقات: {sum(s['total'] for s in today_sales if s['payment_method'] == 'card'):.2f} جنيه
📱 مبيعات المحفظة: {sum(s['total'] for s in today_sales if s['payment_method'] == 'wallet'):.2f} جنيه
        """
        
        messagebox.showinfo("التقرير اليومي", report_text)
    
    def show_inventory_window(self):
        """عرض نافذة إدارة المخزون"""
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("إدارة المخزون")
        inventory_window.geometry("1000x700")
        inventory_window.configure(bg=COLORS['background'])
        
        # العنوان
        header_frame = tk.Frame(inventory_window, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📦 إدارة المخزون",
            font=("Cairo", 18, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        # أزرار الإدارة
        buttons_frame = tk.Frame(inventory_window, bg=COLORS['background'])
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        ModernButton(
            buttons_frame,
            text="➕ إضافة منتج",
            command=self.add_product_dialog,
            bg_color=COLORS['success']
        ).pack(side='left', padx=5)
        
        ModernButton(
            buttons_frame,
            text="📝 تعديل منتج",
            command=lambda: self.edit_product_dialog(inventory_tree),
            bg_color=COLORS['warning'],
            fg_color=COLORS['dark']
        ).pack(side='left', padx=5)
        
        ModernButton(
            buttons_frame,
            text="🗑️ حذف منتج",
            command=lambda: self.delete_product_dialog(inventory_tree),
            bg_color=COLORS['danger']
        ).pack(side='left', padx=5)
        
        ModernButton(
            buttons_frame,
            text="🏷️ إدارة الفئات",
            command=self.manage_categories_dialog,
            bg_color=COLORS['primary']
        ).pack(side='left', padx=5)
        
        # جدول المنتجات
        columns = ('ID', 'اسم المنتج', 'الفئة', 'السعر', 'المخزون', 'الحالة', 'الباركود')
        inventory_tree = ttk.Treeview(inventory_window, columns=columns, show='headings')
        
        for col in columns:
            inventory_tree.heading(col, text=col)
            inventory_tree.column(col, width=120, anchor='center')
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(inventory_window, orient='vertical', command=inventory_tree.yview)
        inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        inventory_tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 20), pady=10)
        
        # تحديث البيانات
        self.update_inventory_tree(inventory_tree)
    
    def update_inventory_tree(self, tree):
        """تحديث جدول المخزون"""
        for item in tree.get_children():
            tree.delete(item)
        
        for product in self.data['inventory']:
            status = "متوفر" if product['stock'] > 10 else "قليل" if product['stock'] > 0 else "نفد"
            tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                product.get('category', 'غير محدد'),
                f"{product['price']:.2f}",
                product['stock'],
                status,
                product.get('barcode', 'غير محدد')
            ))
    
    def add_product_dialog(self):
        """نافذة إضافة منتج"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة منتج جديد")
        dialog.geometry("500x600")
        dialog.configure(bg=COLORS['background'])
        dialog.resizable(False, False)
        
        # توسيط النافذة
        dialog.transient(self.root)
        dialog.grab_set()
        
        # العنوان
        tk.Label(
            dialog,
            text="➕ إضافة منتج جديد",
            font=("Cairo", 16, "bold"),
            bg=COLORS['background'],
            fg=COLORS['primary']
        ).pack(pady=20)
        
        # الحقول
        fields_frame = tk.Frame(dialog, bg=COLORS['white'], padx=30, pady=20)
        fields_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # اسم المنتج
        tk.Label(fields_frame, text="اسم المنتج:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        name_entry = tk.Entry(fields_frame, font=("Cairo", 12), bg=COLORS['light'], 
                             relief='flat', bd=5)
        name_entry.pack(fill='x', pady=(0, 15), ipady=5)
        
        # الفئة
        tk.Label(fields_frame, text="الفئة:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(fields_frame, textvariable=category_var, 
                                     values=self.data['product_categories'], 
                                     font=("Cairo", 12))
        category_combo.pack(fill='x', pady=(0, 15), ipady=5)
        
        # السعر
        tk.Label(fields_frame, text="السعر:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        price_entry = tk.Entry(fields_frame, font=("Cairo", 12), bg=COLORS['light'], 
                              relief='flat', bd=5)
        price_entry.pack(fill='x', pady=(0, 15), ipady=5)
        
        # الكمية
        tk.Label(fields_frame, text="الكمية:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        stock_entry = tk.Entry(fields_frame, font=("Cairo", 12), bg=COLORS['light'], 
                              relief='flat', bd=5)
        stock_entry.pack(fill='x', pady=(0, 15), ipady=5)
        
        # الباركود
        tk.Label(fields_frame, text="الباركود:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        barcode_entry = tk.Entry(fields_frame, font=("Cairo", 12), bg=COLORS['light'], 
                                relief='flat', bd=5)
        barcode_entry.pack(fill='x', pady=(0, 15), ipady=5)
        
        # الوصف
        tk.Label(fields_frame, text="الوصف:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        description_text = tk.Text(fields_frame, font=("Cairo", 10), bg=COLORS['light'], 
                                  relief='flat', bd=5, height=4)
        description_text.pack(fill='x', pady=(0, 15))
        
        # أزرار الإجراءات
        actions_frame = tk.Frame(dialog, bg=COLORS['background'])
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        def save_product():
            try:
                name = name_entry.get().strip()
                category = category_var.get()
                price = float(price_entry.get())
                stock = int(stock_entry.get())
                barcode = barcode_entry.get().strip()
                description = description_text.get(1.0, tk.END).strip()
                
                if not name:
                    raise ValueError("اسم المنتج مطلوب")
                if price <= 0:
                    raise ValueError("السعر يجب أن يكون أكبر من صفر")
                if stock < 0:
                    raise ValueError("الكمية لا يمكن أن تكون سالبة")
                
                # التحقق من عدم تكرار الباركود
                if barcode and any(p.get('barcode') == barcode for p in self.data['inventory']):
                    raise ValueError("الباركود موجود بالفعل")
                
                # إنشاء المنتج
                product = {
                    'id': max([p['id'] for p in self.data['inventory']], default=0) + 1,
                    'name': name,
                    'category': category,
                    'price': price,
                    'stock': stock,
                    'barcode': barcode,
                    'description': description,
                    'created_date': datetime.now().isoformat()
                }
                
                self.data['inventory'].append(product)
                self.save_data()
                self.update_products_display()
                
                dialog.destroy()
                messagebox.showinfo("نجح", "تم إضافة المنتج بنجاح")
                
            except ValueError as e:
                messagebox.showerror("خطأ", str(e))
        
        ModernButton(
            actions_frame,
            text="💾 حفظ",
            command=save_product,
            bg_color=COLORS['success']
        ).pack(side='left', padx=5, fill='x', expand=True, ipady=8)
        
        ModernButton(
            actions_frame,
            text="❌ إلغاء",
            command=dialog.destroy,
            bg_color=COLORS['danger']
        ).pack(side='right', padx=5, fill='x', expand=True, ipady=8)
    
    def edit_product_dialog(self, tree):
        """نافذة تعديل منتج"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للتعديل")
            return
        
        item_values = tree.item(selection[0])['values']
        product_id = item_values[0]
        product = next((p for p in self.data['inventory'] if p['id'] == product_id), None)
        
        if not product:
            messagebox.showerror("خطأ", "المنتج غير موجود")
            return
        
        # نفس نافذة الإضافة مع القيم الحالية
        dialog = tk.Toplevel(self.root)
        dialog.title("تعديل منتج")
        dialog.geometry("500x600")
        dialog.configure(bg=COLORS['background'])
        dialog.resizable(False, False)
        
        # توسيط النافذة
        dialog.transient(self.root)
        dialog.grab_set()
        
        # العنوان
        tk.Label(
            dialog,
            text="📝 تعديل منتج",
            font=("Cairo", 16, "bold"),
            bg=COLORS['background'],
            fg=COLORS['primary']
        ).pack(pady=20)
        
        # الحقول مع القيم الحالية
        fields_frame = tk.Frame(dialog, bg=COLORS['white'], padx=30, pady=20)
        fields_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # اسم المنتج
        tk.Label(fields_frame, text="اسم المنتج:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        name_entry = tk.Entry(fields_frame, font=("Cairo", 12), bg=COLORS['light'], 
                             relief='flat', bd=5)
        name_entry.pack(fill='x', pady=(0, 15), ipady=5)
        name_entry.insert(0, product['name'])
        
        # الفئة
        tk.Label(fields_frame, text="الفئة:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        category_var = tk.StringVar(value=product.get('category', ''))
        category_combo = ttk.Combobox(fields_frame, textvariable=category_var, 
                                     values=self.data['product_categories'], 
                                     font=("Cairo", 12))
        category_combo.pack(fill='x', pady=(0, 15), ipady=5)
        
        # السعر
        tk.Label(fields_frame, text="السعر:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        price_entry = tk.Entry(fields_frame, font=("Cairo", 12), bg=COLORS['light'], 
                              relief='flat', bd=5)
        price_entry.pack(fill='x', pady=(0, 15), ipady=5)
        price_entry.insert(0, str(product['price']))
        
        # الكمية
        tk.Label(fields_frame, text="الكمية:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        stock_entry = tk.Entry(fields_frame, font=("Cairo", 12), bg=COLORS['light'], 
                              relief='flat', bd=5)
        stock_entry.pack(fill='x', pady=(0, 15), ipady=5)
        stock_entry.insert(0, str(product['stock']))
        
        # الباركود
        tk.Label(fields_frame, text="الباركود:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        barcode_entry = tk.Entry(fields_frame, font=("Cairo", 12), bg=COLORS['light'], 
                                relief='flat', bd=5)
        barcode_entry.pack(fill='x', pady=(0, 15), ipady=5)
        barcode_entry.insert(0, product.get('barcode', ''))
        
        # الوصف
        tk.Label(fields_frame, text="الوصف:", font=("Cairo", 12, "bold"), 
                bg=COLORS['white'], fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        description_text = tk.Text(fields_frame, font=("Cairo", 10), bg=COLORS['light'], 
                                  relief='flat', bd=5, height=4)
        description_text.pack(fill='x', pady=(0, 15))
        description_text.insert(1.0, product.get('description', ''))
        
        # أزرار الإجراءات
        actions_frame = tk.Frame(dialog, bg=COLORS['background'])
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        def update_product():
            try:
                name = name_entry.get().strip()
                category = category_var.get()
                price = float(price_entry.get())
                stock = int(stock_entry.get())
                barcode = barcode_entry.get().strip()
                description = description_text.get(1.0, tk.END).strip()
                
                if not name:
                    raise ValueError("اسم المنتج مطلوب")
                if price <= 0:
                    raise ValueError("السعر يجب أن يكون أكبر من صفر")
                if stock < 0:
                    raise ValueError("الكمية لا يمكن أن تكون سالبة")
                
                # التحقق من عدم تكرار الباركود
                if barcode and any(p.get('barcode') == barcode and p['id'] != product['id'] 
                                 for p in self.data['inventory']):
                    raise ValueError("الباركود موجود بالفعل")
                
                # تحديث المنتج
                product['name'] = name
                product['category'] = category
                product['price'] = price
                product['stock'] = stock
                product['barcode'] = barcode
                product['description'] = description
                product['updated_date'] = datetime.now().isoformat()
                
                self.save_data()
                self.update_products_display()
                self.update_inventory_tree(tree)
                
                dialog.destroy()
                messagebox.showinfo("نجح", "تم تحديث المنتج بنجاح")
                
            except ValueError as e:
                messagebox.showerror("خطأ", str(e))
        
        ModernButton(
            actions_frame,
            text="💾 حفظ التغييرات",
            command=update_product,
            bg_color=COLORS['success']
        ).pack(side='left', padx=5, fill='x', expand=True, ipady=8)
        
        ModernButton(
            actions_frame,
            text="❌ إلغاء",
            command=dialog.destroy,
            bg_color=COLORS['danger']
        ).pack(side='right', padx=5, fill='x', expand=True, ipady=8)
    
    def delete_product_dialog(self, tree):
        """حذف منتج"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للحذف")
            return
        
        item_values = tree.item(selection[0])['values']
        product_id = item_values[0]
        product = next((p for p in self.data['inventory'] if p['id'] == product_id), None)
        
        if not product:
            messagebox.showerror("خطأ", "المنتج غير موجود")
            return
        
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف المنتج '{product['name']}'؟"):
            self.data['inventory'].remove(product)
            self.save_data()
            self.update_products_display()
            self.update_inventory_tree(tree)
            messagebox.showinfo("نجح", "تم حذف المنتج بنجاح")
    
    def manage_categories_dialog(self):
        """إدارة فئات المنتجات"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إدارة فئات المنتجات")
        dialog.geometry("400x500")
        dialog.configure(bg=COLORS['background'])
        
        # توسيط النافذة
        dialog.transient(self.root)
        dialog.grab_set()
        
        # العنوان
        tk.Label(
            dialog,
            text="🏷️ إدارة فئات المنتجات",
            font=("Cairo", 16, "bold"),
            bg=COLORS['background'],
            fg=COLORS['primary']
        ).pack(pady=20)
        
        # قائمة الفئات
        categories_frame = tk.Frame(dialog, bg=COLORS['white'])
        categories_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        categories_listbox = tk.Listbox(categories_frame, font=("Cairo", 12), 
                                       bg=COLORS['light'])
        for category in self.data['product_categories']:
            categories_listbox.insert(tk.END, category)
        categories_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        # إضافة فئة جديدة
        add_frame = tk.Frame(dialog, bg=COLORS['background'])
        add_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            add_frame,
            text="فئة جديدة:",
            font=("Cairo", 12, "bold"),
            bg=COLORS['background'],
            fg=COLORS['dark']
        ).pack(anchor='w')
        
        new_category_entry = tk.Entry(add_frame, font=("Cairo", 12), bg=COLORS['light'], 
                                     relief='flat', bd=5)
        new_category_entry.pack(fill='x', pady=5, ipady=5)
        
        def add_category():
            new_category = new_category_entry.get().strip()
            if new_category and new_category not in self.data['product_categories']:
                self.data['product_categories'].append(new_category)
                categories_listbox.insert(tk.END, new_category)
                new_category_entry.delete(0, tk.END)
                self.save_data()
                messagebox.showinfo("نجح", "تم إضافة الفئة بنجاح")
            else:
                messagebox.showwarning("تحذير", "الفئة موجودة بالفعل أو فارغة")
        
        def delete_category():
            selection = categories_listbox.curselection()
            if selection:
                category_index = selection[0]
                category_name = self.data['product_categories'][category_index]
                
                # التحقق من وجود منتجات بهذه الفئة
                products_with_category = [p for p in self.data['inventory'] 
                                        if p.get('category') == category_name]
                if products_with_category:
                    messagebox.showerror("خطأ", 
                                       f"لا يمكن حذف الفئة. يوجد {len(products_with_category)} منتج بهذه الفئة")
                    return
                
                if messagebox.askyesno("تأكيد", f"هل تريد حذف الفئة '{category_name}'؟"):
                    del self.data['product_categories'][category_index]
                    categories_listbox.delete(category_index)
                    self.save_data()
                    messagebox.showinfo("نجح", "تم حذف الفئة بنجاح")
        
        # أزرار الإجراءات
        actions_frame = tk.Frame(dialog, bg=COLORS['background'])
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        ModernButton(
            actions_frame,
            text="➕ إضافة",
            command=add_category,
            bg_color=COLORS['success']
        ).pack(side='left', padx=5, fill='x', expand=True)
        
        ModernButton(
            actions_frame,
            text="🗑️ حذف المحدد",
            command=delete_category,
            bg_color=COLORS['danger']
        ).pack(side='right', padx=5, fill='x', expand=True)
    
    def show_reports_window(self):
        """عرض نافذة التقارير"""
        reports_window = tk.Toplevel(self.root)
        reports_window.title("التقارير والإحصائيات")
        reports_window.geometry("1200x800")
        reports_window.configure(bg=COLORS['background'])
        
        # العنوان
        header_frame = tk.Frame(reports_window, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📊 التقارير والإحصائيات",
            font=("Cairo", 18, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        # إحصائيات سريعة
        stats_frame = tk.Frame(reports_window, bg=COLORS['background'])
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # حساب الإحصائيات
        total_sales = sum(sale['total'] for sale in self.data['sales'])
        total_expenses = sum(expense['amount'] for expense in self.data['expenses'])
        profit = total_sales - total_expenses
        
        # بطاقات الإحصائيات
        self.create_stat_card(stats_frame, "إجمالي المبيعات", f"{total_sales:.2f} جنيه", COLORS['success'])
        self.create_stat_card(stats_frame, "إجمالي المصروفات", f"{total_expenses:.2f} جنيه", COLORS['danger'])
        self.create_stat_card(stats_frame, "صافي الربح", f"{profit:.2f} جنيه", COLORS['primary'])
        self.create_stat_card(stats_frame, "عدد المنتجات", str(len(self.data['inventory'])), COLORS['warning'])
        
        # تقارير مفصلة
        reports_frame = tk.Frame(reports_window, bg=COLORS['background'])
        reports_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # أزرار التقارير
        buttons_frame = tk.Frame(reports_frame, bg=COLORS['background'])
        buttons_frame.pack(fill='x', pady=10)
        
        ModernButton(
            buttons_frame,
            text="📈 تقرير المبيعات اليومية",
            command=self.daily_sales_report,
            bg_color=COLORS['primary']
        ).pack(side='left', padx=5)
        
        ModernButton(
            buttons_frame,
            text="🏆 المنتجات الأكثر مبيعاً",
            command=self.top_products_report,
            bg_color=COLORS['success']
        ).pack(side='left', padx=5)
        
        ModernButton(
            buttons_frame,
            text="⚠️ المخزون المنخفض",
            command=self.low_stock_report,
            bg_color=COLORS['danger']
        ).pack(side='left', padx=5)
        
        ModernButton(
            buttons_frame,
            text="📋 جميع المبيعات",
            command=self.show_all_sales_window,
            bg_color=COLORS['warning'],
            fg_color=COLORS['dark']
        ).pack(side='left', padx=5)
        
        # منطقة عرض التقارير
        self.reports_display = tk.Text(
            reports_frame,
            font=("Cairo", 11),
            bg=COLORS['white'],
            fg=COLORS['dark'],
            relief='flat',
            bd=10,
            wrap=tk.WORD
        )
        self.reports_display.pack(fill='both', expand=True, pady=10)
        
        # عرض تقرير افتراضي
        self.show_summary_report()
    
    def create_stat_card(self, parent, title, value, color):
        """إنشاء بطاقة إحصائية"""
        card_frame = tk.Frame(parent, bg=color, relief='flat', bd=0)
        card_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            card_frame,
            text=title,
            font=("Cairo", 12, "bold"),
            bg=color,
            fg=COLORS['white']
        ).pack(pady=(15, 5))
        
        tk.Label(
            card_frame,
            text=value,
            font=("Cairo", 16, "bold"),
            bg=color,
            fg=COLORS['white']
        ).pack(pady=(0, 15))
    
    def show_summary_report(self):
        """عرض تقرير ملخص"""
        today = datetime.now().date()
        this_month = datetime.now().replace(day=1).date()
        
        # مبيعات اليوم
        today_sales = [s for s in self.data['sales'] 
                      if datetime.fromisoformat(s['date']).date() == today]
        today_total = sum(s['total'] for s in today_sales)
        
        # مبيعات الشهر
        month_sales = [s for s in self.data['sales'] 
                      if datetime.fromisoformat(s['date']).date() >= this_month]
        month_total = sum(s['total'] for s in month_sales)
        
        # أكثر المنتجات مبيعاً
        product_sales = {}
        for sale in self.data['sales']:
            for item in sale['items']:
                if item['name'] in product_sales:
                    product_sales[item['name']] += item['quantity']
                else:
                    product_sales[item['name']] = item['quantity']
        
        top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # المخزون المنخفض
        low_stock = [p for p in self.data['inventory'] if p['stock'] <= 5]
        
        report = f"""
📊 تقرير ملخص - {datetime.now().strftime('%Y-%m-%d %H:%M')}

{'='*50}

📈 مبيعات اليوم ({today.strftime('%Y-%m-%d')}):
   💰 الإجمالي: {today_total:.2f} جنيه
   🛒 عدد الفواتير: {len(today_sales)}

📈 مبيعات الشهر الحالي:
   💰 الإجمالي: {month_total:.2f} جنيه
   🛒 عدد الفواتير: {len(month_sales)}

🏆 أكثر المنتجات مبيعاً:
"""
        
        for i, (product, quantity) in enumerate(top_products, 1):
            report += f"   {i}. {product}: {quantity} قطعة\n"
        
        report += f"""
⚠️ تنبيهات المخزون:
   🔴 منتجات بمخزون منخفض: {len(low_stock)}
"""
        
        if low_stock:
            report += "\n   المنتجات:\n"
            for product in low_stock[:10]:  # أول 10 منتجات
                report += f"   • {product['name']}: {product['stock']} قطعة\n"
        
        report += f"""
📦 إحصائيات المخزون:
   📚 إجمالي المنتجات: {len(self.data['inventory'])}
   🟢 متوفر (>10): {len([p for p in self.data['inventory'] if p['stock'] > 10])}
   🟡 قليل (1-10): {len([p for p in self.data['inventory'] if 0 < p['stock'] <= 10])}
   🔴 نفد (0): {len([p for p in self.data['inventory'] if p['stock'] == 0])}

💰 الوضع المالي:
   📈 إجمالي المبيعات: {sum(s['total'] for s in self.data['sales']):.2f} جنيه
   📉 إجمالي المصروفات: {sum(e['amount'] for e in self.data['expenses']):.2f} جنيه
   💵 صافي الربح: {sum(s['total'] for s in self.data['sales']) - sum(e['amount'] for e in self.data['expenses']):.2f} جنيه
        """
        
        self.reports_display.delete(1.0, tk.END)
        self.reports_display.insert(1.0, report)
    
    def daily_sales_report(self):
        """تقرير المبيعات اليومية"""
        today = datetime.now().date()
        today_sales = [s for s in self.data['sales'] 
                      if datetime.fromisoformat(s['date']).date() == today]
        
        report = f"""
📈 تقرير المبيعات اليومية - {today.strftime('%Y-%m-%d')}

{'='*60}

📊 ملخص المبيعات:
   💰 إجمالي المبيعات: {sum(s['total'] for s in today_sales):.2f} جنيه
   🛒 عدد الفواتير: {len(today_sales)}
   📦 إجمالي المنتجات المباعة: {sum(len(s['items']) for s in today_sales)}

💳 تفصيل طرق الدفع:
   💵 نقدي: {sum(s['total'] for s in today_sales if s['payment_method'] == 'cash'):.2f} جنيه
   💳 بطاقة: {sum(s['total'] for s in today_sales if s['payment_method'] == 'card'):.2f} جنيه
   📱 محفظة: {sum(s['total'] for s in today_sales if s['payment_method'] == 'wallet'):.2f} جنيه

📋 تفاصيل الفواتير:
"""
        
        for sale in today_sales:
            sale_time = datetime.fromisoformat(sale['date']).strftime('%H:%M')
            report += f"""
   🧾 فاتورة #{sale['invoice_number']} - {sale_time}
      👤 العميل: {sale['customer']}
      💰 المبلغ: {sale['total']:.2f} جنيه
      💳 الدفع: {sale['payment_method']}
      👨‍💼 الكاشير: {sale['cashier']}
"""
        
        if not today_sales:
            report += "\n   لا توجد مبيعات اليوم."
        
        self.reports_display.delete(1.0, tk.END)
        self.reports_display.insert(1.0, report)
    
    def top_products_report(self):
        """تقرير المنتجات الأكثر مبيعاً"""
        product_sales = {}
        product_revenue = {}
        
        for sale in self.data['sales']:
            for item in sale['items']:
                name = item['name']
                quantity = item['quantity']
                revenue = item['total']
                
                if name in product_sales:
                    product_sales[name] += quantity
                    product_revenue[name] += revenue
                else:
                    product_sales[name] = quantity
                    product_revenue[name] = revenue
        
        # ترتيب حسب الكمية
        top_by_quantity = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
        # ترتيب حسب الإيرادات
        top_by_revenue = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
        
        report = f"""
🏆 تقرير المنتجات الأكثر مبيعاً

{'='*60}

📦 أكثر المنتجات مبيعاً (حسب الكمية):
"""
        
        for i, (product, quantity) in enumerate(top_by_quantity[:10], 1):
            revenue = product_revenue.get(product, 0)
            report += f"   {i:2d}. {product}\n"
            report += f"       📦 الكمية: {quantity} قطعة\n"
            report += f"       💰 الإيرادات: {revenue:.2f} جنيه\n\n"
        
        report += "\n💰 أكثر المنتجات إيراداً:\n"
        
        for i, (product, revenue) in enumerate(top_by_revenue[:10], 1):
            quantity = product_sales.get(product, 0)
            report += f"   {i:2d}. {product}\n"
            report += f"       💰 الإيرادات: {revenue:.2f} جنيه\n"
            report += f"       📦 الكمية: {quantity} قطعة\n\n"
        
        self.reports_display.delete(1.0, tk.END)
        self.reports_display.insert(1.0, report)
    
    def low_stock_report(self):
        """تقرير المخزون المنخفض"""
        threshold = self.data.get('settings', {}).get('low_stock_threshold', 5)
        low_stock = [p for p in self.data['inventory'] if p['stock'] <= threshold]
        out_of_stock = [p for p in self.data['inventory'] if p['stock'] == 0]
        
        report = f"""
⚠️ تقرير المخزون المنخفض

{'='*60}

📊 ملخص:
   🔴 منتجات نفدت: {len(out_of_stock)}
   🟡 منتجات بمخزون منخفض: {len(low_stock) - len(out_of_stock)}
   📏 حد التنبيه: {threshold} قطع

🔴 منتجات نفدت من المخزون:
"""
        
        if out_of_stock:
            for product in out_of_stock:
                report += f"   • {product['name']}\n"
                report += f"     🏷️ الفئة: {product.get('category', 'غير محدد')}\n"
                report += f"     💰 السعر: {product['price']:.2f} جنيه\n\n"
        else:
            report += "   ✅ لا توجد منتجات نفدت من المخزون\n\n"
        
        report += "🟡 منتجات بمخزون منخفض:\n"
        
        low_but_available = [p for p in low_stock if p['stock'] > 0]
        if low_but_available:
            for product in low_but_available:
                report += f"   • {product['name']}\n"
                report += f"     📦 المخزون: {product['stock']} قطعة\n"
                report += f"     🏷️ الفئة: {product.get('category', 'غير محدد')}\n"
                report += f"     💰 السعر: {product['price']:.2f} جنيه\n\n"
        else:
            report += "   ✅ جميع المنتجات المتوفرة بمخزون كافي\n"
        
        report += f"""
💡 توصيات:
   • إعادة تموين المنتجات النافدة
   • طلب كميات إضافية للمنتجات ذات المخزون المنخفض
   • مراجعة حد التنبيه الحالي ({threshold} قطع)
   • تحديث أسعار المنتجات حسب الحاجة
        """
        
        self.reports_display.delete(1.0, tk.END)
        self.reports_display.insert(1.0, report)
    
    def show_all_sales_window(self):
        """عرض نافذة جميع المبيعات"""
        sales_window = tk.Toplevel(self.root)
        sales_window.title("جميع المبيعات")
        sales_window.geometry("1200x700")
        sales_window.configure(bg=COLORS['background'])
        
        # العنوان
        header_frame = tk.Frame(sales_window, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📋 جميع المبيعات",
            font=("Cairo", 18, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        # فلاتر البحث
        filters_frame = tk.Frame(sales_window, bg=COLORS['background'])
        filters_frame.pack(fill='x', padx=20, pady=10)
        
        # فلتر طريقة الدفع
        tk.Label(
            filters_frame,
            text="طريقة الدفع:",
            font=("Cairo", 10, "bold"),
            bg=COLORS['background'],
            fg=COLORS['dark']
        ).pack(side='left', padx=(0, 5))
        
        payment_filter_var = tk.StringVar(value="الكل")
        payment_filter = ttk.Combobox(
            filters_frame,
            textvariable=payment_filter_var,
            values=["الكل", "cash", "card", "wallet"],
            font=("Cairo", 10),
            state="readonly",
            width=10
        )
        payment_filter.pack(side='left', padx=5)
        
        # فلتر التاريخ
        tk.Label(
            filters_frame,
            text="التاريخ:",
            font=("Cairo", 10, "bold"),
            bg=COLORS['background'],
            fg=COLORS['dark']
        ).pack(side='left', padx=(20, 5))
        
        date_filter_var = tk.StringVar(value="الكل")
        date_filter = ttk.Combobox(
            filters_frame,
            textvariable=date_filter_var,
            values=["الكل", "اليوم", "أمس", "هذا الأسبوع", "هذا الشهر"],
            font=("Cairo", 10),
            state="readonly",
            width=15
        )
        date_filter.pack(side='left', padx=5)
        
        # جدول المبيعات
        columns = ('رقم الفاتورة', 'التاريخ', 'الوقت', 'العميل', 'الإجمالي', 'طريقة الدفع', 'الكاشير')
        sales_tree = ttk.Treeview(sales_window, columns=columns, show='headings')
        
        for col in columns:
            sales_tree.heading(col, text=col)
            sales_tree.column(col, width=120, anchor='center')
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(sales_window, orient='vertical', command=sales_tree.yview)
        sales_tree.configure(yscrollcommand=scrollbar.set)
        
        sales_tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 20), pady=10)
        
        # أزرار العمليات
        actions_frame = tk.Frame(sales_window, bg=COLORS['background'])
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        ModernButton(
            actions_frame,
            text="👁️ عرض التفاصيل",
            command=lambda: self.view_sale_details(sales_tree),
            bg_color=COLORS['primary']
        ).pack(side='left', padx=5)
        
        ModernButton(
            actions_frame,
            text="📄 طباعة PDF",
            command=lambda: self.print_selected_invoice(sales_tree),
            bg_color=COLORS['danger']
        ).pack(side='left', padx=5)
        
        ModernButton(
            actions_frame,
            text="🖼️ حفظ كصورة",
            command=lambda: self.save_selected_invoice_image(sales_tree),
            bg_color=COLORS['success']
        ).pack(side='left', padx=5)
        
        # إجمالي المبيعات
        total_sales = sum(sale['total'] for sale in self.data['sales'])
        tk.Label(
            actions_frame,
            text=f"إجمالي المبيعات: {total_sales:.2f} جنيه",
            font=("Cairo", 14, "bold"),
            bg=COLORS['background'],
            fg=COLORS['success']
        ).pack(side='right', padx=20)
        
        # تحديث البيانات
        def update_sales_tree():
            # مسح البيانات الحالية
            for item in sales_tree.get_children():
                sales_tree.delete(item)
            
            # فلترة البيانات
            filtered_sales = self.data['sales'].copy()
            
            # فلتر طريقة الدفع
            payment_method = payment_filter_var.get()
            if payment_method != "الكل":
                filtered_sales = [s for s in filtered_sales if s['payment_method'] == payment_method]
            
            # فلتر التاريخ
            date_filter_value = date_filter_var.get()
            if date_filter_value != "الكل":
                today = datetime.now().date()
                if date_filter_value == "اليوم":
                    filtered_sales = [s for s in filtered_sales 
                                    if datetime.fromisoformat(s['date']).date() == today]
                elif date_filter_value == "أمس":
                    yesterday = today - timedelta(days=1)
                    filtered_sales = [s for s in filtered_sales 
                                    if datetime.fromisoformat(s['date']).date() == yesterday]
                elif date_filter_value == "هذا الأسبوع":
                    week_start = today - timedelta(days=today.weekday())
                    filtered_sales = [s for s in filtered_sales 
                                    if datetime.fromisoformat(s['date']).date() >= week_start]
                elif date_filter_value == "هذا الشهر":
                    month_start = today.replace(day=1)
                    filtered_sales = [s for s in filtered_sales 
                                    if datetime.fromisoformat(s['date']).date() >= month_start]
            
            # إضافة البيانات المفلترة
            for sale in filtered_sales:
                sale_date = datetime.fromisoformat(sale['date'])
                sales_tree.insert('', 'end', values=(
                    sale.get('invoice_number', sale['id'][:8]),
                    sale_date.strftime('%Y-%m-%d'),
                    sale_date.strftime('%H:%M'),
                    sale['customer'],
                    f"{sale['total']:.2f}",
                    sale['payment_method'],
                    sale.get('cashier', 'غير محدد')
                ))
        
        # ربط الفلاتر بالتحديث
        payment_filter.bind('<<ComboboxSelected>>', lambda e: update_sales_tree())
        date_filter.bind('<<ComboboxSelected>>', lambda e: update_sales_tree())
        
        # تحديث أولي
        update_sales_tree()
    
    def view_sale_details(self, tree):
        """عرض تفاصيل البيع"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار فاتورة")
            return
        
        item_values = tree.item(selection[0])['values']
        invoice_number = item_values[0]
        
        # البحث عن البيع
        sale = next((s for s in self.data['sales'] 
                    if str(s.get('invoice_number', s['id'][:8])) == str(invoice_number)), None)
        
        if not sale:
            messagebox.showerror("خطأ", "الفاتورة غير موجودة")
            return
        
        # نافذة التفاصيل
        details_window = tk.Toplevel(self.root)
        details_window.title(f"تفاصيل الفاتورة #{invoice_number}")
        details_window.geometry("600x700")
        details_window.configure(bg=COLORS['background'])
        
        # العنوان
        header_frame = tk.Frame(details_window, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"🧾 فاتورة #{invoice_number}",
            font=("Cairo", 16, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        # معلومات الفاتورة
        info_frame = tk.Frame(details_window, bg=COLORS['white'], padx=20, pady=15)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        sale_date = datetime.fromisoformat(sale['date'])
        
        info_text = f"""
📅 التاريخ: {sale_date.strftime('%Y-%m-%d %H:%M')}
👤 العميل: {sale['customer']}
📞 الهاتف: {sale.get('phone', 'غير محدد')}
💳 طريقة الدفع: {sale['payment_method']}
✅ الحالة: {sale.get('status', 'مكتمل')}
👨‍💼 الكاشير: {sale.get('cashier', 'غير محدد')}
        """
        
        tk.Label(
            info_frame,
            text=info_text,
            font=("Cairo", 12),
            bg=COLORS['white'],
            fg=COLORS['dark'],
            justify='left'
        ).pack(anchor='w')
        
        # تفاصيل المنتجات
        items_frame = tk.LabelFrame(
            details_window,
            text="المنتجات",
            font=("Cairo", 12, "bold"),
            bg=COLORS['background'],
            fg=COLORS['primary']
        )
        items_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # جدول المنتجات
        items_columns = ('المنتج', 'الكمية', 'السعر', 'الإجمالي')
        items_tree = ttk.Treeview(items_frame, columns=items_columns, show='headings', height=8)
        
        for col in items_columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=120, anchor='center')
        
        for item in sale['items']:
            items_tree.insert('', 'end', values=(
                item['name'],
                item['quantity'],
                f"{item['price']:.2f}",
                f"{item['total']:.2f}"
            ))
        
        items_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # الإجماليات
        totals_frame = tk.Frame(details_window, bg=COLORS['light'], padx=20, pady=15)
        totals_frame.pack(fill='x', padx=20, pady=10)
        
        if 'subtotal' in sale and 'tax_amount' in sale:
            totals_text = f"""
المجموع الفرعي: {sale['subtotal']:.2f} جنيه
الضريبة: {sale['tax_amount']:.2f} جنيه
الإجمالي: {sale['total']:.2f} جنيه
            """
        else:
            totals_text = f"الإجمالي: {sale['total']:.2f} جنيه"
        
        tk.Label(
            totals_frame,
            text=totals_text,
            font=("Cairo", 14, "bold"),
            bg=COLORS['light'],
            fg=COLORS['primary'],
            justify='right'
        ).pack(anchor='e')
    
    def print_selected_invoice(self, tree):
        """طباعة الفاتورة المحددة"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار فاتورة")
            return
        
        item_values = tree.item(selection[0])['values']
        invoice_number = item_values[0]
        
        sale = next((s for s in self.data['sales'] 
                    if str(s.get('invoice_number', s['id'][:8])) == str(invoice_number)), None)
        
        if sale:
            self.generate_invoice_pdf(sale)
    
    def save_selected_invoice_image(self, tree):
        """حفظ الفاتورة المحددة كصورة"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار فاتورة")
            return
        
        item_values = tree.item(selection[0])['values']
        invoice_number = item_values[0]
        
        sale = next((s for s in self.data['sales'] 
                    if str(s.get('invoice_number', s['id'][:8])) == str(invoice_number)), None)
        
        if sale:
            self.generate_invoice_image(sale)
    
    def show_settings_window(self):
        """عرض نافذة الإعدادات"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("الإعدادات")
        settings_window.geometry("600x700")
        settings_window.configure(bg=COLORS['background'])
        
        # العنوان
        header_frame = tk.Frame(settings_window, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="⚙️ إعدادات النظام",
            font=("Cairo", 18, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        # إطار الإعدادات
        settings_frame = tk.Frame(settings_window, bg=COLORS['white'], padx=30, pady=20)
        settings_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # إعدادات اللغة
        lang_section = tk.LabelFrame(
            settings_frame,
            text="إعدادات اللغة",
            font=("Cairo", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        lang_section.pack(fill='x', pady=10)
        
        lang_frame = tk.Frame(lang_section, bg=COLORS['white'])
        lang_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            lang_frame,
            text="اللغة:",
            font=("Cairo", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(side='left')
        
        language_var = tk.StringVar(value=self.current_language)
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=language_var,
            values=[("ar", "العربية"), ("en", "English")],
            font=("Cairo", 11),
            state="readonly",
            width=15
        )
        lang_combo.set("العربية" if self.current_language == "ar" else "English")
        lang_combo.pack(side='left', padx=10)
        
        def change_language():
            new_lang = "ar" if "العربية" in lang_combo.get() else "en"
            if new_lang != self.current_language:
                self.current_language = new_lang
                self.data['settings']['language'] = new_lang
                self.save_data()
                messagebox.showinfo("نجح", "سيتم تطبيق اللغة الجديدة عند إعادة تشغيل البرنامج")
        
        ModernButton(
            lang_frame,
            text="تطبيق",
            command=change_language,
            bg_color=COLORS['success']
        ).pack(side='left', padx=10)
        
        # إعدادات المسارات
        paths_section = tk.LabelFrame(
            settings_frame,
            text="مسارات الحفظ",
            font=("Cairo", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        paths_section.pack(fill='x', pady=10)
        
        # مسار البيانات
        data_path_frame = tk.Frame(paths_section, bg=COLORS['white'])
        data_path_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            data_path_frame,
            text="مسار حفظ البيانات:",
            font=("Cairo", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w')
        
        data_path_var = tk.StringVar(value=self.data.get('settings', {}).get('data_path', os.getcwd()))
        data_path_entry = tk.Entry(
            data_path_frame,
            textvariable=data_path_var,
            font=("Cairo", 10),
            bg=COLORS['light'],
            state='readonly',
            relief='flat',
            bd=5
        )
        data_path_entry.pack(fill='x', pady=2, ipady=3)
        
        def change_data_path():
            new_path = filedialog.askdirectory(title="اختر مجلد حفظ البيانات")
            if new_path:
                data_path_var.set(new_path)
        
        ModernButton(
            data_path_frame,
            text="تغيير المسار",
            command=change_data_path,
            bg_color=COLORS['warning'],
            fg_color=COLORS['dark']
        ).pack(pady=5)
        
        # مسار النسخ الاحتياطية
        backup_path_frame = tk.Frame(paths_section, bg=COLORS['white'])
        backup_path_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            backup_path_frame,
            text="مسار النسخ الاحتياطية:",
            font=("Cairo", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w')
        
        backup_path_var = tk.StringVar(value=self.data.get('settings', {}).get('backup_path', self.backup_path))
        backup_path_entry = tk.Entry(
            backup_path_frame,
            textvariable=backup_path_var,
            font=("Cairo", 10),
            bg=COLORS['light'],
            state='readonly',
            relief='flat',
            bd=5
        )
        backup_path_entry.pack(fill='x', pady=2, ipady=3)
        
        def change_backup_path():
            new_path = filedialog.askdirectory(title="اختر مجلد النسخ الاحتياطية")
            if new_path:
                backup_path_var.set(new_path)
        
        ModernButton(
            backup_path_frame,
            text="تغيير المسار",
            command=change_backup_path,
            bg_color=COLORS['warning'],
            fg_color=COLORS['dark']
        ).pack(pady=5)
        
        # إعدادات المتجر
        store_section = tk.LabelFrame(
            settings_frame,
            text="معلومات المتجر",
            font=("Cairo", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        store_section.pack(fill='x', pady=10)
        
        # اسم المتجر
        tk.Label(
            store_section,
            text="اسم المتجر:",
            font=("Cairo", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w', padx=10, pady=(10, 2))
        
        store_name_var = tk.StringVar(value=self.data.get('settings', {}).get('store_name', 'Book Bliss'))
        store_name_entry = tk.Entry(
            store_section,
            textvariable=store_name_var,
            font=("Cairo", 11),
            bg=COLORS['light'],
            relief='flat',
            bd=5
        )
        store_name_entry.pack(fill='x', padx=10, pady=(0, 5), ipady=3)
        
        # عنوان المتجر
        tk.Label(
            store_section,
            text="عنوان المتجر:",
            font=("Cairo", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w', padx=10, pady=(5, 2))
        
        store_address_var = tk.StringVar(value=self.data.get('settings', {}).get('store_address', 'شارع الكتب، القاهرة'))
        store_address_entry = tk.Entry(
            store_section,
            textvariable=store_address_var,
            font=("Cairo", 11),
            bg=COLORS['light'],
            relief='flat',
            bd=5
        )
        store_address_entry.pack(fill='x', padx=10, pady=(0, 5), ipady=3)
        
        # رقم هاتف المتجر
        tk.Label(
            store_section,
            text="رقم الهاتف:",
            font=("Cairo", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(anchor='w', padx=10, pady=(5, 2))
        
        store_phone_var = tk.StringVar(value=self.data.get('settings', {}).get('store_phone', '01234567890'))
        store_phone_entry = tk.Entry(
            store_section,
            textvariable=store_phone_var,
            font=("Cairo", 11),
            bg=COLORS['light'],
            relief='flat',
            bd=5
        )
        store_phone_entry.pack(fill='x', padx=10, pady=(0, 10), ipady=3)
        
        # إعدادات أخرى
        other_section = tk.LabelFrame(
            settings_frame,
            text="إعدادات أخرى",
            font=("Cairo", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        other_section.pack(fill='x', pady=10)
        
        # معدل الضريبة
        tax_frame = tk.Frame(other_section, bg=COLORS['white'])
        tax_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            tax_frame,
            text="معدل الضريبة (%):",
            font=("Cairo", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(side='left')
        
        tax_rate_var = tk.StringVar(value=str(self.data.get('settings', {}).get('tax_rate', 0.14) * 100))
        tax_rate_entry = tk.Entry(
            tax_frame,
            textvariable=tax_rate_var,
            font=("Cairo", 11),
            bg=COLORS['light'],
            relief='flat',
            bd=5,
            width=10
        )
        tax_rate_entry.pack(side='left', padx=10, ipady=3)
        
        # حد تنبيه المخزون
        stock_frame = tk.Frame(other_section, bg=COLORS['white'])
        stock_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            stock_frame,
            text="حد تنبيه المخزون:",
            font=("Cairo", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['dark']
        ).pack(side='left')
        
        stock_threshold_var = tk.StringVar(value=str(self.data.get('settings', {}).get('low_stock_threshold', 5)))
        stock_threshold_entry = tk.Entry(
            stock_frame,
            textvariable=stock_threshold_var,
            font=("Cairo", 11),
            bg=COLORS['light'],
            relief='flat',
            bd=5,
            width=10
        )
        stock_threshold_entry.pack(side='left', padx=10, ipady=3)
        
        # أزرار الحفظ
        actions_frame = tk.Frame(settings_window, bg=COLORS['background'])
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        def save_settings():
            try:
                # تحديث الإعدادات
                self.data['settings']['data_path'] = data_path_var.get()
                self.data['settings']['backup_path'] = backup_path_var.get()
                self.data['settings']['store_name'] = store_name_var.get()
                self.data['settings']['store_address'] = store_address_var.get()
                self.data['settings']['store_phone'] = store_phone_var.get()
                self.data['settings']['tax_rate'] = float(tax_rate_var.get()) / 100
                self.data['settings']['low_stock_threshold'] = int(stock_threshold_var.get())
                
                # تحديث مسار النسخ الاحتياطية
                self.backup_path = backup_path_var.get()
                if not os.path.exists(self.backup_path):
                    os.makedirs(self.backup_path)
                
                self.save_data()
                messagebox.showinfo("نجح", "تم حفظ الإعدادات بنجاح")
                settings_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("خطأ", "يرجى التأكد من صحة القيم المدخلة")
        
        ModernButton(
            actions_frame,
            text="💾 حفظ الإعدادات",
            command=save_settings,
            bg_color=COLORS['success']
        ).pack(side='left', padx=5, fill='x', expand=True, ipady=8)
        
        ModernButton(
            actions_frame,
            text="❌ إلغاء",
            command=settings_window.destroy,
            bg_color=COLORS['danger']
        ).pack(side='right', padx=5, fill='x', expand=True, ipady=8)
    
    def start_auto_backup(self):
        """بدء النسخ الاحتياطي التلقائي"""
        def auto_backup():
            try:
                # إنشاء نسخة احتياطية كل ساعة
                backup_filename = f"auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_filepath = os.path.join(self.backup_path, backup_filename)
                
                with open(backup_filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
                
                # حذف النسخ القديمة (الاحتفاظ بآخر 24 نسخة)
                backup_files = [f for f in os.listdir(self.backup_path) if f.startswith('auto_backup_')]
                backup_files.sort(reverse=True)
                
                for old_backup in backup_files[24:]:
                    try:
                        os.remove(os.path.join(self.backup_path, old_backup))
                    except:
                        pass
                        
            except Exception as e:
                print(f"Auto backup failed: {e}")
            
            # جدولة النسخة التالية بعد ساعة
            self.root.after(3600000, auto_backup)  # 3600000 ms = 1 hour
        
        # بدء النسخ الاحتياطي التلقائي بعد 5 دقائق من التشغيل
        self.root.after(300000, auto_backup)  # 300000 ms = 5 minutes
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SalesManagementSystem()
    app.run()
