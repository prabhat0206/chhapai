from typing import List
from woocommerce import API
import os
import dotenv
import requests
from io import BytesIO
from PIL import Image
from chhapai.models import Orders

from chhapai.serializer import JobSerializer, OrderSerializer

dotenv.load_dotenv()

wcapi = API(
    url="https://chhapai.com",
    consumer_key=os.environ.get("WOO_KEY"),
    consumer_secret=os.environ.get("WOO_SECRET"),
    version="wc/v3"
)

def get_data():
    orders = wcapi.get("orders").json()
    return orders

def get_product(id: int) -> dict:
    product = wcapi.get(f"products/{id}").json()
    return product

def download_image_from_src(src: str):
    response = requests.get(src)
    img = BytesIO(response.content)
    return img


def structure_orders(orders):
    structured_list = []
    for order in orders:
        billing = order["billing"]
        delivery = order["shipping"]
        billing_address = f'{billing.get("company")}, {billing.get("address_1")}, {billing.get("address_2")}, {billing.get("city")}, {billing.get("state")}, {billing.get("postcode")}, {billing.get("country")}, {billing.get("email")}, {billing.get("phone")}'
        shipping_address = f'{delivery.get("company")}, {delivery.get("address_1")}, {delivery.get("address_2")}, {delivery.get("city")}, {delivery.get("state")}, {delivery.get("postcode")}, {delivery.get("country")}, {delivery.get("email")}, {delivery.get("phone")}'
        data = {
            "customer_name": billing["first_name"] + " " + billing["last_name"],
            "tax": order["total_tax"],
            "discount": order["discount_total"],
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "woo_id": order["id"],
            "woo_date": order["date_created"],
        }
        jobs = []
        for item in order["line_items"]:
            # try:
            #     product = get_product(item["product_id"])
            # except:
            #     product = {"images": []}
            job = {
                "item": item["name"],
                "description": item["name"],
                "quantity": int(item["quantity"]),
                "unit_cost": int(float(item["price"])) or 0,
                "total_cost": int(float(item["total"])) or 0,
                "discount": 0,
                "isOnHold": False,
                "mode": "normal_mode",
            }
            # if product.get("images"):
            #     image = download_image_from_src(product["images"][0]["src"])
            #     print(image)
            #     job["design"] = image
            jobs.append(job)
        data["jobs"] = jobs
        structured_list.append(data)
    return structured_list


def save_data_in_db(data: List[dict]):
    for order in data:
        existing_order = Orders.objects.filter(woo_id=order["woo_id"]).first()
        if existing_order:
            continue
        serialized_order = OrderSerializer(data=order)
        if serialized_order.is_valid():
            serialized_order.save()
            for job in order["jobs"]:
                job["order"] = serialized_order.data["oid"]
                serialized_job = JobSerializer(data=job)
                if serialized_job.is_valid():
                    serialized_job.save()


def job_scheduler():
    print("I am here")
    data = get_data()
    structured_data = structure_orders(data)
    save_data_in_db(structured_data)
    print("Data saved in db")

