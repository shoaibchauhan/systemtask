# System Monitoring Application  

This project is a system monitoring application built using FastAPI, Django ORM, Pydantic, Uvicorn, Pytz, Requests, Psycopg, and PostgreSQL.  It monitors and logs data related to system processes.  

## Getting Started  

### Prerequisites  

*   Python 3.7+
*   django
*   fastapi
*   pydantic
*   uvicorn
*   PostgreSQL
*   psutil  
*   Git 
 

### Installation  

1.  **Clone the repository:**  

    ```bash  
    git clone https://github.com/shoaibchauhan/systemtask.git
    ```  

2.  **Create a virtual environment:**  

    ```bash  
    python3 -m venv .venv  # Or your preferred virtual environment creation method  
    source .venv/bin/activate  # Activate the virtual environment (Linux/macOS)  
    .venv\Scripts\activate  # Activate the virtual environment (Windows)  
    ```  

3.  **Install dependencies:(if needed)**  

    ```bash  
    pip install fastapi django uvicorn pydantic requests pytz psycopg  
    ```  

4.  **Configure the database:**  

    Update the `settings.py` file with your PostgreSQL database connection details (host, port, database name, username, password).  

5.  **Run database migrations:**  

    ```bash  
    python manage.py migrate  
    ```  

6.  **Start the server:**  

    ```bash  
    uvicorn app.main:app --reload  
    ```  
    The application will be available at `http://127.0.0.1:8000`.  

7.  **Run the monitoring script:**  

    ```bash  
    python system_monitoring.py  
    ```  
    This script continuously monitors and logs system process data.  

8.  **Test the API:**  

    Interact with the API using the Swagger UI at `http://127.0.0.1:8000/docs`.  


## Database Design Note  

For this project, a single table was used for simplicity during development.(becasue i have only one laptop and its an assignment )  For improved scalability and organization, separate tables for `system_name` and `username` are recommended for more efficient querying and data management in a production environment.  


## Technologies Used  

*   **FastAPI:**  API framework.  
*   **Django ORM:** Object-Relational Mapper.  
*   **Pydantic:** Data validation and parsing.  
*   **Uvicorn:** ASGI server.  
*   **Pytz:** Timezone support.  
*   **Requests:** HTTP library (if needed).  
*   **Psycopg:** PostgreSQL adapter.
*   **Psutils:** for background task management
*   **socket:** for API connection 