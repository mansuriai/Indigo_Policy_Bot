# core/llm.py
from typing import List, Dict, Optional, Generator
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.callbacks.base import BaseCallbackHandler
from utils.config import config
from utils.helpers import format_chat_history

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
        
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

class LLMManager:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=config.LLM_MODEL,
            temperature=0.7,
            api_key=config.OPENAI_API_KEY,
            streaming=True
        )
        
        self.system_prompt = """You are an AI travel assistant designed to provide clear, concise, and precise answers. Use the provided context and entire chat history to ensure accurate responses. 
        Acknowledge when context is insufficient and avoid hallucinating. Always consider the user's intent from the conversation history.
        
        Context: {context}
        
        Chat History: {chat_history}
        """
        
        self.human_prompt = "{question}"
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", self.human_prompt)
        ])
        
        self.chain = (
            {"context": RunnablePassthrough(), 
             "chat_history": RunnablePassthrough(), 
             "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def generate_response(
        self,
        question: str,
        context: List[Dict],
        chat_history: Optional[List[Dict]] = None,
        streaming_container = None
    ) -> str:
        """Generate a streaming response based on context and chat history."""
        formatted_context = "\n\n".join([doc['text'] for doc in context])
        formatted_history = format_chat_history(chat_history) if chat_history else ""
        
        callbacks = [StreamHandler(streaming_container)] if streaming_container else None
        
        # Update the LLM's callbacks for this specific generation
        self.llm.callbacks = callbacks
        
        response = self.chain.invoke({
            "context": formatted_context,
            "chat_history": formatted_history,
            "question": question
        })
        
        return response