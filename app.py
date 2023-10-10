from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_user ,LoginManager, logout_user
from flask_bcrypt import check_password_hash
from datetime import datetime



app=Flask(__name__)
db=SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
login_manager = LoginManager()
login_manager.init_app(app)



# models
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    password=db.Column(db.String(80),nullable=False)
    fname=db.Column(db.String(80),nullable=False)
 
    lname=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(80),nullable=False,unique=True)
    
class Blog(db.Model,UserMixin):
    blog_id=db.Column(db.Integer,primary_key=True)
    blog_title=db.Column(db.String(80),nullable=False)
    author=db.Column(db.String(80),nullable=False)
    content=db.Column(db.Text(),nullable=False)
    pub_date=db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)
    
try:
    db.init_app(app)
    with app.app_context():
        db.create_all()
except Exception as User:
    print(User)

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

    
@app.route("/")
def index():
    blog_posts = Blog.query.all()
    return render_template("index.html",blog_posts=blog_posts)

    
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password==user.password:
      
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        mail=request.form.get('email')
        passw=request.form.get('password')
        fname=request.form.get('firstname')
        lname=request.form.get('lastname')
        uname=request.form.get('username')
        user=User(username=uname, password=passw,fname=fname,lname=lname,email=mail)
        print(user)
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful. You can now log in.", "success")
        return redirect("/login")
    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/postblog",methods=['GET','POST'])
def postblog():
    if request.method=="POST":
        title=request.form.get('title')
        author=request.form.get('author')
        content=request.form.get('content')
        
        blog=Blog(blog_title=title,author=author,content=content)
        db.session.add(blog)
        db.session.commit()
        flash("your post has been subbmitted successfully","success")
        return redirect("/")
    return render_template('blog.html')


@app.route("/blogdetail/<int:id>",methods=['GET','POST'])
def blogdetail(id):
    blog=Blog.query.get(id)
    return render_template('blogdetail.html',blog=blog)

@app.route("/delete/<int:id>",methods=['GET','POST'])
def deletepost(id):
    blog=Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash("post has been deleted")
    return redirect('/')

@app.route("/edit/<int:id>",methods=['GET','POST'])
def editpost(id):
    blog=Blog.query.get(id)
    if request.method=='POST':
        blog.blog_title=request.form.get('title')
        blog.author=request.form.get('author')
        blog.content=request.form.get('content')
        db.session.commit()
        flash("post has been updated")
        return redirect("/")
    return render_template('edit.html',blog=blog)




if __name__=="__main__":
    app.run(debug=True)