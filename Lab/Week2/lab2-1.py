num = int(input("กรุณากรอกจำนวนเต็ม: "))

if num > 0 and num % 2 == 0:
    print("The number is positive and even.")
elif num > 0 and num % 2 != 0:
    print("The number is positive and odd.")
elif num < 0 and num % 2 == 0:
    print("The number is negative and even.")
elif num < 0 and num % 2 != 0:
    print("The number is negative and odd.")
else:
    print("The number is zero.")