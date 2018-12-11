import http.client

def login():
    conn = http.client.HTTPSConnection("moodle.htwg-konstanz.de")
    params = "{'@password': 'ntsmobil', '@username': 'rnetin'}"
    conn.request("POST", "/moodle/login/index.php", params)
    r1 = conn.getresponse()

    print(r1.getheader('Set-Cookie'))
    cookie = r1.getheader('Set-Cookie').split(';')[0]
    print(cookie)


    print(r1.status, r1.reason)

if __name__ == '__main__':
    login()
