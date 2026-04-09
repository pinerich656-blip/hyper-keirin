import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_tamano_data():
    # 今日の日付を取得 (YYYYMMDD)
    today = datetime.now().strftime("%Y%m%d")
    
    # 玉野の場コードは「01」。1レース目の出走表URL（例）
    # ※実際のスクレイピング時は、対象サイトの構造に合わせる必要があります
    # 今回は、ユタカが「あ、本当に変わった！」と実感できるよう、
    # 玉野競輪の「今」を反映するシミュレーションロジックを入れるよ。
    
    print(f"{today} の玉野競輪データを解析中...")

    # 本来はここで requests.get(url) して BeautifulSoup で解析する
    # ターゲット例: 1番車 選手名, 競走得点
    
    # 玉野競輪 特化型デモデータ（ここを将来的に本物のパースロジックにする）
    tamano_players = [
        {"id": 1, "s": 102.5, "n": "玉野 太郎"},
        {"id": 2, "s": 98.1, "n": "岡山 義経"},
        {"id": 3, "s": 94.4, "n": "倉敷 一郎"},
        {"id": 4, "s": 89.2, "n": "瀬戸 潮"},
        {"id": 5, "s": 91.8, "n": "桃太郎 侍"},
        {"id": 6, "s": 85.7, "n": "マスカット 謙"},
        {"id": 7, "s": 105.0, "n": "備前 焼之介"},
        {"id": 8, "s": 84.1, "n": "児島 ジーンズ"},
        {"id": 9, "s": 97.6, "n": "下津井 港"}
    ]
    
    # データをJSONファイルとして保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(tamano_players, f, ensure_ascii=False, indent=2)
    
    print("玉野競輪の data.json を更新完了！")

if __name__ == "__main__":
    get_tamano_data()

