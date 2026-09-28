
def valid_product(product_dict):
    error = {"error":[]}

    for key in ("title", "price", "description", "category", "image"):
        if key not in product_dict:
            error["error"].append("Some fields are missing ")
    
    if not product_dict["title"]:
        error["error"].append("Title is required ")

    if not product_dict["price"]:
        error["error"].append("Price is required ")
    else:
        try:
            price = float(product_dict["price"])
            if product_dict["price"] < 0:
                error["error"].append("Invalid price ")
        except ValueError:
            error["error"].append("Invalid price ")
        

    if not product_dict["description"]:
        error["error"].append("description is required ")

    if not product_dict["category"]:
        error["error"].append("category is required ")

    if not product_dict["image"]:
        error["error"].append("image is required ")

    if not error["error"]:
        return True
    else:
        return error


def valid_cart(cart_dict):
    error={"error":[]}

    for key in ("username", "products"):
        if key not in cart_dict:
            error["error"].append("Some fields are missing ")
    
    if not cart_dict["username"]:
        error["error"].append("username is required ")
    
    if not cart_dict["products"]:
        error["error"].append("products is required ")
    
    if not error["error"]:
        return True
    else:
        return error

    



