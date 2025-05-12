from datetime import datetime, timedelta
import random
from functools import lru_cache
from flask import Flask, render_template, abort, request, make_response,session,redirect, url_for, jsonify, flash
from FuncPY.CheckAndFomatNP import valid_phone_number, format_phone_number
from FuncPY.CheckUserName import CheckUserName
from FuncPY.CheckPassWord import is_valid_password
# from app.FuncPY.CheckAndFomatNP import valid_phone_number, format_phone_number
from flask_login import LoginManager,login_user,UserMixin,logout_user,current_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

fake = Faker()
app = Flask(__name__)
application = app
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
# Thiết lập khóa bí mật để Flask có thể sử dụng session
app.secret_key = 'chunghuynhdiem'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'UserAuth'  # tên function, không phải URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datauser.db'  # Sử dụng SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Tắt tính năng theo dõi thay đổi
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(100))
    PassWord = db.Column(db.String(200))  
    FullName = db.Column(db.String(100))
    UserRole = db.Column(db.String(50))
    CreatedAt = db.Column(db.DateTime, default=datetime.now) #server_default=db.func.now()
    UpdatedAt = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, UserName, PassWord, FullName, UserRole):
        self.UserName = UserName
        self.PassWord = PassWord
        self.FullName = FullName
        self.UserRole = UserRole

        # Phải có hàm get_id() để Flask-Login hoạt động
    def get_id(self):
        return str(self.id)
    
    # Phải có hàm is_active để xác định người dùng có tài khoản hoạt động không
    def is_active(self):
        return True  # Bạn có thể thay đổi điều kiện này theo nhu cầu, ví dụ như kiểm tra xem người dùng có bị khóa hay không.
    # is_authenticated và is_anonymous có sẵn khi kế thừa từ UserMixin

    @property
    def is_authenticated(self):
        # Cung cấp giá trị của is_authenticated, thường sẽ là True nếu người dùng đã đăng nhập
        return True  # Giả sử người dùng đã đăng nhập
    
    @property
    def is_anonymous(self):
        # Đảm bảo rằng người dùng không phải là người ẩn danh
        return False  # Đảm bảo người dùng không phải là người ẩn danh


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
    status = request.args.get('Status')
    # Convert string to actual boolean
    # if status is not None:
    #     status = status == 'True'  # Convert "True" => True 
    print(status)
    return render_template('index.html', users = User.query.all(), current_user=current_user,Status=status)

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
    return User.query.get(int(user_id))

def get_user_by_username(username, password):
    user = User.query.filter_by(UserName=username).first()  # Lấy người dùng theo tên đăng nhập
    print(user.PassWord," ",generate_password_hash(password))
    if user and check_password_hash(user.PassWord, password):  # Kiểm tra mật khẩu
        return user
    return None


@app.route('/UserAuth', methods=['GET', 'POST'])
def UserAuth():
    next_page = request.args.get('next')  # Lấy trang đích sau khi đăng nhập
    status_danger = request.args.get('StatusDanger') 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'RememberMe' in request.form
        next_page = request.form.get('next')

        user = get_user_by_username(username, password)
        if user:
            print(user)
            login_user(user, remember=remember)
            print(next_page)
            # Nếu có next_page thì redirect tới đó, không thì về trang chính
            if next_page and next_page.lower() != 'none':
                return redirect('/' + next_page)
            else:
                return redirect(url_for('index', Status=True))

        return render_template('UserAuthentication.html', Status=False,WebContent='SignIn')
    if(status_danger=="True"):
        status_danger=True
    if(status_danger=="False"):
        status_danger=False
    return render_template('UserAuthentication.html', Status=True, StatusDanger=status_danger, WebContent='SignIn')



# Tạo bảng nếu chưa tồn tại
with app.app_context():
    db.create_all()

