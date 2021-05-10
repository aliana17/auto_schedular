import requests
import json, os
from flask import  Flask, render_template, session, flash
from flask import request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import models, const

app = Flask(__name__)
app.config['SECRET_KEY'] = '_5#y2L"F4Q8z\n\xec]/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

upload_path = r"E:\auto_schedular\uploads"
app.config['UPLOAD_FOLDER'] = upload_path
#db.init_app(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/schedular'

@app.route('/')
def login():
    if 'loggedin' in session:
        username = print(session.get('curr_user'))
        return redirect(url_for('get_dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    error = None
    tg_user_otp_received = request.form['otp']
    new_sess = models.Session()
    tg_user = new_sess.query(models.User.tg_username).filter(models.User.otp==tg_user_otp_received).all()
    print("printing tg_user")
    print(tg_user)

    if not tg_user:
        flash('Please generate an OTP using telegram')
        error = "Invalid OTP. Please generate an OTP using telegram bot"
        return render_template('login.html', error = error)
    else:
        session['loggedin'] = True
        session['curr_user'] = str(tg_user[0][0])
        print(session.get('curr_user'))
        return redirect(url_for('get_dashboard'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    return redirect(url_for('login'))
    
@app.route('/dashboard/')
def get_dashboard():
    #    tg_handle_of_user = request.args['tg_handle_of_user']
    if 'loggedin' in session:
        tg_handle_of_user = session.get('curr_user')
        new_session = models.Session()
        try:
            u_id = new_session.query(models.User.id).filter(models.User.tg_username==tg_handle_of_user).all()
            u_id = u_id[0][0]
            session['curr_user_id'] = u_id
            group_names_of_user = new_session.query(models.Group).filter(models.Link.user_id==u_id).all()
            print("group_names")
            print(group_names_of_user)
            groups_id_of_user = new_session.query(models.Link.group_id).filter(models.Link.user_id==u_id).all()
            data = []
            for row in groups_id_of_user:
                data.append([x for x in row])    
            session['groups_id_of_user'] = data
            print("Inside dashboard")
            print(groups_id_of_user)



            #session['group_names_displayed'] = group_names_of_user
            #print(session.get('groups_id_of_user'))
        finally:
            new_session.close()
        return render_template('dashboard.html',tg_handle_of_user = tg_handle_of_user, groups_details = group_names_of_user)
    else:
        return render_template('login.html')

@app.route('/message')
def message_form():
    return render_template('message.html', status="None")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/user_message/', methods=['POST'])    
def send_message():
    platform = []
    media = request.files['file']
    msg = request.form['msg']
    if media and allowed_file(media.filename):
            filename = secure_filename(media.filename)
            media.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    if request.form.get('cb1'):
        from platforms.facebook import Facebook
        sess = models.Session()
        u_id = session.get('curr_user_id')
        page_id = sess.query(models.Event.fb_pg_id).filter(models.Event.user_id==u_id).all()
        print(u_id)
        print(page_id)
        fb_page_access_token = sess.query(models.Event.fb_token).filter(models.Event.user_id==u_id).all()
        if not page_id:
            return render_template('message.html', status="Please add your facebook credentials")
        
        # add media for posting 
        page_id = page_id[0][0]
        print(page_id)
        res = Facebook.event_call(page_id,fb_page_access_token,msg)
        if (res.status_code):
            platform.append("Facebook")
        print(res.text)

    if request.form.get('cb2'):
        import tweepy
        print("inside twitter")
        platform.append("Twitter")
    
    if request.form.get('cb4'):
        print("Inside telegram")
        from platforms.telegram import Telegram
        groups_id_of_user = session.get('groups_id_of_user')
        print(str(groups_id_of_user))
        tg_token = const.tg_token
        Telegram.event_call(tg_token,groups_id_of_user,msg)
        platform.append("Telegram")
    
    return render_template('message.html', status=platform)

@app.route('/select_group',methods=['POST'])
def select_group():
    req = request.get_json()
    session.pop('groups_id_of_user', None)
    data = []
    for row in req:
        data.append([row]) 
    session['groups_id_of_user'] = data
    print(session.get('groups_id_of_user'))
    return "abc"

@app.route('/config_accounts',methods=['POST'])
def account_config():
    fb_token = request.form['fb_token']
    twitter_token = request.form['twitter_token']
    linkedin_token = request.form['linkedin_token']
    fb_page_id = request.form['fb_page_id']
    config_session = models.Session()
    u_id = session.get('curr_user_id')
    models.Event.insert_record(config_session, str(fb_token), str(twitter_token), str(linkedin_token),fb_page_id, u_id)
    #config_session.close()
    return redirect(url_for('get_dashboard'))

if __name__=='__main__':
    app.run(host='localhost',port=8080,debug=True)
    

