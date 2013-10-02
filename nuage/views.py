############################################################################
# The MIT License (MIT)
#
# Copyright (c) 2013 Guillaume Delpierre
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNES FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
############################################################################

""" Nuage
"""

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound

import couchdbkit
from couchdbkit.designer import push

from nuage.models.user import User

# Couchdb
server = couchdbkit.Server(settings['couchdb.url'])
db = server.get_or_create_db(settings['couchdb.db'])

User.set_db(db)

@view_config(route_name='home_notlog', renderer='templates/home_notlog.pt')
def home_notlog(request):
    """
    Default homepage.
    """
    return {'project': 'nuage'}

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    """
    Homepage when you're loggued.
    """
    return {'project': 'nuage'}

@view_config(route_name='submitLogin')
def submitLogin(request):
    """
    Log in
    """
    try:
        User.get(request.POST['login'])
    except couchdbkit.exceptions.ResourceNotFound:
        request.session.flash(u"User not found, please signup")
        return HTTPFound(location=request.route_path('signup'))

    if not request.POST['password'].strip():
        request.session.flash(u"Wrong password")
        return HTTPFound(location=request.route_path('home_notlog'))

    if bcrypt.hashpw(request.POST['password'].encode('utf-8'), \
                     user.password) != user.password:
        request.session.flash(u"Wrong password")
        return HTTPFound(location=request.route_path('home_notlog'))

    request.session['login'] = user._id
    request.session.save()
    return HTTPFound(location=request.route_path('home'), headers=headers)

