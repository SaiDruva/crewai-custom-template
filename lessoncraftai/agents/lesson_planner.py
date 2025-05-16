from crewai import Agent
from tools.plan_lessons import PlanLessonsTool

class LessonPlannerAgent:
    def __init__(self):
        pass
        
    def build(self):
        # Create the tool
        plan_lessons_tool = PlanLessonsTool()
        
        # Create and return the agent
        return Agent(
            role="Lesson Planner",
            goal="Create effective and engaging lesson plans based on curriculum topics",
            backstory="You are an experienced educator with expertise in instructional design. You create comprehensive lesson plans that incorporate best practices in teaching and learning.",
            verbose=True,
            tools=[plan_lessons_tool]
        )