import io
import os
from pathlib import Path

import requests
from django.template.loader import get_template
from weasyprint import HTML

from apps.product.models import Order


def bot_send_message(message, order_id=None):
    token = "6711417231:AAH4fBwj12FNyQ2i1VX2jA3atceH18qOfKY"
    channel_id = -1002025795462

    if order_id:
        order = Order.objects.get(pk=order_id)

    # Create PDF file
    pdf_file_path = create_order_pdf(order)

    print(pdf_file_path)

    # Send PDF file as a document to Telegram
    files = {"document": open(pdf_file_path, "rb")}
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    params = {"chat_id": channel_id, "caption": message}
    requests.post(url, data=params, files=files)

    # Delete PDF file
    os.remove(pdf_file_path)


def create_order_pdf(order):
    template = get_template("order.html")

    cart_items = order.cart.items.all()

    for cart_item in cart_items:
        cart_item.total_price = cart_item.quantity * cart_item.product.price

    context = {
        "order": order,
        "cart_items": cart_items,
        "order_status": order.get_status_display(),
        "order_date": order.created_at.strftime("%Y-%m-%d %H:%M"),
    }

    html = template.render(context)
    output = io.BytesIO()
    HTML(string=html, base_url=os.getcwd()).write_pdf(output)

    # save file inside root directory
    file_path = Path(__file__).resolve().parent.parent.parent / f"order_{order.pk}.pdf"

    with open(file_path, "wb") as pdf_file:
        pdf_file.write(output.getvalue())

    return file_path
