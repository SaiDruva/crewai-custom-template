from crewai import Agent
from tools.design_assessments import DesignAssessmentsTool

class AssessmentDesignerAgent:
    def __init__(self):
        pass
        
    def build(self):
        # Create the tool
        design_assessments_tool = DesignAssessmentsTool()
        
        # Create and return the agent
        return Agent(
            role="Assessment Designer",
            goal="Create effective assessments to measure student learning and progress",
            backstory="You are an assessment specialist with expertise in creating various forms of assessment that accurately measure student understanding and progress. You design both formative and summative assessments aligned with learning objectives.",
            verbose=True,
            tools=[design_assessments_tool]
        )