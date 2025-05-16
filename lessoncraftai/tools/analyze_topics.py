from typing import Dict, Any, Optional
from crewai.tools import BaseTool
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import os
import json
from pydantic import Field, BaseModel

# Define a schema for the input
class AnalyzeTopicsToolSchema(BaseModel):
    arguments: Optional[Dict[str, Any]] = Field(default={}, description="Optional arguments for the tool")

class AnalyzeTopicsTool(BaseTool):
    name: str = "AnalyzeTopics"
    description: str = "Analyzes the curriculum to extract key topics and learning objectives"
    
    # Define fields that the class will use
    persist_dir: str = Field(description="Directory containing the vector database")
    
    # Define the input schema
    args_schema: type[BaseModel] = AnalyzeTopicsToolSchema
    
    def _run(self, arguments: Dict[str, Any] = None) -> str:
        """Required implementation of the _run method from BaseTool"""
        print(f"Running analyze_topics with arguments: {arguments}")
        
        # Check if vector store exists
        if not os.path.exists(self.persist_dir):
            return f"Error: Vector store not found at {self.persist_dir}. Please run the VectorizePDF tool first."
        
        try:
            vectordb = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=OpenAIEmbeddings()
            )
            
            # Get document count to verify content
            collection = vectordb.get()
            if not collection['ids']:
                return "Error: Vector store exists but appears to be empty. Please rerun the curriculum ingestor."
            
            print(f"Vector store loaded with {len(collection['ids'])} documents")
            
            # Create retriever with slightly larger k for better context
            retriever = vectordb.as_retriever(search_kwargs={"k": 10})
            
            # Use RetrievalQA chain with structured output
            llm = ChatOpenAI(temperature=0.2)
            
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever,
                chain_type="stuff"
            )
            
            # Create a more detailed prompt that ensures grounding in the actual content
            prompt = (
                "Based ONLY on the curriculum documents provided in the context, extract the key topics and their "
                "associated learning objectives. Do not hallucinate or add information not present in the documents. "
                "If a topic doesn't have clear objectives, just include what you can find. "
                "\n\nFormat your response as a valid JSON list with this structure:\n"
                "[{\"topic\": \"Topic Name\", \"objectives\": [\"Objective 1\", \"Objective 2\"]}, ...]\n\n"
                "If you cannot find any clear topics or objectives, respond with an empty array: []"
            )
            
            print("Querying the vector store...")
            result = qa.run(prompt)
            
            # Try to validate and format the JSON
            try:
                # Parse the result to ensure it's valid JSON
                parsed_result = json.loads(result)
                if not isinstance(parsed_result, list):
                    return f"Error: Expected a JSON list but got {type(parsed_result)}. Raw result: {result}"
                
                print(f"Successfully extracted {len(parsed_result)} topics")
                return json.dumps(parsed_result, indent=2)
                
            except json.JSONDecodeError:
                # If not valid JSON, try to clean it up
                print("Result is not valid JSON, attempting to fix...")
                # Try to extract just the JSON part if there's extra text
                if "[" in result and "]" in result:
                    json_part = result[result.find("["):result.rfind("]")+1]
                    try:
                        parsed_result = json.loads(json_part)
                        return json.dumps(parsed_result, indent=2)
                    except:
                        pass
                
                return f"Error: Could not parse the result as JSON. Raw result: {result}"
                
        except Exception as e:
            return f"Error analyzing topics: {str(e)}"