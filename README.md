# CommerceCopilot 🛍️
### AI-Powered Shopping & Customer Support Assistant

CommerceCopilot is an AI-powered conversational shopping and customer-support assistant that combines **Retrieval-Augmented Generation (RAG), semantic search, LLM-based tool calling, and conversational memory** to handle e-commerce queries intelligently.

Built using Python, Streamlit, and Groq, the application enables customers to discover products, retrieve company policy information, check order details, and interact with an AI assistant through a conversational interface.

Instead of relying entirely on an LLM's pretrained knowledge, CommerceCopilot integrates a custom knowledge base and structured business data to generate context-aware responses.

---

## ✨ Key Features

- **Retrieval-Augmented Generation (RAG):** Answers customer questions using information retrieved from a custom e-commerce knowledge base.
- **Semantic Search:** Uses Sentence Transformers and `all-MiniLM-L6-v2` to generate text embeddings and retrieve semantically relevant information.
- **Intelligent Tool Calling:** Selects and executes predefined Python functions when queries require structured data.
- **Product Discovery:** Searches and filters a structured product catalog.
- **Order Information:** Retrieves order-related information from structured datasets.
- **Catalog Insights:** Handles queries involving product availability and catalog information.
- **Conversational Memory:** Maintains context across multiple messages within a conversation.
- **Chat History:** Uses SQLite to store conversation messages locally.
- **Domain Restriction:** Handles shopping and customer-support-related queries while restricting unrelated requests.
- **Interactive Chat Interface:** Provides a conversational frontend using Streamlit.

---

## 🏗️ System Architecture

CommerceCopilot follows a modular architecture that separates user interaction, AI processing, knowledge retrieval, structured tool execution, and conversation storage.

### 1. Application Flowchart

The following flowchart illustrates the complete query-processing workflow, from user input to response generation.

```mermaid
flowchart TD
    A(["User submits a query"]) --> B["Streamlit Frontend"]
    B --> C["AI Assistant"]
    C --> D[("SQLite Conversation Memory")]
    D --> E{"Determine Query Type"}

    E -->|"Knowledge Question"| F["RAG Pipeline"]
    E -->|"Structured Query"| G["Tool Calling"]
    E -->|"General Conversation"| H["LLM Response"]

    F --> I["Semantic Search"]
    I --> J[("Knowledge Base")]
    J --> K["Retrieve Relevant Context"]

    G --> L{"Select Appropriate Tool"}
    L -->|"Product Query"| M["Product Catalog"]
    L -->|"Order Query"| N["Order Dataset"]
    L -->|"Catalog Query"| O["Catalog Functions"]

    M --> P["Tool Execution Result"]
    N --> P
    O --> P

    K --> Q["Context-Aware Response Generation"]
    P --> Q
    H --> Q

    Q --> R["Save Conversation History"]
    R --> S["Streamlit Displays Response"]
    S --> T(["User receives answer"])
```

### 2. RAG Pipeline

CommerceCopilot uses a custom knowledge base containing e-commerce information, including:

- Return policies
- Delivery policies
- Frequently asked questions

The embedding model converts text into numerical representations, allowing the system to retrieve relevant information based on semantic similarity.

```mermaid
flowchart TD
    A(["Knowledge Base Documents"]) --> B["Document Processing"]
    B --> C["Generate Text Embeddings"]
    C --> D[("Embedding Model<br/>all-MiniLM-L6-v2")]
    D --> E["Indexed Knowledge"]

    F(["User Query"]) --> G["Query Embedding"]
    G --> D
    D --> H["Semantic Similarity Search"]
    E --> H

    H --> I["Retrieve Relevant Information"]
    I --> J["Construct Context"]
    J --> K["Groq LLM"]
    K --> L(["Context-Grounded Response"])
```

### 3. Tool Calling Workflow

Not every customer query requires document retrieval. For structured queries, the assistant invokes predefined Python functions to access the appropriate data source.

```mermaid
flowchart TD
    A(["User submits structured query"]) --> B["AI Assistant"]
    B --> C{"Identify Required Tool"}

    C -->|"Product Search"| D["Product Search Function"]
    C -->|"Order Lookup"| E["Order Lookup Function"]
    C -->|"Catalog Information"| F["Catalog Query Function"]

    D --> G[("Products Dataset")]
    E --> H[("Orders Dataset")]
    F --> I["Catalog Data Processing"]

    G --> J["Return Tool Result"]
    H --> J
    I --> J

    J --> K["Groq LLM Processes Result"]
    K --> L(["Natural Language Response"])
```

---

## 🧠 AI Models and Technologies

