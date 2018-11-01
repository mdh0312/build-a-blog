from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:foobar@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods = ['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['post_title']
        body = request.form['post_body']
        title_error = ""
        body_error = ""

        if title == "":
            title_error = "Please enter the title"

			
        if body == "":
            body_error = "Please type something to post"


        if (title_error  != "") or (body_error != ""):
            return render_template('newpost.html', title_error = title_error, 
            body_error = body_error, post_title = title, body = body)
        else:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            posts = Blog.query.all()
            last = posts[len(posts)-1]
            return redirect('/blog?id=' + str(last.id))

    return render_template('newpost.html', title = 'New Post')

@app.route('/blog', methods = ['POST', 'GET'])
def index():

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = Blog.query.get(int(post_id))
        return render_template('post.html', post = post, title = 'Blog Post')
    
    posts = Blog.query.all()
    return render_template('blog.html', title = "Blog", posts = posts)
        
if __name__ == '__main__':
    app.run()