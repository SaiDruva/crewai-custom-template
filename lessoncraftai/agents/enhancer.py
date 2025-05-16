from crewai import Agent
from tools.enhance_lessons import EnhanceLessonsTool

class EnhancerAgent:
    def __init__(self):
        pass
        
    def build(self):
        # Create the tool
        enhance_lessons_tool = EnhanceLessonsTool()
        
        # Create and return the agent
        return Agent(
            role="Lesson Enhancer",
            goal="Enrich lesson plans with supplementary resources and activities",
            backstory="You are an educational resource specialist who excels at finding and recommending high-quality supplementary materials. You have extensive knowledge of educational websites, videos, interactive tools, and hands-on activities that can enhance learning experiences.",
            verbose=True,
            tools=[enhance_lessons_tool]
        )