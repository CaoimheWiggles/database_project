from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import random, os
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:caoimhe@localhost:5432/mydatabase'
app.config['SECRET_KEY'] = 'mydatabase'


db = SQLAlchemy(app)



class User(db.Model):
    

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  

    def __repr__(self):
        return f'<User {self.username}>'
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='feedbacks')

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage {self.id}>'
    

   

with app.app_context():
    db.create_all()



@app.route('/user', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    password_hash = sha256_crypt.hash(password)
    
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully"}), 201


@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"username": user.username, "email": user.email})


@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    
    username = request.json['username']
    email = request.json['email']
    
    user.username = username
    user.email = email
    db.session.commit()
    
    return jsonify({"message": "User updated successfully"})


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"})
    


poll_results = {
    "Keeping a consistent routine": 0,
    "Using positive reinforcement": 0,
    "Setting clear boundaries": 0,
    "Distracting with activities": 0
}

poll_options = ["Keeping a consistent routine", "Using positive reinforcement", "Setting clear boundaries", "Distracting with activities"]


@app.route('/')
def index():
    now = datetime.now()
    current_time = now.time()
    greeting = get_greeting(current_time)
    return render_template('index.html', greeting=greeting)

def get_greeting(current_time):
    if current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
        return 'Good morning!'
    elif current_time < datetime.strptime('17:00:00', '%H:%M:%S').time():
        return 'Good afternoon!'
    else:
        return 'Good evening!'
    

@app.route('/get_message')
def get_message():
    return jsonify({'message': 'This is a test message from the server!'})


@app.route('/featured')
def featured_post():
    return render_template('featured-post.html')


@app.route('/post1')
def post1():
    return render_template('post1.html')


@app.route('/post2')  
def post2(): 
    return render_template('post2.html', poll_results=poll_results)


@app.route('/post3')
def post3():
    return render_template('post3.html')


@app.route('/post4')
def post4():
    return render_template('post4.html')


@app.route('/post5')
def post5():
    return render_template('post5.html')


@app.route('/post6')
def post6():
    return render_template('post6.html')
    

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blogs')
def blogs():
    return render_template('blogs.html')


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        new_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('thanks_feedback'))
    
    return render_template('contact.html')


@app.route('/thanks_feedback')
def thanks_feedback():
    username = request.args.get('username', 'Guest')  
    return render_template('thanks_feedback.html', name=username)


@app.route('/feedback', methods=['POST'])
def feedback():
    if 'user_id' not in session:
        flash('You need to be logged in to leave feedback.', 'danger')
        return redirect(url_for('contact'))
    
    feedback_message = request.form['feedback_message']
    user_id = session['user_id']
    
    user = User.query.get(user_id)
    username = user.username if user else 'User'

    new_feedback = Feedback(user_id=user_id, message=feedback_message)
    db.session.add(new_feedback)
    db.session.commit()
    
    flash('Feedback submitted successfully!', 'success')
    return redirect(url_for('thanks_feedback', username=username)) 


@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    choice = data.get('choice')
    if choice in poll_results:
        poll_results[choice] += 1
    return jsonify({option: poll_results.get(option, 0) for option in poll_options})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists', 'danger')
            return redirect(url_for('register'))

        password_hash = sha256_crypt.hash(password)

        new_user = User(username=username, email=email, password_hash=password_hash)

        db.session.add(new_user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and sha256_crypt.verify(password, user.password_hash):
            session['user_id'] = user.id  
            flash('You are now logged in', 'success')
            return redirect(url_for('index'))  
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('A password reset link has been sent to your email', 'info')
        else:
            flash('No account found with that email address', 'danger')

        return redirect(url_for('login'))

    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))  


if __name__ == '__main__':
    app.run(debug=True)