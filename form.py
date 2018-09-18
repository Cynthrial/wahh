# !/usr/bin/env python 
# -*- coding:utf-8 -*-
# Auth: Conners Chan
# 2018/8/30   14:14


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, HiddenField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, IPAddress


# form test : What is your name?
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# this filed is for choosing the log_view
class SelectTime(FlaskForm):
    start_time = DateField('起始时间', format='%Y-%m-%d')
    end_time = DateField('结束时间', format='%Y-%m-%d')
    select_method = SelectField('请求方式', choices=(['', '不限'], ['GET', 'GET'], ['POST', 'POST']))
    mod_type = SelectField('监控模式', choices=(
        ['args', 'args_Mod'], ['post', 'post_mod'], ['remote_ip', 'remote_ip'], ['base', 'base'],
        ['cookie', 'cookie_Mod'], ['network', 'network_Mod'], ['uri', 'uri_Mod'],
        ['user_agent', 'userAgent_Mod']
    ))
    submit = SubmitField('Submit')


class ConfigForm(FlaskForm):
    mod = SelectField('监控模式', choices=(
        ['args_Mod', 'args_Mod'], ['post_Mod', 'post_mod'], ['base', 'base'],
        ['cookie_Mod', 'cookie_Mod'], ['network_Mod', 'network_Mod'], ['uri_Mod', 'uri_Mod'],
        ['useragent_Mod', 'userAgent_Mod']
    ))
    id = StringField('规则编号', default='null')
    value_type = HiddenField('value_type', default='json')
    value = TextAreaField('value', render_kw={'placeholder': u'eg:\r{\r'
                                                             u'\t"state": "on" / "off",\r'
                                                             u'\t"action": ["log"] / ["allow"] / ["deny"],\r'
                                                             u'\t"hostname": ["127.0.0.1",""],\r'
                                                             u'\t"uri": ["^/log$","jio"],\r'
                                                             u'}'
                                              })
    action = SelectField('操作参数', choices=(['get', 'get'], ['set', 'set'], ['delete', 'del'],
                                          ['save', 'save'], ['add', 'add'], ['open', 'open'],
                                          ['close', 'off'], ['reload', 'reload'], ['search', 'search']))
    waf_action = SelectField('waf_action', choices=(['nul', ''], ['allow', 'allow'], ['deny', 'deny']))
    waf_state = SelectField('waf_state', choices=(['nul', ''], ['on', 'on'], ['off', 'off']))


class ConfigIp(FlaskForm):
    action = SelectField('操作参数', choices=(['get', 'get'], ['set', 'set'], ['delete', 'del'],
                                          ['save', 'save'], ['add', 'add']))
    ip = StringField('IP地址', default='0.0.0.0', validators=[IPAddress()])

    valid_time = IntegerField('生效时长(s)')
    value = SelectField('Waf_Action', choices=(['deny', 'deny'], ['allow', 'allow']))
