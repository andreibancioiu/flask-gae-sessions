# -*- coding: utf-8 -*-

from myapp import app
from gaesession import SessionModel
from flask import render_template, request, redirect, url_for, session


@app.route('/', methods=['get', 'post'])
def index():
    if request.method == 'GET':
        return render_template('index.html', model=SessionDescription())

    create = "create" in request.form
    create_permanent = "create_permanent" in request.form
    destroy = "destroy" in request.form
    mutate = "mutate" in request.form

    if create:
        session.must_create = True
    elif create_permanent:
        session.must_create = True
        session.permanent = True
    elif destroy:
        session.must_destroy = True
    elif mutate:
        key = request.form.get("key") or "foobar"
        value = request.form.get("value")
        session["u:" + key] = value

    return redirect(url_for('index'))


class SessionDescription():

    def __init__(self):
        iface = app.session_interface

        self.sid = session.sid
        self.is_permanent = session.permanent
        self.data = dict(session)
        self.renewed_on = session.renewed_on()

        db_session = SessionModel.get_by_id(session.sid)

        if db_session:
            self.created_on = db_session.created_on
            self.updated_on = db_session.updated_on
            self.expires_on = db_session.expires_on
