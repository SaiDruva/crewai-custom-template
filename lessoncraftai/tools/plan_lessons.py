from typing import Dict, Any, Optional
from crewai.tools import BaseTool
import json
from pydantic import Field, BaseModel

# Define a schema for the input
class PlanLessonsToolSchema(BaseModel):
    arguments: Optional[Dict[str, Any]] = Field(default={}, description="Optional arguments for the tool")

class PlanLessonsTool(BaseTool):
    name: str = "PlanLessons"
    description: str = "Generate lesson plans based on curriculum topics and objectives"
    
    # Define the input schema
    args_schema: type[BaseModel] = PlanLessonsToolSchema
    
    def _run(self, arguments: Dict[str, Any] = None) -> str:
        """Required implementation of the _run method from BaseTool"""
        print(f"Running plan_lessons with arguments: {arguments}")
        
        # Default topics if none provided
        default_topics = [{"topic": "Sample Topic", "objectives": ["Sample Objective"]}]
        
        # Try to extract topics from the input
        topics = default_topics
        try:
            if arguments:
                # Try to find or extract a JSON array of topics
                text_to_search = str(arguments)
                if "[" in text_to_search and "]" in text_to_search:
                    json_part = text_to_search[text_to_search.find("["):text_to_search.rfind("]")+1]
                    try:
                        extracted_topics = json.loads(json_part)
                        if isinstance(extracted_topics, list) and len(extracted_topics) > 0:
                            topics = extracted_topics
                    except:
                        pass
        except Exception as e:
            print(f"Error extracting topics: {e}")
        
        # Generate lesson plans for each topic
        lesson_plans = []
        for topic in topics:
            topic_name = topic.get("topic", "Unknown Topic")
            objectives = topic.get("objectives", ["Understand the topic"])
            
            # Create a comprehensive lesson plan structure
            lesson_plan = {
                "topic": topic_name,
                "objectives": objectives,
                "duration": "60 minutes",
                "materials_needed": ["Handouts", "Presentation slides", "Reference materials"],
                "activities": [
                    {
                        "name": "Introduction",
                        "duration": "10 minutes",
                        "description": f"Introduce the topic of {topic_name} and establish learning objectives."
                    },
                    {
                        "name": "Direct Instruction",
                        "duration": "20 minutes",
                        "description": f"Present key concepts related to {topic_name}."
                    },
                    {
                        "name": "Guided Practice",
                        "duration": "15 minutes",
                        "description": "Students work on exercises with teacher guidance."
                    },
                    {
                        "name": "Independent Practice",
                        "duration": "10 minutes",
                        "description": "Students demonstrate understanding independently."
                    },
                    {
                        "name": "Closure",
                        "duration": "5 minutes",
                        "description": "Summarize key learning and check for understanding."
                    }
                ],
                "assessment": {
                    "formative": ["Exit tickets", "Guided practice observations", "Q&A during instruction"],
                    "summative": ["End-of-unit project", "Quiz in next class"]
                }
            }
            
            lesson_plans.append(lesson_plan)
        
        return json.dumps(lesson_plans, indent=2)