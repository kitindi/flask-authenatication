from flask import Flask, request,render_template, redirect, url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = "your_secret_key"


# configure the SQLAlchemy 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRAC_MODIFICATIONs'] = False


db = SQLAlchemy(app)

# createing user model  
class UserModel(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password_hash = db.Column(db.String(120), nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username
        
        def set_password(self, password):
            self.password_hash = generate_password_hash(password)
        
        def check_password(self, password):
            return check_password_hash(self.password_hash, password)
        


@app.route('/')
def index():
 
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('index.html')


# login
@app.route('/login', methods=['POST'])
def login():
    # collect info from the form
      username = request.form['username']
      password = request.form['password']
      user = UserModel.query.filter_by(username = username).first()
      
     # Check if the user is already logged in
     
      if user and user.check_password(password):
          session['username'] = username
          return redirect(url_for('dashboard'))
      else:
          return render_template('index.html')
          
# register  
@app.route('/register', methods=['POST', 'GET'])

def register():
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        user = UserModel.query.filter_by(username = username).first()
    
        if user:
            return render_template('register.html',error="User already exists")
        else:
            new_user = UserModel(username = username)
            new_user.set_password(password)
        
            db.session.add(new_user)
            db.session.commit()
        
            session['username'] = username
        
            return  redirect(url_for('dashboard'))
    else:  
         return render_template('register.html')
        
    

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else: 
        return redirect(url_for('index'))




# Logout

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
    
    







if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
  
    app.run(debug=True)
    

    