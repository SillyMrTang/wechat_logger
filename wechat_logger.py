#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import logging  # 引入logging模块
import os.path
import time


class WechatNotice(object):

    def __init__(self):
        """
        企业微信注册链接 https://work.weixin.qq.com/wework_admin/register_wx?from=myhome
        corpid 注册完企业微信后的企业ID
        corpsecret 应用与小程序栏中自己创建一个应用得到的 secret

        """
        self.corpid = 'xxxxxxxxxx'
        self.corpsecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    def get_token(self):
        """
        根据API获取token
        """
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret,
        }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def log_manage(self):
        """

        log日志管理
        log_path 需要自己新建一个logs文件夹

        """
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_path = os.path.dirname(os.getcwd() + '/logs/')
        logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                            filename=log_path + rq + '.log',
                            filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                            # a是追加模式，默认如果不写的话，就是追加模式
                            format=
                            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            # 日志格式
                            )

    def send_msg(self, msg):
        """

        调用企业微信发送信息API, 参考链接 https://work.weixin.qq.com/api/doc#10167
        参考链接上有详细的参数说明
        touser: 默认为@all
        agentid: 创建应用时的 agentid
        msg: 程序报错时需要报警提示,在爬虫程序中传递过来
        需要在所创建的应用中设置可见范围,可自己创建群组
        在程序中调用方式 WechatNotice().send_msg(msg)

        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_token()
        data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": 1000002,
            "text": {
                "content": msg
            },
            "safe": 0
        }
        try:
            res = requests.post(url, json.dumps(data))
            result = json.loads(res.content.decode())
            if result["errmsg"] != "ok":
                self.log_manage()
                logging.error(result)
        except Exception as e:
            self.log_manage()
            logging.error(e)
