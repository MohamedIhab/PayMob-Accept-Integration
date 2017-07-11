import requests
import json
from IPython.display import IFrame


# INPUT: merchant's credentials
# OUTPUT: authentication token , merchant id
def authentication_token_request(username, password):
    url = "https://accept.paymobsolutions.com/api/auth/tokens"
    payload = {
        "username": username,
        "password": password,
    }
    headers = {
        "content-type": "application/json"
    }
    modified_payload = json.dumps(payload)
    response = requests.post(url, data=modified_payload, headers=headers)
    response = response.json()
    final_response = {
        "token": response['token'],
        "merchant_id": response['profile']['id'],
    }
    return final_response


# INPUT: return output from authentication method + amount + currency + shipping_info. The items, merchant order id,
# delivery need are optional fields.
# OUTPUT: order id
def create_order(previous_response, amount, currency, shipping_info, items=False, merchant_order_id=False,
                 delivery_needed=False):
    url = "https://accept.paymobsolutions.com/api/ecommerce/orders"
    querystring = {"token": previous_response['token']}
    payload = {
        "delivery_needed": delivery_needed,
        "merchant_id": previous_response['merchant_id'],
        "amount_cents": amount,
        "currency": currency,
        "items": [],
        "shipping_data": shipping_info,
    }
    if merchant_order_id:
        payload["merchant_order_id"] = merchant_order_id
    if items:
        payload["items"] = items
    headers = {
        "content-type": "application/json"
    }
    modified_payload = json.dumps(payload)
    response = requests.post(url, data=modified_payload, headers=headers, params=querystring)
    response = response.json()
    previous_response['order_id'] = response['id']
    previous_response['amount'] = amount
    previous_response['currency'] = currency
    return previous_response


# INPUT: return output from order creation method + merchant's card integration ID + client's billing information
# OUTPUT: payment key token
def generate_payment_key(previous_response, card_integration_id, billing_info):
    url = "https://accept.paymobsolutions.com/api/acceptance/payment_keys"
    querystring = {"token": previous_response['token']}
    payload = {
        "amount_cents": previous_response['amount'],
        "currency": previous_response['currency'],
        "card_integration_id": card_integration_id,
        "order_id": previous_response['order_id'],
        "billing_data": billing_info,
    }
    headers = {
        "content-type": "application/json"
    }
    modified_payload = json.dumps(payload)
    response = requests.post(url, data=modified_payload, headers=headers, params=querystring)
    response = response.json()
    # print(response)
    previous_response['payment_key'] = response['token']
    return previous_response


# INPUT: Authentication token from authentication token request method in step 1
# OUTPUT: iFrame ID
def upload_iframe(auth_token, name, description, html, css, js):
    url = "https://accept.paymobsolutions.com/api/acceptance/iframes"
    querystring = {"token": auth_token}
    payload = {
        "name": name,
        "description": description,
        "content_html": html,
        "content_js": js,
        "content_css": css,
    }
    headers = {
        "content-type": "application/json"
    }
    modified_payload = json.dumps(payload)
    response = requests.post(url, data=modified_payload, headers=headers, params=querystring)
    if response.status_code == 201:
        response = response.json()
        return response['id']
    else:
        return response.status_code


# INPUT: iFrame ID from upload method and payment key token from generate payment key method
# OUTPUT: rendering the payment processing iFrame within an HTML page to get the client's credit card information
def render_iframe(payment_key, iframe_id):
    IFrame('https://accept.paymobsolutions.com/api/acceptance/iframes/'+str(iframe_id)+'?payment_token='+payment_key,
           width=700, height=350)


# INPUT: Merchant's domain name and the query parameters of the transaction
# OUTPUT: Corresponding response according to the transaction status
def transaction_response(params):
    query_params = {'id': str(params['id']), 'pending': str(params['pending']), 'amount_cents': str(params['amount']),
                    'success': str(params['success']), 'is_auth': str(params['is_auth']), 'is_capture':
                        str(params['is_capture']), 'is_standalone_payment': str(params['is_standalone']), 'is_voided':
                        str(params['is_voided']), 'is_refunded': str(params['is_refunded']), 'is_3d_secure':
                        str(params['3d_secure']), 'integration_id': str(params['integration_id']), 'profile_id':
                        str(params['profile_id']), 'has_parent_transaction': str(params['has_parent']), 'order':
                        str(params['order_id']), 'created_at': str(params['created_at']), 'currency':
                        str(params['currency']), 'error_occured': str(params['error']), 'owner': str(params['owner']),
                    'parent_transaction': str(params['parent_transaction']), 'source_data.type':
                        str(params['source_type']), 'source_data.pan': str(params['source_pan']),
                    'source_data.sub_type': str(params['source_sub_type'])}
    html = ""
    return query_params, html

