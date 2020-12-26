from transitions.extensions import GraphMachine

from utils import send_text_message,select_time,weather_crawl,push_notify,fsm_pic
from test import *
import datetime

from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.text= ""
        self.condition = [0]
    def is_going_to_time_county(self, event):
        text = event.message.text
        return text.lower() == "p"

    def on_enter_time_county(self, event):
        print("I'm entering time_county")
        reply_token = event.reply_token
        send_text_message(reply_token, "您已進入推播模式\n請選擇要查詢的縣市:\n\t臺北市(數字1)\n\t新北市(數字2)\n\t桃園市(數字3)\n\t臺中市(數字4)\n\t臺南市(數字5)\n\t高雄市(數字6)\n\t基隆市(數字7)\n\t新竹市(數字8)\n\t嘉義市(數字9)\n\t新竹縣(數字10)\n\t苗栗縣(數字11)\n\t彰化縣(數字12)\n\t南投縣(數字13)\n\t雲林縣(數字14)\n\t嘉義縣(數字15)\n\t屏東縣(數字16)\n\t宜蘭縣(數字17)\n\t花蓮市(數字18)\n\t臺東縣(數字19)\n\t澎湖縣(數字20)\n\t金門縣(數字21)\n\t連江縣(數字22)\n\n輸入 m 回到功能選單")

    def on_exit_time_county(self, event):
        print("Leaving time_county")

    def time_county_back_menu (self, event):
        text = event.message.text
        return text.lower() == "m"

    def is_going_to_time(self, event):
        self.text = event.message.text
        if c.get(self.text.lower()) != None:
            return True
        else:
            return False

    def on_enter_time(self, event):
        print("I'm entering time")
        reply_token = event.reply_token
        userid = event.source.user_id
        select_time(reply_token, userid) 

    def on_exit_time(self, event):
        print("Leaving time")


    def time_back_time_county(self, event):
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage):
                text = event.message.text
                return text.lower() == "c"

    def time_back_menu(self, event):
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage):
                text = event.message.text
                return text.lower() == "m"


    def is_going_to_push_notify(self, event):
        return True

    def on_enter_push_notify(self, event):
        print("I'm entering push_notify")
        reply_token = event.reply_token
        userid = event.source.user_id
        text = self.text.lower()
        current_date = ""
        send_text_message(reply_token,"您設定的時間為每日的"+event.postback.params.get('time')+"\n選擇的縣市為"+c_c.get(c.get(text)) +"\n\n輸入 m 回到功能選單\n輸入 c 重新選擇縣市和時間\n輸入 t 重新輸入時間")
        self.condition = [1]
        while True:
            if self.condition[0] == 0:
                break;
            else:
                if datetime.datetime.now().strftime('%H:%M') ==  event.postback.params.get('time'):
                    if current_date != datetime.datetime.now().strftime('%d'):
                        current_date = datetime.datetime.now().strftime('%d')
                        push_notify(userid,event,text,self.condition)
        '''
        push_notify(userid,event,text,self.condition)
        '''

    def on_exit_push_notify(self, event):
        self.condition = [0]
        print("Leaving push_notify")


    def push_notify_back_time_county(self, event):
        text = event.message.text
        return text.lower() == "c"

    def push_notify_back_time(self, event):
        text = event.message.text
        return text.lower() == "t"

    def push_notify_back_menu(self, event):
        text = event.message.text
        return text.lower() == "m"

    def is_going_to_weather(self, event):
        text = event.message.text
        return text.lower() == "w"

    def on_enter_weather(self, event):
        print("I'm entering weather")

        reply_token = event.reply_token
        send_text_message(reply_token,"請選擇要查詢的縣市:\n\t臺北市(數字1)\n\t新北市(數字2)\n\t桃園市(數字3)\n\t臺中市(數字4)\n\t臺南市(數字5)\n\t高雄市(數字6)\n\t基隆市(數字7)\n\t新竹市(數字8)\n\t嘉義市(數字9)\n\t新竹縣(數字10)\n\t苗栗縣(數字11)\n\t彰化縣(數字12)\n\t南投縣(數字13)\n\t雲林縣(數字14)\n\t嘉義縣(數字15)\n\t屏東縣(數字16)\n\t宜蘭縣(數字17)\n\t花蓮市(數字18)\n\t臺東縣(數字19)\n\t澎湖縣(數字20)\n\t金門縣(數字21)\n\t馬祖縣(數字22)\n\n輸入 m 回到功能選單")

    def on_exit_weather(self, event):
        print("Leaving weather")


    def weather_back_menu(self, event):
        text = event.message.text
        return text.lower() == "m"

    def is_going_to_weather_county(self, event):
        self.text = event.message.text
        if c.get(self.text.lower()) != None:
            return True
        else:
            return False

    def on_enter_weather_county(self, event):
        print("I'm entering weather_county")

        userid = event.source.user_id
        reply_token = event.reply_token
        text = self.text.lower()
        send_text_message(reply_token,"選擇的縣市為"+c_c.get(c.get(text))+"\n查詢中請稍候")
        weather_crawl(userid, c.get(text))

    def on_exit_weather_county(self, event):
        print("Leaving weather_county")

    def weather_county_back_weather(self, event):
        text = event.message.text
        return text.lower() == "c"

    def weather_county_back_menu(self, event):
        text = event.message.text
        return text.lower() == "m"

    def is_going_to_menu(self, event):
        return True 

    def on_enter_menu(self, event):
        print("I'm entering menu")
        reply_token = event.reply_token
        send_text_message(reply_token, "歡迎使用天氣機器人\n功能:\n\t可供查詢當前所在縣市的天氣\n\t像是氣溫，降雨機率等\n\t也可設定固定時間\n\t每日推播最新天氣訊息。\n\n輸入 w 以查詢天氣\n輸入 p 以設定推播時間\n輸入 s 以查看fsm diagram")

    def on_exit_menu(self,event):
        print("Leaving menu")


   
    def is_going_to_show_picture(self, event):
        text = event.message.text
        return text.lower() == "s"

    def on_enter_show_picture(self, event):
        print("I'm entering show picture")

        reply_token = event.reply_token
        userid = event.source.user_id
        fsm_pic(reply_token,userid)

    def on_exit_show_picture(self,event):
        print("Leaving show_picture")

    def show_picture_back_menu(self, event):
        text = event.message.text
        return text.lower() == "m"
