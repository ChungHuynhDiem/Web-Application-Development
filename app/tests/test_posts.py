import pytest
from flask import session, url_for  # Thêm dòng này ở đầu file
from flask_login import current_user,UserMixin

def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.text

def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        # Sửa lại patch thành đúng tên module và hàm
        mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1

def test_posts_0(client):
    response = client.get("/post/0")
    assert response.status_code == 200
    assert "Chung Huynh Diem" in response.text

def test_posts_1(client):
    response = client.get("/post/1")
    assert response.status_code == 200
    assert "Chung Huynh Diem" in response.text

def test_posts_2(client):
    response = client.get("/post/2")
    assert response.status_code == 200
    assert "Chung Huynh Diem" in response.text

def test_posts_3(client):
    response = client.get("/post/3")
    assert response.status_code == 200
    assert "Chung Huynh Diem" in response.text

def test_posts_4(client):
    response = client.get("/post/4")
    assert response.status_code == 200
    assert "Chung Huynh Diem" in response.text


def test_post_template(client, captured_templates, posts_list, mocker):
    """Test template rendering for a specific post"""
    # Mock hàm posts_list để trả về dữ liệu test thay vì dữ liệu ngẫu nhiên
    mocker.patch('app.app.posts_list', return_value=posts_list)
    
    with captured_templates as templates:
        response = client.get('/post/0')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'post.html'
        assert context['title'] == 'Заголовок поста'
        assert context['post']['author'] == 'Иванов Иван Иванович'
        assert context['post']['text'] == 'Текст поста'

def test_post_data_on_page(client, posts_list):
    """Test that post data is properly displayed on the post page"""
    response = client.get('/post/0')
    assert response.status_code == 200
    assert 'Заголовок поста' in response.data.decode('utf-8')
    assert 'Иванов Иван Иванович' in response.data.decode('utf-8')
    assert 'Текст поста' in response.data.decode('utf-8')

def test_post_data_on_page(client, posts_list, mocker):
    """Test that post data is properly displayed on the post page"""
    # Mock hàm posts_list để trả về dữ liệu test
    mocker.patch('app.app.posts_list', return_value=posts_list)
    
    response = client.get('/post/0')
    assert response.status_code == 200
    decoded_data = response.data.decode('utf-8')
    assert 'Заголовок поста' in decoded_data
    assert 'Иванов Иван Иванович' in decoded_data
    assert 'Текст поста' in decoded_data

def test_post_date_format(client, posts_list, mocker):
    """Test that the post date is displayed correctly"""
    # Mock hàm posts_list để trả về dữ liệu test
    mocker.patch('app.app.posts_list', return_value=posts_list)
    
    response = client.get('/post/0')
    assert response.status_code == 200
    decoded_data = response.data.decode('utf-8')
    assert '2025-03-10' in decoded_data

def test_post_not_found(client, mocker):
    """Test 404 error when accessing a non-existent post"""
    # Mock posts_list để trả về list rỗng hoặc list có ít phần tử
    mocker.patch('app.app.posts_list', return_value=[{}]*3)  # Giả sử chỉ có 3 post
    
    # Test với index vượt quá
    response = client.get('/post/999')
    assert response.status_code == 404
    
    # Test với index âm
    response = client.get('/post/-1')
    assert response.status_code == 404

def test_about_page(client, captured_templates):
    """Test the /about page"""
    with captured_templates as templates:
        response = client.get('/about')
        assert response.status_code == 200
        
        # Kiểm tra template
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'about.html'
        assert context['title'] == 'Об авторе'
        
        # Kiểm tra nội dung render
        decoded_data = response.data.decode('utf-8')
        assert "Об авторе" in decoded_data

def test_index_template(client, captured_templates):
    """Test the index page template"""
    with captured_templates as templates:
        response = client.get('/')
        assert response.status_code == 200
        
        # Kiểm tra template
        assert len(templates) == 1
        template = templates[0]
        # assert template.name == 'index.html'
        
        # Kiểm tra không có lỗi render
        assert response.data.decode('utf-8') != ""

def test_post_author_and_comments(client, posts_list, mocker):
    """Test that author and comments are properly displayed in post"""
    # Mock posts_list để sử dụng dữ liệu test từ fixture
    mocker.patch('app.app.posts_list', return_value=posts_list)
    
    response = client.get('/post/0')
    assert response.status_code == 200
    decoded_data = response.data.decode('utf-8')
    
    # Kiểm tra thông tin author
    assert 'Иванов Иван Иванович' in decoded_data
    
    # Kiểm tra không có comments (vì fixture posts_list có comments là list rỗng)
    assert 'Комментарий' not in decoded_data
    assert 'Комментарии' not in decoded_data  # Thêm check cho cả số nhiều

