# -*- coding: utf-8 -*-
"""
03 - 请求参数签名（MD5）
=========================
学习点：
  1. 部分系统要求请求参数按固定规则排序后拼成字符串，再做 MD5 签名
  2. 签名用于服务端校验参数没有被篡改（防伪造）
  3. 与前端 JavaScript 的签名逻辑保持一致才能通过校验

⚠️ 本文件演示通用签名技术，规则为教学示例，不代表任何真实系统。
"""

import hashlib


def sign_params(params: dict, seed: str) -> str:
    """
    通用参数签名思路：
      1) 参数按 key 字典序排序
      2) 每个参数拼成 [key=value]
      3) 末尾追加一个页面提供的"种子值"（seed）
      4) 整体做 MD5

    :param params: 请求参数字典
    :param seed: 页面动态值（签名种子）
    :return: 32 位小写 MD5
    """
    sorted_keys = sorted(params.keys())
    hash_parts = []
    for key in sorted_keys:
        hash_parts.append(f"[{key}={params[key]}]")
    hash_parts.append(f"[{seed}]")
    hash_string = "".join(hash_parts)
    return hashlib.md5(hash_string.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    demo_params = {
        "roomId": "1234",          # 占位：教室 ID
        "seatNum": "082",          # 占位：座位号
        "startTime": "08:30",      # 占位：开始时间
        "endTime": "15:30",        # 占位：结束时间
        "token": "a1b2c3d4e5f6",   # 占位：页面令牌
    }
    seed = "5f4dcc3b5aa765d61d8327deb882cf99"  # 占位：页面种子值

    sig = sign_params(demo_params, seed)
    print("参数字典:", demo_params)
    print("签名结果:", sig)
    print("说明: 相同参数+相同种子 -> 相同签名；任何参数被改 -> 签名变化")
