# -*- coding: utf-8 -*-
"""
01 - 会话与会话保持 (requests.Session)
======================================
学习点：
  1. requests.Session 会保存 Cookie，模拟"登录后保持登录态"
  2. 登录接口通常需要加密传输（示例演示对称加密的思路，key/iv 仅为示意）
  3. 登录成功后后续请求携带同一会话的 Cookie

⚠️ 本文件仅演示通用网络请求技术，接口地址为占位符，不可用于任何真实系统。
"""

import requests
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

# ---------- 演示 1：对称加密（模拟登录参数的加密传输） ----------
# 真实系统里，登录参数往往不是明文传输，而是用固定密钥做 AES 加密。
# 这里仅展示"加密-解密"的技术思路，密钥为占位示意值。
DEMO_KEY = b"0123456789abcdef"  # 占位 key（16字节）
DEMO_IV = b"0123456789abcdef"   # 占位 iv


def aes_encrypt_demo(plaintext: str) -> str:
    """AES-CBC 加密 + Base64 输出（学习示例）"""
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode("utf-8")) + padder.finalize()
    cipher = Cipher(algorithms.AES(DEMO_KEY), modes.CBC(DEMO_IV), backend=default_backend())
    enc = cipher.encryptor()
    return base64.b64encode(enc.update(padded) + enc.finalize()).decode("utf-8")


def aes_decrypt_demo(cipher_b64: str) -> str:
    """AES-CBC 解密（学习示例，与上面互为逆运算）"""
    raw = base64.b64decode(cipher_b64)
    cipher = Cipher(algorithms.AES(DEMO_KEY), modes.CBC(DEMO_IV), backend=default_backend())
    dec = cipher.decryptor()
    padded = dec.update(raw) + dec.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return (unpadder.update(padded) + unpadder.finalize()).decode("utf-8")


# ---------- 演示 2：会话保持 ----------
def session_login_demo():
    """登录流程的通用模式：GET 登录页 -> POST 凭据 -> 会话自动携带 Cookie"""
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (learning demo)"})

    # 1) 先访问登录页，获取必要的 Cookie / 页面状态
    #    （真实系统的登录页地址各不相同，这里用占位符）
    login_page = "https://example.com/login"
    try:
        s.get(login_page, timeout=5)
    except Exception:
        pass  # 占位地址必然失败，仅示意流程

    # 2) POST 登录凭据（真实系统通常参数加密、字段名各异）
    payload = {
        "uname": aes_encrypt_demo("demo_user"),   # 加密后的用户名
        "password": aes_encrypt_demo("demo_pass"),  # 加密后的密码
        "fid": -1,
    }
    # resp = s.post("https://example.com/fanyalogin", params=payload)
    # 登录成功后，s 内保存的 Cookie 会自动用于后续所有请求

    # 3) 校验登录结果（真实系统返回 JSON，字段如 status/success）
    # result = resp.json()
    # if result.get("status"):
    #     print("登录成功")
    print("[示意] 登录流程：GET 登录页 -> POST 加密凭据 -> Session 保持登录态")


if __name__ == "__main__":
    print("加密示例：", aes_encrypt_demo("hello")[:24] + "...")
    print("解密还原：", aes_decrypt_demo(aes_encrypt_demo("hello")))
    session_login_demo()
