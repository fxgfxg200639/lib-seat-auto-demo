# -*- coding: utf-8 -*-
"""
06 - 签到链路流程（接口顺序示意）
==================================
学习点：
  1. 一个完整的业务动作（如"到场签到"）通常由多个接口按顺序协作
  2. 典型顺序：查状态 -> 取位置 -> 上报位置 -> 提交动作 -> 复核结果
  3. 失败处理：根据返回 msg 分类（已处理过 / 未到时间 / 系统异常）

⚠️ 本文件为流程讲解代码：接口地址均为占位符，不包含任何可运行的
   真实系统调用，仅用于理解"多接口协作"这一通用设计模式。
"""

import json


def mock_request(endpoint: str, payload: dict) -> dict:
    """
    模拟接口返回（学习用）。
    真实环境中应替换为 requests.post(endpoint, data=payload).json()。
    """
    print(f"    [请求] POST {endpoint}")
    print(f"    [参数] {json.dumps(payload, ensure_ascii=False)}")
    # 按接口名返回不同的模拟结果，方便演示分支逻辑
    if "info" in endpoint:
        return {"success": True, "data": {"seatReserve": {"id": "DEMO-12345",
                                                          "seatNum": "082",
                                                          "startTime": "16:30",
                                                          "endTime": "22:00",
                                                          "status": 0}}}
    if "address" in endpoint:
        return {"success": True, "data": {"addressArr": [{"location": "119.000000,34.000000"}]}}
    if "location" in endpoint:
        return {"success": True}
    if "sign" in endpoint:
        return {"success": False, "msg": "不在签到时间内无法签到"}
    return {"success": False, "msg": "未知"}


def checkin_flow_demo():
    """签到多接口协作的流程示意（只演示分支逻辑，不真实调用）"""
    print("开始签到流程（学习示意）:")

    # ① 查询当前预约状态
    info = mock_request("https://example.com/api/reserve/info", {"id": "1234", "seatNum": "082"})
    sr = (info.get("data") or {}).get("seatReserve") or {}
    if not sr:
        print("    无预约记录，结束")
        return
    print(f"    检测到预约: 座位 {sr['seatNum']} {sr['startTime']}~{sr['endTime']}")

    # ② 获取位置（用于证明人在现场）
    addr = mock_request("https://example.com/api/seat/address", {"deptId": "100000", "roomId": "1234"})
    loc = ((addr.get("data") or {}).get("addressArr") or [{}])[0].get("location", "")

    # ③ 上报位置
    mock_request("https://example.com/api/location/log", {"location": loc})

    # ④ 提交签到
    sign = mock_request("https://example.com/api/seat/sign", {"id": sr["id"]})

    # ⑤ 结果分类处理（学习重点：按返回 msg 分类）
    if sign.get("success"):
        print("    签到成功")
        return
    msg = str(sign.get("msg", ""))
    if any(k in msg for k in ("已签到", "已在使用", "重复签到")):
        print(f"    已在使用中，视为成功（{msg}）")
        return
    if "签到时间" in msg:
        print(f"    不在签到时间（{msg}）—— 可稍后重试")
        return
    print(f"    签到失败: {msg}")


if __name__ == "__main__":
    checkin_flow_demo()
