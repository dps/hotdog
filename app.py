from functools import wraps
import json
import os
import requests
import stripe
import sys
from flask import Flask, Response, send_file, request, render_template, session, redirect, send_from_directory
from printify import Printify

app = Flask(__name__)
app.debug = False
app.secret_key = os.environ['FLASK_SECRET']
stripe.api_key = os.environ['STRIPE_SECRET_KEY']
stripe.api_version = "2018-11-08; checkout_sessions_beta=v1"

live_client_version = ''.join(file('live_client_version.txt', 'r').readlines())


def currency_minor_units_to_string(minor_units, currency='usd'):
    return '$' + '{:0,.2f}'.format(minor_units / 100.0)


@app.route('/')
def index():
    return render_template(
        'index.html',
        session_data=session,
        live_client_js=live_client_version)


@app.route('/success')
def success():
    return render_template('success.html', session_data=session)


@app.route('/terms')
def terms():
    return render_template('terms.html', session_data=session)


@app.route('/shipping')
def shipping():
    items = request.query_string
    cardholder_fields = [
        ('name',
         'Haute Daug'),
        ('address',
         '1 Bratwurst St'),
        ('city',
         'Frankfurt'),
        ('state',
         'CA'),
        ('zip',
         '94101'),
        ('email',
         'holdthemustard@hotdog.com'),
        ('phone',
         '4645553633')]
    return render_template('shipping.html', session_data=session,
                           cardholder_fields=cardholder_fields,
                           items=items,
                           cart_headline_image_url='')


@app.route('/buy', methods=['POST'])
def buy():
    shipping = {
        'first_name': request.form['name'].split(' ')[0],
        'last_name': request.form['name'].split(' ')[1],
        'addr1': request.form['address'],
        'city': request.form['city'],
        'state': request.form['state'],
        'country': 'US',
        'zip': request.form['zip'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'items': request.form['items'],
        'img': "",
    }
    img = ""
    items = request.form['items'].split(",")
    draft_order = Printify().create_order(img, shipping, items, draft=True)
    shipping['name'] = request.form['name']
    shipping_cost = draft_order['detail']['total_shipping']
    tax_cost = draft_order['detail']['total_tax']
    items_price = 1200 * len(items)
    amount = items_price + int(shipping_cost) + int(tax_cost)

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        payment_method_types=['card'],
        metadata=shipping,
    )
    cardholder_fields = [('name', 'Haute Daug'),
                         ('addr1', '1 Bratwurst St'),
                         ('city', 'Frankfurt'),
                         ('state', 'CA'),
                         ('zip', '94101'),
                         ('email', 'holdthemustard@hotdog.com'),
                         ('phone', '4645553633')]
    cardholder_data = []
    for name, placeholder in cardholder_fields:
        cardholder_data.append((name, shipping[name]))
    return render_template(
        'buy.html',
        session_data=session,
        client_secret=intent.client_secret,
        cardholder_fields=cardholder_data,
        name=shipping["name"],
        stripe_public_key=os.environ['STRIPE_PUBLIC_KEY'],
        shipping_cost=currency_minor_units_to_string(shipping_cost),
        items_price=currency_minor_units_to_string(items_price),
        tax_cost=currency_minor_units_to_string(tax_cost),
        amount=currency_minor_units_to_string(amount),
        items=request.form['items'].split(","),
        cart_headline_image_url=draft_order['front_image_url'])


@app.route('/service-worker.js')
def serve_worker():
    return send_from_directory('./static/js', 'service-worker.js')


@app.route('/imgs/hotdogs/<path:path>')
def serve_dogimg(path):
    return send_from_directory('./static/hotdogs', path)


@app.route('/imgs/previews/<path:path>')
def serve_previewimg(path):
    return send_from_directory('./static/previews', path)


@app.route('/printify_webhook')
def pwebhook():
    print >>sys.stderr, 'pwebhook ->'
    print >>sys.stderr, request.json


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print 'webhook ->'
    print >>sys.stderr, request.json
    print ' type ->'
    type = request.json[u'type']
    print type
    slack_msg = ''
    if type == u'payment_intent.succeeded':
        piid = request.json[u'data'][u'object'][u'id']
        metadata = request.json[u'data'][u'object'][u'metadata']
        shipping = metadata
        items = shipping['items'].split(",")
        order = Printify().create_order('', shipping, items, draft=False)
        pi = stripe.PaymentIntent.modify(
            piid,
            metadata={
                'order_id': order['order_id'],
                'printify_order_id': order['printify_order_id']})
        slack_msg = 'Fulfilled! ' + order['printify_order_id']

    if 'SLACK_WEBHOOK' in os.environ:
        data = {'text': ('*%s*\n' % type) + str(slack_msg)}
        requests.post(os.environ['SLACK_WEBHOOK'], json=data)
    print 'webhook <-'
    return 'ok'
