# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from libs.app.home import blueprint

from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from libs.app.home import blueprint
from libs.webserver.executer import Executer


@blueprint.route('/')
@login_required
def index():
    devices = Executer.instance.device_executer.get_devices()
    # active_effect = Executer.instance.effect_executer.get_active_effect(data_in["device"])
    return render_template('dashboard.html', segment='dashboard', devices=devices)


@blueprint.route('/<page>/<template>', methods=['GET', 'POST'])
@login_required
def route_pages(page, template):
    devices = Executer.instance.device_executer.get_devices()

    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        return render_template(f"/{page}/{template}", segment=segment, devices=devices)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception:
        return render_template('page-500.html'), 500


@blueprint.route('/<template>')
@login_required
def route_template(template):
    devices = Executer.instance.device_executer.get_devices()

    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        return render_template(template, segment=segment, devices=devices)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception:
        return render_template('page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'dashboard'
        return segment
    except Exception:
        return None
