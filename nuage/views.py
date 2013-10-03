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
from pyramid.threadlocal import get_current_registry
from pyramid.response import Response

import couchdbkit
from couchdbkit.designer import push

from nuage.models.user import User

settings = get_current_registry().settings

# Couchdb
server = couchdbkit.Server(settings['couchdb.url'])
db = server.get_or_create_db(settings['couchdb.db'])

User.set_db(db)

@view_config(route_name='home', renderer='templates/home_notlog.pt', \
             logged=False)
def home(request):
    """
    Default homepage.
    """
    return {}

@view_config(route_name='home', renderer='templates/home_notlog.pt', \
             logged=False)
def home(request):
    """
    Homepage when you're loggued.
    """
    return {}

@view_config(route_name='signup', renderer='templates/signup')
def signup(request):
    """
    Signup template.
    """
    return {}

@view_config(route_name='submitSignup')
def submitSignup(request):
    """
    Signup action.
    """
    try:
        User.get(request.POST['login'])
    except couchdbkit.exceptions.ResourceNotFound:
        pass
    else:
        request.session.flash(u"Username already exist")
        return HTTPFound(location=request.route_path('signup'))

    if not request.POST['password'].strip():
        request.session.flash(u"Please set a password")
        return HTTPFound(location=request.route_path('signup'))

    if not len(request.POST['password'].strip()) >= 8:
        request.session.flash(u"Password must have at least 8 characters")
        return HTTPFound(location=request.route_path('signup'))

    if request.POST['password'] == request.POST['confirmPassword']:
        password = bcrypt.hashpw(request.POST['password'].encode('utf-8'), \
                                 bcrypt.gensalt(rounds=14))

        user = User(password=password, \
                    name=request.POST['name'], \
                    description=request.POST['description'], \
                    mail=request.POST['email'], \
                    random=random.randint(1,1000000000), \
                    checked = False \
                    )
        user._id = request.POST['login']
        user.save()

        confirm_link = request.route_url('checkLogin', \
                                        userid = user._id, \
                                        randomid = user.random)

        mailer = Mailer()
        message = Message(subject="Your subsription !", \
                          sender=settings['mail_from'], \
                          recipients=[request.POST['email']], \
                          body="Confirm the link\n\n%s" % confirm_link)
        mailer.send_immediately(message, fail_silently=False)

        return {'name': request.POST['name']}

    else:
        return HTTPFound(location=request.route_path('signup'))

@view_config(route_name='submitLogin')
def submitLogin(request):
    """
    Log in action.
    """
    try:
        User.get(request.POST['login'])
    except couchdbkit.exceptions.ResourceNotFound:
        request.session.flash(u"User not found, please signup")
        return HTTPFound(location=request.route_path('signup'))

    if not request.POST['password'].strip():
        request.session.flash(u"Wrong password")
        return HTTPFound(location=request.route_path('home'))

    if bcrypt.hashpw(request.POST['password'].encode('utf-8'), \
                     user.password) != user.password:
        request.session.flash(u"Wrong password")
        return HTTPFound(location=request.route_path('home'))

    request.session['login'] = user._id
    request.session.save()
    return HTTPFound(location=request.route_path('home'), headers=headers)

