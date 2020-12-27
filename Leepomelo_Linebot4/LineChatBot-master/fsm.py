from transitions.extensions import GraphMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
from bs4 import BeautifulSoup
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
from nlp import nlp_ans
import pandas as pd

# global variable
flag = 0
ans_to_ques = ''
age = 0
gender = ''
height = 0
weight = 0
days = 0
BMR = 0
TDEE = 0
part = ''
diet_type = -1
df = pd.read_csv('food.csv')

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start
    def is_going_to_input_menu(self, event):
        text = event.message.text
        if (self.state == 'input_health_information' or self.state == 'show_pomelo_benefit' or self.state == 'show_pomelo_taboo') and text.lower() == '回上一頁':
            return True
        elif text == '商品資訊':
            return True
        else:
            False
    def is_going_to_menu(self,event):
        text = event.message.text
        if text == '菜單':
            return True
        return False
    def on_enter_menu(self,event):
        title = '歡迎光臨~~ 柚心園'
        text = '以下資訊提供給您，請『點選』'
        btn = [
            MessageTemplateAction(
                label = '商品介紹',
                text ='商品介紹'
            ),
            MessageTemplateAction(
                label = '菜單圖示',
                text = '菜單圖示'
            ),
            MessageTemplateAction(
                label = '回首頁',
                text = '回首頁'
            ),
        ]
        url = 'https://i.imgur.com/By2jInI.gif'
        send_button_message(event.reply_token, title, text, btn, url)
    def is_going_to_menu_pic(self,event):
        text = event.message.text
        if text == '菜單圖示' or (self.state == 'show_pomelo_introduction' and text == '菜單圖示'):
            return True
        return False
    def on_enter_menu_pic(self,event):
        send_image_message(event.reply_token, 'https://i.imgur.com/IwYquKJ.png?1')
    def is_going_to_question(self,event):
        text = event.message.text
        if text == '問答' or (self.state == 'answer' and text == '1') :
            return True
        elif text == '2':
            return False
    def on_enter_question(self,event):
        send_text_message(event.reply_token,'!!離開請輸入2\n\n您好，請輸入您的問題，只要是和本店有關的問題，就讓小柚來替您解答!!')
    def is_going_to_answer(self,event):
        text = event.message.text
        global ans_to_ques
        ans_to_ques = ''
        boss = '柚心園: '
        if text != '回首頁' and text != 'FSM' and text != '2':
            ans_to_ques = boss + nlp_ans(text)
            return True
        return False
    def on_enter_answer(self,event):
        global ans_to_ques
        ans_to_ques = ans_to_ques + '\n\n!!繼續問答請輸入『1』!!\n!!離開請輸入『2』'
        send_text_message(event.reply_token, ans_to_ques)  
    def on_enter_input_menu(self, event):
        title = '商品資訊主選單'
        text = '以下資訊提供給您，請『點選』'
        btn = [
            MessageTemplateAction(
                label = '商品優惠資訊',
                text ='商品優惠資訊'
            ),
            MessageTemplateAction(
                label = '商品介紹',
                text = '商品介紹'
            ),
            MessageTemplateAction(
                label = '健康資訊',
                text = '健康資訊'
            ),
            MessageTemplateAction(
                label = '回首頁',
                text = '回首頁'
            ),
        ]
        url = 'https://i.imgur.com/nuLVjN0.mp4'
        send_button_message(event.reply_token, title, text, btn, url)
    def is_going_to_show_pomelo_discount(self,event):
        text = event.message.text
        if text == '商品優惠資訊':
            return True
        return False
    def on_enter_show_pomelo_discount(self,event):
        send_text_message(event.reply_token,'!!!!優惠優惠看這裡!!!!\n1.目前使用線上表單訂購商品即可打9折\n2.天天買10斤就送1斤')
    def is_going_to_show_pomelo_introduction(self,event):
        text = event.message.text
        if text == '商品介紹':
            return True
        return False
    def on_enter_show_pomelo_introduction(self,event):
        send_text_message(event.reply_token,'麻豆老樹文旦，走過百年時光，在時光的陶冶之下，肉質鮮嫩多汁，甜而不膩，果粒晶瑩，飽滿的果肉裡滿滿的都是水分，獨特清新的果香絕對讓你難以忘懷')
    def is_going_to_input_health_information(self, event):
        text = event.message.text
        if text == '健康資訊' or ((self.state == 'input_health_information' or self.state == 'show_pomelo_benefit' or self.state == 'show_pomelo_taboo') and text == '回上一頁'):
            return True
        return False

    def on_enter_input_health_information(self, event):
        title = '健康資訊'
        text = '以下資訊提供給您，請『點選』'
        btn = [
            MessageTemplateAction(
                label = '對身體的益處',
                text ='益處'
            ),
            MessageTemplateAction(
                label = '飲食禁忌',
                text = '禁忌'
            ),
            MessageTemplateAction(
                label = '回上一頁',
                text = '回上一頁'
            ),
        ]
        url = 'https://i.imgur.com/IdtMhao.gif'
        send_button_message(event.reply_token, title, text, btn, url)
    def is_going_to_show_pomelo_benefit(self,event):
        text = event.message.text
        if text == '益處':
            return True
        return False
    def on_enter_show_pomelo_benefit(self,event):
        send_text_message(event.reply_token,'網頁資訊都在這->->->\nhttps://superfit.com.tw/all/eat-grapefruit-to-lose-weight/\nhttps://yesser99.pixnet.net/blog/post/371682337\nhttps://kknews.cc/culture/')
    def is_going_to_show_pomelo_taboo(self,event):
        text = event.message.text
        if text == '禁忌':
            return True
        return False
    def on_enter_show_pomelo_taboo(self,event):
        send_text_message(event.reply_token,'網頁資訊都在這->->->\nhttps://www.commonhealth.com.tw/article/article.action?nid=82870\nhttps://health.tvbs.com.tw/medical/318620')

    def is_going_to_choose(self, event):
        global days, diet_type
        text = event.message.text
        if text == '好' and diet_type != -1:
            return True
        if text.lower() == 'back' and diet_type != -1:
            return True
        #return True
        return True
    

    # state of choose
    def on_enter_choose(self, event):
        title = '健康資訊'
        text = '以下資訊提供給您，請點選'
        btn = [
            MessageTemplateAction(
                label = '對身體的益處',
                text ='益處'
            ),
            MessageTemplateAction(
                label = '飲食禁忌',
                text = '禁忌'
            ),
        ]
        url = 'https://i.imgur.com/3i4SoVG.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

