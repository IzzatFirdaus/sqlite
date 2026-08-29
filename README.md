# SQLite (with FastAPI)

A lightweight RESTful API built with Python, FastAPI, and SQLModel designed to demonstrate persistent data storage, ORM schema design, and full CRUD operations using an SQLite database.

## Features
- **SQLModel ORM:** Unified data modeling combining Pydantic type validation with SQLAlchemy database mappings.
- **SQLite Database:** Persistent local file-based storage across server restarts.
- **Dependency Injection:** Safe database session management per request via FastAPI's `Depends`.
- **Interactive OpenAPI Documentation:** Live endpoint testing and API contract visualization via Swagger UI at `/docs`.

## Database Schema & Endpoints

### Data Model (`Item`)
- `id`: Primary key (Integer, Auto-incremented)
- `name`: String (Indexed)
- `description`: String (Optional)
- `price`: Float
- `is_available`: Boolean (Default: `True`)

### REST Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/items/` | Create a new item record in the SQLite database |
| `GET` | `/items/` | Retrieve all items from the database |
| `GET` | `/items/{item_id}` | Fetch a specific item by its primary key ID |
| `DELETE` | `/items/{item_id}` | Delete an item record by ID |

## Getting Started

### Prerequisites
- Python 3.10+ installed on your machine.

### Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/IzzatFirdaus/sqlite.git](https://github.com/IzzatFirdaus/sqlite.git)
cd sqlite
```

2. **Create and activate a virtual environment:**
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```


3. **Install dependencies:**
```bash
pip install -r requirements.txt
```


4. **Run the development server:**
```bash
fastapi dev main.py
```


5. **Test the API:**
Open `http://127.0.0.1:8000/docs` in your web browser to interactively execute queries and verify database persistence.