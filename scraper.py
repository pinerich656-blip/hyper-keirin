import requests
import json
import time
from datetime import datetime

def get_keirin_data():
    # 本物のスマホブラウザを完璧に模倣するヘッダー
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ja-jp",
    }
    
    today = datetime.now().strftime("%Y%m%d")
    master_data = {}

    try:
        # ターゲット：netkeirinの出走表一覧
        # ※GitHub（海外）からでも比較的通りやすいURL構造を狙う
        url = f"https://keirin.netkeiba.com/db/program/?date={today}"
        
        session = requests.Session() # セッションを維持して「人間らしさ」を出す
        res = session.get(url, headers=headers, timeout=15)
        
        import re
        # 開催場とIDを抽出
        stadiums = re.findall(r'bankid=(\d+)".*?title="([^"]+)"', res.text)
        
        if not stadiums:
            print("開催が見つかりませんでした。")
        else:
            for bankid, name in stadiums:
                print(f"【{name}】を取得中...")
                stadium_races = {}
                
                # 負荷をかけないよう、各場1R〜12Rを丁寧に取得
                for r in range(1, 13):
                    race_url = f"https://keirin.netkeiba.com/db/shusso/?bankid={bankid}&race_no={r}"
                    r_res = session.get(race_url, headers=headers, timeout=15)
                    
                    # 選手名と得点を抽出（正規表現で柔軟に）
                    names = re.findall(r'class="PlayerName">(.*?)</span>', r_res.text)
                    scores = re.findall(r'class="Score">(\d+\.\d+)</span>', r_res.text)
                    
                    players = []
                    for i in range(len(names)):
                        p_name = names[i].strip()
                        p_score = float(scores[i]) if i < len(scores) else 0.0
                        players.append({"id": i+1, "s": p_score, "n": p_name})
                    
                    if players:
                        stadium_races[str(r)] = players
                    
                    # サーバーへの礼儀：1秒待機
                    time.sleep(1) 
                
                master_data[name] = stadium_races

    except Exception as e:
        print(f"エラーが発生したよ: {e}")

    # 万が一失敗しても、アプリを壊さないための空データを書き込まない工夫
    if master_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(master_data, f, ensure_ascii=False, indent=2)
        print("データの更新に成功したよ！")
    else:
        print("データが取得できなかったため、更新をスキップしました。")

if __name__ == "__main__":
    get_keirin_data()

