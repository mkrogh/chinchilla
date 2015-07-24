from chinchilla import chinchilla
import unittest
import os


class FileClient():
    def __init__(self, pages, base_path=""):
        self.pages = pages
        self.base_path = base_path
        self.content = ""
        self.url = ""
    def open(self, url, data=None):
        with open(self.__path(url)) as f:
            self.content = f.read()
        self.url = url
        return self
    def read(self):
        return self.content
    def geturl(self):
        return self.url
    def __path(self,url):
        return os.path.join(self.base_path, self.pages[url])


class BasicTest(unittest.TestCase):

    def setUp(self):
        client = FileClient({
            "http://localhost/": "index.html",
            "http://localhost/login": "login.html",
            "http://localhost/secret": "secret.html",
            "https://www.google.com/": "index.html",
            },
            "test/pages/")
        chinchilla._client(client)
        chinchilla.visit("http://localhost/")

    def test_visit_page(self):
        self.assertEqual(chinchilla.page_url(),"http://localhost/")
        self.assertTrue(chinchilla.has_content("Welcome"))
    def test_click_link(self):
        chinchilla.click_link("Login")
        self.assertEqual(chinchilla.page_url(), "http://localhost/login")
    def test_click_link_external(self):
        chinchilla.click_link("Google")
        self.assertEqual(chinchilla.page_url(), "https://www.google.com/")
    def test_form(self):
        chinchilla.visit("http://localhost/login")
        chinchilla.fill_in("username", "test")
        chinchilla.fill_in("password", "secret")
        chinchilla.submit()
        self.assertEqual(chinchilla.page_url(), "http://localhost/secret")
        self.assertIn("kummefryser", chinchilla.page_content())
