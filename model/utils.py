from model import sentiment_pipeline

def predict(comment: str) -> dict:
    result = sentiment_pipeline(comment)[0]
    return {
        "label": result['label'],
        "confidence": round(result['score'] * 100, 2)
    }