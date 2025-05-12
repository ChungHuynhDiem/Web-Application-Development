import re

def is_valid_password(password: str) -> bool:
    # Độ dài
    if len(password) < 8 or len(password) > 128:
        return False

    # Không có khoảng trắng
    if re.search(r"\s", password):
        return False

    # Ít nhất một chữ hoa và một chữ thường
    if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password):
        return False

    # Chỉ chữ cái Latin hoặc Kirin (Cyrl)
    if re.search(r"[^\w~!?@#$%^&*_\-+()\[\]{}><\\/|\"'\.,:;]", password, re.UNICODE):
        # Nếu có ký tự không hợp lệ
        return False

    # Phải có ít nhất một chữ cái Latin hoặc Kirin
    if not re.search(r"[A-Za-zА-Яа-яЁё]", password):
        return False

    # Có ít nhất một chữ số Ả Rập
    if not re.search(r"\d", password):
        return False

    return True
