# app/services/moderation.py
from __future__ import annotations
import threading
from typing import Dict, Any

# Cargamos perezosamente (evita costo al boot)
_analyzers_lock = threading.Lock()
ANALYZERS: Dict[str, Any] = {"sentiment": None, "toxicity": None, "hate": None}

def _load_analyzers():
    with _analyzers_lock:
        if ANALYZERS["sentiment"] is None:
            from pysentimiento import create_analyzer
            ANALYZERS["sentiment"] = create_analyzer(task="sentiment", lang="es")
            # toxicity y hate speech están entrenados para español
            ANALYZERS["toxicity"]  = create_analyzer(task="toxicity", lang="es")
            ANALYZERS["hate"]      = create_analyzer(task="hate_speech", lang="es")

def analyze_text(text: str) -> dict:
    """
    Usa pysentimiento para:
      - sentiment: POS, NEU, NEG (+ probabilidades)
      - toxicity: TOXIC vs NOT_TOXIC (+ score)
      - hate speech: HATE vs NOT_HATE (+ score)
    Devuelve un dict con label 'positive'/'negative', score [-1..1], reasons y suggestions.
    """
    t = (text or "").strip()
    if not t:
        return {
            "label": "negative",
            "score": -1.0,
            "reasons": ["Mensaje vacío"],
            "suggestions": ["Escribe un mensaje con contexto y una propuesta concreta."]
        }

    try:
        _load_analyzers()
        sa   = ANALYZERS["sentiment"].predict(t)   # .output: POS/NEG/NEU, .probas: dict
        tox  = ANALYZERS["toxicity"].predict(t)    # .output: TOXIC/NOT_TOXIC
        hate = ANALYZERS["hate"].predict(t)        # .output: HATE/NOT_HATE

        # Puntaje agregado
        # base: +1 si POS, -1 si NEG, 0 si NEU (suavizado con probas)
        base = (
            sa.probas.get("POS", 0) -
            sa.probas.get("NEG", 0)
        )  # en [-1..1] aprox

        # Penalizaciones si hay toxicidad/odio
        penalty = 0.0
        reasons = []
        if tox.output == "TOXIC":
            penalty -= 0.6
            reasons.append("Se detectó toxicidad.")
        if hate.output == "HATE":
            penalty -= 0.8
            reasons.append("Se detectó discurso de odio.")

        score = max(-1.0, min(1.0, base + penalty))

        # Umbral: exigimos tono ≥ 0.15 y sin flags TOXIC/HATE
        positive = (score >= 0.15) and tox.output != "TOXIC" and hate.output != "HATE"

        if sa.output == "NEG":
            reasons.append("Sentimiento negativo predominante.")
        elif sa.output == "NEU" and not reasons:
            reasons.append("Tono neutral.")

        suggestions = []
        if not positive:
            if tox.output == "TOXIC" or hate.output == "HATE":
                suggestions.append("Evita lenguaje ofensivo o ataques personales; describe el problema sin descalificar.")
            if sa.output == "NEG":
                suggestions.append("Cambia adjetivos negativos por descripciones objetivas y propone una solución.")
            suggestions.append("Estructura en positivo: “Observé ___; propongo ___ porque ___”.")
            suggestions.append("Agradece el esfuerzo si aplica y enfoca en el objetivo: “Gracias por ___; ¿podemos ajustar ___ para mejorar ___?”")

        return {
            "label": "positive" if positive else "negative",
            "score": float(score),
            "sentiment": {"label": sa.output, "probas": sa.probas},
            "toxicity": tox.output,
            "hate": hate.output,
            "reasons": reasons,
            "suggestions": suggestions,
        }

    except Exception as e:
        # Fallback seguro si el modelo no carga en el server
        return {
            "label": "negative",
            "score": -1.0,
            "reasons": [f"Moderador no disponible: {e}"],
            "suggestions": ["Temporalmente no se puede moderar. Intenta con un tono constructivo y vuelve a enviar."]
        }
