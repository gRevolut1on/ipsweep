from flask import Flask, render_template, request, redirect
from models import db, login, UserModel
from flask_login import login_required, current_user, login_user, logout_user

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFCATIONS']= False
app.secret_key="XXYSSS"

db.init_app(app)
login.init_app(app)

login.login_view= 'login'

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/blogs')

    if request.method == 'POST':
        email= request.form['email']
        user= UserModel.query.filter_by(email= email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/blogs')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/blogs')

    if request.method == 'POST':
        email= request.form['email']
        username= request.form['username']
        password= request.form['password']

        if UserModel.query.filter_by(email=email).first():
            return ('Email already present')
        
        user= UserModel(email=email, username= username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/blogs')
@login_required
def blog():
    return render_template('blog.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/blogs')

if __name__=="__main__":
    app.run(debug=True)