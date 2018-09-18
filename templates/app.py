from flask import Flask, render_template, session, redirect, url_for, make_response, flash, request
from flask_bootstrap import Bootstrap
from form import *
import requests
from flask_datepicker import datepicker
from logview import log_view
from api.config_ctl import ctl
from api.ip_ctl import ip
import models.db

# from flask_nav.elements import *
# from flask_admin.contrib.fiTrueleadmin import FileAdmin

ssourl = 'http://10.59.3.216:8080/'
inssourl = 'http://10.59.3.216:8080/'
loginurl = 'http://10.59.17.32:5000/login'

app = Flask(__name__)
app.register_blueprint(log_view)
app.register_blueprint(ctl)
app.register_blueprint(ip, url_prefix='/ip')
bootstrap = Bootstrap(app)
datepicker(app)
app.config['SECRET_KEY'] = 'hard to guess string'


@app.route('/', methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get('User-Agent')
    # return '< p > Your browser is % s < / p >' % user_agent
    # return '<a href="/admin/">Click me to get to Admin!</a>'

    # post / redirect /get mod
    # form = NameForm()
    # if form.validate_on_submit():
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form, name=session.get('name'))

    error = None
    if 'logged_in' in session and session.get('logged_in'):
        simple_sum = models.db.four_sky_blade()
        form = NameForm()
        if form.validate_on_submit():
            old_name = session.get('name')
            if old_name is not None and old_name != form.name.data:
                flash('Looks like you have changed your name!')
            session['name'] = form.name.data
            form.name.data = ''
            return redirect(url_for('index'))
        return render_template('index.html', form=form, name=session.get('name'), simple_sum=simple_sum)
    else:
        return redirect(url_for('login'))

# cookie response
@app.route('/res')
def res():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')  # name = answer; value = 42
    return response


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.args.get('token'):
        token_tmp = request.args.get('token')
        r = requests.get(inssourl + 'api/get_token_by_tmp_token/?token=' + token_tmp)
        token = r.json()['token']
        userinfo_json = requests.get(inssourl + 'api/get_userinfo?token=' + token)
        if userinfo_json:
            userinfo = userinfo_json.json()
            um = userinfo['um'].lower()
            session['user'] = um
            session['name'] = userinfo['name']
            session['logged_in'] = True
            referer = session.pop('referer', None)
            if referer:
                return redirect(referer)
            else:
                return redirect(url_for('index'))
            #         # referer = session.pop('referer', None)
            # #         if referer:
            # #             return redirect(referer)
            # #         else:
            # #             return redirect(url_for('index'))
            # # except BaseException, e:
            # #     print(e)

    else:
        if request.args.get('referer'):
            session['referer'] = request.args.get('referer')
        return redirect(ssourl + '/login?referer=' + loginurl)


# logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('name', None)
    session.pop('logged_in', None)

    return redirect(ssourl + '/logout?referer=' + loginurl)



@app.route('/redirect')
def redirects():
    return redirect(url_for("uploads"))


# dynamic url
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)


@app.route('/rule_admin', methods=['GET', 'POST'])
def rule_admin():
    config_form = ConfigForm()
    if config_form.validate_on_submit():
        print("hello rule_admin")
    return render_template("rule_admin.html", config_form=config_form, name=session.get('name'))


@app.route('/detail')  # used to display the log detail
def detail():
    time_s = SelectTime()

    if time_s.validate_on_submit():
        print("hello")
    return render_template("detail.html", time_s=time_s, name=session.get('name'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',name=session.get('name')), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html',name=session.get('name')), 500


@app.route('/view_test', methods=['GET', 'POST'])
def view_test():
    return render_template('viewtest.html',name=session.get('name'))


@app.route('/ip_config')  # used to display the log detail
def ip_config():
    config_ip = ConfigIp()

    if config_ip.validate_on_submit():
        print("hello")
    return render_template("ip_config.html", name=session.get('name'), config_ip=config_ip)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='10.59.17.32')
