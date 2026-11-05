"""Product Store Service routes."""
from flask import jsonify, request, abort, url_for
from service.models import Product, Category
from service.common import status
from . import app


@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )
    if request.headers["Content-Type"] == content_type:
        return
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


@app.route("/products", methods=["POST"])
def create_products():
    """Create a Product"""
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("read_product", product_id=product.id, _external=True)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


@app.route("/products", methods=["GET"])
def list_products():
    """List all Products, optionally filtered by name, category or availability"""
    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)
    elif available:
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id):
    """Read a single Product"""
    product = Product.find(product_id)
    if product:
        return jsonify(product.serialize()), status.HTTP_200_OK
    return jsonify({"error": "Product not found"}), status.HTTP_404_NOT_FOUND


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update a Product"""
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Product with id '{product_id}' was not found.",
        )
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a Product"""
    product = Product.find(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), status.HTTP_404_NOT_FOUND
    product.delete()
    return "", status.HTTP_204_NO_CONTENT
