from functools import wraps
import json
import io
import os
import redis
import requests
import stripe
import sys
from flask import Flask, Response, send_file, request, render_template, session, redirect, send_from_directory
from printify import Printify

app = Flask(__name__)
app.debug = True #hup
app.secret_key = os.environ['FLASK_SECRET']
stripe.api_key = os.environ['STRIPE_SECRET_KEY']
stripe.api_version = "2018-11-08; checkout_sessions_beta=v1"

je = json.JSONEncoder()

appredis = redis.StrictRedis(
    host='spadefish.redistogo.com', 
    port=9148, 
    db=0,
    password=os.environ['REDISKEY'])

FAKE_ORDER = {'order_id': 'poid_948sych39e8pclsd', 'printify_order_id': u'5ca1948847b39faea623dbfd', 'front_image_url': 'https://images.printify.com/mockup/5CA1948847B39FAEA623DBFC/45153/1535/?s=400', 'detail': {u'status': u'pending', u'line_items': [{u'status': u'pending', u'product_id': u'5ca1948847b39faea623dbfc', u'shipping_cost': 400, u'print_provider_id': 20, u'cost': 978, u'variant_id': 45153, u'metadata': {u'sku': u'caseypin10_none_silver', u'country': u'United States', u'price': 1630, u'variant_label': u'1"', u'title': u'Metal Pin'}, u'quantity': 1}], u'total_price': 978, u'shipping_method': 1, u'total_tax': 0, u'created_at': 1554093192, u'address_to': {u'city': u'San Francisco', u'first_name': u'David', u'last_name': u'Singleton', u'zip': u'94114', u'country': u'United States', u'region': u'CA', u'phone': u'6464505078', u'address1': u'234 Eureka St', u'email': u'davidsingleton@gmail.com'}, u'id': u'5ca1948847b39faea623dbfd', u'total_shipping': 400, u'metadata': {u'shop_order_label': u'poid_948sych39e8pclsd', u'order_type': u'api', u'shop_order_id': u'poid_948sych39e8pclsd'}}}
def currency_minor_units_to_string(minor_units, currency='usd'):
  return '$' + '{:0,.2f}'.format(minor_units/100.0)

def authenticate(f):
    """Sends a 401 response that enables basic auth"""

    session['continue_to_url'] = '/' + f.func_name
    return redirect('/signin')

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.has_key('user_email'):
            return authenticate(f)
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
  return render_template('index.html', session_data=session)

@app.route('/success')
def success():
  return render_template('success.html', session_data=session)

@app.route('/terms')
def terms():
  return render_template('terms.html', session_data=session)

@app.route('/shipping')
def shipping():
  items = request.query_string
  cardholder_fields = [('name', 'Haute Daug'), ('address', '1 Bratwurst St'), ('city', 'Frankfurt'), ('state', 'CA'), ('zip', '94101'), ('email', 'holdthemustard@hotdog.com'), ('phone', '4645553633')]
  return render_template('shipping.html', session_data=session,
                         cardholder_fields=cardholder_fields,
                         items=items,
                         cart_headline_image_url='')

@app.route('/buy', methods=['POST'])
def buy():
  print >>sys.stderr,request.form

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
  print >>sys.stderr, draft_order
  shipping_cost = draft_order['detail']['total_shipping']
  tax_cost = draft_order['detail']['total_tax']
  items_price = 1200 * len(items)
  amount = items_price + int(shipping_cost) + int(tax_cost)

  intent = stripe.PaymentIntent.create(
    amount=amount,
    currency='usd',
    payment_method_types=['card'],
    metadata = shipping,
  )
  cardholder_fields = [('name', 'Haute Daug'), ('addr1', '1 Bratwurst St'), ('city', 'Frankfurt'), ('state', 'CA'), ('zip', '94101'), ('email', 'holdthemustard@hotdog.com'), ('phone', '4645553633')]
  cardholder_data = []
  for name, placeholder in cardholder_fields:
    cardholder_data.append((name, shipping[name]))
  return render_template('buy.html', session_data=session,
                         client_secret=intent.client_secret,
                         cardholder_fields=cardholder_data,
                         name = shipping["name"],
                         shipping_cost=currency_minor_units_to_string(shipping_cost),
                         items_price=currency_minor_units_to_string(items_price),
                         tax_cost=currency_minor_units_to_string(tax_cost),
                         amount=currency_minor_units_to_string(amount),
                         items=request.form['items'].split(","),
                         cart_headline_image_url=draft_order['front_image_url'])

@app.route('/service-worker.js')
def serve_worker():
    return send_from_directory('./react', 'service-worker.js')

@app.route('/imgs/hotdogs/<path:path>')
def serve_dogimg(path):
  print >>sys.stderr, path
  return send_from_directory('./static/hotdogs', path)

@app.route('/imgs/previews/<path:path>')
def serve_previewimg(path):
  print >>sys.stderr, path
  return send_from_directory('./static/previews', path)

@app.route('/printify_webhook')
def pwebhook():
    print >>sys.stderr,'pwebhook ->'
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
      pi = stripe.PaymentIntent.modify(piid,
             metadata={'order_id':order['order_id'],
                       'printify_order_id': order['printify_order_id']})
      slack_msg = 'Fulfilled! ' + order['printify_order_id']

        
    if os.environ.has_key('SLACK_WEBHOOK'):
        data = {'text': ('*%s*\n' % type) + str(slack_msg)}
        requests.post(os.environ['SLACK_WEBHOOK'], json=data)
    print 'webhook <-'
    return 'ok'


