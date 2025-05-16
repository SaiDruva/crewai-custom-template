from crewai import Crew, Task, Process
from dotenv import load_dotenv
import os

# Import agents
from agents.curriculum_ingestor import CurriculumIngestorAgent
from agents.topic_analyzer import TopicAnalyzerAgent
from agents.lesson_planner import LessonPlannerAgent
from agents.assessment_designer import AssessmentDesignerAgent
from agents.enhancer import EnhancerAgent

# Load environment variables
load_dotenv()

# Check for OpenAI API Key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set!")

# Define paths
curriculum_path = "./data/sample_curriculum.pdf"
persist_dir = "./data/vectorstore"

# Ensure directories exist
os.makedirs("./data", exist_ok=True)
os.makedirs(persist_dir, exist_ok=True)

# Initialize agents
curriculum_ingestor = CurriculumIngestorAgent(
    pdf_path=curriculum_path,
    persist_dir=persist_dir
).build()

topic_analyzer = TopicAnalyzerAgent(
    persist_dir=persist_dir
).build()

lesson_planner = LessonPlannerAgent().build()
assessment_designer = AssessmentDesignerAgent().build()
enhancer = EnhancerAgent().build()

# Define tasks without task dependencies
curriculum_task = Task(
    description="Load and vectorize the curriculum file for topic analysis.",
    expected_output="A confirmation that the curriculum has been properly indexed with details about the number of chunks created.",
    agent=curriculum_ingestor
)

topic_task = Task(
    description="Analyze the vectorized curriculum to identify key topics and learning objectives. The curriculum has already been vectorized and is stored in the vector database.",
    expected_output="A structured JSON list of key topics and learning objectives found in the curriculum.",
    agent=topic_analyzer
)

lesson_task = Task(
    description="Generate a lesson plan for each topic including time blocks and activities. Use the topics and objectives extracted from the curriculum.",
    expected_output="Structured lesson plans for each topic.",
    agent=lesson_planner
)

assessment_task = Task(
    description="Generate quiz and assessment questions based on the lesson plan. Create formative and summative assessments aligned with the learning objectives.",
    expected_output="Assessments for each lesson.",
    agent=assessment_designer
)

enhancer_task = Task(
    description="Recommend additional resources (videos, articles) per lesson. Find high-quality supplementary materials that enhance the learning experience.",
    expected_output="List of external links and resources per topic.",
    agent=enhancer
)

# Create the crew with a sequential process to ensure tasks run in order
crew = Crew(
    agents=[curriculum_ingestor, topic_analyzer, lesson_planner, assessment_designer, enhancer],
    tasks=[curriculum_task, topic_task, lesson_task, assessment_task, enhancer_task],
    verbose=True,
    process=Process.sequential  # This ensures tasks run in the order they're listed
)

# Run the crew if this file is executed directly
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n=== RESULT ===")
    print(result)