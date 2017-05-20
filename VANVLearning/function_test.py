# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class NewMaterialContentTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def testCreateNewMaterial(self):
        self.browser.get('http://127.0.0.1:8000/MaterialADocument/material/create/')
        self.assertEqual(u'製作獨立素材 | 數理學習平台', self.browser.title)

        # 1. 選擇科目: Math2  //*[@id="createMaterial"]
        lable = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[1]/label');
        self.assertEquals(u'科目', lable.text)
        selectSubject = self.browser.find_element_by_xpath('//*[@id="selectSubject"]')
        subjectOptions = selectSubject.find_elements_by_tag_name("option")
        self.assertEquals(u'Math', subjectOptions[0].text)
        self.assertEquals(u'Math2', subjectOptions[1].text)
        self.assertEquals(u'Math3', subjectOptions[2].text)
        subjectOptions[1].click()

        # 2. 選擇主題: 代數
        lable = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[2]/label');
        self.assertEquals(u'主題', lable.text)
        selectTopic = self.browser.find_element_by_xpath('//*[@id="selectTopic"]')
        topicOptions = selectTopic.find_elements_by_tag_name("option")
        self.assertEquals(u'代數', topicOptions[0].text)
        self.assertEquals(u'三角函數', topicOptions[1].text)
        self.assertEquals(u'四則運算', topicOptions[2].text)
        subjectOptions[0].click()

        # 3. 選擇權限: 公開
        lable = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[3]/label');
        self.assertEquals(u'權限設定', lable.text)
        radioPrivicy = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[3]/div/label[1]').text
        self.assertEquals(u'私人', radioPrivicy)
        radioPrivicy = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[3]/div/label[2]').text
        self.assertEquals(u'特殊', radioPrivicy)
        radioPrivicy = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[3]/div/label[3]').text
        self.assertEquals(u'公開', radioPrivicy)
        radio = self.browser.find_element_by_id('radioPrivicy3')
        radio.click()

        # 4. 編輯標題  // *[ @ id = "titleForm"]


        # 4. 種類: 是非
        lable = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[4]/label');
        self.assertEquals(u'種類', lable.text)
        radioType = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[4]/div/label[1]').text
        self.assertEquals(u'Text', radioType)
        radioType = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[4]/div/label[2]').text
        self.assertEquals(u'是非', radioType)
        radioType = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[4]/div/label[3]').text
        self.assertEquals(u'選擇', radioType)
        radioType = self.browser.find_element_by_xpath('//*[@id="createMaterial"]/div[4]/div/label[4]').text
        self.assertEquals(u'問答', radioType)
        radioTypeInput = self.browser.find_element_by_id('radioType2')
        radioTypeInput.click()

        # 根據所選種類產生新的欄位
        # self.browser.implicitly_wait(3)
        # element = WebDriverWait(self.browser, 10).until(
        #     EC.presence_of_element_located((By.ID, "radioTF1"))
        # )
        self.assertEquals('form-group', self.browser.find_element_by_xpath('//*[@id="trueFalseForm"]').get_attribute('class'))
        self.assertEquals(u'是否為答案', self.browser.find_element_by_xpath('//*[@id="trueFalseForm"]/label').text)
        radioTrueFalse = self.browser.find_element_by_xpath('//*[@id="trueFalseForm"]/div/label[1]').text
        self.assertEquals(u'是', radioTrueFalse)
        radioTrueFalse = self.browser.find_element_by_xpath('//*[@id="trueFalseForm"]/div/label[2]').text
        self.assertEquals(u'否', radioTrueFalse)
        radioFalseInput = self.browser.find_element_by_id('radioTF2')
        radioFalseInput.click()

        # 最後送出


if __name__ == '__main__':
    unittest.main()
