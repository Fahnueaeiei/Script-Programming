# my_utils.py  -- Custom module สำหรับ Lab 6.2

def greet(name):
    """แสดงข้อความทักทายผู้ใช้"""
    print(f"Hello, {name}!")

def is_prime(number):
    """คืนค่า True ถ้า number เป็นจำนวนเฉพาะ ไม่เช่นนั้นคืน False"""
    if number < 2:
        return False
    i = 2
    while i * i <= number:       # ตรวจถึงแค่ sqrt(number) ก็พอ
        if number % i == 0:
            return False
        i += 1
    return True
