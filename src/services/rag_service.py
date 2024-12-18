from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.prompts import PromptTemplate
from src.core.config import settings
import torch
from typing import Dict, List

class RAGService:
    def __init__(
        self, 
        embedding_service,
        vector_store,
        chat_history_service
    ):
        # Load LLM
        # cache_dir = "/Users/amgad/Downloads/models--microsoft--phi-1_5"
        self.tokenizer = AutoTokenizer.from_pretrained(settings.LLM_MODEL, 
                                                       token="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", 
                                                       trust_remote_code=True,
                                                    #    cache_dir=cache_dir
                                                        # use_auth_token=True,
                                                        skip_ssl_verification=True,  
                                                       )
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.LLM_MODEL, 
            torch_dtype=torch.float16,
            device_map='auto',
            token = "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",
            trust_remote_code=True,
            # cache_dir=cache_dir,
            # skip_ssl_verification=True,  
        ) 
        
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.chat_history_service = chat_history_service
        
        # Advanced RAG Prompt Template
        self.prompt_template = PromptTemplate(
            template="""
            Context: {context}
            Chat History: {chat_history}
            Question: {question}
            
            Based on the context and previous conversation, provide a precise and helpful answer.
            If the answer is not in the context, state that you don't have enough information.
            """,
            input_variables=["context", "chat_history", "question"]
        )
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve relevant document chunks
        
        Args:
            query (str): User query
            top_k (int): Number of context chunks to retrieve
        
        Returns:
            List[str]: Relevant document chunks
        """
        query_embedding = self.embedding_service.generate_embeddings([query])[0]
        retrieved_docs = self.vector_store.search(query_embedding, top_k)
        return [doc['text'] for doc in retrieved_docs]
    
    def generate_response(
        self, 
        query: str, 
        chat_history: List[Dict[str, str]]
    ) -> str:
        """
        Generate response using RAG
        
        Args:
            query (str): User query
            chat_history (List[Dict]): Previous conversation context
        
        Returns:
            str: Generated response
        """
        # Retrieve context
        context_chunks = self.retrieve_context(query)
        context = "\n".join(context_chunks)
        
        # Prepare chat history
        history_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in chat_history
        ])
        
        # Format prompt
        formatted_prompt = self.prompt_template.format(
            context=context,
            chat_history=history_text,
            question=query
        )
        
        # Generate response
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs, 
            max_length=600, 
            # num_return_sequences=1,
            temperature=0.7,
            repetition_penalty=1.7
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(response)
        return response.split("Answer provided by user (Chatterbot):")[-1].strip()