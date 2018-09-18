from flask import Blueprint, request, jsonify, json
from form import *
from models.db import select

log_view = Blueprint('log_view', __name__)


@log_view.route('/mystring')
def mystring():
    return 'my string'


@log_view.route('/dataFromAjax')
def dataFromAjax():
    test = request.args.get('mydata')
    print(test)
    return 'dataFromAjax'


@log_view.route('/mydict', methods=['GET', 'POST'])
def mydict():
    print('post')
    if request.method == 'POST':
        a = request.form['mydata']
        print(a)
    d = {'name': 'yzm', 'age': 18}
    return jsonify(d)


@log_view.route('/name', methods=['POST'])
def getname():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    d = {'name': firstname + ' ' + lastname, 'age': 18}
    print(d)
    return jsonify(d)


@log_view.route('/myform', methods=['POST'])
def myform():
    print('post')
    a = request.form['FirstName']
    print(a)
    d = {'name': 'xmr', 'age': 18}
    return jsonify(d)


@log_view.route('/mylist')
def mylist():
    l = ['xmr', 18]
    print('mylist')
    return json.dumps(l)  # 用jsonify前端会出错


@log_view.route('/mytable')
def mytable():
    table = [('id', 'name', 'age', 'score'),
             ('1', 'xiemanrui', '18', '100'),
             ('2', 'yxx', '18', '100'),
             ('4', 'bbb', '19', '99'),
             ('3', 'yaoming', '37', '88')
             ]
    print('mytable')
    data = json.dumps(table)
    print(data)
    return data


@log_view.route('/ajax/', methods=['POST'])
def ajax():
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    select_method = request.form.get('select_method')
    mod_type = request.form.get('mod_type')
    r = select(start_time, end_time, select_method, mod_type)
    count = len(r)
    result = waf_log_json(r, count)
    return json.dumps(result)


'''
    table = [('id', 'name', 'age', 'score'),
             ('1', 'xiemanrui', '18', '100'),
             ('2', 'yxx', '18', '100'),
             ('3', 'yaomingsadas', '37', '88'),
             ('4', 'yangziming', '19', '99')]

    print('mytable')
    data = json.dumps(table)
    print(data)
    return data
    # if hh.validate_on_submit():
    #     result = {"status": "success"}
    # else:
    #     result = {"status": "fail"}
    # return json.dumps(result)
'''


# waf log to json   for print the log to log_view
#    eg: print json.dumps([your obj], default=waf_log_json)
def waf_log_json(obj,count):
    result = {}
    for i in range(count):
        result[i] = {
            "no": obj[i].no,
            "time": obj[i].time,
            "remote_ip": obj[i].remote_ip,
            "host": obj[i].host,
            "ip": obj[i].ip,
            "method": obj[i].method,
            "status": obj[i].status,
            "request_uri": obj[i].request_uri,
            "referer": obj[i].referer,
            "waf_log": obj[i].waf_log,
            "cookie": obj[i].cookie,
            "posts": obj[i].posts,
            "args": obj[i].args,
            "headers": obj[i].headers
        }
    return result