from crewai import Agent
from tools.analyze_topics import AnalyzeTopicsTool

class TopicAnalyzerAgent:
    def __init__(self, persist_dir: str):
        self.persist_dir = persist_dir
        
    def build(self):
        # Create the tool - pass parameters as keyword arguments
        analyze_tool = AnalyzeTopicsTool(
            persist_dir=self.persist_dir
        )
        
        # Create and return the agent
        return Agent(
            role="Topic Analyzer",
            goal="Identify structured topics and learning objectives from the curriculum",
            backstory="You are an expert in academic planning and curriculum design who extracts relevant topics and learning objectives from educational content.",
            verbose=True,
            tools=[analyze_tool]
        )