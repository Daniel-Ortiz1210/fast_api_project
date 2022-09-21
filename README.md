***Project Overview:***

Simple API to query, update, create and delete users connected to a MySQL database.

**Tech Stack:** 👨🏻‍💻

- bcrypt==4.0.0
- cryptography==38.0.1
- email-validator==1.2.1
- fastapi==0.83.0
- passlib==1.7.4
- pydantic==1.10.2
- PyMySQL==1.0.2
- python-jose==3.3.0
- python-multipart==0.0.5
- SQLAlchemy==1.4.41
- starlette==0.19.1
- uvicorn==0.18.3

**How To Run:**

MacOS 🖥

Inside this folder...

- Create a virtual environment: python3 -m venv _name_
- Activate virtual environment: source _name_/bin/activate
- Install packages: pip install -r requirements.txt
- Run server: uvicorn main:app --reload

Database config... 
- Download MySQL
- Create a DB named *users* hosted by localhost and your root user as the user.
- You could modify these defaults in *fast_api/config/db.py*

Once server is running...
- Visit the project [Docs](http://localhost:8000/docs)
- There you´ll find all the necesary documentation that you need to start making requests.
