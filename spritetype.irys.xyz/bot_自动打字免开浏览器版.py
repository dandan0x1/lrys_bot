#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 依赖: requests, pyyaml, hashlib, json, time, random
# 安装: pip install requests pyyaml

import os, requests, hashlib, json, time, random, asyncio
from datetime import datetime
from colorama import *


def show_copyright():
    """展示版权信息"""
    copyright_info = f"""{Fore.CYAN}
    *****************************************************
    *           X:https://x.com/ariel_sands_dan         *
    *           Tg:https://t.me/sands0x1                *
    *           Copyright (c) 2025                      *
    *           All Rights Reserved                     *
    *****************************************************
    {Style.RESET_ALL}
    """
    print(copyright_info)
    print("=" * 50)
    print(f"{Fore.GREEN}申请key: https://661100.xyz/ {Style.RESET_ALL}")
    print(
        f"{Fore.RED}联系Dandan: \n QQ:712987787 QQ群:1036105927 \n 电报:sands0x1 电报群:https://t.me/+fjDjBiKrzOw2NmJl \n 微信: dandan0x1{Style.RESET_ALL}"
    )
    print("=" * 50)


# ========== 配置设置 ==========
# 直接设置配置，不使用config.yaml文件
config = {
    "run_count": 5,  # 每个账号运行次数
    "run_mode": 1,  # 运行模式：1=正常，2=快速
}


# ========== 账号与代理加载 ==========
def load_addresses():
    with open("config/address.txt", "r", encoding="utf-8") as f:
        addresses = [line.strip() for line in f.readlines() if line.strip()]
    return addresses


def load_proxies():
    proxies = []
    if os.path.exists("config/proxy.txt"):
        with open("config/proxy.txt", "r", encoding="utf-8") as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
    return proxies


addresses = load_addresses()
proxies = load_proxies()


# ========== 日志输出 ==========
def show_msg(msg, level=0):
    prefix_map = {1: "✔", 2: "⚠", 3: "❌"}
    prefix = prefix_map.get(level, "")
    out = f"{prefix + ' ' if prefix else ''}{msg}"
    print(out)

    with open("config/log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} - {msg}\n")


# ========== antiCheatHash 算法 ==========
def compute_anti_cheat_hash(e, t, a, r, s, i):
    l = s + i
    n = 0 + 23 * t + 89 * a + 41 * r + 67 * s + 13 * i + 97 * l
    o = 0
    for idx in range(len(e)):
        o += ord(e[idx]) * (idx + 1)  # 对应 e.charCodeAt(idx) * (idx + 1)
    n += 31 * o

    # 模拟JavaScript的浮点数精度问题
    # 将大数转换为浮点数进行计算，然后转回整数
    big_num_float = float(0x178BA57548D)
    n_float = float(n)
    mod_num_float = float(9007199254740991)

    # 使用浮点数运算模拟JavaScript行为
    c_float = (big_num_float * n_float) % mod_num_float
    c = int(c_float)

    result = f"{e.lower()}_{t}_{a}_{r}_{s}_{i}_{c}"
    return hashlib.sha256(result.encode()).hexdigest()[:32]  # 对应 .substring(0, 32)


