import streamlit as st
import requests
import uuid

class ChatbotUI:
    def __init__(self, api_base_url="http://localhost:8000"):
        self.api_base_url = api_base_url
        self.session_id = str(uuid.uuid4())
    
    def render_sidebar(self):
        """
        Render sidebar for document upload
        """
        st.sidebar.title("PDF Chatbot")
        uploaded_file = st.sidebar.file_uploader(
            "Upload PDF Document", 
            type=["pdf"]
        )
        
        if uploaded_file is not None:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(
                f"{self.api_base_url}/documents/upload", 
                files=files
            )
            
            if response.status_code == 200:
                st.sidebar.success("Document uploaded successfully!")
            else:
                st.sidebar.error("Upload failed")
    
    def render_chat_interface(self):
        """
        Render main chat interface
        """
        st.title("Document Q&A Chatbot")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your document"):
            # Add user message to chat history
            st.session_state.messages.append({
                "role": "user", 
                "content": prompt
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                
                try:
                    response = requests.post(
                        f"{self.api_base_url}/chat", 
                        json={
                            "session_id": self.session_id, 
                            "query": prompt
                        }
                    ).json()
                    
                    response_placeholder.markdown(response['response'])
                    
                    # Add assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response['response']
                    })
                except Exception as e:
                    response_placeholder.error(f"Error: {e}")
    
    def run(self):
        """
        Run Streamlit application
        """
        self.render_sidebar()
        self.render_chat_interface()

def main():
    app = ChatbotUI()
    app.run()

if __name__ == "__main__":
    main()