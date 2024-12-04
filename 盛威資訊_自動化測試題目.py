"""使用python 3.13.0"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# 設定logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CathayBankScraper:
    def __init__(self):
        # 創建一個新的 Chrome 選項實例
        self.options = Options()
        # 設定手機模擬
        self.options.add_experimental_option("mobileEmulation", {
            "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 3.0},
        })
        # 創建一個新的 Chrome 驅動器實例
        self.driver = webdriver.Chrome(options=self.options)

    def navigate_to_homepage(self):
        try:
            # 前往網站首頁
            self.driver.get("https://www.cathaybk.com.tw/cathaybk/")
            # 等待網頁加載完成
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception as e:
            logging.error(f"Failed to navigate to website homepage: {e}")

    def save_homepage_screenshot(self):
        try:
            # 儲存首頁截圖
            self.driver.save_screenshot("Home page.png")
        except Exception as e:
            logging.error(f"Failed to save homepage screenshot: {e}")

    def navigate_to_credit_card_list(self):
        try:
            # 點擊左上角的"三"
            self.driver.find_element(By.CLASS_NAME, "cubre-o-header__burger").click()
            # 等待菜單加載完成
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cubre-o-menu__btn")))
            # 點擊產品介紹
            self.driver.find_element(By.CSS_SELECTOR, 'div.cubre-o-nav__menu > div > div:nth-child(1)').click()
            # 點擊信用卡
            self.driver.find_element(By.CLASS_NAME, "cubre-o-menuLinkList__btn").click()
            # 等待信用卡列表加載完成
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.cubre-o-menuLinkList__item.is-L2open > div.cubre-o-menuLinkList__content > a")))
        except Exception as e:
            logging.error(f"Failed to navigate to credit card list: {e}")

    def get_credit_card_list(self):
        try:
            # 取得信用卡列表
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.cubre-o-menuLinkList__item.is-L2open > div.cubre-o-menuLinkList__content > a")
            return elements
        except Exception as e:
            logging.error(f"Failed to get credit card list: {e}")
            return []

    def save_credit_card_list_screenshot(self):
        try:
            # 儲存信用卡列表截圖
            self.driver.save_screenshot("Credit card list.png")
        except Exception as e:
            logging.error(f"Failed to save credit card list screenshot: {e}")

    def navigate_to_card_introduction(self):
        # 點擊卡片介紹
        try:
            elements = self.get_credit_card_list()
            for element in elements:
                if element.text == "卡片介紹":
                    element.click()
                    break
        except Exception as e:
            logging.error(f"Failed to navigate to card introduction: {e}")

    def get_stopped_credit_cards(self):
        # 取得停發卡列表
        try:
            slide_bar = self.driver.find_element(By.XPATH, "//div[contains(text(), '停發卡')]/../../../../..").find_elements(By.CSS_SELECTOR, "span.swiper-pagination-bullet")
            ActionChains(self.driver).move_to_element(slide_bar[-1]).perform() # 把視窗移到指定位置

            stopped_credit_cards = []
            for i, point in enumerate(slide_bar):
                point.click()
                time.sleep(5)
                self.driver.save_screenshot(f"停用信用卡截圖/Credit card {i+1}.png")
                print(f"儲存第{i+1}張信用卡截圖")
                stopped_credit_cards.append(self.driver.find_elements(By.CSS_SELECTOR, "div.swiper-wrapper > div"))
            return stopped_credit_cards
        except Exception as e:
            logging.error(f"Failed to get stopped credit cards: {e}")
            return []

    def get_stopped_credit_card_count(self):
        try:
            # 取得停發卡數量
            stopped_credit_cards = self.get_stopped_credit_cards()
            return len(stopped_credit_cards)
        except Exception as e:
            logging.error(f"Failed to get stopped credit card count: {e}")
            return 0

if __name__ == "__main__":
    # 創建一個新的 CathayBankScraper 實例
    scraper = CathayBankScraper()
    # 前往網站首頁
    scraper.navigate_to_homepage()
    # 儲存首頁截圖
    scraper.save_homepage_screenshot()
    # 前往信用卡列表
    scraper.navigate_to_credit_card_list()
    # 儲存信用卡列表截圖
    scraper.save_credit_card_list_screenshot()
    # 前往卡片介紹
    scraper.navigate_to_card_introduction()
    # 取得停發卡數量
    stopped_credit_card_count = scraper.get_stopped_credit_card_count()
    print(f"停發信用卡數量:{stopped_credit_card_count}張")