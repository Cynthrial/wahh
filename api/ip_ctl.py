from flask import  redirect, url_for, request, Blueprint
import requests

ip = Blueprint('ip', __name__)


@ip.route('/choose')
def choose():
    _time = request.args.get("time")
    _ip = request.args.get("ip")
    _value = request.args.get("value")
    _action = request.args.get("action")
    if _action == 'get':
        return redirect(url_for('ip.get', time=_time, ip=_ip, value=_value))
    if _action == 'add':
        return redirect(url_for('ip.add', time=_time, ip=_ip, value=_value))
    if _action == 'set':
        return redirect(url_for('ip.set', time=_time, ip=_ip, value=_value))
    if _action == 'delete':
        return redirect(url_for('ip.delete', time=_time, ip=_ip, value=_value))
    return "ip fail"


@ip.route('/get')
def get():
    _ip = request.args.get("ip")
    payload = {'action': 'get', 'ip': _ip}
    url = "http://10.59.17.33:5460/api/ip_dict"
    result = requests.get(url, params=payload)
    return result.text


@ip.route('/add')
def add():
    _value = request.args.get("value")
    _ip = request.args.get("ip")
    _time = request.args.get("time")
    payload = {'action': 'add', 'ip': _ip, 'value': _value, 'time': _time}
    url = "http://10.59.17.33:5460/api/ip_dict"
    result = requests.get(url, params=payload)
    return result.text


@ip.route('/delete')
def delete():
    _ip = request.args.get("ip")

    payload = {'action': 'add', 'ip': _ip}
    url = "http://10.59.17.33:5460/api/ip_dict"
    result = requests.get(url, params=payload)
    return result.text


@ip.route('/set')
def set():
    _value = request.args.get("value")
    _ip = request.args.get("ip")
    _time = request.args.get("time")
    payload = {'action': 'add', 'ip': _ip, 'value': _value, 'time': _time}
    url = "http://10.59.17.33:5460/api/ip_dict"
    result = requests.get(url, params=payload)
    return result.text
