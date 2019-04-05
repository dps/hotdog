import random
import requests
import simplejson
import string
import time
import os
import uuid

from jinja2 import Template

ORDER_TEMPLATE = Template("""
{"line_items": [
{% for item in items %}
{"blueprint_id": {{ printify_params.blueprint_id}}, "price": {{ printify_params.price }}, "print_provider_id": {{ printify_params.print_provider_id}}, "variant_id": {{ printify_params.variant_id}}, "print_areas": {"front": "http://hotdog.us.davidsingleton.org/static/hotdogs/{{ item }}.png"}, "quantity": 1}{%- if not loop.last -%},{%- endif %}
{% endfor %}
], "external_id": "{{ order_id }}", "shipping_method": 1, "address_to": {"phone": "{{ shipping.phone }}", "first_name": "{{ shipping.first_name }}", "last_name": "{{ shipping.last_name }}", "address2": "{{ shipping.addr2 }}", "zip": "{{ shipping.zip }}", "address1": "{{ shipping.addr1 }}", "country": "{{ shipping.country }}", "region": "{{ shipping.state }}", "city": "{{ shipping.city }}", "email": "{{ shipping.email }}"}, "send_shipping_notification": false}
""")

class Printify(object):

    def __init__(self):
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer %s' % os.environ['PRINTIFY_API_TOKEN']
        }
        self._printify_params = {
            'print_provider_id': os.environ['PRINTIFY_PROVIDER_ID'],
            'blueprint_id': os.environ['PRINTIFY_BLUEPRINT_ID'],
            'variant_id': os.environ['PRINTIFY_VARIANT_ID'],
            'ship_store_id': os.environ['PRINTIFY_SHIP_STORE_ID'],
            'draft_store_id': os.environ['PRINTIFY_DRAFT_STORE_ID'],
            'price': 1200
        }

    def _generate_order_id(self):
        #return str(uuid.uuid1())
        return 'poid_'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    
    def create_order(self, front_img_url, shipping_address, items, draft=True):
        order_id = self._generate_order_id()
        body = ORDER_TEMPLATE.render(order_id=order_id, front_img_url=front_img_url,
                              printify_params=self._printify_params,
                              shipping=shipping_address,
                              items=items)
        body = body.replace('\n', '')
        print body
        r = requests.post('https://api.printify.com/v1/shops/%s/orders.json' % self._printify_params['draft_store_id' if draft else 'ship_store_id'],
                          data=body, headers = self._headers)
        if r.status_code == 200:
            print r.json()
            printify_order = r.json()['id']
            r = requests.get('https://api.printify.com/v1/shops/%s/orders/%s.json' % (self._printify_params['draft_store_id' if draft else 'ship_store_id'], printify_order),
                headers=self._headers)
            order_detail = r.json()
            poh = int(printify_order, 16)
            front_image_url = 'https://images.printify.com/mockup/%X/45153/1535/?s=400' % (poh-1)
            return {'order_id': order_id, 'printify_order_id': printify_order, 'detail': order_detail, 'front_image_url': front_image_url}
        else:
            print 'ERROR CREATING ORDER ' + 'draft_store_id' if draft else 'ship_store_id'
            print r.status_code
            print r.text
            return None



if __name__ == '__main__':
    p = Printify()
    addr = {
        'first_name': "David",
        'last_name': "Singleton",
        'addr1': '234 Eureka St',
        'city': 'San Franciso',
        'state': 'CA',
        'country': 'US',
        'zip': '94114',
        'email': 'davidsingleton@gmail.com',
        'phone': '4156190699'
    }
    res = p.create_draft_order('', addr, ['fire-hotdog', 'airplane-hotdog', 'airplane-hotdog'])
    print res
    # names = file('missing', 'r').readlines()

    # ufile = file('urls2.txt', 'w')
    # for name in names:
    #     name = name.strip()
    #     print '--> %s' % name
    #     res = p.create_draft_order('http://hotdog.us.davidsingleton.org/static/hotdogs/%s' % name, addr)
    #     print res['front_image_url']
    #     ufile.write(name + " " + res['front_image_url'] + " <img src='%s'/>\n" % res['front_image_url'])
    #     time.sleep(5)


# r = requests.get('https://api.printify.com/v1/shops.json', params={}, headers = headers)

# print r.json()
# shop_id = r.json()[0][u'id']

# headers = {
#   'Accept': 'application/json',
#   'Authorization': 'Bearer %s' % os.environ['PRINTIFY_API_TOKEN']
# }

# headers = {
#   'Content-Type': 'application/json',
#   'Accept': 'application/json',
#   'Authorization': 'Bearer %s' % os.environ['PRINTIFY_API_TOKEN']
# }
# # "external_id": "2750e210-39bb-11e9-a503-452618153e54",
# body = {
#   "external_id": "foo1",
#   "line_items": [
#     {
#       "print_provider_id": 20,
#       "blueprint_id": 382,
#       "variant_id": 45153,
#       "print_areas": {
#         "front": "https://emoji.slack-edge.com/T024F4A92/snowboarding-hotdog/ef4fb005a269acf4.png"
#       },
#       "quantity": 1,
#       "price": 1200
#     }
#   ],
#   "shipping_method": 1,
#   "send_shipping_notification": False,
#   "address_to": {
#     "first_name": "David",
#     "last_name": "Singleton",
#     "email": "davidsingleton@gmail.com",
#     "phone": "4156190699",
#     "country": "US",
#     "region": "CA",
#     "address1": "234 Eureka St",
#     "address2": "",
#     "city": "San Francisco",
#     "zip": "94114"
#   }
# }
# body_json = simplejson.dumps(body)
# print body_json
# shop_id = os.environ['PRINTIFY_DRAFT_STORE_ID']
# r = requests.post('https://api.printify.com/v1/shops/%s/orders.json' % shop_id, data=body_json, headers = headers)

# print r.json()

# order_id = '5c9ec339b94c73af696593c0'
# #{u'id': u'5c9ec480b11209e0f6661b5c'}


# r = requests.get('https://api.printify.com/v1/shops/%s/orders/%s.json' % (shop_id, order_id), params={

# }, headers = headers)

# print r.json()

# # {u'status': u'payment-not-received', u'line_items': [{u'status': u'on-hold', u'product_id': u'5c9ec338b94c73af696593bf', u'shipping_cost': 400, u'print_provider_id': 20, u'cost': 978, u'variant_id': 45153, u'metadata': {u'sku': u'caseypin10_none_silver', u'country': u'United States', u'price': 1200, u'variant_label': u'1"', u'title': u'API 2750e210-39bb-11e9-a503-452618153e52 - David Singleton'}, u'quantity': 1}], u'total_price': 978, u'shipping_method': 1, u'total_tax': 0, u'created_at': 1553908537, u'address_to': {u'city': u'San Francisco', u'first_name': u'David', u'last_name': u'Singleton', u'zip': u'94114', u'country': u'United States', u'region': u'CA', u'phone': u'4156190699', u'address1': u'234 Eureka St', u'email': u'davidsingleton@gmail.com'}, u'id': u'5c9ec339b94c73af696593c0', u'total_shipping': 400, u'metadata': {u'shop_order_label': u'2750e210-39bb-11e9-a503-452618153e52', u'order_type': u'api', u'shop_order_id': u'2750e210-39bb-11e9-a503-452618153e52'}}