def CheckUserName(username):
    if len(username) < 5:
        return False  # "Tên đăng nhập phải có ít nhất 5 ký tự"
    
    if not username.isalnum():
        return False # "Chỉ được phép dùng chữ cái Latinh (a-z, A-Z) và số (0-9)"
    
    return True # "Tên đăng nhập hợp lệ"
