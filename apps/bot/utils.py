import os

import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from apps.product.models import Order


def bot_send_message(message, order_id=None):
    token = "6711417231:AAH4fBwj12FNyQ2i1VX2jA3atceH18qOfKY"
    channel_id = -1002025795462

    if order_id:
        order = Order.objects.get(pk=order_id)

    # Create PDF file
    pdf_file_path = create_pdf(order)

    # Send PDF file as a document to Telegram
    files = {"document": open(pdf_file_path, "rb")}
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    params = {"chat_id": channel_id, "caption": message}
    requests.post(url, data=params, files=files)

    # Delete PDF file
    os.remove(pdf_file_path)


def create_pdf(order_instance):
    pdf_file_path = f"order_{order_instance.pk}.pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=letter)

    # Add order details to PDF
    c.drawString(100, 750, f"🏷️ Status: {order_instance.get_status_display()}")
    c.drawString(100, 730, f"🆔 Buyurtma ID: {order_instance.pk}")
    c.drawString(100, 710, f"👤 Ism: {order_instance.name}")
    c.drawString(100, 690, f"📞 Telefon: {order_instance.phone}")
    c.drawString(100, 670, f"📅 Sana: {order_instance.created_at.strftime('%Y-%m-%d %H:%M')}")
    c.drawString(100, 650, f"🧾 Jami: {order_instance.cart.total_price}")

    c.save()
    return pdf_file_path
