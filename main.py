from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranslationLanguageNotAvailable
from typing import List

# 自作コンポーネント
from translator_component import translate_text

# ===== 設定スイッチ ===============================
SHOW_TIMESTAMP: bool = False   # タイムスタンプを表示するか
SHOW_JAPANESE: bool = True    # 日本語訳を同時に表示するか
# Google 翻訳 API を使用するか (True の場合 youtube_transcript_api の translate は使わない)
USE_GOOGLE_TRANSLATOR: bool = False 

# 対象動画ID -----------------------------------------------------------
video_id = "o0em2heVOLo"

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

# 取得した字幕スニペット
original_snippets = base_transcript.fetch()

# 検出言語を表示 ---------------------------------------------------------
print(f"Detected language: {base_transcript.language} ({base_transcript.language_code})")

# 日本語翻訳 -----------------------------------------------------------
translated_snippets: List = []
if SHOW_JAPANESE and not SHOW_TIMESTAMP:
    # タイムスタンプ無しで全文をまとめて翻訳
    original_text_full = " ".join(s.text for s in original_snippets)
    if USE_GOOGLE_TRANSLATOR:
        jp_full = translate_text(original_text_full, use_google=True)
    elif base_transcript.is_translatable:
        try:
            jp_full = " ".join(s.text for s in base_transcript.translate("ja").fetch())
        except TranslationLanguageNotAvailable:
            jp_full = "(翻訳不可)"
    else:
        jp_full = "(翻訳不可)"

# 出力関数 -------------------------------------------------------------

def format_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

if SHOW_TIMESTAMP:
    # タイムスタンプ付き出力 ---------------------------
    for orig in original_snippets:
        print(f"[{format_ts(orig.start)}] {orig.text}")
else:
    # タイムスタンプ無し: 全文まとめて出力 ----------------
    original_text = " ".join(s.text for s in original_snippets)
    if SHOW_JAPANESE:
        print(original_text)
        print("\n---\n")
        print(jp_full)
    else:
        print(original_text)
