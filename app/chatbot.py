from llm import generate_response
from vectorstore import similarity_text, add_book_to_vectorDB
from sessionmng import get_session_history, store
from intents import Intents, detect_intent

class Chatbot:
    def __init__(self):
        self.store = store

    def handle_query(self, session_id, query):
        intent = detect_intent(query)
        
        if intent == Intents.ADD_BOOK:
            response = self.handle_add_book(query)
        elif intent == Intents.GET_RECOMMENDATIONS:
            response = self.handle_get_recommendations(query)
        elif intent == Intents.GET_SUMMARY:
            response = self.handle_get_summary(query)
        else:
            response = generate_response(session_id, query)
        
        return response

    def handle_add_book(self, query):
        # Extract book details from query
        details = self.parse_book_details(query)
        if not details:
            return "Invalid book details provided."

        title = details.get("title")
        authors = details.get("authors")
        categories = details.get("categories")
        description = details.get("description")

        if not title or not authors or not categories or not description:
            return "Missing book details. Please provide title, authors, categories, and description."

        add_book_to_vectorDB(title, authors, categories, description)
        return "Book added successfully!"

    def parse_book_details(self, query):
        details = {}
        parts = query.split(",")
        for part in parts:
            key_value = part.split(":")
            if len(key_value) == 2:
                key = key_value[0].strip().lower()
                value = key_value[1].strip()
                details[key] = value
        return details

    def handle_get_recommendations(self, query):
        recommendations = self.get_recommendations(query)
        return {"recommendations": recommendations}

    def handle_get_summary(self, query):
        summary = generate_response("summary", query)
        return {"summary": summary}

    def get_recommendations(self, query):
        similar_items = similarity_text(query)
        return similar_items

    def print_message_history(self, session_id):

        history = get_session_history(session_id)
        for message in history.messages:
            print(f"{type(message).__name__}: {message.content}")

def handle_get_recommendations(self, query):
    recommendations = self.get_recommendations(query)
    # Apply filtering logic based on metadata
    filters = self.parse_filters(query)
    filtered_recommendations = [rec for rec in recommendations if self.apply_filters(rec, filters)]
    return {"recommendations": filtered_recommendations}

def parse_filters(self, query):
    # Parse filters from query
    filters = {}
    parts = query.split(",")
    for part in parts:
        key_value = part.split(":")
        if len(key_value) == 2:
            key = key_value[0].strip().lower()
            value = key_value[1].strip()
            filters[key] = value
    return filters

def apply_filters(self, rec, filters):
    # Apply filters to a single recommendation
    for key, value in filters.items():
        if rec.get(key) != value:
            return False
    return True
