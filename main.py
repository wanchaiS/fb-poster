import requests
import json
from bs4 import BeautifulSoup

import configger


def main():
    # get config
    config = configger.get_config()

    # get long lived page token, never expired, un comment when want to generate long lived key
    # getLongLivedToken(config["shortlivedUserToken"], config["appId"], config["appSecret"],config["userId"], config["pageId"], config["graphApiVersion"])

    # from this point long lived page token

    # get gold data
    prices = getGoldData()
    print(prices)

    # post face book
    postFB(prices, config["longlivedPageToken"], config["pageId"])
    return


def getGoldData():
    url = "https://goldtraders.or.th/"

    res = requests.get(url)
    res.encoding = "utf-8"
    if res.status_code == 200:
        print("Successfully retrive gold traders page")
    elif res.status_code == 404:
        print("Error 404 page not found")
    else:
        print("Unable to retrive gold traders page")

    soup = BeautifulSoup(res.text, 'html.parser')
    sellPrice = soup.find(id='DetailPlace_uc_goldprices1_lblBLSell')
    buyPrice = soup.find(id='DetailPlace_uc_goldprices1_lblBLBuy')

    prices = {
        "sell": sellPrice.text,
        "buy": buyPrice.text
    }

    return prices


def getLongLivedToken(shortlivedUserToken, appId, appSecret, userId, pageId, graphApiVersion=11.0):
    # exchange short lived user token to long lived user token
    url = 'https://graph.facebook.com/v{graphApiVersion}/oauth/access_token?grant_type=fb_exchange_token&client_id={appId}&client_secret={appSecret}&fb_exchange_token={shortlivedUserToken}'.format(
        graphApiVersion=graphApiVersion, appId=appId, appSecret=appSecret, shortlivedUserToken=shortlivedUserToken)
    res = requests.get(url)
    if res.status_code == 200:
        print("Successfully exchange long lived user token")
    else:
        print("Unable to exchange long lived user token")
        return

    longlivedUserToken = json.loads(res.text)["access_token"]

    # get page long lived token from user long lived token
    longlivedPageTokenUrl = 'https://graph.facebook.com/v{graphApiVersion}/{userId}/accounts?access_token={longlivedUserToken}'.format(
        graphApiVersion=graphApiVersion, userId=userId, longlivedUserToken=longlivedUserToken)

    res2 = requests.get(longlivedPageTokenUrl)
    if res2.status_code == 200:
        print("Successfully retrieve long lived page token")
    else:
        print("Unable to retrive long lived page token", res2.text)
        return

    longlivedPageTokens = json.loads(res2.text)
    longlivedPageToken = None
    for pageToken in longlivedPageTokens["data"]:
        if pageToken["id"] == pageId:
            longlivedPageToken = pageToken["access_token"]

    return longlivedPageToken


def postFB(prices, longlivedPageToken, pageId):
    # Your Access Keys
    msg = 'ราคาทองคำวันนี้  ขาย: ' + prices["sell"] + 'ซื้อ: ' + prices["buy"]
    post_url = 'https://graph.facebook.com/{}/feed'.format(pageId)
    payload = {
        'message': msg,
        'access_token': longlivedPageToken
    }
    r = requests.post(post_url, data=payload)
    print(r.text)


if __name__ == "__main__":
    main()
