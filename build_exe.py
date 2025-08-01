#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لتحويل التطبيق إلى ملف exe
Build script to convert the application to exe file
"""

import os
import sys
import subprocess

def install_pyinstaller():
    """تثبيت PyInstaller"""
    try:
        import PyInstaller
        print("PyInstaller موجود بالفعل")
    except ImportError:
        print("تثبيت PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_exe():
    """بناء ملف exe"""
    print("بدء عملية البناء...")
    
    # معاملات PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # ملف واحد
        "--windowed",  # بدون نافذة console
        "--name=SalesManagementSystem",  # اسم الملف
        "--icon=icon.ico",  # أيقونة (اختيارية)
        "--add-data=sales_data.json;.",  # إضافة ملف البيانات
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("تم بناء الملف بنجاح!")
        print("الملف موجود في مجلد dist/")
    except subprocess.CalledProcessError as e:
        print(f"خطأ في البناء: {e}")
    except FileNotFoundError:
        print("PyInstaller غير موجود. يرجى تثبيته أولاً.")

if __name__ == "__main__":
    install_pyinstaller()
    build_exe()