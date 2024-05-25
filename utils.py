import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sys

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_static_path():
    if getattr(sys, 'frozen', False):  # Check if the app is frozen (PyInstaller)
        return os.path.join(sys._MEIPASS, 'static')
    else:
        return os.path.join(os.path.dirname(__file__), 'static')

def export_to_excel(accounts):
    static_path = get_static_path()
    ensure_directory(static_path)
    data = [{'Name': acc.name, 'A/C no.': acc.account_number, 'Phone': acc.phone, 'Last Deposit Amount': acc.deposit_amount} for acc in accounts]
    df = pd.DataFrame(data)
    file_path = os.path.join(static_path, 'accounts.xlsx')
    df.to_excel(file_path, index=False)
    return file_path

def export_to_pdf(accounts):
    static_path = get_static_path()
    ensure_directory(static_path)
    file_path = os.path.join(static_path, 'accounts.pdf')
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 40, "Account List")
    for i, acc in enumerate(accounts):
        c.drawString(100, height - 60 - i * 20, f"{acc.name}, {acc.account_number}, {acc.phone}, {acc.deposit_amount}")
    c.save()
    return file_path
