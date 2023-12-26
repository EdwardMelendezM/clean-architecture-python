from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from domain.products_entities import Product, CreateBodyProduct, UpdateBodyProduct, PaginatedProductList
from domain.products_repository import ProductsRepository
from domain.products_usecase import ProductsUseCase

app = FastAPI()

db_url = "sqlite:///products.db"
products_repository = ProductsRepository(db_url)
products_use_case = ProductsUseCase(products_repository)


@app.get('/products', response_model=PaginatedProductList)
def get_products(page: int = Query(1, gt=0), size_page: int = Query(10, gt=0, le=100)):
    """
    Retrieve a paginated list of products.

    This endpoint allows you to retrieve a specific page of products, with a specified number of products per page.

    :param page: The page number to retrieve. Must be a positive integer (default: 1).
    :param size_page: The number of products to show per page. (default: 100)

    :return: A paginated list of products.
    :rtype: PaginatedProductList

    :raises HTTPException 404: If the requested page is not found.
    """
    # Retrieve the full list of products
    all_products = products_use_case.get_products()

    # Calculate the start and end index based on pagination parameters
    start_idx = (page - 1) * size_page
    end_idx = start_idx + size_page

    # Return the paginated list of products
    return PaginatedProductList(items=all_products[start_idx:end_idx], total_items=len(all_products))


@app.get('/products/{product_id}', response_model=Product)
def get_product(product_id: int):
    """
    Retrieve a specific product by ID.

    This endpoint allows you to retrieve information about a specific product based on its unique identifier.

    :param product_id: The unique identifier of the product to retrieve.
    :type product_id: int

    :return: The details of the requested product.
    :rtype: Product

    :raises HTTPException 404: If the product with the specified ID is not found.
    """
    # Attempt to retrieve the product by ID
    product = products_use_case.get_product_by_id(product_id)

    # Check if the product exists
    if product:
        return product
    else:
        # Raise a 404 HTTPException if the product is not found
        raise HTTPException(status_code=404, detail="Product not found")


@app.post('/products', response_model=Product, status_code=201)
def create_product(product_body: CreateBodyProduct):
    """
    Create a new product.

    This endpoint allows you to create a new product by providing the necessary information in the request body.

    :param product_body: The information for the new product.
    :type product_body: CreateBodyProduct

    :return: The newly created product.
    :rtype: Product

    :raises HTTPException 400: If there is an error in the request body or the creation process.
    """
    try:
        # Attempt to create the new product
        new_product = products_use_case.create_product(product_body)
        return new_product
    except Exception as e:
        # Raise a 400 HTTPException with details of the error
        raise HTTPException(status_code=400, detail=str(e))


@app.put('/products/{product_id}', response_model=Product)
def update_product(product_id: int, update_body: UpdateBodyProduct):
    """
    Update information for a specific product.

    This endpoint allows you to update the information of a specific product based on its unique identifier.

    :param product_id: The unique identifier of the product to update.
    :type product_id: int
    :param update_body: The updated information for the product.
    :type update_body: UpdateBodyProduct

    :return: The updated details of the product.
    :rtype: Product

    :raises HTTPException 404: If the product with the specified ID is not found.
    """
    # Attempt to update the product by ID
    updated_product = products_use_case.update_product(product_id, update_body)

    # Check if the product exists
    if updated_product:
        return updated_product
    else:
        # Raise a 404 HTTPException if the product is not found
        raise HTTPException(status_code=404, detail="Product not found")


@app.delete('/products/{product_id}', status_code=200)
def delete_product(product_id: int):
    """
    Delete a specific product by ID.

    This endpoint allows you to delete a specific product based on its unique identifier.

    :param product_id: The unique identifier of the product to delete.
    :type product_id: int

    :return: A JSON response indicating the successful deletion of the product.
    :rtype: JSONResponse

    :raises HTTPException 404: If the product with the specified ID is not found.
    """
    # Attempt to delete the product by ID
    products_use_case.delete_product(product_id)

    # Return a JSON response indicating successful deletion
    return JSONResponse(content={"message": "Product deleted successfully"})
