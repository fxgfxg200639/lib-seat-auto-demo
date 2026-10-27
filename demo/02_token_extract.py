# -*- coding: utf-8 -*-
"""
02 - 页面 Token 提取（正则表达式）
====================================
学习点：
  1. 很多网页会把"一次性令牌"写在页面 HTML 里，用于防重复提交
  2. 用正则从 HTML 中提取 hidden input 的 value
  3. 提取结果用于后续请求参数

⚠️ 本文件仅演示通用文本解析技术，页面内容为本地构造的教学样例。
"""

import re

# ---------- 构造一个教学用 HTML 片段 ----------
DEMO_HTML = """
<!DOCTYPE html>
<html>
<head><title>座位预约页(示意)</title></head>
<body>
<form id="reserveForm">
  <input type="hidden" id="submit_enc" value="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6" />
  <input type="text" name="startTime" value="08:30" />
  <input type="text" name="endTime" value="15:30" />
  <button type="submit">提交</button>
</form>
</body>
</html>
"""

# ---------- 通用提取模式 ----------


def extract_hidden_value(html: str, element_id: str) -> str:
    """
    提取形如：<input type="hidden" id="submit_enc" value="..."/>
    的模式。这是前后端交互常见的"令牌"传递方式。

    :param html: 页面源码
    :param element_id: hidden input 的 id
    :return: value 属性值；找不到返回空串
    """
    # 匹配 id="submit_enc" 开头的 input 标签，并捕获其中的 value="..."
    pattern = re.compile(
        r'id="' + re.escape(element_id) + r'"\s+value="(.*?)"'
    )
    match = pattern.search(html)
    return match.group(1) if match else ""


def extract_first_value(html: str) -> str:
    """
    提取页面上第一个 value="..."（作为"页面签名种子"的学习示例）。
    真实系统里，提交参数的 MD5 签名往往依赖页面里某个动态值。
    """
    m = re.search(r'value="(.*?)"', html)
    return m.group(1) if m else ""


if __name__ == "__main__":
    token = extract_hidden_value(DEMO_HTML, "submit_enc")
    print("提取到的 submit_enc value:", token)
    print("页面第一个 value:", extract_first_value(DEMO_HTML))
    print("不存在元素的返回:", repr(extract_hidden_value(DEMO_HTML, "not_exist")))
