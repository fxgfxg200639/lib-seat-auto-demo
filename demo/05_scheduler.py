# -*- coding: utf-8 -*-
"""
05 - 定时调度（守护线程 + 到点执行）
=====================================
学习点：
  1. 后台守护线程每秒检查时间，到点触发任务
  2. "每天只触发一次"：用持久化标记（如写入配置/数据库）防止重复触发
  3. 标记持久化后，服务重启也不会重复执行

⚠️ 本文件演示通用调度模式，任务内容为教学占位。
"""

import time
import threading
from datetime import datetime


class DailyTriggerDemo:
    """到点触发一次任务的通用模式"""

    def __init__(self, trigger_time: str = "08:00"):
        """
        :param trigger_time: 每天触发的时刻，格式 HH:MM
        """
        self.trigger_time = trigger_time
        self._last_run_date = ""      # 内存标记
        self._stop = False

    # ---- 核心：每秒检查 ----
    def _tick(self):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        hh, mm = self.trigger_time.split(":")
        target = now.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)

        # 到点 && 今天还没跑过 -> 触发
        if now >= target and self._last_run_date != today:
            self._last_run_date = today          # 先标记（防重复）
            self._execute()                      # 再执行

    # ---- 守护线程 ----
    def run(self):
        while not self._stop:
            try:
                self._tick()
            except Exception as e:
                print(f"[调度异常] {e}")
            time.sleep(1)          # 每秒轮询；如需"准点执行"可改成按秒对齐

    def start(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        return t

    def stop(self):
        self._stop = True

    def _execute(self):
        print(f"[{datetime.now():%H:%M:%S}] 触发任务（今天已执行标记: {self._last_run_date}）")


if __name__ == "__main__":
    demo = DailyTriggerDemo(trigger_time="23:59")   # 示意：用临近时刻演示
    thread = demo.start()
    print("调度器已启动，演示 3 秒后停止（真实使用无需停止）")
    time.sleep(3)
    demo.stop()
    print("已停止")
