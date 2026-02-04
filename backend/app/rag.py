import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Configuration
# Robustly find the root directory (where backend and data live)
current_dir = os.path.dirname(os.path.abspath(__file__))
# If we are in /app/app/rag.py, then root is /app
app_root = os.path.dirname(os.path.dirname(current_dir))

# Check if we are inside the 'app' subdirectory or at the root
if os.path.basename(current_dir) == 'app':
    # /app/app -> /app
    root_dir = os.path.dirname(current_dir)
else:
    # already at root or elsewhere
    root_dir = current_dir

# For Docker, WORKDIR is /app, code is in /app/app
# We want /app/data and /app/faiss_index
DATA_DIR = os.path.join(os.path.dirname(current_dir), "data")
VECTOR_STORE_PATH = os.path.join(os.path.dirname(current_dir), "faiss_index")

print(f"DEBUG: Calculated DATA_DIR: {DATA_DIR}")
print(f"DEBUG: Calculated VECTOR_STORE_PATH: {VECTOR_STORE_PATH}")

class RAGService:
    def __init__(self):
        self.vector_store = None
        self.chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Configuration
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "project-739cc5a6-82bc-4fc4-a29")
        location = "us-central1"
        
        print(f"DEBUG: Initializing Vertex AI with project={project_id}, location={location}")
        
        # Using Vertex AI for Embeddings
        self.embeddings = VertexAIEmbeddings(
            model_name="text-embedding-004",
            project=project_id,
            location=location
        )
        
        # Using Vertex AI for LLM (Gemini 2.0 Flash)
        self.llm = ChatVertexAI(
            model_name="gemini-2.0-flash",
            project=project_id,
            location=location,
            temperature=0.2,
        )
        
    def initialize(self):
        """Initialize the RAG system: load data or vector store."""
        try:
            if os.path.exists(VECTOR_STORE_PATH):
                print(f"Loading existing vector store from {VECTOR_STORE_PATH}")
                self.vector_store = FAISS.load_local(
                    VECTOR_STORE_PATH, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                print(f"Creating new vector store from data in {DATA_DIR}")
                self.create_vector_store()
                
            self._setup_chain()
            print("DEBUG: RAG system initialization complete.")
        except Exception as e:
            print(f"ERROR: RAG initialization failed: {str(e)}")
            import traceback
            traceback.print_exc()

    def create_vector_store(self):
        """Ingest PDFs and create vector store."""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Warning: Data directory {DATA_DIR} was empty/missing.")
            return

        documents = []
        for filename in os.listdir(DATA_DIR):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(DATA_DIR, filename)
                print(f"Processing {filename}...")
                try:
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

        if not documents:
            print("No documents found to ingest.")
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        print(f"DEBUG: Total documents loaded: {len(documents)} pages from all PDFs")
        print(f"DEBUG: Total chunks created: {len(splits)}")
        print(f"Creating embeddings for {len(splits)} chunks using Vertex AI...")
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        self.vector_store.save_local(VECTOR_STORE_PATH)
        print(f"Vector store saved at {VECTOR_STORE_PATH}")

    def _setup_chain(self):
        """Set up the conversational chain."""
        if not self.vector_store:
            print("Vector store not initialized!")
            return

        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        # Get list of files for context
        try:
            file_list = [f for f in os.listdir(DATA_DIR) if f.lower().endswith('.pdf')]
            files_str = ", ".join(file_list)
        except Exception:
            files_str = "Unknown"

        template = f"""You are a helpful AI assistant tasked with answering questions based on the provided documents.
You have access to the following documents: {files_str}.

Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer concise and helpful.

Context: {{context}}

Question: {{question}}

Helpful Answer:"""
        
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"], 
            template=template
        )

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

    def chat(self, query: str):
        """Run chat query."""
        if not self.chain:
            return {"answer": "System is initializing or no data found.", "sources": []}
            
        result = self.chain.invoke({"question": query})
        return {
            "answer": result["answer"],
            "sources": [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        }

rag_service = RAGService()
