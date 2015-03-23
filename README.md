# Use | 用途

监控当前设备上登录的北邮校园网账户的流量使用情况。

# Dependency | 依赖

+ Python 2.x or 3.x (Tested on 2.7 and 3.3)

# Run | 运行方式

In Terminal:

  python buptInternetDataCLI.py

# Core Technology (Python 3 real code) | 核心科技（Python 3 真代码）

    import http.client
    connection = http.client.HTTPConnection('10.3.8.211')
    connection.request('GET', '/')
    resp_body_str = str(conn.getresponse().read(), encoding='gb2312')
    do_sth_to(resp_body_str)