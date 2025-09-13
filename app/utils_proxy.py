# === FILE: app/utils_proxy.py ===
import requests
from loguru import logger




def test_proxy_http(proxy_host: str, proxy_port: int, username=None, password=None, timeout=10):
"""Test an HTTP/HTTPS proxy by making a simple GET to example.com via proxy."""
proxy = f"http://{proxy_host}:{proxy_port}"
if username and password:
proxy = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
proxies = {"http": proxy, "https": proxy}
try:
r = requests.get('https://www.example.com', proxies=proxies, timeout=timeout)
return r.status_code == 200
except Exception as e:
logger.debug(f'HTTP proxy test failed: {e}')
return False




def test_proxy_socks5(proxy_host: str, proxy_port: int, username=None, password=None, timeout=10):
"""Test a SOCKS5 proxy. Requires requests[socks] (pysocks) installed."""
try:
proxy = f"socks5://{proxy_host}:{proxy_port}"
if username and password:
proxy = f"socks5://{username}:{password}@{proxy_host}:{proxy_port}"
proxies = {"http": proxy, "https": proxy}
r = requests.get('https://www.example.com', proxies=proxies, timeout=timeout)
return r.status_code == 200
except Exception as e:
logger.debug(f'SOCKS5 proxy test failed: {e}')
return False

