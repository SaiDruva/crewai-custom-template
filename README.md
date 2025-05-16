# LessonCraftAI

## Transform Curriculum Documents into Comprehensive Lesson Plans

LessonCraftAI is an AI-powered system that converts curriculum documents into complete, classroom-ready lesson plans. Using advanced NLP and vector embeddings, this tool analyzes curriculum PDFs, extracts key topics and learning objectives, then generates structured lesson plans with timed activities, assessments, and supplementary resources.

## What Problem Does LessonCraftAI Solve?

Teachers and educational content creators often spend countless hours developing lesson plans from curriculum standards. LessonCraftAI dramatically reduces this workload, allowing educators to:

- Process curriculum documents in seconds instead of hours
- Maintain perfect alignment between curriculum standards and classroom activities
- Generate consistent, high-quality lesson materials at scale
- Focus more time on student interaction and less on administrative planning

## Enterprise Value

For educational institutions and corporate training departments, LessonCraftAI offers significant ROI:

- **Time Savings**: Reduce curriculum implementation planning by up to 75%
- **Standards Compliance**: Ensure all lessons precisely align with required standards and objectives
- **Consistency**: Maintain teaching quality across multiple instructors and locations
- **Scalability**: Rapidly adapt to curriculum changes without manual rework
- **Resource Optimization**: Free up instructional designers and subject matter experts for higher-value tasks

## Example Use Cases

### K-12 School Districts
Transform district curriculum documents into ready-to-use daily lesson plans, complete with differentiation strategies, assessments, and supplementary materials.

### Corporate Training Departments
Convert training manuals into structured learning modules with activities, knowledge checks, and resources tailored to different learning styles.

### Educational Publishers
Scale the creation of teacher materials by automatically generating lesson plans and assessments aligned with published curriculum.

### EdTech Companies
Integrate LessonCraftAI into learning management systems to provide real-time lesson planning services to educators.

## Special LLM Requirements

LessonCraftAI performs best with:

- **OpenAI GPT-4** or equivalent model capabilities for high-quality educational content generation
- **Minimum context window of 16K tokens** to process substantial curriculum documents
- **Vector embedding model**: text-embedding-ada-002 or equivalent for accurate curriculum analysis

## Dependencies

LessonCraftAI requires:

- **Python 3.10+**: The system is built on Python 3.10 or higher
- **OpenAI API Key**: Required for embedding generation and content creation
- **Libraries**:
  - crewai==0.120.1: For agent-based workflow management
  - langchain>=0.1.0: For document processing
  - langchain-community>=0.0.13: For document loading
  - langchain-openai>=0.0.2: For OpenAI integration
  - openai>=1.1.0: For API access
  - chromadb>=0.4.22: For vector storage and retrieval
  - pypdf>=3.17.0: For PDF document parsing
  - python-dotenv>=1.0.0: For environment variable management

## Configuration and Customization

### Setting Up Your Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/lessoncraftai.git
   cd lessoncraftai
   ```

2. **Set up environment**:
   ```bash
   # Install UV (recommended)
   pip install uv
   
   # Install dependencies using UV
   uv pip install -r requirements.txt
   ```

3. **Configure API Keys**:
   Create a `.env` file in the project root with your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Customization Options

LessonCraftAI offers multiple customization points for tailoring to your specific needs:

#### PDF Source and Processing
- **Custom Curriculum**: Replace `./data/sample_curriculum.pdf` with your own PDF
- **Vectorization Parameters**: In `tools/vectorize_pdf.py`, adjust:
  ```python
  # Modify chunking parameters for different document types
  chunk_size=500  # Larger for more context, smaller for more precision
  chunk_overlap=50  # Increase for better context preservation
  ```

#### Lesson Plan Structure
- **Template Modification**: In `tools/plan_lessons.py`, customize the lesson template:
  ```python
  # Add or modify lesson components
  lesson_plan = {
      "topic": topic_name,
      "objectives": objectives,
      "duration": "60 minutes",  # Adjust default duration
      "materials_needed": ["Handouts", "Presentation slides", "Your custom materials"],
      # Add custom fields like "grade_level" or "prerequisite_knowledge"
  }
  ```

#### Assessment Configuration
- **Question Types**: In `tools/design_assessments.py`, adjust assessment types:
  ```python
  # Add or modify assessment types
  assessment = {
      "formative_assessment": {
          # Add your custom assessment types
          "exit_ticket": {...},
          "peer_evaluation": {...}  # Add custom assessment types
      }
  }
  ```

#### Agent Behavior
- **Agent Parameters**: Adjust agent temperature and behavior in `crew.py`:
  ```python
  # Increase temperature for more creative lesson plans
  # Decrease for more conservative, standards-focused plans
  curriculum_ingestor = CurriculumIngestorAgent(
      pdf_path=curriculum_path,
      persist_dir=persist_dir,
      temperature=0.2  # Adjust as needed
  ).build()
  ```

## Usage Examples

### Process a Curriculum Document

```bash
# Run using Python directly
python main.py

# Run using CrewAI CLI
crewai run
```

### Programmatic Usage

```python
from lessoncraftai.crew import crew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Run the crew
result = crew.kickoff()

# Process the results
import json
lesson_plans = json.loads(result)
for lesson in lesson_plans:
    print(f"Created lesson plan for: {lesson['topic']}")
    # Further processing as needed
```

### Example Output

LessonCraftAI generates structured output for each stage of the process:

1. **Curriculum Vectorization**:
   ```
   Curriculum indexed successfully with 37 chunks from ./data/sample_curriculum.pdf
   ```

2. **Topic Extraction**:
   ```json
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
   ```

3. **Lesson Plans**:
   ```json
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
   ```

## Performance and Scaling

LessonCraftAI has been tested with:
- Curriculum documents up to 100 pages
- Processing time of approximately 2-5 minutes for a 50-page document
- Generation of up to 25 lesson plans from a single curriculum

For extremely large documents (>100 pages), consider splitting them into smaller sections for optimal performance.

## Contributing

Contributions to LessonCraftAI are welcome! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Created by [Your Name/Organization] for educational excellence at scale*