# ========== Spritetype 提交 ==========
async def spritetype(account, proxy, run_count, run_mode):
    fail_time = 0
    next_execution_time = 0
    i = 0

    while i < run_count:
        if time.time() * 1000 < next_execution_time:
            time.sleep(1)
            continue

        # 生成参数 - 完全按照Node.js版本
        wpm = int(random.random() * 21) + 65  # 对应 Math.floor(Math.random() * 21) + 65
        time_val = 15
        total_chars = int(
            wpm * 5 * time_val / 60
        )  # 对应 Math.floor(wpm * 5 * time / 60)
        incorrect_chars = int(
            random.random() * max(1, total_chars // 15)
        )  # 对应 Math.floor(Math.random() * Math.max(1, totalChars / 15))
        correct_chars = total_chars - incorrect_chars
        accuracy = (
            100 if total_chars == 0 else round(100.0 * correct_chars / total_chars)
        )  # 对应 Math.round(100.0 * correctChars / totalChars)

        progress_data = []
        for j in range(time_val):
            base_val = correct_chars * (j + 1) / time_val
            jitter = (
                int(random.random() * 3) - 1
            )  # 对应 Math.floor(Math.random() * 3) - 1
            val = round(base_val) + jitter
            if j > 0 and val < progress_data[j - 1]:
                val = progress_data[j - 1]
            if val > correct_chars:
                val = correct_chars
            if val < 0:
                val = 0
            progress_data.append(val)

        anti_cheat_hash = compute_anti_cheat_hash(
            account, wpm, accuracy, time_val, correct_chars, incorrect_chars
        )

        payload = {
            "walletAddress": account,
            "gameStats": {
                "wpm": int(wpm),
                "accuracy": int(accuracy),
                "time": int(time_val),
                "correctChars": int(correct_chars),
                "incorrectChars": int(incorrect_chars),
                "progressData": [int(x) for x in progress_data],
            },
            "antiCheatHash": anti_cheat_hash,
            "timestamp": int(time.time() * 1000),
        }

        show_msg(
            f"address={account}, wpm={wpm}, accuracy={accuracy}, time={time_val}, correctChars={correct_chars}, incorrectChars={incorrect_chars}, antiCheatHash={anti_cheat_hash}"
        )

        try:
            headers = {
                "accept": "*/*",
                "content-type": "application/json",
                "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7,en;q=0.6",
                "origin": "https://spritetype.irys.xyz",
                "priority": "u=1, i",
                "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "referer": "https://spritetype.irys.xyz/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }

            # 代理支持
            proxies_dict = None
            if proxy:
                proxies_dict = {"http": proxy, "https": proxy}

            response = requests.post(
                "https://spritetype.irys.xyz/api/submit-result",
                json=payload,
                headers=headers,
                proxies=proxies_dict,
                timeout=30,
            )

            if response.status_code == 200:
                res_data = response.json()
                if res_data.get("success"):
                    show_msg(f"第{i + 1}次-成绩提交: {res_data.get('message', '')}", 1)
                    i += 1
                    fail_time = 0
                    if run_mode == 2:
                        time.sleep(1)
                    else:
                        show_msg("30秒后进行下一轮", 1)
                        # 实时倒计时显示
                        for countdown in range(30, 0, -1):
                            print(f"\r⏰ 倒计时: {countdown}秒", end="", flush=True)
                            time.sleep(1)
                        print()  # 换行
                    next_execution_time = 0
                else:
                    show_msg(f"第{i + 1}次-成绩提交: {json.dumps(res_data)}", 2)
            else:
                # 获取详细的错误信息
                try:
                    error_data = response.json()
                    show_msg(
                        f"HTTP错误: {response.status_code} - {json.dumps(error_data)}",
                        2,
                    )
                except:
                    show_msg(f"HTTP错误: {response.status_code} - {response.text}", 2)

        except requests.exceptions.RequestException as err:
            err_msg = str(err)
            if hasattr(err, "response") and err.response is not None:
                try:
                    err_msg = json.dumps(err.response.json())
                except:
                    err_msg = err.response.text

            show_msg(f"异常信息: {err_msg}", 2)

            # 如果是400错误，显示请求数据用于调试
            if (
                hasattr(err, "response")
                and err.response
                and err.response.status_code == 400
            ):
                show_msg(f"调试信息 - 发送的数据: {json.dumps(payload, indent=2)}", 2)

            if "Please wait" in err_msg:
                import re

                match = re.search(r"Please wait (\d+) seconds", err_msg)
                wait_seconds = 10
                if match:
                    wait_seconds = int(match.group(1))
                show_msg(f"接口已限制，等待{wait_seconds}秒后重试...", 2)
                # 实时倒计时显示
                for countdown in range(wait_seconds, 0, -1):
                    print(f"\r⏰ 等待倒计时: {countdown}秒", end="", flush=True)
                    time.sleep(1)
                print()  # 换行
                continue

            fail_time += 1
            if fail_time < 15:
                next_execution_time = time.time() * 1000 + 10000
            else:
                show_msg("失败次数过多，跳过该账号", 3)
                break


# ========== 代理分配 ==========
def get_proxy(idx):
    if idx < len(proxies):
        return proxies[idx]
    return None


# ========== 主循环 ==========
def main():
    show_copyright()

    async def run_all():
        tasks = []
        for idx, account in enumerate(addresses):
            proxy = get_proxy(idx)
            show_msg(f"当前执行账号: {idx + 1} - {account}")
            task = spritetype(account, proxy, config["run_count"], config["run_mode"])
            tasks.append(task)

        await asyncio.gather(*tasks)

    asyncio.run(run_all())


if __name__ == "__main__":
    main()
