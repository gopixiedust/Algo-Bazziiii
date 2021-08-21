from flask import Blueprint,render_template,redirect,url_for,request
from flask.helpers import flash
auth = Blueprint('auth', __name__)

import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def check(email):
    if(re.match(regex, email)):
        return True
    else:
        return False

# validate password
def password_check(passwd):
	
	SpecialSym =['$', '@', '#', '%']
	val = True
	
	if len(passwd) < 6:
		flash('length should be at least 6 ', 'error')
		val = False
		
	if len(passwd) < 8:
		flash('Password Length should be greater than 8 ', 'error')
		val = False
		
	if not any(char.isdigit() for char in passwd):
		flash('Password should have at least one numeral ', 'error')
		val = False
		
	if not any(char.isupper() for char in passwd):
		flash('Password should have at least one uppercase letter ', 'error')
		val = False
		
	if not any(char.islower() for char in passwd):
		flash('Password should have at least one lowercase letter ', 'error')
		val = False
		
	if not any(char in SpecialSym for char in passwd):
		flash('Password should have at least one of the symbols " $ @ # " ', 'error')
		val = False
	if val:
		return val


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('logemail')
        password=request.form.get('logpass')
        print(email,password)
        if not check(email):
            flash('Invalid email address', 'error')
            return redirect(url_for('auth.login'))
        if not password_check(password):
            flash('Invalid password', 'error')
            return redirect(url_for('auth.login'))

        
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "<h1>LOGOUT</h1>"
