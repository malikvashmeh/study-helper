"""
LLM Manager
Handles Gemini LLM provider and conversation memory
"""

import os
import logging
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.callbacks.manager import CallbackManagerForChainRun

logger = logging.getLogger(__name__)

class LLMManager:
    """Manages LLM operations and conversation memory"""
    
    def __init__(self, 
                 llm_provider: str = "gemini",
                 model_name: str = "gemini-1.5-flash",
                 temperature: float = 0.7,
                 max_tokens: int = 1000):
        
        # Load environment variables
        load_dotenv()
        self.llm_provider = llm_provider.lower()
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize LLM
        self.llm = self._initialize_llm()
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="text"
        )
    
    def _initialize_llm(self):
        """Initialize LLM based on provider"""
        if self.llm_provider == "gemini":
            return ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}. Only 'gemini' is supported.")
    
    def create_qa_chain(self, retriever, system_prompt: str = None):
        """Create a question-answering chain with retrieval"""
        if system_prompt is None:
            system_prompt = """You are a helpful study assistant. Use the provided context to answer questions accurately and comprehensively. 
            If the answer is not in the context, say so and provide general guidance if possible.
            Always cite the source when possible."""
        
        # Create prompt template
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        # Create QA chain
        qa_chain = LLMChain(
            llm=self.llm,
            prompt=qa_prompt,
            memory=self.memory,
            verbose=True
        )
        
        return qa_chain
    
    def create_summarization_chain(self, system_prompt: str = None):
        """Create a summarization chain"""
        if system_prompt is None:
            system_prompt = """You are an expert at creating comprehensive summaries. 
            Create a well-structured summary that captures the key points, main concepts, and important details.
            Use clear headings and bullet points for better readability."""
        
        summary_prompt = PromptTemplate(
            input_variables=["text"],
            template=f"{system_prompt}\n\nText to summarize:\n{{text}}\n\nSummary:"
        )
        
        summary_chain = LLMChain(
            llm=self.llm,
            prompt=summary_prompt,
            verbose=True
        )
        
        return summary_chain
    
    def create_quiz_chain(self, system_prompt: str = None):
        """Create a quiz generation chain"""
        if system_prompt is None:
            system_prompt = """You are an expert educator creating study materials. 
            Generate educational questions based on the provided text.
            Create a mix of question types: multiple choice, true/false, and short answer.
            Return the response in JSON format with the following structure:
            {{
                "questions": [
                    {{
                        "type": "multiple_choice",
                        "question": "Question text",
                        "options": ["A", "B", "C", "D"],
                        "correct_answer": "A",
                        "explanation": "Why this is correct"
                    }},
                    {{
                        "type": "true_false",
                        "question": "Question text",
                        "correct_answer": true,
                        "explanation": "Explanation"
                    }},
                    {{
                        "type": "short_answer",
                        "question": "Question text",
                        "correct_answer": "Expected answer",
                        "explanation": "Additional context"
                    }}
                ]
            }}"""
        
        quiz_prompt = PromptTemplate(
            input_variables=["text", "num_questions"],
            template=f"{system_prompt}\n\nText: {{text}}\n\nNumber of questions: {{num_questions}}\n\nQuiz:"
        )
        
        quiz_chain = LLMChain(
            llm=self.llm,
            prompt=quiz_prompt,
            verbose=True
        )
        
        return quiz_chain
    
    def answer_question(self, question: str, context: str) -> str:
        """Answer a question using provided context"""
        try:
            qa_chain = self.create_qa_chain(None)
            result = qa_chain.run(input=f"Context: {context}\n\nQuestion: {question}")
            return result
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise
    
    def summarize_text(self, text: str) -> str:
        """Summarize provided text"""
        try:
            summary_chain = self.create_summarization_chain()
            result = summary_chain.run(text=text)
            return result
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            raise
    
    def generate_quiz(self, text: str, num_questions: int = 5) -> Dict[str, Any]:
        """Generate quiz questions from text"""
        try:
            quiz_chain = self.create_quiz_chain()
            result = quiz_chain.run(text=text, num_questions=num_questions)
            
            # Try to parse JSON response
            import json
            import re
            
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = result
            
            try:
                parsed = json.loads(json_str)
                return parsed
            except json.JSONDecodeError:
                # If not valid JSON, return as text
                return {"questions": [{"type": "text", "content": result}]}
                
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            raise
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        logger.info("Conversation memory cleared")
    
    def get_memory_summary(self) -> str:
        """Get summary of conversation memory"""
        if hasattr(self.memory, 'chat_memory') and self.memory.chat_memory.messages:
            return f"Memory contains {len(self.memory.chat_memory.messages)} messages"
        return "Memory is empty"
