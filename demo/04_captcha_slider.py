# -*- coding: utf-8 -*-
"""
04 - 滑块验证码缺口识别（OpenCV 模板匹配）
============================================
学习点：
  1. 滑块验证码 = 一张带缺口的大图 + 一张滑块小图
  2. 用 cv2.matchTemplate 做模板匹配，找到缺口位置 x
  3. 该 x 就是滑块需要滑动的距离（可结合微调偏移重试提高通过率）

⚠️ 本文件只演示图像处理算法；真实验证码接口地址为占位，不构成完整破解脚本。
"""

import numpy as np
import cv2


def find_gap_x(background_img: np.ndarray, slider_img: np.ndarray) -> int:
    """
    通过边缘检测 + 模板匹配定位缺口横坐标。

    :param background_img: 背景大图（含缺口）
    :param slider_img: 滑块小图（含透明通道，png）
    :return: 缺口左上角 x 坐标（即滑动距离）
    """
    # 1) 如果滑块图带透明通道（RGBA），先按 alpha 通道裁剪出实心滑块
    if slider_img.shape[2] == 4:
        mask = slider_img[:, :, 3]
        mask[mask != 0] = 255
        x, y, w, h = cv2.boundingRect(mask)
        slider_img = slider_img[y:y + h, x:x + w, :3]

    # 2) 边缘检测：把彩色图转成边缘图，模板匹配对边缘更稳定
    bg_edge = cv2.Canny(background_img, 100, 200)
    tp_edge = cv2.Canny(slider_img, 100, 200)
    bg_rgb = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_rgb = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 3) 模板匹配，取相关系数最高的位置
    res = cv2.matchTemplate(bg_rgb, tp_rgb, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    return max_loc[0]


def make_demo_images() -> tuple:
    """构造一张教学用示例图（模拟真实滑块验证码）：
       - 背景：随机噪点纹理（真实验证码背景通常纹理杂乱）
       - 滑块：从背景缺口位置"原样抠出"的一块（真实滑块图就是从背景上抠下来的）
       - 背景缺口处涂成纯色凹槽
    这样"滑块纹理"只与缺口位置吻合，模板匹配才能正确定位。"""
    rng = np.random.default_rng(7)
    # 随机噪点背景 + 轻微模糊，模拟真实图片纹理
    bg = rng.integers(150, 255, (150, 300, 3), dtype=np.uint8)
    bg = cv2.GaussianBlur(bg, (3, 3), 0)
    # 缺口位置：x=180..209, y=50..79，从背景原样抠出作为滑块
    gap_x, gap_y = 180, 50
    slider_patch = bg[gap_y:gap_y + 30, gap_x:gap_x + 30].copy()
    # 背景缺口处涂纯色凹槽
    cv2.rectangle(bg, (gap_x, gap_y), (gap_x + 29, gap_y + 29), (100, 100, 100), -1)
    # 滑块带透明通道（模拟真实 png 滑块）
    slider_rgba = cv2.cvtColor(slider_patch, cv2.COLOR_BGR2BGRA)
    slider_rgba[:, :, 3] = 255
    return bg, slider_rgba


if __name__ == "__main__":
    bg, slider = make_demo_images()
    gap_x = find_gap_x(bg, slider)
    print(f"实际缺口位置: 180，算法检测到: {gap_x}")
    print("结论: 模板匹配可以定位滑块缺口横坐标（教学示意）")
