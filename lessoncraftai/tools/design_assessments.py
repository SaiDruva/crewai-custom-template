from typing import Dict, Any, Optional
from crewai.tools import BaseTool
import json
from pydantic import Field, BaseModel

# Define a schema for the input
class DesignAssessmentsToolSchema(BaseModel):
    arguments: Optional[Dict[str, Any]] = Field(default={}, description="Optional arguments for the tool")

class DesignAssessmentsTool(BaseTool):
    name: str = "DesignAssessments"
    description: str = "Create assessments based on lesson plans"
    
    # Define the input schema
    args_schema: type[BaseModel] = DesignAssessmentsToolSchema
    
    def _run(self, arguments: Dict[str, Any] = None) -> str:
        """Required implementation of the _run method from BaseTool"""
        print(f"Running design_assessments with arguments: {arguments}")
        
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
        
        # Generate assessments for each lesson plan
        assessments = []
        for plan in lesson_plans:
            topic_name = plan.get("topic", "Unknown Topic")
            objectives = plan.get("objectives", ["Understand the topic"])
            
            # Create an assessment structure
            assessment = {
                "topic": topic_name,
                "objectives": objectives,
                "formative_assessment": {
                    "exit_ticket": {
                        "questions": [
                            {
                                "type": "short_answer",
                                "question": f"What is one thing you learned about {topic_name} today?"
                            },
                            {
                                "type": "multiple_choice",
                                "question": "How confident are you with today's material?",
                                "options": [
                                    "Very confident",
                                    "Somewhat confident",
                                    "Slightly confused",
                                    "Very confused"
                                ]
                            }
                        ]
                    }
                },
                "summative_assessment": {
                    "quiz": {
                        "questions": [
                            {
                                "type": "multiple_choice",
                                "question": f"Which of the following best describes {topic_name}?",
                                "options": [
                                    f"Correct description of {topic_name}",
                                    "Incorrect option 1",
                                    "Incorrect option 2",
                                    "Incorrect option 3"
                                ],
                                "correct_answer": 0
                            },
                            {
                                "type": "short_answer",
                                "question": f"Explain the importance of {topic_name}.",
                                "sample_answer": f"{topic_name} is important because..."
                            },
                            {
                                "type": "true_false",
                                "question": f"{topic_name} is a fundamental concept in this field.",
                                "correct_answer": True
                            }
                        ]
                    }
                }
            }
            
            assessments.append(assessment)
        
        return json.dumps(assessments, indent=2)