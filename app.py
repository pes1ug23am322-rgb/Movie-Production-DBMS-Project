from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Production, Crew, Casting, Budget, Award, Review
from config import get_db_uri
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'studentproject'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    stats = {
        'productions': Production.query.count(),
        'users': User.query.count(),
        'reviews': Review.query.count()
    }
    return render_template('index.html', stats=stats)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        try:
            u = User(
                name=request.form['name'],
                email=request.form['email'],
                role=request.form['role']
            )
            db.session.add(u)
            db.session.commit()
            flash("User added successfully!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Email already exists!", "danger")
        return redirect(url_for('users'))
    return render_template('users.html', users=User.query.all())

@app.route('/productions', methods=['GET', 'POST'])
def productions():
    if request.method == 'POST':
        p = Production(
            title=request.form['title'],
            genre=request.form['genre'],
            language=request.form['language'],
            director=request.form['director']
        )
        db.session.add(p)
        db.session.commit()
        flash("Production added!", "success")
        return redirect(url_for('productions'))
    return render_template('productions.html', productions=Production.query.all())

@app.route('/crew', methods=['GET', 'POST'])
def crew():
    if request.method == 'POST':
        c = Crew(
            prod_id=request.form['prod_id'],
            name=request.form['name'],
            role=request.form['role']
        )
        db.session.add(c)
        db.session.commit()
        flash("Crew added!", "success")
        return redirect(url_for('crew'))
    return render_template('crew.html', crew=Crew.query.all(), productions=Production.query.all())

@app.route('/casting', methods=['GET', 'POST'])
def casting():
    if request.method == 'POST':
        c = Casting(
            prod_id=request.form['prod_id'],
            actor_name=request.form['actor_name'],
            character_name=request.form['character_name']
        )
        db.session.add(c)
        db.session.commit()
        flash("Casting added!", "success")
        return redirect(url_for('casting'))
    return render_template('casting.html', casting=Casting.query.all(), productions=Production.query.all())

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == 'POST':
        try:
            b = Budget(
                prod_id=request.form['prod_id'],
                estimated_cost=request.form['estimated_cost'],
                actual_cost=request.form['actual_cost']
            )
            db.session.add(b)
            db.session.commit()
            flash("Budget added!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Budget for this production already exists.", "danger")
        return redirect(url_for('budget'))
    return render_template('budget.html', budget=Budget.query.all(), productions=Production.query.all())

@app.route('/awards', methods=['GET', 'POST'])
def awards():
    if request.method == 'POST':
        a = Award(
            prod_id=request.form['prod_id'],
            name=request.form['name'],
            category=request.form['category'],
            year=request.form['year']
        )
        db.session.add(a)
        db.session.commit()
        flash("Award added!", "success")
        return redirect(url_for('awards'))
    return render_template('awards.html', awards=Award.query.all(), productions=Production.query.all())

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        r = Review(
            prod_id=request.form['prod_id'],
            user_id=request.form['user_id'],
            rating=request.form['rating'],
            comment=request.form['comment']
        )
        db.session.add(r)
        db.session.commit()
        flash("Review added!", "success")
        return redirect(url_for('reviews'))
    return render_template('reviews.html', reviews=Review.query.all(), productions=Production.query.all(), users=User.query.all())

@app.route('/reports')
def reports():
    top_movies = db.session.query(
        Production.title, func.avg(Review.rating)
    ).join(Review).group_by(Production.prod_id).all()

    budget_variance = db.session.query(
        Production.title, Budget.estimated_cost, Budget.actual_cost,
        (Budget.actual_cost - Budget.estimated_cost).label("variance")
    ).join(Budget).all()

    return render_template('reports.html', top_movies=top_movies, budget_variance=budget_variance)

@app.route('/seed')
def seed():
    if not User.query.first():
        db.session.add_all([
            User(name="Alice", email="alice@gmail.com", role="Viewer"),
            User(name="Bob", email="bob@gmail.com", role="Producer")
        ])
    if not Production.query.first():
        db.session.add_all([
            Production(title="Inception", genre="Sci-Fi", language="English", director="Nolan"),
            Production(title="Pushpa", genre="Action", language="Telugu", director="Sukumar")
        ])
    db.session.commit()
    flash("Seed data added!", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
