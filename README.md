# fastapi-feedback-system

Basic FastAPI project structure:

```text
.
├── app
│   ├── api
│   │   └── routes
│   │       └── feedback.py
│   ├── models
│   ├── schemas
│   ├── services
│   └── main.py
└── tests
```

Install dependencies and run locally:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
