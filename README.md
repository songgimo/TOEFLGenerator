# TOEFLGenerator

## 📖 Overview

TOEFLGenerator is a system of AI agents designed to automatically create complete and authentic TOEFL iBT Reading and Listening tasks. Given a specific academic topic, the system generates a university-level passage and a corresponding set of 10-question TOEFL-style comprehension questions, complete with an answer key.

The project leverages Large Language Models (LLMs) through a modular architecture, making it easy to extend and refine. It includes separate agents for generating passages and questions, which are orchestrated by a main controller. This provides a seamless experience from topic input to the final task output.

## ✨ Key Features

  * **📚 Authentic Passage Generation**: Creates high-quality, TOEFL-style academic reading passages (650-750 words) on a wide range of subjects.
  * **📝 Comprehensive Question Sets**: Generates a full set of 10 TOEFL Reading questions, covering all major types (Factual, Negative Factual, Inference, Rhetorical Purpose, Vocabulary, Sentence Simplification, Insert Text, and Prose Summary).
  * **🤖 Modular Agent-Based Architecture**: Built with distinct, swappable agents for different tasks (e.g., passage generation, question generation), making the system flexible and scalable.
  * **💡 Few-Shot Prompting**: Utilizes few-shot examples to ensure the generated content closely matches the style, tone, and complexity of official TOEFL materials.
  * **💻 Dual Interfaces**: Can be run via a simple Command-Line Interface (CLI) or a user-friendly web interface built with Streamlit.
  * **🧪 Automated Testing**: Includes a suite of tests to validate the functionality of each agent and ensure reliable output.
  * **🤔 "Thought Process" Generation**: A unique feature where helper agents can generate a plausible step-by-step "thought process" that a human expert might follow to create the passages and questions, providing transparency and aiding in prompt refinement.

## 📂 Project Structure

```
TOEFLGenerator/
├── agents/                 # Core AI agent modules
│   ├── reading_passage.py
│   ├── reading_question.py
│   └── thought_process.py
├── prompts/                # Prompt templates and few-shot examples
│   ├── reading/
│   │   ├── passage_examples/
│   │   ├── question_examples/
│   │   └── ...
│   └── listening/
├── tests/                  # Unit and integration tests for agents
│   ├── reading_passage_test.py
│   └── reading_question_test.py
├── config.py               # Pydantic models and configuration
├── llm_client.py           # LLM interaction layer
├── requirements.txt        # Project dependencies
├── run_cli.py              # Entry point for the CLI application
├── run_web.py              # Entry point for the Streamlit web application
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

  * Python 3.9+
  * An environment variable `GOOGLE_API_KEY` with a valid Google AI API key.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd TOEFLGenerator
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the project root and add your Google API key:

    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

### Usage

You can interact with TOEFLGenerator through either the command line or a web interface.

#### CLI

To run the application in your terminal, use the following command:

```bash
python run_cli.py
```

You will be prompted to choose a task (`reading` or `listening`) and then to enter an academic topic. If you enter 'random' or leave it blank, a random topic will be used.

#### Web Interface

To launch the Streamlit web application, run:

```bash
streamlit run run_web.py
```

This will open a new tab in your web browser with an interactive interface where you can input a topic and generate TOEFL tasks.

## 🤖 The Agents

The system is powered by a cluster of specialized agents:

  * **ReadingPassageAgent**: Takes an academic topic as input and generates a TOEFL-style reading passage.
  * **ReadingQuestionAgent**: Analyzes the generated passage and creates a structured set of 10 comprehension questions based on it.
  * **QuestionThoughtProcessAgent**: A helper agent that takes a passage and its corresponding questions to reverse-engineer and generate the "thought process" an expert might have used to create the questions.
  * **PassageThoughtProcessAgent**: A similar helper agent that generates the likely thought process for creating the passage itself from a topic.

## 🧪 Running Tests

To ensure all components are working as expected, you can run the provided tests. Each test file can be run individually:

```bash
# Test the passage generation agent
python -m tests.reading_passage_test

# Test the question generation agent
python -m tests.reading_question_test

# Test the thought process generation agent
python -m tests.thought_process_test
```

## 🔮 Future Enhancements

  * **Listening Task Generation**: Implementing agents to generate audio scripts for TOEFL Listening tasks, including conversations and lectures.
  * **Difficulty Control**: Adding a parameter (e.g., easy, medium, hard) to adjust the complexity of the generated passages and questions.
  * **Caching**: Implementing a caching mechanism to store and retrieve previously generated tasks for the same topic, saving API costs.
  * **RAG Integration**: Exploring Retrieval-Augmented Generation (RAG) to ground the generated content in specific source documents for higher factual accuracy.