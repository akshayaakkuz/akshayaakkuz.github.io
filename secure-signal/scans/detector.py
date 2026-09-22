"""Small independent Python heuristic baseline; not a trained ML model."""
import re
import unicodedata

RULES = [
    ("Credential request", 4, r"\b(?:enter|send|share|verify)\b.{0,50}\b(?:password|otp|verification code)\b"),
    ("Prize claim", 3, r"\b(?:you have won|claim your prize|lottery winner)\b"),
    ("Advance payment", 3, r"\b(?:processing fee|send money|wire transfer|gift cards)\b"),
    ("Urgent pressure", 1, r"\b(?:urgent|immediately|act now|last chance)\b"),
    ("Web address", 1, r"\b(?:https?://|www\.)\S+"),
]


def analyze(message):
    if not isinstance(message, str) or not message.strip() or len(message) > 5000:
        raise ValueError("Provide 1–5,000 characters.")
    normalized = unicodedata.normalize("NFKC", message)
    normalized = re.sub(r"[\u200b-\u200d\ufeff]", "", normalized)
    normalized = " ".join(normalized.split())
    signals = [{"label": label, "points": points} for label, points, pattern in RULES if re.search(pattern, normalized, re.I)]
    score = sum(signal["points"] for signal in signals)
    return {"score": score, "level": "Likely spam" if score >= 5 else "Needs a closer look" if score >= 2 else "Few spam signals", "signals": signals}
