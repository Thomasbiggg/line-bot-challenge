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
headers['Authorization'] = 'Bearer ' + '/sZCPcz0jlqC4zuFfS9wZfu2QmxuzQ84vihUMfnN6ezpZS+eMM2+WYUzzL2pxpRl6BQovQ0zRA1QPlQbsL65h/dsdgmVPMkKJ4TK+08mz6yDkIE0wi+GqqL+Pcv8d+Ssd8bZ2oRCbpQlYsJuhqLHBgdB04t89/1O/w1cDnyilFU='
headers['Content-Type'] = 'application/json'

postbackArr = ['work', 'competition', 'extracurricular', 'hobby']
scoreDic = {'work': 0, 'competition': 0, 'extracurricular': 0, 'hobby': 0}

chooseFlexMessage = json.load(open('selfpromotelinebot/returnTemplates/chooseTemplate.json', encoding='utf-8'))
# print(chooseFlexMessage['messages'][0]['contents']['contents'][1]['body']['contents'][0]['text'])
count = 0
@csrf_exempt
def callback(request):

    global scoreDic
    global postbackArr
    global count
    global chooseFlexMessage

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
            print(event)
            reply_token = event.reply_token
            to = event.source.user_id
            chooseFlexMessage['replyToken'] = reply_token
            chooseFlexMessage['to'] = to
            # 介紹頁面
            if isinstance(event, MessageEvent):
                message = event.message.text

                if message == 'hi':
                    # 顯示來來來哩來
                    body = json.load(open('selfpromotelinebot/returnTemplates/selfIntroduceTemplate.json', encoding='utf-8'))
                    body['replyToken'] = reply_token
                    body['to'] = to
                    connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                    response = connection.getresponse()
                    print(response.read().decode())

            elif isinstance(event, PostbackEvent):

                data = event.postback.data

                # 點擊來來來按鈕後的carousel
                if data == 'hi':
                    body = json.load(open('selfpromotelinebot/returnTemplates/chooseTemplate.json', encoding='utf-8'))
                    body['replyToken'] = reply_token
                    body['to'] = to
                    connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                    response = connection.getresponse()
                    print(response.read().decode())

                # 頁面選擇
                if data == 'work' or data == 'competition' or data == 'extracurricular' or data == 'hobby':

                    # 評分json檔
                    jsonStr = 'selfpromotelinebot/returnTemplates/' + data + 'Template.json'

                    if data not in postbackArr:

                        # 判斷是否評分
                        if scoreDic[data] == 0:
                            text_message = TextSendMessage(text='要先選帥度噢！')
                            line_bot_api.reply_message(reply_token, text_message)

                            # 跳出帥度選擇頁面
                            body = json.load(open(jsonStr, encoding='utf-8'))
                            body['replyToken'] = reply_token
                            body['to'] = to
                            connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                            response = connection.getresponse()
                            print(response.read().decode())

                        # 已經點過項目
                        else:
                            text_message = TextSendMessage(text='給過帥度了噢！')
                            line_bot_api.reply_message(reply_token, text_message)

                            body = chooseFlexMessage
                            connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                            response = connection.getresponse()
                            print(response.read().decode())

                    # 都沒有選過
                    else:
                        postbackArr.remove(data)

                        body = json.load(open(jsonStr, encoding='utf-8'))
                        body['replyToken'] = reply_token
                        body['to'] = to
                        connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                        response = connection.getresponse()
                        print(response.read().decode())
                    print(scoreDic)
                    print(postbackArr)

                # 選擇帥度
                elif isinstance(int(data[0]), int):

                    # 工作/競賽/社團/興趣
                    responseCategory = data[1:]

                    # 用來判斷該項是否選過帥度
                    if scoreDic[responseCategory] > 0:
                        text_message = TextSendMessage(text='給過帥度了噢！')
                        line_bot_api.reply_message(reply_token, text_message)

                        connection.request('POST', '/v2/bot/message/push', json.dumps(chooseFlexMessage), headers)
                        response = connection.getresponse()
                        print(response.read().decode())

                    # 還沒選過帥度
                    else:
                        scoreDic[responseCategory] = int(data[0])
                        # postbackArr.remove(responseCategory)

                        # 用來判斷是否選完所有帥度
                        if len(postbackArr) == 0 and all([x > 0 for x in scoreDic.values()]):
                            scoreArr = [x for x in scoreDic.values()]
                            totalScore = sum(scoreArr)
                            count += 1
                            body = json.load(open('selfpromotelinebot/returnTemplates/degreeTemplate.json', encoding='utf-8'))
                            for i in range(4):
                                body['messages'][0]['contents']['body']['contents'][4]['contents'][i]['contents'][1]['text'] = "☆ " + str(scoreArr[i])
                            body['messages'][0]['contents']['body']['contents'][4]['contents'][5]['contents'][1]['text'] = "☆ " + str(totalScore)
                            body['messages'][0]['contents']['body']['contents'][6]['contents'][1]['text'] = "# " + str(count)
                            body['replyToken'] = reply_token
                            body['to'] = to
                            connection.request('POST', '/v2/bot/message/push', json.dumps(body), headers)
                            response = connection.getresponse()
                            print(response.read().decode())

                            # 刷新紀錄，準備下一份成績單安
                            postbackArr.append('work')
                            postbackArr.append('competition')
                            postbackArr.append('extracurricular')
                            postbackArr.append('hobby')
                            scoreDic['work'] = 0
                            scoreDic['competition'] = 0
                            scoreDic['extracurricular'] = 0
                            scoreDic['hobby'] = 0

                            chooseFlexMessage = json.load(open('selfpromotelinebot/returnTemplates/chooseTemplate.json', encoding='utf-8'))

                        else:
                            blockNum = len(chooseFlexMessage['messages'][0]['contents']['contents'])

                            for i in range(blockNum):
                                if chooseFlexMessage['messages'][0]['contents']['contents'][i]['action']['data'] == responseCategory:
                                    chooseFlexMessage['messages'][0]['contents']['contents'].pop(i)
                                    break
                            connection.request('POST', '/v2/bot/message/push', json.dumps(chooseFlexMessage), headers)
                            response = connection.getresponse()
                            print(response.read().decode())

                    print(scoreDic)
                    print(postbackArr)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()