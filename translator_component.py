from typing import Optional

__all__ = ["translate_text"]


def translate_text(text: str, *, use_google: bool = True, target_lang: str = "ja") -> str:
    """与えられた全文を target_lang に翻訳して返す。

    use_google が True の場合 googletrans を使用する。
    False の場合はそのまま返す（将来他の翻訳手段を追加する余地）。
    例外処理は上位に任せる。
    """
    if not use_google:
        return text  # 現時点では他の翻訳手段を実装しない

    from googletrans import Translator  # type: ignore

    translator = Translator()
    return translator.translate(text, dest=target_lang).text
