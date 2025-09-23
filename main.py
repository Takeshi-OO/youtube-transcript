from youtube_transcript_api import YouTubeTranscriptApi
from typing import List

# ===== 設定スイッチ ===============================
SHOW_TIMESTAMP: bool = False   # タイムスタンプを表示するか
SHOW_JAPANESE: bool = False  # 日本語訳を同時に表示するか

# 対象動画ID -----------------------------------------------------------
video_id = "uyD-Oq3llj0"

ytt_api = YouTubeTranscriptApi()

# 利用可能な字幕を取得 -------------------------------------------------
transcript_list = ytt_api.list(video_id)

# 元字幕(自動生成優先)を決定 -------------------------------------------
base_transcript = None
for t in transcript_list:
    if t.is_generated:  # 自動生成を優先
        base_transcript = t
        break
if base_transcript is None:
    # 自動生成が無ければ最初の字幕を使用
    base_transcript = next(iter(transcript_list))

original_snippets = base_transcript.fetch()

# 検出言語を表示 ---------------------------------------------------------
print(f"Detected language: {base_transcript.language} ({base_transcript.language_code})")

# 日本語翻訳 -----------------------------------------------------------
translated_snippets: List = []
if SHOW_JAPANESE and base_transcript.is_translatable:
    translated_snippets = base_transcript.translate("ja").fetch()

# 出力関数 -------------------------------------------------------------

def format_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

if SHOW_TIMESTAMP:
    # タイムスタンプ付き出力 ---------------------------
    if SHOW_JAPANESE and translated_snippets:
        for orig, jp in zip(original_snippets, translated_snippets):
            print(f"[{format_ts(orig.start)}] {orig.text} / {jp.text}")
    else:
        for orig in original_snippets:
            print(f"[{format_ts(orig.start)}] {orig.text}")
else:
    # タイムスタンプ無し: 全文まとめて出力 ----------------
    original_text = " ".join(s.text for s in original_snippets)
    if SHOW_JAPANESE and translated_snippets:
        jp_text = " ".join(s.text for s in translated_snippets)
        print(original_text)
        print("\n---\n")  # 区切り線
        print(jp_text)
    else:
        print(original_text)
