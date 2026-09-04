#now we r going to make another custom tool,previously we make calculator tool and now we make a tool that can return data like company information
from langchain_core.tools import tool
@tool
def get_product_info(product_name: str) -> str:
    """
    Get information about Styluxe Wears products.
    Use this when user asks about products, prices, or availability.
    Input should be a product name like 'white t-shirt' or 'printed tshirt'.
    """
    products = {
        "white t-shirt": "Price: 2000 PKR, Material: 100% cotton, Available: Yes",
        "printed t-shirt": "Price: 2500 PKR, Material: 100% cotton, Available: Yes",
        "black t-shirt": "Price: 2000 PKR, Material: 100% cotton, Available: Yes",
    }
    
    # Product dhundo
    for key in products:
        if key in product_name.lower():
            return products[key]
    
    return "Product not found in our catalog"
print(get_product_info.name)
print(get_product_info.description)
print(get_product_info.invoke("i want printed t-shirt"))
    