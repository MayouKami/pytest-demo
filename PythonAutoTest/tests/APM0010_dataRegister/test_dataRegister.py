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

@allure.epic("ユーザーアカウント新規登録")
#@allure.feature("01_正常系")
class TestUserRegister:
    #用户管理测试用例#

    insert_test_data = importlib.import_module('utils.insert_test_data')

    # 测试数据
    excel_path = os.path.join(settings.BASE_DIR, 'data', 'user', 'login_normal.xlsx')
    sql = insert_test_data.generate_insert_statements(excel_path)

    @allure.feature("01_正常系")
    @allure.story("01_画面初期化、TextInput全部空であること")
    @pytest.mark.run(order=1)
    def test_init(self, web_driver):

        target_url = "http://localhost:3000/toLogin"  # 替换为你的目标网址
        web_driver.get(target_url)
        # WebDriverWait(web_driver, 10)

        # 初始化全部为空
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

    @allure.feature("01_正常系")
    @allure.story("02_登録成功後、登録成功画面に遷移すること")
    @pytest.mark.run(order=2)
    def test_login_to_success(self, web_driver):

        try:
            # 插入测试数据
            # DBManager.execute_update(db_connection, self.sql)

            wait = WebDriverWait(web_driver, 10)
            wait.until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys('user1')
            wait.until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys('123')
            wait.until(EC.element_to_be_clickable((By.ID, 'email'))).send_keys('3@qq.com')
            wait.until(EC.element_to_be_clickable((By.ID, 'phone'))).send_keys('1234567890123')
            wait.until(EC.element_to_be_clickable((By.ID, 'department'))).send_keys('dept1')

            original_url = web_driver.current_url

            # 保持浏览器打开状态（测试时可取消下一行注释）
            # input("enter to close...")
            button = web_driver.find_element(By.ID, "commit")
            button.click()

            wait.until(lambda d: d.current_url != original_url)

            assert web_driver.current_url == "http://localhost:3000/success.html", "新規登録成功画面に遷移失敗"

        finally:
            pass

    @allure.feature("01_正常系")
    @allure.story("03_登録成功メッセージ確認")
    @pytest.mark.run(order=3)
    def test_login_success_message(self, web_driver):
        success_message = WebDriverWait(web_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-message"))
        )
        assert success_message.text == 'アカウントが作成されました！1', "登録成功メッセージ正しくない"

    @allure.feature("01_正常系")
    @allure.story("04_DBデータ確認")
    @pytest.mark.run(order=4)
    def test_login_data(self, db_connection):
        try:
            results = DBManager.execute_query(db_connection, "SELECT * FROM Users where Username=?", "user1")
            row = results[0]
            assert row[1] == "user1", "ユーザー名が正しくない"
            assert row[3] == "3@qq.com", "emialが正しくない"
            assert row[4] == "1234567890123", "phoneが正しくない"
            assert row[5] == "dept1", "部門が正しくない"
        finally:
            pass

    
    @allure.feature("02_異常系")
    @allure.story("01_同一ユーザー名で登録する場合、登録失敗になること")
    @pytest.mark.run(order=5)
    def test_login_again(self, db_connection, web_driver):
        try:
            target_url = "http://localhost:3000/toLogin"  # 替换为你的目标网址
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
            assert web_driver.find_element(By.ID, "responseMessage").text == "該当ユーザー名すでに存在", "メッセージ正しくない"
        finally:
            usernames = ["'user1'"]  # 注意手动添加引号
            sql = f"DELETE FROM users WHERE Username IN ({','.join(usernames)})"
            DBManager.execute_update(db_connection, sql)  # 无参数

