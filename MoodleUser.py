import http.client, zlib,gzip
import urllib.parse
conn = http.client.HTTPSConnection("moodle.htwg-konstanz.de")

def login():
    #get first cookie
    conn.request('GET','/moodle/')
    r1 = conn.getresponse()
    tempcookie = r1.getheader('Set-Cookie').split(';')[0]
    r1.read()

    #post password and username
    params = urllib.parse.urlencode({'username': 'rnetin', 'password': 'ntsmobil'})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Content-Length': 33,
              'Connection': 'keep-alive',
              'Cookie':tempcookie}
    conn.request("POST", "/moodle/login/index.php",body= params, headers=header)
    r2 = conn.getresponse()
    print(r2.status, r2.reason)
    global cookie
    cookie = r2.getheader('Set-Cookie').split(';')[0]
    #aprove the test
    r2.read()
    params = urllib.parse.urlencode({'testsession': 16509})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/login/index.php?testsession=16509', body=params, headers=header)
    r3 = conn.getresponse()
    r3.read();
    
    print(r3.status, r3.reason)
    params = urllib.parse.urlencode({'id':2279})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/course/view.php?id=2279', body=params, headers=header)
    r4 = conn.getresponse()
    r4.read()
    print(r4.status, r4.reason)

def download():

    
    params = urllib.parse.urlencode({'id':118815})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/mod/assign/view.php?id=118815', body=params, headers=header)
    r5 = conn.getresponse()
    r5.read()
    print(r5.status, r5.reason)
    
    #download file
    params = urllib.parse.urlencode({'forcedownload':1})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf?forcedownload=1', body=params, headers=header)
    r6 = conn.getresponse()
    newfile = open('C:\\Users\\Thimo\\Desktop\\Rechnernetze.pdf','wb')
    newfile.write(r6.read())
    print(newfile)
    print(r6.status, r6.reason)
def read():
    print('read')
def writt():
    print('writ')
def chat():
    params = urllib.parse.urlencode({'id':128994})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/course/view.php?id=2279',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/mod/chat/view.php?id=128994', body=params, headers=header)
    r5 = conn.getresponse()
    r5.read()
    print(r5.status, r5.reason)
    params = urllib.parse.urlencode({'id':183})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/mod/chat/gui_basic/index.php?id=183', body=params, headers=header)
    r5 = conn.getresponse()
    print(r5.read())
    print(r5.status, r5.reason)
    
    
if __name__ == '__main__':
    login()
    #download()
    chat()
