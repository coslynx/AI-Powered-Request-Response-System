<div class="hero-icon" align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
AI Powered Request Response System
</h1>
<h4 align="center">A Python backend application that serves as an AI wrapper, seamlessly connecting users to the power of OpenAI's language models.</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Framework-FastAPI-blue" alt="Framework used">
  <img src="https://img.shields.io/badge/Backend-Python-red" alt="Backend Language">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="Database used">
  <img src="https://img.shields.io/badge/LLMs-OpenAI-black" alt="LLMs used">
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/AI-Powered-Request-Response-System?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/AI-Powered-Request-Response-System?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/AI-Powered-Request-Response-System?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview
The repository contains a Minimum Viable Product (MVP) called "AI Powered Request Response System" that acts as a Python backend application, bridging the gap between human communication and advanced AI technologies. Users can send requests to the system via a defined API endpoint, which then processes them using the OpenAI API and returns a comprehensive response. The system is built with scalability, security, and user experience in mind, using technologies like FastAPI, SQLAlchemy, and PostgreSQL.

## 📦 Features
|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | The system utilizes a REST API architecture based on FastAPI for handling requests and responses. SQLAlchemy is used for database interaction with PostgreSQL. |
| 📄 | **Documentation**  | This README file provides a detailed overview of the MVP, its features, installation, usage, and deployment instructions.|
| 🔗 | **Dependencies**   | The project utilizes packages such as FastAPI, SQLAlchemy, psycopg2-binary, OpenAI, and Pydantic for API development, database interaction, and data validation. |
| 🧩 | **Modularity**     | The codebase is organized into modules for better organization and maintainability, with separate files for models, routers, and utilities. |
| 🧪 | **Testing**        | Includes unit tests using `pytest` to ensure the robustness and reliability of the codebase. |
| ⚡️  | **Performance**    | The backend is designed for efficient processing of user requests and returns responses promptly. Caching strategies are implemented for frequently asked questions. |
| 🔐 | **Security**       | The backend utilizes robust authentication and authorization protocols. Input validation and data sanitization are implemented to prevent security vulnerabilities. |
| 🔀 | **Version Control**| Utilizes Git for version control with a `startup.sh` script for managing the application startup process. |
| 🔌 | **Integrations**   | The backend seamlessly integrates with the OpenAI API, securely communicating with it to process user requests and retrieve responses. |
| 📶 | **Scalability**    | The system is designed for scalability with the use of PostgreSQL for data storage and efficient request handling techniques. |

## 📂 Structure
```text
├── main.py                # Application entry point
├── database.py            # Database setup and session management
├── models
│   └── models.py          # Database models
├── routers
│   └── requests.py        # API routes for handling user requests
├── utils
│   └── helpers.py         # Utility functions
├── services
│   └── openai_service.py  # OpenAI API interaction logic
└── tests
    └── test_main.py      # Unit tests for the main application logic
```

## 💻 Installation
### 🔧 Prerequisites
- Python 3.9+
- PostgreSQL 14+
- Docker (optional, for containerized deployment)

### 🚀 Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/coslynx/AI-Powered-Request-Response-System.git
   cd AI-Powered-Request-Response-System
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the database:**
   - Create a PostgreSQL database.
   - Update the `DATABASE_URL` in the `.env` file with your database connection string.
4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Replace `sk-YOUR_API_KEY_HERE` with your actual OpenAI API key.

## 🏗️ Usage
### 🏃‍♂️ Running the MVP
1. **Start the application:**
   ```bash
   python main.py
   ```

### ⚙️ Configuration
- The `.env` file contains environment variables like the OpenAI API key and database connection string.

### 📚 Examples
- **Sending a request:**
    ```bash
    curl -X POST http://localhost:8000/requests -H "Content-Type: application/json" -d '{"text": "What is the meaning of life?"}'
    ```
- **Response:**
    ```json
    {
        "id": 1,
        "text": "What is the meaning of life?",
        "response": "The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one definitive answer, and the meaning of life may be different for each individual. Some people find meaning in their relationships, their work, their faith, or their hobbies. Ultimately, the meaning of life is up to each individual to decide.",
        "created_at": "2023-12-18T15:10:10.123456Z"
    }
    ```

## 🌐 Hosting
### 🚀 Deployment Instructions
1. **Build a Docker image (optional):**
   ```bash
   docker build -t ai-request-response-system:latest .
   ```
2. **Run the Docker container (optional):**
   ```bash
   docker run -p 8000:8000 ai-request-response-system:latest
   ```
3. **Deploy to a cloud platform (e.g., Heroku):**
    - Create a new Heroku app:
    ```bash
    heroku create ai-request-response-system-production
    ```
    - Set environment variables:
    ```bash
    heroku config:set OPENAI_API_KEY=your_openai_api_key
    heroku config:set DATABASE_URL=your_database_url
    ```
    - Deploy the code:
    ```bash
    git push heroku main
    ```

### 🔑 Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: Your PostgreSQL database connection string (e.g., `postgresql://user:password@host:port/database`)

## 📜 API Documentation
### 🔍 Endpoints
- **POST /requests**
    - Description: Create a new request to the OpenAI API.
    - Request Body: 
        ```json
        {
            "text": "Your request here"
        }
        ```
    - Response:
        ```json
        {
            "id": 1,
            "text": "Your request here",
            "response": "The response from OpenAI",
            "created_at": "2023-12-18T15:10:10.123456Z"
        }
        ```

## 📜 License & Attribution

### 📄 License
This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

### 🤖 AI-Generated MVP
This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).

No human was directly involved in the coding process of the repository: AI-Powered-Request-Response-System

### 📞 Contact
For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
- Website: [CosLynx.com](https://coslynx.com)
- Twitter: [@CosLynxAI](https://x.com/CosLynxAI)

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
  <img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
  <img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
  <img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>