def test_invalid_post_access(client, mocker):
    """Test that an invalid post index returns a 404 error"""
    # Mock posts_list để trả về list có 3 phần tử
    mocker.patch('app.app.posts_list', return_value=[{}, {}, {}])
    
    # Test với index âm
    response = client.get('/post/-1')
    assert response.status_code == 404
    
    # Kiểm tra có sử dụng template 404 không
    assert b'404 Not Found' in response.data

def test_non_existent_post(client, mocker):
    """Test that a non-existent post index returns a 404 error"""
    # Mock posts_list để trả về list có 5 phần tử
    mocker.patch('app.app.posts_list', return_value=[{}, {}, {}, {}, {}])
    
    # Test với index vượt quá
    response = client.get('/post/99999')
    assert response.status_code == 404
    
    # Kiểm tra template 404 và thông báo lỗi
    assert b'404 Not Found' in response.data

# lab 2

def test_url_parameters_route(client):
    """Test basic access to URL parameters route"""
    response = client.get('/urlparameters')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert "URL Parameters" in decoded  # Kiểm tra tiêu đề trang
    assert "Full URL" in decoded       # Kiểm tra một phần nội dung đặc trưng

def test_url_parameters_with_query(client):
    """Test URL parameters route with query string"""
    response = client.get('/urlparameters?name=John&age=30')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert "name=John" in decoded
    assert "age=30" in decoded

def test_url_components_display(client):
    """Test that all URL components are displayed"""
    response = client.get('/urlparameters?test=123')
    decoded = response.data.decode('utf-8')
    assert "Full URL" in decoded
    assert "Base URL" in decoded
    assert "Path" in decoded
    assert "Query String" in decoded
    assert "test=123" in decoded


def test_url_parameters_route(client):
    """Test basic access to URL parameters route"""
    response = client.get('/urlparameters?test=123')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert "URL Parameters" in decoded
    assert "test=123" in decoded  # Kiểm tra query string được hiển thị

def test_headers_display(client):
    """Test that headers are properly displayed"""
    response = client.get('/show_headers', headers={'User-Agent': 'Test-Agent'})
    decoded = response.data.decode('utf-8')
    assert "User-Agent" in decoded
    assert "Test-Agent" in decoded

def test_multiple_headers(client):
    """Test with multiple custom headers"""
    custom_headers = {
        'X-Custom-Header': 'Value1',
        'Accept-Language': 'en-US'
    }
    response = client.get('/show_headers', headers=custom_headers)
    decoded = response.data.decode('utf-8')
    for name, value in custom_headers.items():
        assert name in decoded
        assert value in decoded


def test_cookies_route_initial(client):
    """Test cookies route when no cookie is set"""
    response = client.get('/cookies')
    assert response.status_code == 200
    assert "Cookie not set" in response.data.decode('utf-8')

def test_cookies_set_and_delete(client):
    """Test cookie setting and deletion cycle"""
    # First request should set cookie
    response1 = client.get('/cookies')
    assert 'my_cookie=cookie_value' in response1.headers.get('Set-Cookie', '')

    # Second request should delete cookie
    response2 = client.get('/cookies')
    # Kiểm tra header Set-Cookie có chứa thông tin xóa cookie
    assert 'my_cookie=;' in response2.headers.get('Set-Cookie', '')
    assert 'Expires=Thu, 01 Jan 1970' in response2.headers.get('Set-Cookie', '')

def test_cookies_persistence(client):
    """Test cookie persistence between requests"""
    # First request sets cookie
    r1 = client.get('/cookies')
    assert 'my_cookie=cookie_value' in r1.headers.get('Set-Cookie', '')
    assert "Cookie not set" in r1.data.decode('utf-8')

    # Second request should show cookie is set
    r2 = client.get('/cookies')
    assert "Cookie is set" in r2.data.decode('utf-8')

    # Fourth request should be back to initial state
    r3 = client.get('/cookies')
    assert "Cookie not set" in r3.data.decode('utf-8')


def test_form_parameters_get(client):
    """Test form parameters route with GET method"""
    response = client.get('/form_parameters')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert 'name="name"' in decoded     # Trường input name
    assert 'name="email"' in decoded    # Trường input email
    assert 'name="message"' in decoded  # Trường input message

def test_form_parameters_post_empty(client):
    """Test form submission with empty data"""
    response = client.post('/form_parameters', data={})
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert "name" in decoded  # Field should still appear in output

def test_form_parameters_post_with_data(client):
    """Test form submission with valid data"""
    test_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'message': 'Test message'
    }
    response = client.post('/form_parameters', data=test_data)
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    for value in test_data.values():
        assert value in decoded


