token = "MTE5MjUwODMxNzEzODk2MDUyNA.GQXCFO.Yj3UqwiEOk9jtilHh-xQPyvZkdfhklJG-kKpYs"

class admin:
    error_channel = 1192519269045510194

import re

# 正規表現パターン
pattern = r'self\.bot\.translation\.getText\((.*?)\)'

# 対象の文字列を検索
text = '... self.bot.translation.getText("Hello, world!") ... self.bot.translation.getText("こんにちは、世界！") ...'  # ここに対象の文字列を入力
matches = re.findall(pattern, text)

# 抽出した値を表示
if matches:
    print(matches)
    for i, value in enumerate(matches, start=1):
        print(f"抽出された値 {i}: {value}")
else:
    print("値は見つかりませんでした。")
