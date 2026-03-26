import requests
from flask import Flask, request, render_template
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('currency_converter.html')  # HTML file

def get_currency_param(param):
    # agar list hai → pehla element lo
    if isinstance(param, list):
        param = param[0]
    # agar dict hai aur 'currency' key hai → value lo
    if isinstance(param, dict) and 'currency' in param:
        param = param['currency']
    return param

# safe helper for amount
def get_amount_param(param):
    if isinstance(param, list):
        param = param[0]
    if isinstance(param, dict) and 'amount' in param:
        param = param['amount']
    return float(param)



@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    text = data.get('queryResult', {}).get('queryText', '')
    params = data.get('queryResult', {}).get('parameters', {})
    # params = data['queryResult']['parameters']
    source_currency = get_currency_param(params.get('unit-currency'))
    target_currency = get_currency_param(params.get('currency-name'))
    # source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    # amount = data['queryResult']['parameters']['unit-currency']['amount']
    # amount = get_amount_param(params.get('unit-currency'))
    # target_currency = data['queryResult']['parameters']['currency-name']
    # print(source_currency)
    # print(amount)
    # print(target_currency)

    # cf = fetch_conversion_factor(source_currency, target_currency)
    #############
    # result = amount * cf
    #######################
    amount_param = params.get('unit-currency')
    if isinstance(amount_param, list):
        amount_param = amount_param[0]
    if isinstance(amount_param, dict) and 'amount' in amount_param:
        amount_param = amount_param['amount']
    amount = float(amount_param)

    cf = fetch_conversion_factor(source_currency, target_currency)
    result = round(amount * cf, 2)
    #######################
    # if isinstance(source_currency, list):
    #     source_currency = source_currency[0]
    #
    # if isinstance(target_currency, list):
    #     target_currency = target_currency[0]
    #
    # result = round(amount * cf, 2)
    # if isinstance(target_currency, list):
    #     target_currency = target_currency[0]

    print(f"{amount}{source_currency} is {result}{target_currency}")
    return jsonify({
        "fulfillmentText": f"{amount}{source_currency} is {result}{target_currency}"
    })
    # return f"{source_currency}\n{amount}\n{target_currency}\n{result}"
    # return str(result)
    ##############
    # return "Hello"
    # return str(source_currency + ' ' + str(amount) + ' ' + str(target_currency)


def fetch_conversion_factor(source, target):
    api_key = "976a15c6f5679f761785d6a1"

    if isinstance(source, list):
        source = source[0]
    if isinstance(target, list):
        target = target[0]

    source = source.upper()
    target = target.upper()

    url = f"https://v6.exchangerate-api.com/v6/976a15c6f5679f761785d6a1/pair/{source}/{target}"

    response = requests.get(url)
    response = response.json()
    if response['result'] == 'success':
        return response['conversion_rate']
    else:
        raise ValueError(f"Failed to get conversion rate: {response.get('error-type', 'Unknown error')}")
    # print(response)
    # return response['{},{}'.format(source, target)]
    # or using f-string
    # return response['conversion_rate']
    # return response[f'{source},{target}']
    # return data['{}/{}'.format(source, target)]
    # return data['source_currency,target_currency']
    # .format(source,target)]
    # return data['conversion_rate']

if __name__ == '__main__':
    # print(fetch_conversion_factor("{source}", "{target}"))
    app.run(debug=True)

