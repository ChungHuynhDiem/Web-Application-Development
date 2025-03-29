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
        template, context = templates[0]
        assert template.name == 'index.html'
        
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
