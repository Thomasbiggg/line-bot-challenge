from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

import json
import http.client
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

connection = http.client.HTTPSConnection('api.line.me')
headers = {}
# Add Authorization field
headers['Authorization'] = 'Bearer ' + '1VgBCdRa3TyfPx5OBwrRjuiPXK7LWCPv0s7BX5S7idxa8854ELfwoKn6VHshxgAKjan+can6+A0q6Wz4BBgvtjOrIpfLJ0lrOyF4tvBOicMxgwtaclG+7YlgVhXeyh8cGdUWsDnptCRUWa1JwgwnywdB04t89/1O/w1cDnyilFU='
headers['Content-Type'] = 'application/json'

postbackArr = ['work', 'competition', 'extracurricular', 'hobby']
scoreDic = {'work':0, 'competition':0, 'extracurricular':0, 'hobby':0}
chooseFlexMessage = json.load(open('selfpromotelinebot/returnTemplates/chooseTemplate.json', encoding='utf-8'))
# print(chooseFlexMessage['messages'][0]['contents']['contents'][1]['body']['contents'][0]['text'])
count = 0
@csrf_exempt
def callback(request):
    if request.method == 'POST':

        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                message = event.message.text
                if message == 'hi':
                    # 顯示來來來哩來
                    body = json.load(open('selfpromotelinebot/returnTemplates/selfIntroduceTemplate.json', encoding='utf-8'))
                    connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                    response = connection.getresponse()
                    print(response.read().decode())
            elif isinstance(event, PostbackEvent):
                data = event.postback.data
                reply_token = event.reply_token

                # 點擊來來來按鈕後的carousel
                if data == 'hi':
                    body = json.load(open('selfpromotelinebot/returnTemplates/chooseTemplate.json', encoding='utf-8'))
                    connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                    response = connection.getresponse()
                    print(response.read().decode())

                    # line_bot_api.reply_message(reply_token, FlexSendMessage('來來來哩來', contents=chooseFlexMessage))

                # 點擊工作經驗
                elif data == 'workExp':
                    if 'work' not in postbackArr:
                        text_message = TextSendMessage(text='給過帥度了噢！')
                        line_bot_api.reply_message(reply_token, text_message)

                        body = chooseFlexMessage
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())
                    else:
                        body = json.load(open('selfpromotelinebot/returnTemplates/workTemplate.json', encoding='utf-8'))
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())

                    # line_bot_api.reply_message(reply_token, FlexSendMessage('work', contents=workFlexMessage))

                # 點擊競賽經驗
                elif data == 'competitionExp':
                    if 'competition' not in postbackArr:
                        text_message = TextSendMessage(text='給過帥度了噢！')
                        line_bot_api.reply_message(reply_token, text_message)

                        body = chooseFlexMessage
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())
                    else:
                        body = json.load(open('selfpromotelinebot/returnTemplates/competitionTemplate.json', encoding='utf-8'))
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())

                    # line_bot_api.reply_message(reply_token, FlexSendMessage('competition', contents=competitionFlexMessage))

                # 點擊社團經驗
                elif data == 'extracurricularExp':
                    if 'extracurricular' not in postbackArr:
                        text_message = TextSendMessage(text='給過帥度了噢！')
                        line_bot_api.reply_message(reply_token, text_message)

                        body = chooseFlexMessage
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())
                    else:
                        body = json.load(open('selfpromotelinebot/returnTemplates/extracurricularTemplate.json', encoding='utf-8'))
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())

                    # line_bot_api.reply_message(reply_token, FlexSendMessage('extracurricular', contents=extracurricularFlexMessage))

                # 點擊興趣
                elif data == 'hobby':
                    if 'hobby' not in postbackArr:
                        text_message = TextSendMessage(text='給過帥度了噢！')
                        line_bot_api.reply_message(reply_token, text_message)

                        body = chooseFlexMessage
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())
                    else:
                        body = json.load(open('selfpromotelinebot/returnTemplates/hobbyTemplate.json', encoding='utf-8'))
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())

                    # hobbyFlexMessage = json.load(open('selfpromotelinebot/returnTemplates/hobbyTemplate.json', encoding='utf-8'))
                    # line_bot_api.reply_message(reply_token, FlexSendMessage('hobby', contents=hobbyFlexMessage))
                # 選擇帥度
                elif isinstance(int(data[0]), int):

                    # 工作/競賽/社團/興趣
                    responseCategory = data[1:]

                    # carousel
                    body = chooseFlexMessage

                    if responseCategory not in postbackArr:
                        text_message = TextSendMessage(text='給過帥度了噢！')
                        line_bot_api.reply_message(reply_token, text_message)

                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())
                    else:
                        scoreDic[responseCategory] = int(data[0])
                        postbackArr.remove(responseCategory)
                        if len(postbackArr) == 0:
                            scoreArr = [x for x in scoreDic.values()]
                            totalScore = sum(scoreArr)
                            global count
                            count += 1
                            body = json.load(
                                open('selfpromotelinebot/returnTemplates/degreeTemplate.json', encoding='utf-8'))
                            for i in range(4):
                                body['messages'][0]['contents']['body']['contents'][4]['contents'][i]['contents'][1][
                                    'text'] = "☆ " + str(scoreArr[i])
                            body['messages'][0]['contents']['body']['contents'][4]['contents'][5]['contents'][1][
                                'text'] = "☆ " + str(totalScore)
                            body['messages'][0]['contents']['body']['contents'][6]['contents'][1]['text'] = "# " + str(
                                count)
                            connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                            response = connection.getresponse()
                            print(response.read().decode())
                            postbackArr.append('work')
                            postbackArr.append('competition')
                            postbackArr.append('extracurricular')
                            postbackArr.append('hobby')
                        else:
                            connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                            response = connection.getresponse()
                            print(response.read().decode())


        return HttpResponse()
    else:
        return HttpResponseBadRequest()