def test_phone_form_get(client):
    """Test phone number form GET request"""
    response = client.get('/formnumberphone')
    assert response.status_code == 200

def test_phone_form_valid_number(client):
    """Test with valid phone number"""
    test_cases = [
        ('0123456789', '8-012-345-67-89'),
        ('81234567890', '8-123-456-78-90'),
        ('+71234567890', '8-123-456-78-90'),
        (' 012 345 6789 ', '8-012-345-67-89')
    ]

    for input_num, expected_format in test_cases:
        response = client.post('/formnumberphone',
                             data={'phone_number': input_num},
                             follow_redirects=True)
        
        decoded = response.data.decode('utf-8')
        assert response.status_code == 200
        assert "Success!!!" in decoded
        assert expected_format in decoded

def test_phone_form_formatting(client, mocker):
    """Test phone number formatting"""
    # Mock hàm valid_phone_number để luôn trả về False (valid)
    mocker.patch('app.FuncPY.CheckAndFomatNP.valid_phone_number', return_value=False)
    
    # Mock hàm format_phone_number
    mocker.patch('app.FuncPY.CheckAndFomatNP.format_phone_number', return_value='TEST-FORMATTED')
    
    response = client.post('/formnumberphone', 
                         data={'phone_number': '0123456789'},
                         follow_redirects=True)
    
    decoded = response.data.decode('utf-8')
    print(decoded)  # Debug: In ra HTML response
    
    assert response.status_code == 200

def test_navigation_between_routes(client):
    """Test user can navigate between different routes"""
    routes = ['/', '/about', '/posts', '/urlparameters', '/show_headers', '/cookies', '/form_parameters', '/formnumberphone']
    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, f"Failed on route {route}"

# lab 3

def test_count_of_visits_first_time(client):
    """Test visit counter on first visit"""
    with client:
        response = client.get('/countofvisits')
        assert response.status_code == 200
        # Проверяем, что счётчик установлен в сессии
        assert 'visit_count' in session
        assert session['visit_count'] == 1
        # Проверяем, что значение отображается в ответе
        assert b'1' in response.data

def test_count_of_visits_multiple(client):
    """Test visit counter increments correctly"""
    with client:
        # Первый визит
        client.get('/countofvisits')
        # Второй визит
        response = client.get('/countofvisits')
        assert session['visit_count'] == 2
        assert b'2' in response.data

def test_user_auth_get(client):
    """Test UserAuth route with GET method"""
    response = client.get('/UserAuth')
    assert response.status_code == 200
    assert b'Login' in response.data

@pytest.fixture
def test_user():
    return {
        'id': 1,
        'username': 'user',
        'password': 'qwerty'
    }

class User(UserMixin):
    def __init__(self,id, username, password):
        self.id = id 
        self.username = username
        self.password = password
# Фикстура для аутентифицированного пользователя
@pytest.fixture
def authenticated_user(app, test_user):
    user = User(test_user['id'], test_user['username'], test_user['password'])
    return user


def test_user_auth_successful_login(client, test_user):
    """Test successful user authentication"""
    response = client.post('/UserAuth', data={
        'username': test_user['username'],
        'password': test_user['password'],
        'RememberMe': 'on'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_user_auth_failed_login(client):
    """Test failed user authentication"""
    response = client.post('/UserAuth', data={
        'username': 'wrong',
        'password': 'wrong'
    })
    assert response.status_code == 200

def test_check_login_authenticated(client, authenticated_user):
    """Test checklogin route with authenticated user"""
    # Đăng nhập trước khi test
    with client:
        # 1. Thực hiện đăng nhập
        login_response = client.post('/UserAuth', data={
            'username': authenticated_user.username,
            'password': authenticated_user.password
        }, follow_redirects=True)
        assert login_response.status_code == 200
        
        # 2. Kiểm tra route /checklogin khi đã đăng nhập
        checklogin_response = client.get('/checklogin')
        assert checklogin_response.status_code == 200
        
        decoded_response = checklogin_response.data.decode('utf-8')
        assert 'Привет' in decoded_response
        assert authenticated_user.username in decoded_response

def test_check_login_unauthenticated(client):
    """Test checklogin route with unauthenticated user"""
    response = client.get('/checklogin')
    assert response.status_code == 200
    decoded = response.data.decode('utf-8')
    assert 'Вы не вошли в систему' in decoded

def test_logout_route(client, authenticated_user):
    """Test logout functionality"""
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

def test_secret_page_authenticated(client, authenticated_user):
    """Test access to secret page when authenticated"""
    response = client.get('/secretpage')
    assert response.status_code == 200
