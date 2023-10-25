import os

import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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
    pdfmetrics.registerFont(TTFont("NotoSans-Regular", "staticfiles/assets/fonts/NotoSans-Regular.ttf"))

    # Create a canvas object
    c = SimpleDocTemplate(pdf_file_path, pagesize=letter)

    # Order details
    order_details = [
        ["🏷️ Status", order_instance.get_status_display()],
        ["🆔 Buyurtma ID", order_instance.pk],
        ["👤 Ism", order_instance.name],
        ["📞 Telefon", order_instance.phone],
        ["📅 Sana", order_instance.created_at.strftime("%Y-%m-%d %H:%M")],
        ["🧾 Jami", order_instance.cart.total_price],
        ["", ""],
        ["🛒 Savatcha:", ""],
        ["📦 Mahsulot", "💰 Narxi", "📋 Soni", "🧾 Jami"],  # Header for cart items
    ]

    # Cart items
    cart_items = order_instance.cart.items.all()
    for product in cart_items:
        item_row = [
            product.product.title,
            product.product.price,
            product.quantity,
            product.quantity * product.product.price,
        ]
        order_details.append(item_row)

    # Create a table style
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#77aaff")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#ffffff")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "NotoSans-Regular"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7f7f7")),
        ]
    )

    # Create the table and apply the style
    table = Table(order_details)
    print(table)
    table.setStyle(style)

    # Build the PDF
    elements = [table]
    c.build(elements)

    return pdf_file_path
