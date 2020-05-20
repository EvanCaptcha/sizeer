import requests, threading
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import Flask, render_template, request
webhookUrl = 'https://discord.com/api/webhooks/712487108299718666/g1z8UsfR6K-bqGPtrOtVDnD0FBoV51o7nksgJ70JimL1knSICrpGWBbKlJXwIxkkKfag'
app = Flask(__name__)
jobs = []
@app.route("/")
def home():
    return render_template("index.html")

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
        webhook = DiscordWebhook(url=webhookUrl)
        embed = DiscordEmbed(title='Sizeer - Monitor Started!', description='Monitor started on product ' + link + '. \nCurrent status: OOS \nSizeer by jxn', color=int('009000'))
        webhook.add_embed(embed)
        webhook.execute()
    else:
        inStock = True
        webhook = DiscordWebhook(url=webhookUrl)
        embed = DiscordEmbed(title='Sizeer - Monitor Started!', description='Monitor started on product ' + link + '. \nCurrent status: IN STOCK \nSizeer by jxn', color=int('009000'))
        webhook.add_embed(embed)
        webhook.execute()

    while not inStock:
        try:
            response = requests.get(link, headers=headers)
            if 'Powiadom o dostępności produktu' in response.text:
                print("No restock found on " + link + "...")
            else:
                print("Restock detected on product" + link + "... Sending webhooks...")
                webhook = DiscordWebhook(url=webhookUrl)
                embed = DiscordEmbed(title='Sizeer - Restock!', description='Restock on product ' + link + '. Act fast!', color=int('009000'))
                webhook.add_embed(embed)
                webhook.execute()
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
        webhook = DiscordWebhook(url=webhookUrl)
        embed = DiscordEmbed(title='Sizeer - Monitor Started!', description='Monitor started on product ' + prod + '. \nCurrent status: Available on AJ1 Portal Page \nSizeer by jxn', color=int('009000'))
        webhook.add_embed(embed)
        webhook.execute()
    if prod not in response:
        inStock = False
        webhook = DiscordWebhook(url=webhookUrl)
        embed = DiscordEmbed(title='Sizeer - Monitor Started!', description='Monitor started on product '  + prod + '. \nCurrent status: Unavailable \nSizeer by jxn', color=int('009000'))
        webhook.add_embed(embed)
        webhook.execute()
    while not inStock:
        try:
            response = requests.get('https://sklep.sizeer.com/jordan-air-1', headers=headers).text
            if prod in response:
                print("Product " + prod + " is now available on the AJ1 portal. ")
                webhook = DiscordWebhook(url=webhookUrl)
                embed = DiscordEmbed(title='Sizeer - SKU Monitor!', description='Product ' + prod +  ' now available on AJ1 portal. Act fast!', color=int('009000'))
                webhook.add_embed(embed)
                webhook.execute()
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
