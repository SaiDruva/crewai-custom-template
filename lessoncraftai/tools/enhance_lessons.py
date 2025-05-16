from typing import Dict, Any, Optional
from crewai.tools import BaseTool
import json
from pydantic import Field, BaseModel

# Define a schema for the input
class EnhanceLessonsToolSchema(BaseModel):
    arguments: Optional[Dict[str, Any]] = Field(default={}, description="Optional arguments for the tool")

class EnhanceLessonsTool(BaseTool):
    name: str = "EnhanceLessons"
    description: str = "Recommend additional resources for lesson plans"
    
    # Define the input schema
    args_schema: type[BaseModel] = EnhanceLessonsToolSchema
    
    def _run(self, arguments: Dict[str, Any] = None) -> str:
        """Required implementation of the _run method from BaseTool"""
        print(f"Running enhance_lessons with arguments: {arguments}")
        
        # Default lesson plans if none provided
        default_lesson_plans = [{"topic": "Sample Topic", "objectives": ["Sample Objective"]}]
        
        # Try to extract lesson plans from the input
        lesson_plans = default_lesson_plans
        try:
            if arguments:
                # Try to find or extract a JSON array
                text_to_search = str(arguments)
                if "[" in text_to_search and "]" in text_to_search:
                    json_part = text_to_search[text_to_search.find("["):text_to_search.rfind("]")+1]
                    try:
                        extracted_plans = json.loads(json_part)
                        if isinstance(extracted_plans, list) and len(extracted_plans) > 0:
                            lesson_plans = extracted_plans
                    except:
                        pass
        except Exception as e:
            print(f"Error extracting lesson plans: {e}")
        
        # Generate enhancements for each lesson plan
        enhancements = []
        for plan in lesson_plans:
            topic_name = plan.get("topic", "Unknown Topic")
            objectives = plan.get("objectives", ["Understand the topic"])
            
            # Create a clean version of the topic name for URLs
            clean_topic = topic_name.lower().replace(' ', '-')
            
            # Create an enhancement structure
            enhancement = {
                "topic": topic_name,
                "objectives": objectives,
                "videos": [
                    {
                        "title": f"Introduction to {topic_name}",
                        "url": f"https://www.youtube.com/results?search_query={clean_topic}+introduction",
                        "description": f"An engaging introduction to {topic_name} for beginners."
                    },
                    {
                        "title": f"{topic_name} Explained",
                        "url": f"https://www.khanacademy.org/search?q={clean_topic}",
                        "description": f"Detailed explanation of {topic_name} with helpful visuals."
                    }
                ],
                "articles": [
                    {
                        "title": f"Understanding {topic_name}",
                        "url": f"https://www.britannica.com/search?query={clean_topic}",
                        "description": f"Comprehensive article about {topic_name} from Encyclopedia Britannica."
                    },
                    {
                        "title": f"{topic_name} in Practice",
                        "url": f"https://scholar.google.com/scholar?q={clean_topic}",
                        "description": f"Academic papers related to {topic_name} for in-depth study."
                    }
                ],
                "interactive_resources": [
                    {
                        "title": f"{topic_name} Interactive Quiz",
                        "url": f"https://quizlet.com/search?query={clean_topic}&type=sets",
                        "description": f"Interactive quizzes to test knowledge of {topic_name}."
                    },
                    {
                        "title": f"{topic_name} Simulation",
                        "url": f"https://phet.colorado.edu/en/search?q={clean_topic}",
                        "description": f"Interactive simulations related to {topic_name} concepts."
                    }
                ]
            }
            
            enhancements.append(enhancement)
        
        return json.dumps(enhancements, indent=2)