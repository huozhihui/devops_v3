#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required
import json
from . import inventory_update
from ..models import InventoryUpdate, Inventory

MODULE_NAME = u"资产变更"


@inventory_update.route('/index/<int:id>', methods=['GET'])
@login_required
def index(id):
    header = u'记录'
    inventory = Inventory.query.get_or_404(id)
    data = []
    objects = InventoryUpdate.query.all()
    for obj in objects:
        tmp = {}
        tmp['id'] = obj.id
        tmp['date'] = obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
        tmp['content'] = json.loads(obj.content)
        data.append(tmp)
    return _render('index', locals())


def _render(content, kwargs={}):
    new_header = MODULE_NAME + kwargs.get('header', '')
    kwargs.update(title_name=MODULE_NAME, header=new_header)
    html = "inventory_update/%s.html" % content
    return render_template(html, **kwargs)
