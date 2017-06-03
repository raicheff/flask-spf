#
# Flask-SPF
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import bs4
import flask

from flask import jsonify, render_template, request


class SPF(object):
    """
    Flask-SPF

    Documentation:
    https://flask-spf.readthedocs.io

    :param app: Flask app to initialize with. Defaults to `None`
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """"""


def _render_template(template_name_or_list, **context):
    """"""

    response = render_template(template_name_or_list, **context)

    if request.args.get('spf') == 'navigate':
        response = _render_fragment(response)

    return response


def _render_fragment(html_doc):
    """
    https://youtube.github.io/spfjs/documentation/responses
    ---
    http://atodorov.org/blog/2014/02/21/skip-or-render-specific-blocks-from-jinja2-templates/
    http://stackoverflow.com/questions/32512568/how-to-render-only-given-block-using-jinja2-with-flask-and-pjax
    """

    soup = bs4.BeautifulSoup(html_doc, 'html.parser')

    response = {}

    # `title`: Update document title
    title = soup.find('title').string
    if title is not None:
        response['title'] = title.string

    # `url`: Update document URL
    # TODO
    url = None
    if url:
        response['url'] = url

    # `head`: Install early JS and CSS
    # TODO
    head = None
    if head:
        response['head'] = head

    # `attr`: Set element attributes
    # TODO
    attr = {}
    if attr:
        response['attr'] = attr

    # `body`: Set element content and install JS and CSS
    body = {}
    s = str(soup.find(id='main').div)
    body['main'] = s
    if body:
        response['body'] = body

    # `foot`: Install late JS and CSS
    # TODO
    foot = None
    if foot:
        response['foot'] = foot

    return jsonify(response)


# Monkey-patch the original `render_template` function
flask.render_template = _render_template


# EOF
