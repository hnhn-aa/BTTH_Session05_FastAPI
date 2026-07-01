from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import List

# ==========================================
# 1. DATA MOCKUP (Dữ liệu ban đầu)
# ==========================================
products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]

# ==========================================
# 2. PYDANTIC SCHEMAS (Validate dữ liệu)
# ==========================================
class CreateProduct(BaseModel):
    name: str = Field(min_length=1)  # Đảm bảo tên không được rỗng
    price: float = Field(gt=0)        # Giá phải lớn hơn 0

app = FastAPI()

# ==========================================
# 3. ENDPOINTS (Các chức năng API)
# ==========================================

# API 1: Thêm sản phẩm mới (POST /products)
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(new_product: CreateProduct):
    # Tự động tăng ID dựa trên phần tử cuối cùng trong danh sách
    new_id = products[-1]["id"] + 1 if products else 1
    
    # Tạo dictionary sản phẩm mới
    product_data = {
        "id": new_id,
        "name": new_product.name,
        "price": new_product.price
    }
    
    # Thêm vào danh sách mockup
    products.append(product_data)
    
    return {
        "message": "Thêm sản phẩm thành công",
        "data": product_data
    }


# API 2: Lấy danh sách sản phẩm (GET /products)
@app.get("/products")
def get_products():
    return {
        "data": products
    }


# API 3: Xóa sản phẩm (DELETE /products/{product_id})
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    # Bước 1: Tìm kiếm sản phẩm trong danh sách
    target_product = None
    for product in products:
        if product["id"] == product_id:
            target_product = product
            break
            
    # Bước 2: Nếu không tìm thấy sản phẩm, trả lỗi "Product not found"
    if not target_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
        
    # Bước 3: Nếu tìm thấy, thực hiện xóa cứng khỏi danh sách
    products.remove(target_product)
    
    return {
        "message": "Xóa sản phẩm thành công",
        "data": target_product
    }