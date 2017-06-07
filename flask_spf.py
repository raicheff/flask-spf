#
# Flask-SPF
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import flask

from bs4 import BeautifulSoup
from flask import current_app, jsonify, render_template, request
from htmlmin import Minifier


class SPF(object):
    """
    Flask-SPF

    Documentation:

    https://flask-spf.readthedocs.io

    Usage:

    `<link rel="spf-url" href="/foo/bar">`

    `<link rel="stylesheet" href="/assets/css/page.css" class="spf-head" name="page">`

    `<div id="some-div" data-foo="foo" data-bar="bar" data-spf-attr="data-foo data-bar">`

    `<main id="main" class="spf-body">...</main>`

    `<script src="https://platform.twitter.com/widgets.js" class="spf-foot" name="twitter" async defer></script>`

    :param app: Flask app to initialize with. Defaults to `None`
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('SPF_URL_IDENTIFIER', 'spf')


_minifier = Minifier(
    remove_comments=True,
    remove_empty_space=True,
    reduce_empty_attributes=True,
    reduce_boolean_attributes=True,
    remove_optional_attribute_quotes=False,
)


def _render_template(template_name_or_list, **context):
    """"""

    response = render_template(template_name_or_list, **context)

    if request.args.get(current_app.config.get('SPF_URL_IDENTIFIER')) in ('load', 'navigate'):
        response = _render_fragment(response)

    return response


def _render_fragment(html_doc):
    """
    https://youtube.github.io/spfjs/documentation/responses
    ---
    http://atodorov.org/blog/2014/02/21/skip-or-render-specific-blocks-from-jinja2-templates/
    http://stackoverflow.com/questions/32512568/how-to-render-only-given-block-using-jinja2-with-flask-and-pjax
    """

    soup = BeautifulSoup(html_doc, 'html.parser')

    response = {}

    # `title`: Update document title
    tag = soup.title
    if tag is not None:
        response['title'] = tag.string.strip()

    # `url`: Update document URL
    tag = soup.find('link', rel='spf-url') or soup.find('link', rel='canonical')
    if tag is not None:
        response['url'] = tag['href'].strip()

    # `head`: Install early JS and CSS
    head = ''.join(tag.decode() for tag in soup(['link', 'script'], class_='spf-head'))
    if head:
        response['head'] = _minifier.minify(head).strip()

    # `attr`: Set element attributes
    attr = {}
    tags = soup(lambda tag: tag.has_attr('data-spf-attr'))
    for tag in tags:
        attr[tag['id']] = {name: tag[name] for name in tag.get_attribute_list('data-spf-attr')}
    if attr:
        response['attr'] = attr

    # `body`: Set element content and install JS and CSS
    body = {tag['id']: _minifier.minify(tag.decode_contents()).strip() for tag in soup(class_='spf-body')}
    if body:
        response['body'] = body

    # `foot`: Install late JS and CSS
    foot = ''.join(tag.decode() for tag in soup(['link', 'script'], class_='spf-foot'))
    if foot:
        response['foot'] = _minifier.minify(foot).strip()

    # `name`: ...
    # TODO
    # response['name'] = request.endpoint.replace('.', '-')

    return jsonify(response)


# Monkey-patch the original `render_template` function
flask.render_template = _render_template


# EOF
