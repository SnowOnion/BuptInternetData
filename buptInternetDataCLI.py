#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'SnowOnion'

'''
# 开发文档

## TODO-Feature

+ GUI，360 那样的小悬浮球 \_(:з」∠)\_
+ 长期稳定性测试。暴力except重启。
+ 各种异常后 停止循环 待定时检查或手工重试
+ 即时网速计算...
+ 流量报表 for xk 这种 自掏流量-报销 的大数据工作者

(+ 数据挖掘…… 流量理财orz)

## TODO-BugFix

+ 若是从 10.4.1.2 登录的话（aka 非宿舍的网络？），测量不准。
+ [已修改 测试中] Windows + Python 2.7.0 乱码 via http://bbs.byr.cn/#!article/BUPTNet/73425

## 更新日志

+ （2015-03-18 23:02:08）python 2/3 兼容
+ （2015-03-23 20:05:35）修正 python 2/3 整数除法行为不同引起的余额错误
+ （2015-04-03 11:20:01）u'xxx' 法试图 Windows + Python 2.7.0 乱码 via http://bbs.byr.cn/#!article/BUPTNet/73425
+ （2015-04-07 08:51:35）补上漏掉的 u'￥%.2f'

'''

if __name__ == '__main__':
    HOST = '10.3.8.211'

    import math
    import time
    import datetime
    import sys
    import socket

    if sys.version > '3':
        import http.client as http_client_23

        str_23 = str
    else:
        import httplib as http_client_23

        str_23 = unicode

    def to_file(content, filename):
        f = open(filename, 'w')
        f.write(content)
        f.close()

    def renew_connection():
        """
        SIDE EFFECT!
        :return:
        """
        global connection
        connection = http_client_23.HTTPConnection(HOST, timeout=5)

    def duration_format(dur_min):
        # Zen: explicit is better than implicit...
        if dur_min < 60:
            return '%d min' % dur_min
        else:
            return '%d h %d min' % (math.floor(dur_min / 60), dur_min % 60)

    def data_format(data_k_byte):
        k = 1024
        m = 1024 ** 2
        g = 1024 ** 3

        if data_k_byte < k:
            return '%d KByte' % data_k_byte
        elif data_k_byte < m:
            return '%d MByte %d KByte' % (math.floor(data_k_byte / k), data_k_byte % k)
        elif data_k_byte < g:
            return '%d GByte %d MByte %d KByte' % \
                   (math.floor(data_k_byte / m), math.floor(data_k_byte / k) % k, data_k_byte % k)
        else:
            return '%d TByte %d GByte %d MByte %d KByte' % \
                   (math.floor(data_k_byte / g), math.floor(data_k_byte / m) % k, math.floor(data_k_byte / k) % k,
                    data_k_byte % k)

    def currency_format(cur_rmb_hao):
        """
        不怕 %.2f 给四舍五入的原因：
        服务器给的数据，看起来只精确到分嘛。
        :param cur_rmb_hao: hao for 毫，i.e. 1/10 厘， 1/10000 元
        :return:
        """
        return u'￥%.2f' % (float(cur_rmb_hao) / 10000)

    def get_and_show(conn, show_func):
        try:
            """
            conn.request('GET', '/'):
            + 连着 Ali VPN: TimeoutError：[Errno 60] Operation timed out
            + 断开 WIFI: OSError：[Errno 51] Network is unreachable
            + 连着宿舍 WIFI，OS X 网络偏好设置显示，分到 IP，却上不了 10.3.8.211，可能路由器亟待重启：TimeoutError: [Errno 60] Operation timed out

            """
            conn.request('GET', '/')
            info_response = conn.getresponse()
            # print(info_response.getcode())
            # print(info_response.getheaders())

            # if info_response.status >= 300 or info_response.status < 200:
            # info_response.read()
            # exit()
            resp_body = info_response.read()
            ''' Actually the encoding setting is not necessary when only match the english content in html page '''
            resp_str = str_23(resp_body, encoding='gb2312')

            # TODO 异常的哲学 https://www.python.org/dev/peps/pep-0344/
            # 想到一点：把底层的、技术的异常（ValueError, OSError）捕获后，转抛出高层的、业务的异常
            try:
                time_ind = resp_str.index("time='") + len("time='")
                time_min = int(resp_str[time_ind:time_ind + 10])
                flow_ind = resp_str.index("flow='") + len("flow='")
                flow_k_byte = int(resp_str[flow_ind:flow_ind + 10])
                fee_ind = resp_str.index("fee='") + len("fee='")
                fee_hao = int(resp_str[fee_ind:fee_ind + 10])
                show_func(time_min, flow_k_byte, fee_hao)
            except ValueError:
                """
                搜索不到这几个子串之一。
                （或 没登录 提示页改版）@TroubleShooting
                """
                print('')
                print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
                print(u'貌似没有登录校园网网关 http://10.3.8.211 或 http://10.4.1.2 。')
        # …… TimeoutError 继承 OSError。就让他漏下去吧
        # except TimeoutError:
        # renew_connection()
        # print('')
        # print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        # print('超时啦…… 请检查网络设置。')
        except (OSError, socket.timeout, socket.error):
            # ...否则再次 request 时报 http.client.CannotSendRequest: Request-sent
            renew_connection()
            print('')
            print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            print(u'访问不到 %s , 貌似没有联网或并非北邮校园网。' % HOST)

    def command_line_show(time_min, flow_k_byte, fee_hao):
        print('')
        print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        print(u'已使用时长：' + duration_format(time_min))
        print(u'已使用校外流量：' + data_format(flow_k_byte))
        print(u'余额：' + currency_format(fee_hao))

    connection = 'A HTTP Connection Placeholder'
    renew_connection()

    while True:
        get_and_show(connection, command_line_show)
        time.sleep(1)
