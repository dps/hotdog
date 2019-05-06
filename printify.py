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
        # return str(uuid.uuid1())
        return 'poid_' + \
            ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))

    def create_order(self, front_img_url, shipping_address, items, draft=True):
        order_id = self._generate_order_id()
        body = ORDER_TEMPLATE.render(
            order_id=order_id,
            front_img_url=front_img_url,
            printify_params=self._printify_params,
            shipping=shipping_address,
            items=items)
        body = body.replace('\n', '')
        r = requests.post('https://api.printify.com/v1/shops/%s/orders.json' %
                          self._printify_params['draft_store_id' if draft else 'ship_store_id'], data=body, headers=self._headers)
        if r.status_code == 200:
            printify_order = r.json()['id']
            r = requests.get('https://api.printify.com/v1/shops/%s/orders/%s.json' %
                             (self._printify_params['draft_store_id' if draft else 'ship_store_id'], printify_order), headers=self._headers)
            order_detail = r.json()
            poh = int(printify_order, 16)
            front_image_url = 'https://images.printify.com/mockup/%X/45153/1535/?s=400' % (
                poh - 1)
            return {
                'order_id': order_id,
                'printify_order_id': printify_order,
                'detail': order_detail,
                'front_image_url': front_image_url}
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
    res = p.create_draft_order(
        '', addr, [
            'fire-hotdog', 'airplane-hotdog', 'airplane-hotdog'])
    print res
