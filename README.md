# Dependency

Python 3.x

# Run

    python3 buptInternetDataCLI.py

or

    python buptInternetDataCLI.py

# 原理

    import http.client
    connection = http.client.HTTPConnection('10.3.8.211')
    connection.request('GET', '/')
    resp_body_str = str(conn.getresponse().read(), encoding='gb2312')
    do_sth_to(resp_body_str)