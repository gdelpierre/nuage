# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'pyramid_fanstatic',
    'rebecca.fanstatic',
    'couchdbkit',
    'pyramid_beaker',
    'Pygments',
    'Babel',
    'lingua',
    'pyramid_chameleon',
    'couchdbkit',
    'py-bcrypt',
    'js.bootstrap',
    'css.fontawesome',
    'pyramid_mailer',
    ]

setup(name='nuage',
      version='0.0',
      description='nuage',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author=u'Guillaume Delpierre',
      author_email='gde+code@llew.me',
      url='',
      keywords='nuage pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="nuage",
      entry_points = """\
      [paste.app_factory]
      main = nuage:main
      """,
      )
