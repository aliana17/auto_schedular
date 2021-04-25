from flask import  Flask, render_template
from flask import request, redirect, url_for
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = '_5#y2L"F4Q8z\n\xec]/'
#db.init_app(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/schedular'

@app.route('/')
def login():
#   tg_user_otp=request.form['otp']
#    if tg_user_otp in session:
#        return redirect(url_for(get_dashboard))
    
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    error = None
    tg_user_otp_received = request.form['otp']
    import models
    new_sess = models.Session()
    check_tg_user_otp = new_sess.query(models.Otp).filter(models.Otp.otp==tg_user_otp_received).all()
    tg_user = new_sess.query(models.Otp.tg_username).filter(models.Otp.otp==tg_user_otp_received).all()
#    session['credentials'] = tg_user
    if not check_tg_user_otp:
        flash('Please generate an OTP using telegram')
        error = "Invalid OTP. Please generate an OTP using telegram bot"
        return render_template('login.html', error = error)
    else:
        return redirect(url_for('get_dashboard',tg_handle_of_user = tg_user))
    
@app.route('/dashboard/')
def get_dashboard():
#    messages = request.args['credentials']  # counterpart for url_for()
#    messages = session['credentials'] 
    tg_handle_of_user = request.args['tg_handle_of_user']
    return render_template('dashboard.html',tg_handle_of_user = tg_handle_of_user)

if __name__=='__main__':
    app.run(host='localhost',port=8080,debug=True)
    

