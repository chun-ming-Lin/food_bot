from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage



from .gmaps import Restaurant


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)

        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
 
            if isinstance(event, MessageEvent):  # 如果有訊息事件
 
                food = Restaurant(event.message.text)  #使用者傳入的訊息文字
 
                line_bot_api.reply_message(  # 回復輸入地點附近餐廳
                    event.reply_token,
                    messages=TextSendMessage(text=food.scrape())
                    
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()