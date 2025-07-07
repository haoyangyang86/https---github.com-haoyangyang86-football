import json
from flask import Flask, jsonify, render_template, send_from_directory
from playwright.sync_api import sync_playwright
import time
import os

# 初始化Flask应用
app = Flask(__name__,
            static_folder='frontend/css',  # 指定静态文件（CSS）的目录
            template_folder='frontend')   # 指定HTML模板文件的目录

# --- 之前 data_crawler.py 中的核心抓取逻辑，现在被封装成一个函数 ---

def fetch_and_process_data():
    """
    使用Playwright抓取、处理并返回比赛数据。
    这个函数整合了之前脚本的所有核心功能。
    """
    TARGET_PAGE_URL = "https://www.sporttery.cn/jc/jsq/"
    TARGET_API_KEYWORD = "/gateway/uniform/football/getMatchCalculatorV1.qry"
    
    captured_data = []

    def handle_response(response):
        if TARGET_API_KEYWORD in response.url:
            try:
                data = response.json()
                if data.get("value", {}).get("matchInfoList"):
                    print("--- [后端] 成功拦截到目标API数据 ---")
                    captured_data.append(data)
            except Exception as e:
                print(f"--- [后端] 解析API响应时出错: {e} ---")

    with sync_playwright() as p:
        print("--- [后端] 正在启动浏览器抓取最新数据... ---")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("response", handle_response)
        page.goto(TARGET_PAGE_URL, timeout=60000)
        
        start_time = time.time()
        while not captured_data and time.time() - start_time < 30:
            page.wait_for_timeout(500)
        
        browser.close()
        print("--- [后端] 浏览器已关闭 ---")

    if not captured_data:
        print("--- [后端] 未能捕获到任何数据 ---")
        return None

    # --- 数据解析逻辑 ---
    raw_data = captured_data[0]
    processed_matches = []
    if raw_data.get("value", {}).get("matchInfoList"):
        match_days = raw_data.get("value", {}).get("matchInfoList", [])
        for day in match_days:
            sub_match_list = day.get('subMatchList', [])
            for match in sub_match_list:
                match_info = {
                    "matchNum": match.get("matchNumStr", "N/A"),
                    "leagueName": match.get("leagueAllName", "未知联赛"),
                    "homeTeamName": match.get("homeTeamAbbName", "主队"),
                    "awayTeamName": match.get("awayTeamAbbName", "客队"),
                    "matchTime": f"{match.get('matchDate', '')} {match.get('matchTime', '')}",
                    "had": { "h": match.get("had", {}).get("h", "-"), "d": match.get("had", {}).get("d", "-"), "a": match.get("had", {}).get("a", "-")},
                    "hhad": {"goalLine": match.get("hhad", {}).get("goalLine", "0"), "h": match.get("hhad", {}).get("h", "-"), "d": match.get("hhad", {}).get("d", "-"),"a": match.get("hhad", {}).get("a", "-")}
                }
                processed_matches.append(match_info)
    
    return processed_matches

# --- Flask路由定义 ---

@app.route('/api/matches')
def get_matches():
    """
    这是我们的数据API接口。
    当前端访问 /api/matches 时，这个函数会被触发。
    """
    print("--- [服务器] 接到前端 /api/matches 请求 ---")
    data = fetch_and_process_data()
    if data:
        print(f"--- [服务器] 成功获取 {len(data)} 条比赛数据，返回给前端 ---")
        return jsonify(data) # 使用jsonify将Python列表转换为JSON响应
    else:
        print("--- [服务器] 获取数据失败，向前端返回错误信息 ---")
        return jsonify({"error": "未能获取比赛数据"}), 500

@app.route('/')
def index():
    """
    这是我们的主页路由。
    当用户访问网站根目录时，返回 index.html。
    """
    return render_template('index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    """这个路由用来服务JavaScript文件"""
    return send_from_directory('frontend/js', filename)

if __name__ == '__main__':
    # 启动Flask服务器
    # host='0.0.0.0' 让局域网内的其他设备也能访问
    # debug=True 让我们修改代码后服务器能自动重启，方便调试
    app.run(host='0.0.0.0', port=5000, debug=True)