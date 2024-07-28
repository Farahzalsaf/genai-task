from intents import Intents, intent_graph

def detect_intent(query):
    intent = intent_graph.match(query)
    return intent if intent else Intents.UNKNOWN
