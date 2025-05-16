from crewai import Agent
from tools.vectorize_pdf import VectorizePDFTool

class CurriculumIngestorAgent:
    def __init__(self, pdf_path: str, persist_dir: str):
        self.pdf_path = pdf_path
        self.persist_dir = persist_dir
        
    def build(self):
        # Create the tool - pass parameters as keyword arguments
        vectorize_tool = VectorizePDFTool(
            pdf_path=self.pdf_path,
            persist_dir=self.persist_dir
        )
        
        # Create and return the agent
        return Agent(
            role="Curriculum Ingestor",
            goal="Load and index the curriculum PDF",
            backstory="You ingest educational curriculum documents and convert them into searchable vector embeddings.",
            verbose=True,
            tools=[vectorize_tool]
        )