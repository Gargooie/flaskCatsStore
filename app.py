from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True

db=SQLAlchemy(app)



search = Search()
search.init_app(app)

class Cat(db.Model):
    __tablename__ = 'cat'
    __searchable__  = ['title', 'breed', 'age', 'description']
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    breed =db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def home():
    return redirect('/1')


@app.route('/<int:page_num>')
def index(page_num):

    cats = Cat.query.paginate(per_page=6, page=page_num, error_out=False)
    # cats = Cat.query.all()
    return render_template('index.html', data=cats)

@app.route('/<int:page_num>/<order>')
def ordered(page_num,order):

    cats = Cat.query.order_by(order).paginate(per_page=6, page=page_num, error_out=False)
    # cats = Cat.query.all()
    return render_template('index.html', data=cats)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    keyword = request.args.get('query')
    cats = Cat.query.msearch(keyword, fields=['title', 'price'])
    # return render_template("home.html", title='Searching..' + keyword, posts=posts)
    # cats = Cat.query.whoosh_search(request.args.get('query')).all()
    return render_template('search.html', data=cats)

@app.route('/detailed/<int:id>')
def detailed(id):
    cats = Cat.query.get(id)
    # return render_template("home.html", title='Searching..' + keyword, posts=posts)
    # cats = Cat.query.whoosh_search(request.args.get('query')).all()
    return render_template('detailed.html', data=cats)


@app.route('/create', methods=['POST', "GET"])
def create():
    if request.method=="POST":
        title = request.form['title']
        price = request.form['price']

        cat = Cat(title=title, price=price)
        try:
            db.session.add(cat)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

