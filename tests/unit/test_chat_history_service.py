import pytest
from src.services.chat_history_service import ChatHistoryService

class TestChatHistoryService:
    @pytest.fixture
    def chat_history_service(self):
        return ChatHistoryService()
    
    def test_add_and_get_history(self, chat_history_service):
        session_id = "test_session"
        
        # Add messages
        chat_history_service.add_message(session_id, "user", "Hello")
        chat_history_service.add_message(session_id, "assistant", "Hi there")
        
        # Retrieve history
        history = chat_history_service.get_history(session_id)
        
        assert len(history) == 2
        assert history[0]['role'] == 'user'
        assert history[0]['content'] == 'Hello'