class Intents:
    ADD_BOOK = "add_book"
    GET_RECOMMENDATIONS = "get_recommendations"
    GET_SUMMARY = "get_summary"
    UNKNOWN = "unknown"

def detect_intent(query):
    query_lower = query.lower()
    if "add book" in query_lower or "new book" in query_lower:
        return Intents.ADD_BOOK
    elif "recommend books" in query_lower or "book recommendations" in query_lower:
        return Intents.GET_RECOMMENDATIONS
    elif "summary" in query_lower or "book summary" in query_lower:
        return Intents.GET_SUMMARY
    else:
        return Intents.UNKNOWN
