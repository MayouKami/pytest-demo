
from utils.db_utils import DBManager
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager


service = Service(EdgeChromiumDriverManager(version="120.0.0").install())
driver = webdriver.Edge(service=service)