| Component | Technology | Purpose |
|---|---|---|
| LLM Provider | Groq | Natural-language understanding and response generation |
| Embedding Model | `all-MiniLM-L6-v2` | Semantic text embeddings |
| Embedding Framework | Sentence Transformers | Embedding generation |
| Vector Database | ChromaDB | Storing and retrieving document embeddings |
| Retrieval Approach | RAG | Knowledge-grounded question answering |

### Application Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Interactive frontend and application runtime |
| SQLite | Local conversation storage |
| Pandas | Structured data processing |
| Mermaid | Architecture and workflow diagrams |

---

## 💬 Conversational Memory

CommerceCopilot supports multi-turn conversations by maintaining contextual information from previous messages.

**Example interaction:**

**User:** Show me some headphones.

**Assistant:** Displays matching products from the product catalog.

**User:** Which one is the cheapest?

**Assistant:** Uses the previous conversational context to identify the cheapest option.

Conversation messages are stored using SQLite. Local conversation history can persist across application restarts, while cloud-hosted storage may reset depending on the hosting environment.

---

## 📁 Project Structure

```text
CommerceCopilot/
│
├── frontend/
│   └── app.py
│
├── src/
│   ├── memory/
│   │   └── chat_memory.py
│   │
│   ├── rag/
│   │   ├── rag_pipeline.py
│   │   └── semantic_search.py
│   │
│   ├── tools/
│   │   ├── tool_calling.py
│   │   └── tools.py
│   │
│   └── prepare_data.py
│
├── data/
│   ├── products.csv
│   ├── orders.csv
│   │
│   └── knowledge_base/
│       ├── delivery_policy.md
│       ├── faq.md
│       └── return_policy.md
│
├── test_tool_calling.py
├── test_tools.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 Installation and Setup

### Prerequisites

- Python 3.10 or later
- Groq API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/funcoderror/CommerceCopilot.git

cd CommerceCopilot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Groq API Credentials

Obtain an API key from [Groq Console](https://console.groq.com/).

Set the `GROQ_API_KEY` environment variable or configure it through the application's secrets mechanism.

Keep API credentials private. Never commit API keys to GitHub.

### 5. Prepare the Data

Ensure that the product catalog, order dataset, and knowledge-base documents are available in the `data/` directory.

The RAG pipeline automatically initializes the ChromaDB knowledge base from the Markdown documents when required.

### 6. Run the Application

```bash
streamlit run frontend/app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

---

## 🧪 Testing

The project includes tests for structured tools and tool-calling functionality.

Execute the test suite using:

```bash
python -m pytest test_tools.py test_tool_calling.py
```

### Tested Functionality

- Product search and structured catalog queries.
- Order-related tool execution.
- Retrieval-based responses using the knowledge base.
- Handling of unrelated queries.
- Tool selection based on user intent.
- Multi-turn conversational context.
- Conversation history management.
- Streamlit chat interface.

---

## 📸 Application Screenshots

Screenshots of the working application can be added here.

Suggested screenshots:

1. Main Streamlit chat interface.
2. Product search response.
3. RAG-based return or delivery policy response.
4. Order status lookup.
5. Multi-turn conversation demonstrating conversational memory.

---

## ⚠️ Limitations

- Product and order information is based on locally available datasets rather than a live e-commerce database.
- The knowledge base contains a limited collection of sample company documents.
- Response accuracy depends on the quality of retrieved information and the underlying LLM.
- The application is a functional prototype and does not implement a complete e-commerce checkout or payment system.
- Cloud-hosted local storage may not provide permanent persistence across application restarts.
- External production integrations and live inventory synchronization are not currently included.

---

## 🔮 Future Improvements

- Integration with live product inventory and order-management systems.
- Improved retrieval quality through experimentation with embedding models and retrieval strategies.
- More advanced product recommendation capabilities.
- User authentication and individual customer sessions.
- More reliable persistent storage and production monitoring.
- Expanded evaluation using a larger collection of representative customer queries.

---

## 🎯 Project Objective

CommerceCopilot demonstrates the practical integration of **Retrieval-Augmented Generation, semantic search, LLM-based tool calling, and conversational memory** into an intelligent e-commerce assistant.

The project explores how LLM capabilities can be combined with structured business data and domain-specific knowledge to address practical shopping and customer-support requirements.

---

## 👨‍💻 Author

**Daksh Jha**

GitHub: [@funcoderror](https://github.com/funcoderror)

Project Repository: [CommerceCopilot](https://github.com/funcoderror/CommerceCopilot)

---

*CommerceCopilot — Making conversational commerce smarter with AI.*
