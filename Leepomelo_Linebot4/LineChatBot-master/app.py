import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
from fsm import TocMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message


load_dotenv()


machine = TocMachine(
    states=[
        'question',
        'answer',
        'input_health_information',
        'input_menu',
        'menu',
        'menu_pic',
        'show_pomelo_discount',
        'show_pomelo_introduction',
        'show_pomelo_benefit',
        'show_pomelo_taboo',
    ],
    transitions=[
        #Initial
        {'trigger': 'advance', 'source': 'user', 'dest': 'input_menu', 'conditions': 'is_going_to_input_menu'},
        {'trigger': 'advance', 'source': 'user', 'dest': 'question', 'conditions': 'is_going_to_question'},
        {'trigger': 'advance', 'source': 'user', 'dest': 'menu', 'conditions': 'is_going_to_menu'},
        #menu
        {'trigger': 'advance', 'source': 'menu', 'dest': 'show_pomelo_introduction', 'conditions': 'is_going_to_show_pomelo_introduction'},
        {'trigger': 'advance', 'source': 'menu', 'dest': 'menu_pic', 'conditions': 'is_going_to_menu_pic'},
        #menu_pic
        {'trigger': 'advance', 'source': 'menu_pic', 'dest': 'menu_pic', 'conditions': 'is_going_to_menu_pic'},
        {'trigger': 'advance', 'source': 'menu_pic', 'dest': 'show_pomelo_introduction', 'conditions': 'is_going_to_show_pomelo_introduction'},
        #question Answer
        {'trigger': 'advance', 'source': 'question', 'dest': 'answer', 'conditions': 'is_going_to_answer'},
        {'trigger': 'advance', 'source': 'answer', 'dest': 'question', 'conditions': 'is_going_to_question'},
        #Health_Information
        {'trigger': 'advance', 'source': 'input_menu', 'dest': 'input_health_information', 'conditions': 'is_going_to_input_health_information'},
        {'trigger': 'advance', 'source': 'input_health_information', 'dest': 'input_menu', 'conditions': 'is_going_to_input_menu'},
        {'trigger': 'advance', 'source': 'input_health_information', 'dest': 'input_health_information', 'conditions': 'is_going_to_input_health_information'},
        #Pomelo discount
        {'trigger': 'advance', 'source': 'input_menu', 'dest': 'show_pomelo_discount', 'conditions': 'is_going_to_show_pomelo_discount'},
        {'trigger': 'advance', 'source': 'show_pomelo_discount', 'dest': 'show_pomelo_discount', 'conditions': 'is_going_to_show_pomelo_discount'},
        {'trigger': 'advance', 'source': 'show_pomelo_discount', 'dest': 'show_pomelo_introduction', 'conditions': 'is_going_to_show_pomelo_introduction'},
        {'trigger': 'advance', 'source': 'show_pomelo_discount', 'dest': 'input_health_information', 'conditions': 'is_going_to_input_health_information'},
        #Pomelo introduction
        {'trigger': 'advance', 'source': 'input_menu', 'dest': 'show_pomelo_introduction', 'conditions': 'is_going_to_show_pomelo_introduction'},
        {'trigger': 'advance', 'source': 'show_pomelo_introduction', 'dest': 'show_pomelo_discount', 'conditions': 'is_going_to_show_pomelo_discount'},
        {'trigger': 'advance', 'source': 'show_pomelo_introduction', 'dest': 'show_pomelo_introduction', 'conditions': 'is_going_to_show_pomelo_introduction'},
        {'trigger': 'advance', 'source': 'show_pomelo_introduction', 'dest': 'input_health_information', 'conditions': 'is_going_to_input_health_information'},
        {'trigger': 'advance', 'source': 'show_pomelo_introduction', 'dest': 'menu_pic', 'conditions': 'is_going_to_menu_pic'},
        #Pomelo benefit
        {'trigger': 'advance', 'source': 'input_health_information', 'dest': 'show_pomelo_benefit', 'conditions': 'is_going_to_show_pomelo_benefit'},
        {'trigger': 'advance', 'source': 'show_pomelo_taboo', 'dest': 'show_pomelo_benefit', 'conditions': 'is_going_to_show_pomelo_benefit'},
        {'trigger': 'advance', 'source': 'show_pomelo_benefit', 'dest': 'show_pomelo_benefit', 'conditions': 'is_going_to_show_pomelo_benefit'},
        {'trigger': 'advance', 'source': 'show_pomelo_benefit', 'dest': 'input_menu', 'conditions': 'is_going_to_input_menu'},
        #Pomelo taboo
        {'trigger': 'advance', 'source': 'input_health_information', 'dest': 'show_pomelo_taboo', 'conditions': 'is_going_to_show_pomelo_taboo'},
        {'trigger': 'advance', 'source': 'show_pomelo_benefit', 'dest': 'show_pomelo_taboo', 'conditions': 'is_going_to_show_pomelo_taboo'},
        {'trigger': 'advance', 'source': 'show_pomelo_taboo', 'dest': 'show_pomelo_taboo', 'conditions': 'is_going_to_show_pomelo_taboo'},
        {'trigger': 'advance', 'source': 'show_pomelo_taboo', 'dest': 'input_menu', 'conditions': 'is_going_to_input_menu'},
        {
            'trigger': 'go_back',
            'source': [
                'question',
                'answer',
                'input_health_information',
                'input_menu',
                'menu',
                'menu_pic',
                'show_pomelo_discount',
                'show_pomelo_introduction',
                'show_pomelo_benefit',
                'show_pomelo_taboo',
            ],
            'dest': 'user'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path='')


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

mode = 0

@app.route('/callback', methods=['POST'])
def webhook_handler():
    global mode
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')
        response = machine.advance(event)
        if response == False:
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, 'https://i.imgur.com/j75C7Jo.png?1')
            elif event.message.text == '訂購':
                send_text_message(event.reply_token, '!!線上訂購請點以下連結\nhttps://docs.google.com/forms/d/e/1FAIpQLSdA2XJr4gzZOMetY-DJbEmCCpGLSoAy5o3xsCi0aMYP7dANEA/viewform?usp=sf_link\n\n有任何問題都可聯絡李老闆\n手機:09-58975339')
            elif event.message.text == '柚心園' or event.message.text == '回首頁' or machine.state == 'user' or ((machine.state == 'answer' or machine.state == 'question') and event.message.text == '2'):
                title = '歡迎光臨~~ 柚心園'
                text = '以下資訊提供給您，請『點選』'#text不能太長
                btn = [ #不可超過4個選項
                    MessageTemplateAction(
                        label = '商品資訊',
                        text ='商品資訊'
                    ),
                    MessageTemplateAction(
                        label = '訂購',
                        text = '訂購'
                    ),
                    MessageTemplateAction(
                        label = '問答',
                        text = '問答'
                    ),
                    MessageTemplateAction(
                        label = 'MENU',
                        text = '菜單'
                    ),
                ]
                url = 'https://i.imgur.com/5Yi13jZ.gif'
                send_button_message(event.reply_token, title, text, btn, url)
                machine.go_back()
            elif machine.state == 'answer' or machine.state == 'sale_address':
                send_text_message(event.reply_token, '!!繼續問答請輸入『1』!!\n!!離開請輸入『2』')
            elif machine.state == 'show_pomelo_discount' or machine.state == 'input_health_introduction' or machine.state == 'input_menu':
                send_text_message(event.reply_token, '您的選項不在列表中，請您重新輸入')
            elif machine.state == 'show_pomelo_taboo' or machine.state == 'input_health_information' or machine.state == 'show_pomelo_benefit':
                send_text_message(event.reply_token, '您的選項不在列表中，請您重新輸入')
            elif machine.state == 'input_menu':
                send_text_message(event.reply_token, '請重新選擇!!!')
            else:
                send_text_message(event.reply_token, '請重新選擇!!!')

    return 'OK'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')


if __name__ == '__main__':
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port, debug=True)
