import requests
import time
import random
import sys

# CẤU HÌNH ĐỊA CHỈ WEB (Dựa trên log của bạn)
BASE_URL = "http://192.168.12.190:8095"

# Danh sách sản phẩm mẫu
PRODUCT_IDS = [
    "0PUK6V6EV0", "1YMWWN1N4O", "2ZYFJ3GM2N", "66VCHSJNUP", 
    "6E92ZMYYFZ", "9SIQT8TOJO", "L9ECAV7KIM", "LS4PSXUNUM", "OLJCESPC7Z"
]

def simulate_user_activity(user_id):
    # Sử dụng Session để giữ Cookie/Session
    session = requests.Session()
    
    print(f"--- [User {user_id}] Bắt đầu phiên mua hàng ---")

    try:
        # 1. Truy cập Trang chủ
        resp = session.get(BASE_URL)
        if resp.status_code == 200:
            print(f"[User {user_id}] ✅ Đã vào Trang chủ")
        else:
            print(f"[User {user_id}] ❌ Lỗi vào Trang chủ: {resp.status_code}")
            # Nếu trang chủ lỗi (500), có thể thử tiếp hoặc dừng. Ở đây ta thử tiếp.
        
        # 2. Thêm vào giỏ hàng
        product_id = random.choice(PRODUCT_IDS)
        resp = session.post(f"{BASE_URL}/cart", data={
            "product_id": product_id,
            "quantity": 1
        })
        
        if resp.status_code in [200, 302, 303]:
            print(f"[User {user_id}] ✅ Đã thêm sản phẩm {product_id} vào giỏ")
        else:
            print(f"[User {user_id}] ❌ Lỗi thêm giỏ hàng: {resp.status_code}")
            return

        # 3. THANH TOÁN (Checkout)
        # Sử dụng số thẻ TEST hợp lệ (Visa Test)
        checkout_data = {
            "email": f"user{user_id}@example.com",
            "street_address": "123 Seeker St",
            "zip_code": "94043",
            "city": "Mountain View",
            "state": "CA",
            "country": "United States",
            "credit_card_number": "4242424242424242", 
            "credit_card_expiration_month": "12",
            "credit_card_expiration_year": "2027",
            "credit_card_cvv": "123"
        }
        
        # Thêm header Referer để giả lập browser tốt hơn
        headers = {'Referer': f"{BASE_URL}/cart"}
        
        resp = session.post(f"{BASE_URL}/cart/checkout", data=checkout_data, headers=headers)
        
        if resp.status_code in [200, 302, 303]:
            print(f"[User {user_id}] 💰 THANH TOÁN THÀNH CÔNG! (Traffic đã đi qua Node.js PaymentService)")
        elif resp.status_code == 422:
            print(f"[User {user_id}] ⚠️ Lỗi 422: Dữ liệu không hợp lệ. Server phản hồi: {resp.text[:100]}")
        else:
            print(f"[User {user_id}] ⚠️ Thanh toán thất bại: {resp.status_code}")

    except Exception as e:
        print(f"[User {user_id}] ❌ Lỗi kết nối (Connection Error): {e}")

if __name__ == "__main__":
    print(f"Đang bắn traffic vào: {BASE_URL}")
    print("Nhấn Ctrl+C để dừng.\n")
    
    count = 1
    while True:
        simulate_user_activity(count)
        count += 1
        # Nghỉ 2 giây giữa mỗi lần mua
        time.sleep(2)
