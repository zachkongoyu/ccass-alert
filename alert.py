from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

df = pd.read_excel("C:/Users/rtamc-F/Desktop/CCASS Alert/全部港股.xlsx")

today = datetime.datetime.today()
day_of_week = today.weekday()

if day_of_week == 0:
    trace = (today - datetime.timedelta(days=3)).strftime("%Y/%m/%d")
    compare = (today - datetime.timedelta(days=4)).strftime("%Y/%m/%d")
elif day_of_week == 1:
    trace = (today - datetime.timedelta(days=1)).strftime("%Y/%m/%d")
    compare = (today - datetime.timedelta(days=3)).strftime("%Y/%m/%d")
else:
    trace = (today - datetime.timedelta(days=1)).strftime("%Y/%m/%d")
    compare = (today - datetime.timedelta(days=2)).strftime("%Y/%m/%d")

def get_ticker(s):
    return s.split('.')[0]

def get_data(ticker, date):

    ticker = ticker.zfill(5)

    headers = {
        'authority': 'www.hkexnews.hk',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'origin': 'https://www.hkexnews.hk',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'TSfff9c5ca027=086f2721efab2000a9657b64725b508c867217dd26cc0181be0e99eb35083ea11fd01b72333d5a3f08a4c75f1c113000048c94b49701d56cc3261667cf335595876f6d84abe32701b6f25dd4aa8a146c01748e6dcd54a3ed54d01f0c6d191042; sclang=en; TS6b4c3a62027=08754bc291ab200002a61ee46d02d19be959ef1a5454612afd8979b06c19063227d8aa39282f0a7f0885dbf241113000da48d77fff775a8d64eb398380c371f04e785a0452ad16b24d233db2f8fa9f336a9a06ac06cda2ff8e188b470387092f; WT_FPC=id=23.44.4.173-3930005568.30898667:lv=1626403730039:ss=1626403221035',
    }

    data = {
      '__EVENTTARGET': 'btnSearch',
      '__EVENTARGUMENT': '',
      '__VIEWSTATE': '/wEPDwULLTIwNTMyMzMwMThkZLiCLeQCG/lBVJcNezUV/J0rsyMr',
      '__VIEWSTATEGENERATOR': 'A7B2BBE2',
      'today': '20210716',
      'sortBy': 'shareholding',
      'sortDirection': 'desc',
      'alertMsg': '',
      'txtShareholdingDate': date,
      'txtStockCode': ticker,
      'txtStockName': '',
      'txtParticipantID': '',
      'txtParticipantName': '',
      'txtSelPartID': ''
    }

    response = requests.post('https://www.hkexnews.hk/sdw/search/searchsdw.aspx', headers=headers, data=data)
    soup = BeautifulSoup(response.content, 'html.parser')

    return float(soup.find_all('div', class_='value')[-1].text.replace('%', ''))

tickers = df['代码'].apply(get_ticker)

if day_of_week >= 0 and day_of_week <= 4:
    for ticker in tickers:
        try:
            trace_data = 100 - get_data(ticker, trace)
            compare_data = 100 - get_data(ticker, compare)

            diff = round(trace_data - compare_data, 1)

            print(compare, trace, ticker, diff)

            if abs(diff) >= 0.5:
                with open("C:/Users/rtamc-F/Desktop/CCASS Alert/tickers.txt", 'a') as f:
                    f.write(compare)
                    f.write('-')
                    f.write(trace)
                    f.write(' ')
                    f.write(ticker)
                    f.write(' ')
                    f.write(f'{diff}%')
                    f.write('\n')
        except:
            print(ticker, "Error occured: ", compare, trace)

with open("C:/Users/rtamc-F/Desktop/CCASS Alert/tickers.txt", 'a') as f:
                    f.write("--"*50)
                    f.write('\n')