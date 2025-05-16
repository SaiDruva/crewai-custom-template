LessonCraftAI
Transform Curriculum Documents into Comprehensive Lesson Plans
LessonCraftAI is an AI-powered system that converts curriculum documents into complete, classroom-ready lesson plans. Using advanced NLP and vector embeddings, this tool analyzes curriculum PDFs, extracts key topics and learning objectives, then generates structured lesson plans with timed activities, assessments, and supplementary resources.

What Problem Does LessonCraftAI Solve?
Teachers and educational content creators often spend countless hours developing lesson plans from curriculum standards. LessonCraftAI dramatically reduces this workload, allowing educators to:

Process curriculum documents in seconds instead of hours
Maintain perfect alignment between curriculum standards and classroom activities
Generate consistent, high-quality lesson materials at scale
Focus more time on student interaction and less on administrative planning
Example Use Cases
K-12 Teachers
Transform district curriculum documents into ready-to-use daily lesson plans, complete with differentiation strategies, assessments, and supplementary materials.

Corporate Trainers
Convert training manuals into structured learning modules with activities, knowledge checks, and resources tailored to different learning styles.

Educational Publishers
Scale the creation of teacher materials by automatically generating lesson plans and assessments aligned with published curriculum.

Curriculum Developers
Test curriculum documents by seeing how they translate into practical classroom activities, identifying gaps and opportunities for improvement.

Dependencies
LessonCraftAI requires:

Python 3.10+: The system is built on Python 3.10 or higher
OpenAI API Key: Required for embedding generation and content creation
Libraries:
crewai: For agent-based workflow management
langchain/langchain-community: For document processing
langchain-openai: For OpenAI integration
chromadb: For vector storage and retrieval
pypdf: For PDF document parsing
python-dotenv: For environment variable management
Configuration Instructions
Setting Up Your Environment
Clone the repository:
bash
git clone https://github.com/yourusername/lessoncraftai.git
cd lessoncraftai
Set up environment:
bash
# Install UV (recommended)
pip install uv

# Install dependencies using UV
uv pip install -r requirements.txt
Configure API Keys: Create a .env file in the project root with your API key:
OPENAI_API_KEY=your_api_key_here
Customization Options
PDF Source: Replace the sample PDF in the data directory with your own curriculum document
Vector Store: Adjust chunk size and overlap in the vectorize_pdf.py tool to optimize for your document type
Lesson Structure: Modify activity templates in plan_lessons.py to match your preferred instructional format
Assessment Types: Customize assessment templates in design_assessments.py for your evaluation needs
Usage Examples
Process a Curriculum Document
bash
# Run using Python directly
python main.py

# Run using CrewAI CLI
crewai run
Example Output
LessonCraftAI generates structured output for each stage of the process:

Curriculum Vectorization:
Curriculum indexed successfully with 37 chunks from ./data/sample_curriculum.pdf
Topic Extraction:
json
[
  {
    "topic": "Photosynthesis",
    "objectives": [
      "Explain the process of photosynthesis",
      "Identify the reactants and products involved",
      "Describe the role of chlorophyll in capturing light energy"
    ]
  },
  {
    "topic": "Cellular Respiration",
    "objectives": [
      "Compare and contrast cellular respiration and photosynthesis",
      "Explain how energy is released from glucose during respiration",
      "Identify the stages of cellular respiration"
    ]
  }
]
Lesson Plans:
json
[
  {
    "topic": "Photosynthesis",
    "objectives": ["Explain the process of photosynthesis", "..."],
    "duration": "60 minutes",
    "materials_needed": ["Handouts", "Plant specimens", "Light sources"],
    "activities": [
      {
        "name": "Introduction",
        "duration": "10 minutes",
        "description": "Introduce the concept of photosynthesis through a brief demo"
      },
      "..."
    ]
  }
]
Contributing
Contributions to LessonCraftAI are welcome! Please see our CONTRIBUTING.md for guidelines.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Created by Dhruv@CloudBridgeusa.com for educators and learning professionals

