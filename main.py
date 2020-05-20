import requests, threading
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import Flask, render_template, request
webhookUrl = 'https://discordapp.com/api/webhooks/712647826777309185/02hRwcoHIWu3SRyXXA1htmHlA_otxxJx-63DqE3q8cwvyfXlAAsKZeGdlfj_ZbHMNxhR'
webhookUrl2 = 'https://discordapp.com/api/webhooks/712648700559884322/xXqtrixh9sVvdZIovRERRPRYvLosY2I3tP3uat7gLp2TyFOjkoskC7MKmIDGA93NRf_h'
app = Flask(__name__)
jobs = []
@app.route("/")
def home():
    return render_template("index.html")

def sendHook(title, content, url):
    webhook = DiscordWebhook(url=url)
    embed = DiscordEmbed(title=title,description= content + '\nSizeer by jxn',color=int('009000'))
    webhook.add_embed(embed)
    webhook.execute()
def monitor(link):
    headers = {
    'authority': 'sklep.sizeer.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'sec-fetch-user': '?1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',}
    response = requests.get(link, headers=headers)
    if 'Powiadom o dostępności produktu' in response.text:
        inStock = False
        sendHook(title='Sizeer - Monitor Started!',content='Monitor started on product ' + link + '\nCurrent Status: OOS\nSizeer by jxn', url=webhookUrl)
        sendHook(title='Sizeer - monitor started!', content='Monitor started on product '+ link + '\nCurrent Status: OOS\nSizeer by jxn', url=webhookUrl2)
    else:
        inStock = True
        sendHook(title='Sizeer - Monitor Started!', content='Monitor started on product ' + link + '\nCurrent Status: In Stock\nSizeer by jxn', url=webhookUrl)
        sendHook(title='Sizeer - monitor started!', content='Monitor started on product ' + link + '\nCurrent Status: In Stock\nSizeer by jxn', url=webhookUrl2)

    while not inStock:
        try:
            response = requests.get(link, headers=headers)
            if 'Powiadom o dostępności produktu' in response.text:
                print("No restock found on " + link + "...")
            else:
                print("Restock detected on product" + link + "... Sending webhooks...")
                sendHook(title='Sizeer - Restock Detected!',
                         content='restock detected on product  '  + link + '\nAct fast!\nSizeer by jxn',
                         url=webhookUrl)
                sendHook(title='Sizeer - Restock Detected!',
                         content='Restock detected on product  '  + link + '\nAct fast!\nSizeer by jxn',
                         url=webhookUrl2)
                inStock = True
        except:
            pass
    while inStock:
        try:
            response = requests.get(link, headers=headers)
            if 'Powiadom o dostępności produktu' in response.text:
                print(link + " now OOS.")
                inStock = False
            else:
                print(link + " still in stock...")
        except:
            pass
def monSku(prod):
    headers = {
        'authority': 'sklep.sizeer.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'referer': 'https://sklep.sizeer.com/jordan-air-1',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
    }

    response = requests.get('https://sklep.sizeer.com/jordan-air-1', headers=headers).text
    if prod in response:
        inStock = True
        sendHook(title='Sizeer - Monitor Started!',
                 content='Monitor started on product  ' + prod + '\nCurent status: Available on AJ1 Portal \nSizeer by jxn',
                 url=webhookUrl)
        sendHook(title='Sizeer - Monitor Started!',
                 content='Monitor started on product  ' + prod + '\nCurent status: Available on AJ1 Portal \nSizeer by jxn',
                 url=webhookUrl2)
    if prod not in response:
        inStock = False
        sendHook(title='Sizeer - Monitor Started!',
                 content='Monitor started on product  ' + prod + '\nCurent status: Unavailable on AJ1 Portal \nSizeer by jxn',
                 url=webhookUrl)
        sendHook(title='Sizeer - Monitor Started!',
                 content='Monitor started on product  ' + prod + '\nCurent status: Unavailable on AJ1 Portal \nSizeer by jxn',
                 url=webhookUrl2)
    while not inStock:
        try:
            response = requests.get('https://sklep.sizeer.com/jordan-air-1', headers=headers).text
            if prod in response:
                print("Product " + prod + " is now available on the AJ1 portal. ")
                sendHook(title='Sizeer - SKU Monitor!',
                         content='Product  ' + prod + 'is now available on the AJ1 portal page.\nSizeer by jxn',
                         url=webhookUrl)
                sendHook(title='Sizeer - SKU Monitor!',
                         content='Product  ' + prod + 'is now available on the AJ1 portal page.\nSizeer by jxn',
                         url=webhookUrl2)
                inStock = True
            else:
                print("Product " + prod + " still unavailable")
        except:
            pass
    while inStock:
        try:
            response = requests.get('https://sklep.sizeer.com/jordan-air-1', headers=headers).text
            if prod not in response:
                print("Product " +  prod + " is no longer available...")
                inStock = False
            else:
                print("Product " + prod + " is still available on the AJ1 portal page... ")
        except:
            pass
@app.route("/monitor", methods=["POST", "GET"])
def spam():
    if request.method == "POST":
        product = request.form["product"]
        for i in range(0, 1):
            jobs.append(threading.Thread(target=monitor(product)))
        return "Success"
    elif request.method == 'GET':
        return "Wrong method."
@app.route("/sku", methods=["POST", "GET"])
def sku():
    if request.method == "POST":
        sku = request.form['productSku']
        for i in range(0, 1):
            jobs.append(threading.Thread(target=monSku(sku)))
        return "Success"
    elif request.method == 'GET':
        return "Wrong method."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
