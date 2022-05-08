from flask import redirect, flash, url_for
from flask_login import current_user
from functools import wraps


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user and current_user.role == 1:
            return f(*args, **kwargs)
        flash("Ooops login or your privilege is not satisfied", "info")
        return redirect(url_for('home'))
    return wrap


def doctor_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user and current_user.role == 2 :
            return f(*args, **kwargs)
        flash("Ooops login or your privilege is not satisfied", "info")
        return redirect(url_for('home'))
    return wrap


