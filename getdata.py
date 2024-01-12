import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()

#　VDNの設定
driver = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = webdriver.ChromeOptions()
)

options.add_argument('--headless')
wait = WebDriverWait(driver,10)

# 競馬サイトからデータ取得

URL = "https://db.netkeiba.com/?pid=race_search_detail"
driver.get(URL)
time.sleep(1)
wait.until(EC.presence_of_all_elements_located)

# 月ごとに検索
sartyear = 2023
startmonth = 12
endyear = 2023
endmonth = 12


# 期間を選択
start_year_element = driver.find_element(By.NAME,'start_year')
start_year_select = Select(start_year_element)
start_year_select.select_by_value(str(startyear))
start_mon_element = driver.find_element(By.NAME,'start_mon')
start_mon_select = Select(start_mon_element)
start_mon_select.select_by_value(str(startmonth))
end_year_element = driver.find_element(By.NAME,'end_year')
end_year_select = Select(end_year_element)
end_year_select.select_by_value(str(endyear))
end_mon_element = driver.find_element(By.NAME,'end_mon')
end_mon_select = Select(end_mon_element)
end_mon_select.select_by_value(str(endmonth))

# 中央競馬場から対象の競馬場をチェック
# 1:札幌、2:函館、3:福島、4:新潟、5:東京、6:中山、7:中京、8:京都、9:阪神、10:小倉
# 東京、中山をチェック
for i in range(5,7):
    terms = driver.find_element(By.ID,"check_Jyo_"+ str(i).zfill(2))
    terms.click()
        
# 表示件数を選択(20,50,100の中から最大の100へ)
list_element = driver.find_element(By.NAME,'list')
list_select = Select(list_element)
list_select.select_by_value("100")

# フォームを送信
frm = driver.find_element(By.CSS_SELECTOR,"#db_search_detail_form > form")
frm.submit()
time.sleep(5)
wait.until(EC.presence_of_all_elements_located)
time.sleep(10)

# ページ送りにてURL取得
# with構文によるファイルオープン
with open(str(startyear)+"-"+str(startmonth)+".txt", mode='w') as f:
    while True:
        time.sleep(5)
        wait.until(EC.presence_of_all_elements_located)
        all_rows = driver.find_element(By.CLASS_NAME,'race_table_01').find_elements_by_tag_name("tr")
        for row in range(1, len(all_rows)):
            race_href=all_rows[row].find_elements(By.TAG_NAME,"td")[4].find_element_by_tag_name("a").get_attribute("href")
            f.write(race_href+"\n")
        try:
            target = driver.find_elements(By.LINK_TEXT,"次")[0]
            driver.execute_script("arguments[0].click();", target) #javascriptでクリック処理
        except IndexError:
            break
#　!!!!!!ドライバー終了!!!!!!
driver.quit()



