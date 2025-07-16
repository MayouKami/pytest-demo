# -*- coding: gbk -*-
from utils.db_utils import DBManager
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

@pytest.fixture(scope="function", autouse=True)
def db_connection():
    """ȫ�����ݿ�����"""
    conn = DBManager.get_connection()
    yield conn
    conn.commit()
    conn.close()

@pytest.fixture(scope="module", autouse=True)
def web_driver():
    try:
        # ����Edge�����ѡ��
        options = webdriver.EdgeOptions()
        options.use_chromium = True  # ʹ��Chromium�ں˵�Edge

        # ��ʼ�����������
        service = Service(r'C:\python\tools\webDriver\edgedriver_win64\msedgedriver.exe')
        #service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        yield driver
        driver.quit()
        #service.stop()
    except Exception as e:
        print(f"������װʧ��: {e}")
        raise
