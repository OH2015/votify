import re
from selenium import webdriver
import chromedriver_binary
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import MeCab
import pandas as pd

# s = Service('../lib/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
# 10秒まで待つ
driver.set_page_load_timeout(10)

# [○,○,○,ケ、○],「あいうえお」ときたら？
def search_answers(regex,keyword,is_wait=False):
  # 検索URL
  url = 'https://www.google.co.jp/search?q=' + keyword
  # 目的の文字数
  target_length = len(regex)

  # URLにアクセス
  driver.get(url)

  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html, "html.parser")
  links = [i.get('href') for i in soup.find_all('a')]

  word_list = pd.DataFrame({'word' :[], 'count' : [],})
  startTime = time.time()
  for url in links:
    start = time.time()

    if not url or 'google' in url or 'facebook' in url or 'youtube' in url or 'en.wik' in url or not url[:4] == 'http' or url[-4:] == '.pdf':
      continue
    
    print(url)
    try:
      driver.get(url)
    except:
      print("読み込みに時間がかかっているのでスキップします")

    # ここからテキスト抽出
    text = driver.find_element_by_tag_name("html").text
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
      if len(word_list[word_list['word'].isin([katakana])]) > 0:
        print(word_list[word_list['word'].isin([katakana])]['word'] + "が重複")
        word_list.loc[word_list['word'].isin([katakana]),['count']] += 1
        node = node.next
        continue

      # 名詞のみ抽出,何も無し、文字数確認
      if word_type != '名詞' or katakana == '*' or len(katakana) != target_length:
        node = node.next
        continue

      if re.fullmatch(r'' + regex, katakana):
        print(katakana + "を発見")
        tmp_df = pd.DataFrame({'word':[katakana],'count':[1],})
        word_list = pd.concat([word_list,tmp_df])

      node = node.next
    
    print(f'{time.time() - start}秒. {node_count}個')
    if not is_wait and time.time() - startTime > 60:
      break

  word_list.sort_values(by='count',ascending=False,inplace=True)
  word_list.reset_index(inplace=True)
  print(f'処理時間: {time.time() - startTime}   秒')

  return word_list

