import requests
from bs4 import BeautifulSoup
import json
import re

def get_real_keirin_data(place_code="01", race_num="1"):
    # ターゲットURL（netkeirinの出走表ページ例）
    # ※開催日によってURLが変わるため、本来は日付も動的に生成します
    url = f"https://keirin.netkeiba.com/db/shusso/?bankid={place_code}&race_no={race_num}"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    players = []
    
    # サイトのHTML構造に合わせてデータを抽出
    # (注: サイトの仕様変更によりクラス名は変わることがあります)
    rows = soup.select("tr.PlayerList_Row")
    
    for i, row in enumerate(rows, 1):
        try:
            name = row.select_one(".PlayerName").text.strip()
            # 競走得点などを探す（例：得点が記載されているセル）
            score_text = row.select_one(".Score").text.strip()
            score = float(re.findall(r"\d+\.\d+", score_text)[0])
            
            players.append({
                "id": i,
                "s": score,
                "n": name
            })
        except:
            # データが取れなかった時のバックアップ
            continue

    # もし空っぽならテストデータを入れる（エラー防止）
    if not players:
        print("本物のデータが取得できなかったため、ダミーを出力します。")
        players = [{"id": i, "s": 80.0, "n": f"確認中 {i}番車"} for i in range(1, 10)]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 玉野(01)の1レース目を取得
    get_real_keirin_data("01", "1")


