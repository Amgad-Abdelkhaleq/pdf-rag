from typing import List, Dict
import threading

class ChatHistoryService:
    def __init__(self, max_history: int = 10):
        self._history = {}
        self._lock = threading.Lock()
        self.max_history = max_history
    
    def add_message(self, session_id: str, role: str, content: str):
        """
        Add a message to chat history
        
        Args:
            session_id (str): Unique session identifier
            role (str): Message role (user/assistant)
            content (str): Message content
        """
        with self._lock:
            if session_id not in self._history:
                self._history[session_id] = []
            
            self._history[session_id].append({
                "role": role,
                "content": content
            })
            
            # Trim history if exceeds max
            if len(self._history[session_id]) > self.max_history:
                self._history[session_id] = self._history[session_id][-self.max_history:]
    
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Retrieve chat history for a session
        
        Args:
            session_id (str): Unique session identifier
        
        Returns:
            List[Dict[str, str]]: Chat history
        """
        return self._history.get(session_id, [])
    
    def clear_history(self, session_id: str):
        """
        Clear chat history for a session
        
        Args:
            session_id (str): Unique session identifier
        """
        with self._lock:
            if session_id in self._history:
                del self._history[session_id]