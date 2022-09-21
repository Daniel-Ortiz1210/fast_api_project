***Project Overview:***



**Tech Stack:**

anyio==3.6.1
bcrypt==4.0.0
cffi==1.15.1
click==8.1.3
cryptography==38.0.1
dnspython==2.2.1
ecdsa==0.18.0
email-validator==1.2.1
fastapi==0.83.0
h11==0.13.0
idna==3.4
passlib==1.7.4
pyasn1==0.4.8
pycparser==2.21
pydantic==1.10.2
PyMySQL==1.0.2
python-jose==3.3.0
python-multipart==0.0.5
rsa==4.9
six==1.16.0
sniffio==1.3.0
SQLAlchemy==1.4.41
starlette==0.19.1
typing_extensions==4.3.0
uvicorn==0.18.3

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