@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        UserName = request.form.get('UserName')
        PassWord = request.form.get('PassWord')
        FullName = request.form.get('FullName')
        UserRole = request.form.get('Role')
        hashed_password = generate_password_hash(PassWord)

        if User.query.filter_by(UserName=UserName).first():
            return render_template('UserAuthentication.html',WebContent='SignUp', Status='UsernameExists')

        Is_User=CheckUserName(UserName)
        if Is_User == False:
            return render_template('UserAuthentication.html',WebContent='SignUp', Status='IncorrectUsername')
        
        Is_PassWord=is_valid_password(PassWord)
        if Is_PassWord == False:
            return render_template('UserAuthentication.html',WebContent='SignUp', Status='IncorrectPassWord')

        print(UserName,' ',hashed_password,' ',FullName,' ',UserRole)
        new_user = User(UserName, hashed_password, FullName, UserRole)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('UserAuth', WebContent='SignIn', Status='CreatedSuccessfully'))
    return render_template('UserAuthentication.html',WebContent='SignUp') #Status=True, StatusDanger=status_danger


from flask_login import current_user

# Trong một route
@app.route('/checklogin')
def checklogin():
    print("Is authenticated: ", current_user.is_authenticated)  # Debugging line
    print(current_user)
    return render_template('checklogin.html',current_user=current_user)
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('UserAuth'))

@app.route('/secretpage')
def SecretPage():
    if current_user.is_authenticated:
        return render_template('secretpage.html', users = User.query.all())
    else:
        # Lưu lại trang cần truy cập sau khi đăng nhập bằng next
        return redirect(url_for('UserAuth', next='secretpage', StatusDanger=False))

@app.route('/user_details/<int:user_id>')
def get_user_details(user_id):
    # Kiểm tra xem user có tồn tại hay không
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'UserName': user.UserName,
            'PassWord': user.PassWord,
            'FullName': user.FullName,
            'UserRole': user.UserRole,
            'CreatedAt': user.CreatedAt,
            'UpdatedAt': user.UpdatedAt
        })
    # Trả về lỗi nếu không tìm thấy user
    return jsonify({'error': 'User not found'}), 404

@app.route('/update_user', methods=['POST'])
def update_user():
    data = request.get_json()
    user = User.query.get(data['id'])

    if user:
        user.UserName = data['UserName']
        user.PassWord = data['PassWord']
        user.FullName = data['FullName']
        user.UserRole = data['UserRole']
        user.UpdatedAt = datetime.now()

        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 404

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

@app.route('/CreateAcc', methods=['POST'])
def CreateAcc():
    data = request.get_json()  # Lấy dữ liệu JSON đúng cách
    if request.method == 'POST':
        UserName = data.get('Create_UserName')
        PassWord = data.get('Create_PassWord')
        FullName = data.get('Create_FullName')
        UserRole = data.get('Create_UserRole')
        hashed_password = generate_password_hash(PassWord)

        if User.query.filter_by(UserName=UserName).first():
            print("error")
            return redirect(url_for('index', Status='UsernameExists'))
        
        print(UserName,' ',hashed_password,' ',FullName,' ',UserRole)
        new_user = User(UserName, hashed_password, FullName, UserRole)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully'}), 200

@app.route('/ChangePassWord', methods=['POST','GET'])
@login_required
def ChangePassWord():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Данные не получены, попробуйте снова'
            }), 400

        old_pw = data.get('old_password')
        new_pw = data.get('new_password')
        confirm_pw = data.get('confirm_password')

        if not check_password_hash(current_user.PassWord, old_pw):
            return jsonify({
                'status': 'error',
                'message': 'Неверный старый пароль'
            }), 400

        if not is_valid_password(new_pw):
            return jsonify({
                'status': 'error',
                'message': 'Новый пароль не соответствует требованиям безопасности'
            }), 400

        if new_pw != confirm_pw:
            return jsonify({
                'status': 'error',
                'message': 'Пароли не совпадают'
            }), 400

        current_user.PassWord = generate_password_hash(new_pw)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Пароль успешно изменён',
            'redirect': url_for('index')
        })

    return render_template('ChangePassWord.html')


if __name__ == '__main__':
    app.run(debug=True)