import bs4
import traceback
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_binary

# ドライバーのフルパス
# CHROMEDRIVER = "chromedriver.exeのパス"
# 改ページ（最大）
PAGE_MAX = 2
# 遷移間隔（秒）
INTERVAL_TIME = 3
 
 
# ドライバー準備
def get_driver():
    # ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
 
    # ブラウザーを起動
    driver = webdriver.Chrome(options=options)
 
    return driver
 
 
# 対象ページのソース取得
def get_source_from_page(driver, page):
    try:
        # ターゲット
        driver.get(page)
        # id="RaceTopRace"の要素が見つかるまで10秒は待つ
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'RaceTopRace')))
        page_source = driver.page_source
 
        return page_source
 
    except Exception as e:
 
        print("Exception\n" + traceback.format_exc())
 
        return None
 
 
# ソースからスクレイピングする
def get_data_from_source(src):
    # スクレイピングする
    soup = bs4.BeautifulSoup(src, features='lxml')
 
    try:
        info = []
        elem_base = soup.find(id="RaceTopRace")
 
        if elem_base:
            elems = elem_base.find_all("li", class_="RaceList_DataItem")
 
            for elem in elems:
                # 最初のaタグ
                a_tag = elem.find("a")
 
                if a_tag:
                    href = a_tag.attrs['href']
                    match = re.findall("\/race\/result.html\?race_id=(.*)&amp;rf=race_list", href)
 
                    if len(match) > 0:
                        item_id = match[0]
                        info.append(item_id)
 
        return info
 
    except Exception as e:
 
        print("Exception\n" + traceback.format_exc())
 
        return None
 
# kaisai_dateリストを取得する
def get_list_id():
 
    return ['20180106', '20180107', '20180108', '20180113', '20180114', '20180120', '20180121', '20180127', '20180128']
 
 
if __name__ == "__main__":
 
    # kaisai_dateリスト取得
    list_id = get_list_id()
 
    # ブラウザのdriver取得
    driver = get_driver()
 
    # ページカウンター制御
    page_counter = 0
 
    for kaisai_date in list_id:
 
        page_counter = page_counter + 1
 
        # 対象ページURL
        page = "https://race.netkeiba.com/top/race_list.html?kaisai_date=" + str(kaisai_date)
 
        # ページのソース取得
        source = get_source_from_page(driver, page)
 
        # ソースからデータ抽出
        data = get_data_from_source(source)
 
        # データ保存
        print(data)
 
        # 間隔を設ける(秒単位）
        time.sleep(INTERVAL_TIME)
 
        # 改ページ処理を抜ける
        if page_counter == PAGE_MAX:
            break
 
 
    # 閉じる
    driver.quit()