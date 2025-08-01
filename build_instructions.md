# تعليمات بناء ملف exe
# Instructions for Building EXE File

## الطريقة الأولى: استخدام PyInstaller

### 1. تثبيت PyInstaller
```bash
pip install pyinstaller
```

### 2. بناء ملف exe بسيط
```bash
pyinstaller --onefile main.py
```

### 3. بناء ملف exe مع إعدادات متقدمة
```bash
pyinstaller --onefile --windowed --name="SalesSystem" --icon=icon.ico main.py
```

### 4. استخدام سكريبت البناء المرفق
```bash
python build_exe.py
```

## الطريقة الثانية: استخدام cx_Freeze

### 1. تثبيت cx_Freeze
```bash
pip install cx_Freeze
```

### 2. إنشاء ملف setup_cx.py
```python
from cx_Freeze import setup, Executable

setup(
    name="Sales Management System",
    version="1.0",
    description="نظام إدارة المبيعات والمصروفات",
    executables=[Executable("main.py", base="Win32GUI")]
)
```

### 3. بناء الملف
```bash
python setup_cx.py build
```

## الطريقة الثالثة: استخدام auto-py-to-exe (واجهة رسومية)

### 1. تثبيت auto-py-to-exe
```bash
pip install auto-py-to-exe
```

### 2. تشغيل الواجهة الرسومية
```bash
auto-py-to-exe
```

### 3. إعداد الخيارات:
- اختر ملف main.py
- اختر "One File"
- اختر "Window Based"
- أضف أيقونة إذا أردت
- اضغط "Convert .py to .exe"

## نصائح مهمة:

### 1. تحسين حجم الملف
```bash
pyinstaller --onefile --windowed --optimize=2 main.py
```

### 2. إضافة ملفات إضافية
```bash
pyinstaller --onefile --add-data "sales_data.json;." main.py
```

### 3. استبعاد مكتبات غير ضرورية
```bash
pyinstaller --onefile --exclude-module matplotlib main.py
```

### 4. إنشاء ملف spec للتحكم الكامل
```bash
pyinstaller --onefile main.py
# ثم تعديل ملف main.spec وإعادة البناء
pyinstaller main.spec
```

## حل المشاكل الشائعة:

### 1. مشكلة عدم ظهور الواجهة
- استخدم `--windowed` أو `--noconsole`

### 2. مشكلة حجم الملف الكبير
- استخدم `--optimize=2`
- استبعد المكتبات غير المستخدمة

### 3. مشكلة عدم وجود الملفات المطلوبة
- استخدم `--add-data` لإضافة الملفات

### 4. مشكلة بطء التشغيل
- استخدم `--onedir` بدلاً من `--onefile`

## اختبار الملف المبني:

1. انسخ الملف إلى مجلد جديد
2. شغل الملف للتأكد من عمله
3. اختبر جميع الوظائف
4. تأكد من وجود ملف البيانات

## توزيع التطبيق:

1. أنشئ مجلد للتوزيع
2. انسخ ملف exe
3. أضف ملف README
4. أضف أي ملفات مطلوبة أخرى
5. أنشئ ملف zip للتوزيع