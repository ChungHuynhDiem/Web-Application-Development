import re

# def valid_phone_number(phone_number):
#     # Xóa các ký tự không phải số hoặc các ký tự đặc biệt
#     phone_number = phone_number.strip()
#     # Kiểm tra ký tự không hợp lệ
#     digits=""
#     for char in phone_number:
#         if (char != " " and char != "+" and char!="-" and char!="." and char!="(" and char!=")"):
#             digits+=char

#     # Kiểm tra xem chuỗi có chứa ký tự đặc biệt hoặc ký tự không phải chữ cái/số hay không
#     if  re.search(r'[^0-9]', digits):
#         return "Недопустимый ввод. В номере телефона встречаются недопустимые символы"

#     # Kiểm tra độ dài của số điện thoại
#     if len(digits) not in [10, 11]:
#         return "Недопустимый ввод. Неверное количество цифр."

#     # Kiểm tra xem số điện thoại có bắt đầu với +7 hoặc 8 không
#     if len(digits) == 11 and not (phone_number.startswith('+7') or phone_number.startswith('8')):
#         return "Недопустимый ввод. Неверное количество цифр."

#     return False

# def format_phone_number(phone_number):
#     digits = re.sub(r"[^\d]", "", phone_number)  # Lấy chỉ các chữ số
#     if len(digits) == 11 and digits.startswith('7'):
#         digits = '8' + digits[1:]  # Đổi số +7 thành 8
#     if len(digits)==10:
#         digits = "7"+digits
#     return f"{digits[:1]}-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

def valid_phone_number(phone_number):
    # Xóa khoảng trắng đầu cuối
    phone_number = phone_number.strip()
    
    # Lọc chỉ giữ lại số và dấu +
    cleaned = re.sub(r'[^\d+]', '', phone_number)
    
    # Kiểm tra ký tự không hợp lệ
    if re.search(r'[^0-9+]', cleaned):
        return "Недопустимый ввод. В номере телефона встречаются недопустимые символы"
    
    # Xóa dấu + nếu có
    digits = cleaned.replace('+', '')
    
    # Kiểm tra độ dài
    if len(digits) not in [10, 11]:
        return "Недопустимый ввод. Неверное количество цифр."
    
    # Kiểm tra đầu số
    if len(digits) == 11 and not (cleaned.startswith('+7') or cleaned.startswith('8')):
        return "Недопустимый ввод. Неверное количество цифр."
    
    return False

def format_phone_number(phone_number):
    digits = re.sub(r"[^\d]", "", phone_number)
    if len(digits) == 11 and digits.startswith('7'):
        digits = '8' + digits[1:]
    if len(digits) == 10:
        digits = "8" + digits  # Thêm số 8 đầu nếu là số 10 chữ số
    return f"{digits[:1]}-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:]}"