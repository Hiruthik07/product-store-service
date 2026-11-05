"""Step to load the background product data."""
import requests
from behave import given


@given('the following products')
def step_impl(context):
    """Delete all existing products, then load the ones in the table"""
    rest_endpoint = f"{context.base_url}/products"

    # List all products and delete them one by one
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == 200
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert context.resp.status_code == 204

    # Load the database with the new products
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "available": row["available"] in ["True", "true", "1"],
            "category": row["category"],
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == 201
