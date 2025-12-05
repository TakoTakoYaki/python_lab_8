import unittest
import threading
import time
import socket

import requests

from myapp import HTTPServer, MyRequestHandler


def run_test_server(port_holder):
    # выбираем свободный порт
    s = socket.socket()
    s.bind(("localhost", 0))
    addr, port = s.getsockname()
    s.close()

    httpd = HTTPServer(("localhost", port), MyRequestHandler)
    port_holder.append(port)
    httpd.serve_forever()


class TestController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port_holder = []
        cls.thread = threading.Thread(
            target=run_test_server, args=(cls.port_holder,), daemon=True
        )
        cls.thread.start()
        # ждём, пока сервер поднимется
        time.sleep(0.5)
        cls.base_url = f"http://localhost:{cls.port_holder[0]}"

    def test_index_route(self):
        resp = requests.get(self.base_url + "/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("CurrenciesListApp", resp.text)

    def test_users_route(self):
        resp = requests.get(self.base_url + "/users")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Пользователи", resp.text)

    def test_currencies_route(self):
        resp = requests.get(self.base_url + "/currencies")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Курсы валют", resp.text)

    def test_user_route_with_query_param(self):
        # предполагаем, что у нас есть пользователь с id=1
        resp = requests.get(self.base_url + "/user?id=1")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Пользователь:", resp.text)

    def test_user_route_missing_id(self):
        resp = requests.get(self.base_url + "/user")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Missing id", resp.text)


if __name__ == "__main__":
    unittest.main()
