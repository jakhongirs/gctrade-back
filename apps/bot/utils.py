import os
from pathlib import Path

import pandas as pd
import requests

from apps.product.models import Order


def bot_send_message(message, order_id=None):
    token = "6711417231:AAH4fBwj12FNyQ2i1VX2jA3atceH18qOfKY"
    channel_id = -1002025795462

    if order_id:
        order = Order.objects.get(pk=order_id)

        # Create Excel file
        excel_file_path = create_order_excel(order)

        # Send Excel file as a document to Telegram
        files = {"document": open(excel_file_path, "rb")}
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        params = {"chat_id": channel_id, "caption": message}
        requests.post(url, data=params, files=files)

        # Delete Excel file
        os.remove(excel_file_path)


def create_order_excel(order):
    cart_items = order.cart.items.all()

    # Prepare data for Excel
    order_data = {
        "Buyurtma ID": [order.pk],
        "Status": [order.get_status_display()],
        "Ism": [order.name],
        "Telefon": [order.phone],
        "Sana": [order.created_at.strftime("%Y-%m-%d %H:%M")],
        "Jami": [order.cart.total_price],
    }

    cart_data = {
        "Mahsulot": [cart_item.product.title for cart_item in cart_items],
        "Narxi": [cart_item.product.price for cart_item in cart_items],
        "Soni": [cart_item.quantity for cart_item in cart_items],
        "Jami": [cart_item.product.price * cart_item.quantity for cart_item in cart_items],
    }

    # Create DataFrames
    order_df = pd.DataFrame(order_data)
    cart_df = pd.DataFrame(cart_data)

    # Save DataFrames to an Excel file
    excel_file_path = Path(__file__).resolve().parent.parent.parent / f"order_{order.pk}.xlsx"
    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as writer:
        order_df.to_excel(writer, sheet_name="Buyurtma", index=False)
        cart_df.to_excel(writer, sheet_name="Savatcha", index=False)

        # Iterate through all sheets
        for sheet in writer.sheets.values():
            # Iterate through all columns and set the width based on the maximum length of the content in each column
            for column in sheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except TypeError:
                        pass
                adjusted_width = (max_length + 2) * 1.2  # Adjust the width for padding and aesthetics
                sheet.column_dimensions[column[0].column_letter].width = adjusted_width

    return excel_file_path
