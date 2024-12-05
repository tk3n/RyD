import requests
from bs4 import BeautifulSoup
import json
import re
import traceback
import os

def get_soup(url):
    """URLからBeautifulSoupオブジェクトを取得"""
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def clean_text(text):
    """テキストから特殊文字や絵文字を削除"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        "]+", flags=re.UNICODE)
    
    text = emoji_pattern.sub('', text)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    return text

def get_child_elements(element, max_elements=4):
    """要素から4個の空でない子要素を取得"""
    elements = []
    count = 0
    
    for child in element.find_all(recursive=False):
        if count >= max_elements:
            break
        if child.get_text().strip():
            elements.append(clean_text(str(child)))
            count += 1
            
    return elements

def convert_mark_to_p(soup):
   """markタグをpタグに変換し、style属性を除去"""
   for mark in soup.find_all('mark'):
       mark.name = 'p'
       if 'style' in mark.attrs:
           del mark.attrs['style']
   return soup

def remove_ogp_cards(entry_body):
    """ogpCard_rootクラスを持つdivを削除"""
    for div in entry_body.find_all('div', class_='ogpCard_root'):
        div.decompose()
    return entry_body

def process_images(entry_body):
    """
    画像の一連の処理を行う
    1. 絵文字以外の画像を削除
    2. 残った画像にinline-blockクラスを追加
    """
    # 絵文字以外の画像を削除
    entry_body = remove_non_emoji_images(entry_body)
    
    # 残った画像にinline-blockクラスを追加
    entry_body = add_inline_block_class(entry_body)
    
    return entry_body

def remove_non_emoji_images(entry_body):
    """emoji以外の画像を削除"""
    for img in entry_body.find_all('img'):
        if not img:
            continue
        
        if 'emoji' not in img.get('class', []):
            img.decompose()
    
    return entry_body

def add_inline_block_class(soup):
    """画像にinline-blockクラスを追加"""
    for img in soup.find_all('img'):
        if not img:
            continue
        
        # 現在のクラスリストを取得
        current_classes = img.get('class', [])
        if not isinstance(current_classes, list):
            current_classes = [current_classes] if current_classes else []
        
        # inline-blockクラスを追加
        if 'inline-block' not in current_classes:
            current_classes.append('inline-block')
            img['class'] = current_classes
            
    return soup

def get_article_data(entry_item_body):
    """記事のタイトル、URL、内容を取得"""
    # タイトルとURLを取得
    title_element = entry_item_body.find('h2', attrs={'data-uranus-component': 'entryItemTitle'})
    title_link = title_element.find('a')
    
    title = title_link.text.strip()
    url = f"https://ameblo.jp{title_link.get('href')}"
    
    # 記事本文を取得
    article_soup = get_soup(url)
    entry_body = article_soup.find('div', id='entryBody')

    # リンクのカードを除去
    entry_body = remove_ogp_cards(entry_body)

    # 画像処理
    entry_body = process_images(entry_body)

    # マーカーをpタグにする
    entry_body = convert_mark_to_p(entry_body)

    # 四行分取り出す
    content_elements = get_child_elements(entry_body)
    content = ''.join(content_elements)
    
    return {
        'title': title,
        'url': url,
        'content': content
    }

def main(file_path):
    # ブログ記事一覧を取得
    article_list_url = "https://ameblo.jp/luidasbar/entrylist.html"
    soup = get_soup(article_list_url)
    archive_list = soup.find(class_='skin-archiveList')
    
    # 最新3記事のデータを取得
    entry_items = archive_list.find_all('div', attrs={'data-uranus-component': 'entryItemBody'})[:3]
    articles_data = [get_article_data(item) for item in entry_items]
    
    # JSONに保存
    data = {"articles": articles_data}
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    file_path = os.environ['FILE_PATH']
    try:
        main(file_path)
    except:
        os.remove(file_path)
        traceback.print_exc()
