from typing import Dict, Any, Optional
from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pydantic import Field, BaseModel

# Define a schema for the input
class VectorizePDFToolSchema(BaseModel):
    arguments: Optional[Dict[str, Any]] = Field(default={}, description="Optional arguments for the tool")

class VectorizePDFTool(BaseTool):
    name: str = "VectorizePDF"
    description: str = "Loads and vectorizes a PDF document for later retrieval and querying"
    
    # Define fields that the class will use
    pdf_path: str = Field(description="Path to the PDF file")
    persist_dir: str = Field(description="Directory to store the vector database")
    
    # Define the input schema
    args_schema: type[BaseModel] = VectorizePDFToolSchema
    
    def _run(self, arguments: Dict[str, Any] = None) -> str:
        """Required implementation of the _run method from BaseTool"""
        print(f"Running vectorize_pdf with arguments: {arguments}")
        
        # Make sure vectorstore directory exists
        os.makedirs(self.persist_dir, exist_ok=True)
        
        # Check if vector store already exists and has content
        if os.path.exists(self.persist_dir) and self._vector_store_has_content():
            print(f"Vector store already exists at {self.persist_dir} and has content.")
            return f"Curriculum is already indexed in {self.persist_dir}. Found existing vector store with content."
        
        # Check if PDF file exists
        if not os.path.exists(self.pdf_path):
            return f"Curriculum PDF not found at: {self.pdf_path}"
            
        # Verify file extension
        if not self.pdf_path.lower().endswith('.pdf'):
            return f"File at {self.pdf_path} is not a PDF file."

        try:
            print(f"Loading PDF from {self.pdf_path}")
            loader = PyPDFLoader(self.pdf_path)
            pages = loader.load()
            print(f"Loaded {len(pages)} pages from PDF")
        except ImportError:
            return "The pypdf package is not installed. Please install it with 'pip install pypdf'."
        except Exception as e:
            return f"Error loading PDF: {str(e)}"

        if not pages:
            return "No content found in the curriculum PDF. Please check the file."

        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            docs = splitter.split_documents(pages)
            print(f"Split into {len(docs)} chunks")
        except Exception as e:
            return f"Error splitting documents: {str(e)}"

        if not docs:
            return "PDF loaded, but no documents could be chunked."

        try:
            print("Creating embeddings...")
            embeddings = OpenAIEmbeddings()
            print(f"Storing vectors in {self.persist_dir}")
            vectordb = Chroma.from_documents(
                documents=docs, 
                embedding=embeddings, 
                persist_directory=self.persist_dir
            )
            vectordb.persist()
            print("Vectorstore created and persisted successfully")
        except Exception as e:
            return f"Error creating vector store: {str(e)}"

        return f"Curriculum indexed successfully with {len(docs)} chunks from {self.pdf_path}"
    
    def _vector_store_has_content(self) -> bool:
        """Check if the vector store exists and has content"""
        try:
            # Try to load the vector store
            if not os.path.exists(os.path.join(self.persist_dir, "chroma.sqlite3")):
                return False
                
            vectordb = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=OpenAIEmbeddings()
            )
            
            # Get collection info to check if it has documents
            collection = vectordb.get()
            return len(collection['ids']) > 0
        except Exception as e:
            print(f"Error checking vector store: {e}")
            return False