from chatterbot import ChatBot
import logging
logger =  logging.getLogger()
logger.setLevel(logging.CRITICAL)
chatbot = ChatBot('bot',storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
            logic_adapters=[
            "chatterbot.logic.BestMatch",
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.TimeLogicAdapter"]
            ,read_only=False)
def response(query):
    l = str(chatbot.get_response(query))
    return l