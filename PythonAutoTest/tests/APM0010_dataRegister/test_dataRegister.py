# -*- coding: gbk -*-
import pymssql
from configs import settings
import cursor

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utils.db_utils import DBManager
import pytest

import importlib
import os
import allure

@allure.epic("��`���`�����������Ҏ���h")
#@allure.feature("01_����ϵ")
class TestUserRegister:
    #�û������������#

    insert_test_data = importlib.import_module('utils.insert_test_data')

    # ��������
    excel_path = os.path.join(settings.BASE_DIR, 'data', 'user', 'login_normal.xlsx')
    sql = insert_test_data.generate_insert_statements(excel_path)

    @allure.feature("01_����ϵ")
    @allure.story("01_������ڻ���TextInputȫ���դǤ��뤳��")
    @pytest.mark.run(order=1)
    def test_init(self, web_driver):

        target_url = "http://localhost:3000/toLogin"  # �滻Ϊ���Ŀ����ַ
        web_driver.get(target_url)
        # WebDriverWait(web_driver, 10)

        # ��ʼ��ȫ��Ϊ��
        username = web_driver.find_element(By.ID, "username")
        assert username.get_attribute("value") == ""

        password = web_driver.find_element(By.ID, "password")
        assert password.get_attribute("value") == ""

        email = web_driver.find_element(By.ID, "email")
        assert email.get_attribute("value") == ""

        phone = web_driver.find_element(By.ID, "phone")
        assert phone.get_attribute("value") == ""

        department = web_driver.find_element(By.ID, "department")
        assert department.get_attribute("value") == ""

    @allure.feature("01_����ϵ")
    @allure.story("02_���h�ɹ��ᡢ���h�ɹ�������w�Ƥ��뤳��")
    @pytest.mark.run(order=2)
    def test_login_to_success(self, web_driver):

        try:
            # �����������
            # DBManager.execute_update(db_connection, self.sql)

            wait = WebDriverWait(web_driver, 10)
            wait.until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys('user1')
            wait.until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys('123')
            wait.until(EC.element_to_be_clickable((By.ID, 'email'))).send_keys('3@qq.com')
            wait.until(EC.element_to_be_clickable((By.ID, 'phone'))).send_keys('1234567890123')
            wait.until(EC.element_to_be_clickable((By.ID, 'department'))).send_keys('dept1')

            original_url = web_driver.current_url

            # �����������״̬������ʱ��ȡ����һ��ע�ͣ�
            # input("enter to close...")
            button = web_driver.find_element(By.ID, "commit")
            button.click()

            wait.until(lambda d: d.current_url != original_url)

            assert web_driver.current_url == "http://localhost:3000/success.html", "��Ҏ���h�ɹ�������w��ʧ��"

        finally:
            pass

    @allure.feature("01_����ϵ")
    @allure.story("03_���h�ɹ���å��`���_�J")
    @pytest.mark.run(order=3)
    def test_login_success_message(self, web_driver):
        success_message = WebDriverWait(web_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-message"))
        )
        assert success_message.text == '��������Ȥ����ɤ���ޤ�����1', "���h�ɹ���å��`���������ʤ�"

    @allure.feature("01_����ϵ")
    @allure.story("04_DB�ǩ`���_�J")
    @pytest.mark.run(order=4)
    def test_login_data(self, db_connection):
        try:
            results = DBManager.execute_query(db_connection, "SELECT * FROM Users where Username=?", "user1")
            row = results[0]
            assert row[1] == "user1", "��`���`�����������ʤ�"
            assert row[3] == "3@qq.com", "emial���������ʤ�"
            assert row[4] == "1234567890123", "phone���������ʤ�"
            assert row[5] == "dept1", "���T���������ʤ�"
        finally:
            pass

    
    @allure.feature("02_����ϵ")
    @allure.story("01_ͬһ��`���`���ǵ��h������ϡ����hʧ���ˤʤ뤳��")
    @pytest.mark.run(order=5)
    def test_login_again(self, db_connection, web_driver):
        try:
            target_url = "http://localhost:3000/toLogin"  # �滻Ϊ���Ŀ����ַ
            web_driver.get(target_url)

            wait = WebDriverWait(web_driver, 10)
            wait.until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys('user1')
            wait.until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys('123')
            wait.until(EC.element_to_be_clickable((By.ID, 'email'))).send_keys('3@qq.com')
            wait.until(EC.element_to_be_clickable((By.ID, 'phone'))).send_keys('1234567890123')
            wait.until(EC.element_to_be_clickable((By.ID, 'department'))).send_keys('dept1')

            button = web_driver.find_element(By.ID, "commit")
            button.click();

            WebDriverWait(web_driver, 50).until(
                lambda d: d.find_element(By.ID, "responseMessage").text.strip() != ""
            )
            assert web_driver.find_element(By.ID, "responseMessage").text == "ԓ����`���`�����Ǥ˴���", "��å��`���������ʤ�"
        finally:
            usernames = ["'user1'"]  # ע���ֶ��������
            sql = f"DELETE FROM users WHERE Username IN ({','.join(usernames)})"
            DBManager.execute_update(db_connection, sql)  # �޲���

