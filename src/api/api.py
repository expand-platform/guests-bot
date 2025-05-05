import json
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# API Settings
AUTH_TOKEN = "c374931b5c8c0595b80756645f61d6428dc07e2b"  # Your authorization token
HOST = "my.prom.ua"  # e.g.: my.prom.ua, my.satu.kz, my.prom.md

app = FastAPI()


class HTTPError(Exception):
    pass


class EvoClient:
    def __init__(self, token: str):
        self.token = token
        self.client = httpx.AsyncClient()

    async def make_request(self, method: str, url: str, body: Optional[dict] = None):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-type": "application/json",
        }
        try:
            response = await self.client.request(
                method, url, json=body, headers=headers
            )
            response.raise_for_status()  # Will raise an HTTPError if status code is not 2xx
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"{e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPError(f"Error: {str(e)}")

    # ✅ Orders API Methods
    async def get_order_list(self):
        url = f"https://{HOST}/api/v1/orders/list"
        return await self.make_request("GET", url)

    async def get_order(self, order_id: int):
        url = f"https://{HOST}/api/v1/orders/{order_id}"
        return await self.make_request("GET", url)

    async def set_order_status(
        self,
        status: str,
        ids: List[int],
        cancellation_reason: Optional[str] = None,
        cancellation_text: Optional[str] = None,
    ):
        url = f"https://{HOST}/api/v1/orders/set_status"
        body = {"status": status, "ids": ids}
        if cancellation_reason:
            body["cancellation_reason"] = cancellation_reason
        if cancellation_text:
            body["cancellation_text"] = cancellation_text
        return await self.make_request("POST", url, body)

    # ✅ Products API Methods
    async def get_product_list(self):
        url = f"https://{HOST}/api/v1/products/list?limit=4000&group_id=133187134"
        # url = f"https://{HOST}/api/v1/products/list?limit=5000"
        return await self.make_request("GET", url)

    async def get_product(self, product_id: int):
        url = f"https://{HOST}/api/v1/products/{product_id}"
        return await self.make_request("GET", url)
   
    async def get_product_by_external_id(self, external_product_id: str):
        print(external_product_id)
        print(type(external_product_id))
        url = f"https://{HOST}/api/v1/products/by_external_id/{external_product_id}"
        return await self.make_request("GET", url)

    async def edit_products(self, products: List[dict]):
        url = f"https://{HOST}/api/v1/products/edit"
        return await self.make_request("POST", url, products)
    
    async def edit_products_by_external_id(self, products: List[dict]):
        url = f"https://{HOST}/api/v1/products/edit_by_external_id"
        return await self.make_request("POST", url, products)
    
    # groups
    async def get_groups_list(self):
        url = f"https://{HOST}/api/v1/groups/list?limit=1000"
        return await self.make_request("GET", url)

# Create EvoClient instance
evo_client = EvoClient(AUTH_TOKEN)

# ✅ Pydantic models for validation


class OrderStatusRequest(BaseModel):
    status: str
    ids: List[int]
    cancellation_reason: Optional[str] = None
    cancellation_text: Optional[str] = None


class ProductEditRequest(BaseModel):
    id: int
    presence: str
    in_stock: bool
    regions: List[dict]
    price: float
    oldprice: float
    status: str
    prices: List[dict]
    discount: Optional[dict] = None
    name: str
    keywords: str
    description: str
    quantity_in_stock: int
    main_image: str


# ✅ API Routes for Orders


@app.get("/orders")
async def get_orders():
    try:
        order_list = await evo_client.get_order_list()
        if not order_list.get("orders"):
            raise HTTPException(status_code=404, detail="No orders found.")
        return order_list
    except HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")


@app.get("/groups")
async def get_groups():
    try:
        order = await evo_client.get_groups_list()
        return order
    except HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching order: {str(e)}")

        
@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    try:
        order = await evo_client.get_order(order_id)
        return order
    except HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching order: {str(e)}")


@app.post("/orders/set_status")
async def set_order_status(request: OrderStatusRequest):
    try:
        response = await evo_client.set_order_status(
            request.status,
            request.ids,
            request.cancellation_reason,
            request.cancellation_text,
        )
        return response
    except HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Error setting order status: {str(e)}"
        )


# ✅ API Routes for Products
@app.get("/products")
async def get_products():
    try:
        product_list = await evo_client.get_product_list()
        if not product_list.get("products"):
            raise HTTPException(status_code=404, detail="No products found.")
        return product_list
    except HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching products: {str(e)}"
        )


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    try:
        product = await evo_client.get_product(product_id)
        return product
    except HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

# get by external_id
@app.get("/products/by_external_id/{product_id}")
async def get_product(product_id: str):
    try:
        product = await evo_client.get_product_by_external_id(product_id)
        return product
    except HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


@app.post("/products/edit")
async def edit_products(products: List[ProductEditRequest]):
    try:
        response = await evo_client.edit_products([p.model_dump() for p in products])
        return response
    except HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error editing products: {str(e)}")

# edit by external ids
@app.post("/products/edit_by_external_id")
async def edit_products(products: List[ProductEditRequest]):
    try:
        response = await evo_client.edit_products([p.model_dump() for p in products])
        return response
    except HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error editing products: {str(e)}")
