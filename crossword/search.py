import re
# from selenium import webdriver
# import chromedriver_binary
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import MeCab
import pandas as pd
import requests

# [○○○ケ○],「あいうえお」ときたら？
def search_answers(regex,keyword,is_wait=False):
  # 検索URL
  url = 'https://search.yahoo.co.jp/search?p=' + keyword
  # 目的の文字数
  target_length = len(regex)

  ## Requests
  response = requests.get(url)
  soup = BeautifulSoup(response.content,'html.parser')

  # 開かないURL
  ng_links = ['yahoo','google','facebook','youtube','en.wik']
  # 取得できたURL一覧
  links = [i.get('href') for i in soup.find_all('a')]

  df = pd.DataFrame({'word' :[], 'count' : [],})
  startTime = time.time()
  for url in links:
    start = time.time()
    print(url)

    is_ng_link = True in [ng in url for ng in ng_links]
    if not url or is_ng_link or not url[:4] == 'http' or url[-4:] == '.pdf':
      continue
    
    try:
        response = requests.get(url)
    except  requests.exceptions.RequestException as err:
        # 同じURLに短時間でアクセスした時のエラー
        print(f"{type(err)}: {err}")
        continue

    # ここからテキスト抽出
    soup = BeautifulSoup(response.content,'html.parser')
    text = soup.text
    # 全角→半角
    text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

    # 日本語のみに限定
    text = re.sub('[a-z|A-Z|0-9| -/:-@\[-~]*','',text)

    # タガー
    tagger = MeCab.Tagger()

    node = tagger.parseToNode(text)

    node_count = 0
    while node:
      if node_count > 2000:
        break
      node_count += 1
      word_type = node.feature.split(',')[0]
      word_surf = node.surface

      katakana = node.feature.split(',')[-2]
      # 重複した場合はカウントを増やす
      if len(df[df['word'].isin([katakana])]) > 0:
        print(df[df['word'].isin([katakana])]['word'] + "が重複")
        df.loc[df['word'].isin([katakana]),['count']] += 1
        node = node.next
        continue

      # 名詞のみ抽出,何も無し、文字数確認
      if word_type != '名詞' or katakana == '*' or len(katakana) != target_length:
        node = node.next
        continue

      if re.fullmatch(r'' + regex, katakana):
        print(katakana + "を発見")
        tmp_df = pd.DataFrame({'word':[katakana],'count':[1],})
        df = pd.concat([df,tmp_df])

      node = node.next
    
    print(f'{str(time.time() - start)[:3]}秒. {node_count}個')
    if not is_wait and time.time() - startTime > 60:
      break

  df.sort_values(by='count',ascending=False,inplace=True)
  df.reset_index(inplace=True)
  print(f'処理時間: {str(time.time() - startTime)[:5]}秒')

  return df

