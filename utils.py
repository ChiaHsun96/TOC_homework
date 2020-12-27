import os
from bs4 import BeautifulSoup
from selenium import webdriver
from test import *
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageCarouselTemplate,ImageCarouselColumn,DatetimePickerAction,FlexSendMessage,ImageSendMessage
import datetime
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"
def select_time(reply_token,userid):

    message = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://img.komicolle.org/2020-12/16074154393411.jpg",
        "size": "full",
        "aspectRatio": "620:438",
        "aspectMode": "cover",
        "action": {
          "type": "datetimepicker",
          "label": "action",
          "data": "hello",
          "mode": "time",
          "initial": "00:00"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "點選本圖片設定推播時間",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          }
        ]
      }
    }
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text = "推播設定",contents=message))
    line_bot_api.push_message(userid, TextSendMessage(text = "輸入 m 回到功能選單\n輸入 c 重新選擇縣市"))
    return "OK"

def weather_crawl(userid,county):
    line_bot_api = LineBotApi(channel_access_token)
    crawl(userid, county)
    line_bot_api.push_message(userid, TextSendMessage(text = "輸入 m 回到功能選單\n輸入 c 重新選擇縣市"))
    return "OK"


def push_notify(userid, event,text,var):
    line_bot_api = LineBotApi(channel_access_token)
    message = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://img.komicolle.org/2017-09/15042700021590.jpg",
        "size": "full",
        "aspectRatio": "620:529",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "天氣通知",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          }
        ]
      }
    }
    line_bot_api.push_message(userid, FlexSendMessage(alt_text = "天氣通知",contents=message))
    crawl(userid, c.get(text.lower()))
    line_bot_api.push_message(userid, TextSendMessage(text = "輸入 m 回到功能選單\n輸入 c 重新選擇縣市和時間\n輸入 t 重新選擇時間"))


def fsm_pic(reply_token,userid): 
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, ImageSendMessage(original_content_url='https://i.imgur.com/cy1Vpba.png',preview_image_url='https://i.imgur.com/cy1Vpba.png'))
    line_bot_api.push_message(userid, TextSendMessage(text = "輸入 m 回到功能選單"))

def crawl(userid ,county):
    line_bot_api = LineBotApi(channel_access_token)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    chrome.get("https://www.cwb.gov.tw/V8/C/")

    soup = BeautifulSoup(chrome.page_source, 'html.parser')

    cont = soup.find('div', {'class': 'city-in'})

    date = cont.find('span', {'class': 'date'})


    if county == '1':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=63")
    elif county == '2':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=65")
    elif county == '3':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=68")
    elif county == '4':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=66")
    elif county == '5':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=67")
    elif county == '6':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=64")
    elif county == '7':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10017")
    elif county == '8':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10018")
    elif county == '9':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10020")
    elif county == '10':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10004")
    elif county == '11':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10005")
    elif county == '12':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10007")
    elif county == '13':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10008")
    elif county == '14':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10009")
    elif county == '15':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10010")
    elif county == '16':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10013")
    elif county == '17':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10002")
    elif county == '18':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10015")
    elif county == '19':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10014")
    elif county == '20':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=10016")
    elif county == '21':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=09020")
    elif county == '22':
        chrome.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=09007")
    else:
        exit(0)

    soup = BeautifulSoup(chrome.page_source, 'html.parser')

    data = soup.find('div', {'class': 'banner_wrap'})
    
    title = soup.find('div', {'class': 'main-title-bar'})


    for i in range(3):
        message = {
          "type": "bubble",
          "hero": {
            "type": "image",
            "url": "https://www.cwb.gov.tw" + data.find_all('img')[i].get('src') ,
            "size": "5xl",
            "aspectRatio": "92:64",
            "aspectMode": "fit",
            "action": {
              "type": "uri",
              "uri": "http://linecorp.com/"
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": data.find_all('span', {'class': 'title'})[i].getText(),
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "日期",
                        "color": "#aaaaaa",
                        "size": "sm"
                      },
                      {
                        "type": "text",
                        "text": date.getText(),
                        "color": "#666666",
                        "size": "sm",
                        "position": "absolute",
                        "offsetStart": "45%"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": "縣市",
                        "size": "sm",
                        "color": "#aaaaaa"
                      },
                      {
                        "type": "text",
                        "text": title.find('h2', {'class': 'main-title'}).getText()[8:],
                        "size": "sm",
                        "color": "#666666",
                        "position": "absolute",
                        "offsetStart": "45%"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "氣溫",
                        "color": "#aaaaaa",
                        "size": "sm"
                      },
                      {
                        "type": "text",
                        "text": data.find_all('span', {'class': 'tem-C is-active'})[i].getText()+"°C",
                        "color": "#666666",
                        "size": "sm",
                        "position": "absolute",
                        "offsetStart": "45%"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": "降雨機率",
                        "size": "sm",
                        "color": "#aaaaaa"
                      },
                      {
                        "type": "text",
                        "text": data.find_all('span', {'class': 'rain'})[i].getText(),
                        "size": "sm",
                        "color": "#666666",
                        "position": "absolute",
                        "offsetStart": "45%"
                      }
                    ]
                  }
                ]
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "align": "center",
                "text": data.find_all('span', {'class': 'text'})[i].getText()
              }
            ]
          }
        }
        line_bot_api.push_message(userid, FlexSendMessage(alt_text = "天氣通知",contents=message))
    chrome.close()
    return "OK"
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
