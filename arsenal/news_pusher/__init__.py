#!/usr/bin/python  
#-*-coding:utf-8-*-
import jpush
from conf import app_key, master_secret, gunner_app_key, gunner_master_secret


def push_news(artical_id, header):
    server = jpush.JPush(app_key, master_secret)
    push = server.create_push()
    push.audience = jpush.all_
    android_msg = jpush.android(alert=header,
                                title="ArsenalNews",
                                extras={"Header": header,
                                        "ArticalId": artical_id})
    push.notification = jpush.notification(alert="Hello, Arsenal",
                                           android=android_msg)
    push.platform = jpush.platform("android")
    push.send()


def push_gunners_news(artical_id, header):
    server = jpush.JPush(gunner_app_key, gunner_master_secret)
    push = server.create_push()
    push.audience = jpush.all_
    android_msg = jpush.android(alert=header,
                                title="ArsenalNews",
                                extras={"header": header,
                                        "articleId": artical_id})
    push.notification = jpush.notification(alert="Hello, Arsenal",
                                           android=android_msg)
    push.platform = jpush.platform("android")
    push.send()
