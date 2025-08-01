# نظام إدارة المبيعات والمصروفات - Sales Management System

نظام شامل لإدارة المبيعات والمصروفات مع واجهة مستخدم رسومية بسيطة وأنيقة.

## المميزات

### 🛒 إدارة المبيعات
- إضافة المنتجات إلى سلة التسوق
- حساب الإجمالي تلقائياً
- دعم طرق الدفع المختلفة (نقدي/آجل)
- إنشاء فواتير مع أرقام فريدة
- تتبع أسماء العملاء

### 📦 إدارة المخزون
- إضافة وتعديل وحذف المنتجات
- مراقبة مستويات المخزون
- تنبيهات المخزون المنخفض
- إدارة الأسعار والكميات

### 💰 إدارة المصروفات
- تسجيل المصروفات بأنواعها المختلفة
- تصنيف المصروفات
- حساب إجمالي المصروفات
- تتبع تواريخ المصروفات

### 📊 التقارير والإحصائيات
- تقارير المبيعات اليومية
- ملخص مالي شامل
- إحصائيات الأرباح والخسائر
- تقارير المنتجات الأكثر مبيعاً

### 💾 إدارة البيانات
- نسخ احتياطية تلقائية
- استيراد وتصدير البيانات
- حفظ البيانات بصيغة JSON

## متطلبات التشغيل

- Python 3.7 أو أحدث
- نظام التشغيل: Windows, macOS, Linux
- مكتبة tkinter (مدمجة مع Python)

## التثبيت والتشغيل

### الطريقة الأولى: تشغيل مباشر
```bash
python main.py
```

### الطريقة الثانية: تحويل إلى exe
```bash
# تثبيت PyInstaller
pip install pyinstaller

# تشغيل سكريبت البناء
python build_exe.py
```

سيتم إنشاء ملف exe في مجلد `dist/`

## كيفية الاستخدام

1. **بدء التشغيل**: شغل التطبيق وستظهر الواجهة الرئيسية
2. **إضافة المنتجات**: اذهب إلى قسم المخزون وأضف منتجاتك
3. **تسجيل المبيعات**: استخدم قسم المبيعات لإضافة المنتجات للسلة وإتمام البيع
4. **تسجيل المصروفات**: سجل مصروفاتك في القسم المخصص
5. **مراجعة التقارير**: اطلع على الإحصائيات والتقارير المالية

## هيكل الملفات

```
sales-management-system/
├── main.py              # الملف الرئيسي للتطبيق
├── build_exe.py         # سكريبت تحويل إلى exe
├── setup.py             # ملف الإعداد
├── requirements.txt     # المتطلبات
├── README.md           # هذا الملف
├── sales_data.json     # ملف البيانات (ينشأ تلقائياً)
└── dist/               # مجلد الملفات المبنية
```

## الدعم الفني

للحصول على المساعدة أو الإبلاغ عن مشاكل، يرجى إنشاء issue في المستودع.

## الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف LICENSE للتفاصيل.

---

## English

A comprehensive sales and expense management system with a simple and elegant graphical user interface.

### Features
- Sales management with shopping cart
- Inventory management with stock tracking
- Expense tracking and categorization
- Financial reports and analytics
- Data backup and restore functionality

### Requirements
- Python 3.7+
- tkinter (included with Python)

### Installation
1. Run directly: `python main.py`
2. Build exe: `python build_exe.py`

### Usage
The application provides an intuitive interface for managing sales, inventory, expenses, and generating reports.