ScamGuardian

AI-Powered Scam Message Detection using RAG

ScamGuardian is an AI-powered web application that analyzes suspicious messages and identifies potential scams using Retrieval-Augmented Generation (RAG).

The application retrieves relevant information from a scam knowledge base and uses a Large Language Model (LLM) to analyze the user's message, determine its scam type and risk level, and provide safety recommendations.

Project Objective

Online scams such as phishing, fake offers, fraudulent payment requests, and impersonation messages are becoming increasingly common.

ScamGuardian aims to help users understand whether a suspicious message may be a scam and what actions they should or should not take.

Features

- Analyze suspicious messages
- AI-powered scam detection
- Retrieval-Augmented Generation (RAG)
- Knowledge-base retrieval using vector search
- Risk classification into Low, Medium, and High
- Scam type identification
- Explanation of why a message is suspicious
- Recommended actions
- Actions users should avoid
- Display the knowledge-base sources used for analysis
- Interactive Streamlit web interface

Architecture

User Message
      |
      v
Streamlit Interface
      |
      v
Hugging Face Embeddings
all-MiniLM-L6-v2
      |
      v
ChromaDB Vector Database
      |
      v
Retrieve Top 3 Relevant Chunks
      |
      v
RAG Context
Knowledge Base
      |
      v
Groq LLM
GPT-OSS-20B
      |
      v
ScamGuardian Analysis
      |
      +------------------+
      |                  |
      v                  v
  Scam Type          Risk Level
                         |
                         v
                  Safety Guidance

How It Works

1. Knowledge Base

Scam-related information is stored as ".txt" files inside the "policy_data" folder.

policy_data/
├── scam_information.txt
├── phishing.txt
└── other_policy_files.txt

2. Document Loading

The application loads the knowledge-base files using LangChain's "DirectoryLoader" and "TextLoader".

3. Text Splitting

The documents are divided into smaller chunks using "RecursiveCharacterTextSplitter".

Chunk Size    : 500
Chunk Overlap : 50

4. Embedding Generation

The project uses the Hugging Face embedding model:

all-MiniLM-L6-v2

The text chunks are converted into vector representations called embeddings.

5. Vector Database

The embeddings are stored in ChromaDB.

When a user enters a suspicious message, the system retrieves the top 3 relevant knowledge-base chunks.

6. RAG and LLM Analysis

The retrieved information is added to a prompt and sent to the Groq-hosted LLM.

The LLM analyzes the user's message using the retrieved knowledge.

7. Result Generation

ScamGuardian provides:

- Scam Type
- Risk Level
- Reason for the classification
- What the user should do
- What the user should not do

Technologies Used

Technology| Purpose
Python| Core programming language
Streamlit| Web application interface
LangChain| RAG application framework
Hugging Face| Text embedding model
all-MiniLM-L6-v2| Text embeddings
ChromaDB| Vector database
Groq| LLM inference
GPT-OSS-20B| Language model
Sentence Transformers| Embedding support
Git and GitHub| Version control

Project Structure

ScamGuardian/
│
├── app.py
│
├── policy_data/
│   └── *.txt
│
├── requirements.txt
│
└── README.md

Installation

1. Clone the Repository

git clone https://github.com/Mythilikalidhasan/ScamGuardian.git

2. Navigate to the Project

cd ScamGuardian

3. Create a Virtual Environment

python -m venv venv

For Windows:

venv\Scripts\activate

For Linux/macOS:

source venv/bin/activate

4. Install Dependencies

pip install -r requirements.txt

API Key Configuration

ScamGuardian uses the Groq API.

Create the following file:

.streamlit/
└── secrets.toml

Add your Groq API key:

GROQ_API_KEY = "your_groq_api_key"

Do not upload your API key or "secrets.toml" file to GitHub.

Run the Application

Run the following command:

streamlit run app.py

The application will open in your browser.

Example

Input

Congratulations! You have won ₹25,00,000.
Click this link and pay ₹500 processing fee to claim your prize.

Output

SCAM TYPE: Prize / Lottery Scam

RISK LEVEL: High

WHY IS IT A SCAM:
The message promises a large prize and asks the user
to pay a processing fee. This is a common warning sign
of fraudulent prize messages.

WHAT TO DO:
- Do not make the payment.
- Verify the offer through an official source.
- Report the suspicious message.

WHAT NOT TO DO:
- Do not click suspicious links.
- Do not share personal information.
- Do not send money.

Screenshots

Add screenshots of the application here.

![ScamGuardian Home](screenshots/home.png)

![ScamGuardian Result](screenshots/high-risk-result.png)

![Knowledge Sources](screenshots/knowledge-sources.png)

Security

ScamGuardian is designed as an informational scam-detection tool.

Users should independently verify important messages through official sources, especially before making payments or sharing sensitive information.

API keys and other secrets should never be committed to the GitHub repository.

Future Enhancements

- SMS and WhatsApp message analysis
- Suspicious URL detection
- Multilingual scam detection
- Scam analytics dashboard
- Email scam detection
- Real-time scam detection
- Improved retrieval and detection accuracy
- Cloud deployment
- Mobile-friendly interface

Key Concepts Demonstrated

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Vector databases
- Text embeddings
- Semantic search
- Document chunking
- Prompt engineering
- LangChain
- Streamlit
- AI-powered text analysis

Author

Mythili Kalidasan

B.Sc. Computer Science — Artificial Intelligence

"GitHub" (https://github.com/Mythilikalidhasan)

Project Repository

"ScamGuardian" (https://github.com/Mythilikalidhasan/ScamGuardian)
