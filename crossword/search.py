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
import chardet


# [○○○ケ○],「あいうえお」ときたら？
def search_answers(regex,keyword,is_wait=False):
  startTime = time.time()
  df = pd.DataFrame({'word' :[],'word_kanji':[], 'count' : [],})

  # 検索URL
  # url = 'https://www.google.co.jp/search'
  url = 'https://search.yahoo.co.jp/search'
  
  ## Requests
  try:
    response = requests.get(url,timeout=(3.0, 7.5),params={'p':keyword})
  except:
    print("検索に失敗しました")
    return df

  soup = BeautifulSoup(response.content,'lxml')

  # 開かないURL
  ng_links = ['yahoo','google','facebook','youtube','rakuten','amazon','en.wik','.pdf']
  # 取得できたURL一覧
  links = [i.get('href') for i in soup.find_all('a')]
  # リンクの存在確認
  if links is None or len(links) <= 0:
    print("リンクが見つかりませんでした")
  
  for url in links:
    # 検索を開始してから６０秒以上で強制終了
    if not is_wait and time.time() - startTime > 60:
      break

    is_ng_link = True in [ng_link in url for ng_link in ng_links]
    if url is None or is_ng_link or url[:4] != 'http':
      continue

    print(url)
    start = time.time()
    
    try:
        response = requests.get(url,timeout=(3.0, 7.5))
    except:
        continue
    # 文字コード判定、UTF８以外は終了
    print(chardet.detect(response.content))
    if chardet.detect(response.content)['encoding'] != 'utf-8':
      continue

    # ここからテキスト抽出
    soup = BeautifulSoup(response.content,'lxml')
    # 日本語のみに限定
    text = re.sub('[^一-龠ぁ-んァ-ヶー]','',soup.text)
    # タガー
    tagger = MeCab.Tagger()
    # ノードごとに分割
    node = tagger.parseToNode(text)
    # ノード数
    node_count = 0
    # 発見した単語数
    det_count = 0

    # ノード(単語)ごとに判定
    while node:
      node_count += 1
      # 2000ノード過ぎたら終了
      if node_count > 2000:
        break
      
      # そのままの表現
      word_surf = node.surface
      # カタカナ
      katakana = node.feature.split(',')[-2]
      # 名詞以外はスキップ
      if word_surf == '' or not '名詞' in node.feature:
        node = node.next
        continue
      # カタカナの表現がなければ終了
      if katakana == '*':
        if re.fullmatch('^[ァ-ヶー]+$', word_surf):
          katakana = word_surf
        else:
          node = node.next
          continue

      # 重複した場合はカウントを増やす
      if len(df[df['word'].isin([katakana])]) > 0 :
        df.loc[df['word'].isin([katakana]),['count']] += 1
        node = node.next
        continue

      # 正規表現に一致するか判定
      if re.fullmatch(r'' + regex, katakana):
        tmp_df = pd.DataFrame({'word':[katakana],'word_kanji':[word_surf],'count':[1],})
        df = pd.concat([df,tmp_df])
        det_count += 1

      node = node.next
      
    
    print(f'{str(time.time() - start)[:3]}秒 {node_count}ノード {det_count}単語発見')
    
  # ヒット数と単語でソート
  df.sort_values(by=['count','word'],ascending=[False,True],inplace=True)
  # インデックスのふり直し
  df.reset_index(inplace=True)

  return df

