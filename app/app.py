from datetime import timedelta
import random
from functools import lru_cache
from flask import Flask, render_template, abort, request, make_response,session,redirect, url_for
from FuncPY.CheckAndFomatNP import valid_phone_number, format_phone_number
# from app.FuncPY.CheckAndFomatNP import valid_phone_number, format_phone_number
from flask_login import LoginManager,login_user,UserMixin,logout_user,current_user,login_required
from faker import Faker
fake = Faker()
app = Flask(__name__)
application = app
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
# Thiết lập khóa bí mật để Flask có thể sử dụng session
app.secret_key = 'chunghuynhdiem'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'UserAuth'  # tên function, không phải URL


users = {
    "user": {
        "id": 1,
        "username": "user",
        "password": "qwerty"
    }
}


images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments(),
        'avatarclient': 'client.jpg',
    }

# Định nghĩa hàm create_app
# def create_app():
#     app = Flask(__name__)

@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list())

@app.route('/post/<int:index>')
def post(index):
    posts = posts_list()
    if index < 0 or index >= len(posts):  # Kiểm tra index hợp lệ
        abort(404)  # Trả về trang lỗi 404 nếu index không tồn tại
    p = posts[index]
    print(p['comments'])
    return render_template('post.html', title=p['title'], post=p)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.route('/urlparameters')
def show_url_params():
    # return render_template("urlparameters.html", params=request.args)
        # Lấy các thành phần của URL
    full_url = request.url  # Full URL
    base_url = request.base_url  # URL mà không có query string
    path = request.path  # Đường dẫn (path)
    args = request.args  # Các tham số query
    query_string = request.query_string  # Query string nguyên bản

    # Trả các thành phần cho template
    return render_template("urlparameters.html", full_url=full_url, base_url=base_url, path=path, args=args, query_string=query_string)

@app.route('/show_headers')
def show_headers():
    headers = []
    for key, value in request.headers.items():
        headers.append({'name': key, 'value': value})

    return render_template("RequestHeaders.html", headers=headers)

@app.route('/cookies', methods=['GET', 'POST'])
def cookies():
    if 'my_cookie' not in request.cookies:
        resp = make_response(render_template("Cookies.html", message="Cookie not set. Setting cookie now."))
        resp.set_cookie('my_cookie', 'cookie_value')  # Set cookie
        return resp
    else:
        resp = make_response(render_template("Cookies.html", message="Cookie is set. Deleting cookie now."))
        resp.delete_cookie('my_cookie')  # Delete cookie
        return resp
    
@app.route('/form_parameters', methods=['GET', 'POST'])
def form_parameters():
    # Nếu phương thức là POST (tức là form đã được gửi)
    if request.method == 'POST':
        # Lấy các giá trị từ form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Trả về trang với giá trị đã nhập
        return render_template("FormParameters.html", name=name, email=email, message=message)

    # Nếu phương thức là GET, chỉ hiển thị form
    return render_template("FormParameters.html")

@app.route('/formnumberphone', methods=['GET', 'POST'])
def form_number():
    error = None
    formatted_number = None
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        validation_error = valid_phone_number(phone_number)
        if validation_error:
            error = validation_error
        else:
            error = "Success!!!"
            formatted_number = format_phone_number(phone_number)
    return render_template("CheckPhoneNumber.html",
                         error=error,
                         phone_number=formatted_number)

@app.route('/countofvisits')
def countofvisits():
    if 'visit_count' in session:
        session['visit_count'] +=1
    else:
        session['visit_count']=1
    return render_template('VisitorCount.html',resultcount = session['visit_count'])

@login_manager.user_loader
def load_user(user_id):
    for user_data in users.values():
        if str(user_data['id']) == str(user_id):
            return User(user_data['id'], user_data['username'], user_data['password'])
    return None

class User(UserMixin):
    def __init__(self,id, username, password):
        self.id = id 
        self.username = username
        self.password = password

def get_user_by_username(username, password):
    user_data = users.get(username)
    if user_data and user_data['password'] == password:
        return User(user_data['id'], user_data['username'], user_data['password'])
    return None


@app.route('/UserAuth', methods=['GET', 'POST'])
def UserAuth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'RememberMe' in request.form

        user = get_user_by_username(username, password)
        if(user):
            login_user(user, remember=remember)
            return render_template('index.html',Status=True)
        else:
            return render_template('UserAuthentication.html',Status=False)
 
    return render_template('UserAuthentication.html',Status=True)

from flask_login import current_user

# Trong một route
@app.route('/checklogin')
def checklogin():
    return render_template('checklogin.html',current_user=current_user)
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('UserAuth'))

@app.route('/secretpage')
def SecretPage():
    if current_user.is_authenticated:
        return render_template('secretpage.html')
    else:
        return render_template('UserAuthentication.html',StatusDanger=False)

if __name__ == '__main__':
    app.run(debug=True)