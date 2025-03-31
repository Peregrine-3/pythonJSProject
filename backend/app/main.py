from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt
import pyodbc

serverName = 'IXP-829\\SQLEXPRESS'
databaseName = 'PythonAPI'

connectionString = (
    f'DRIVER=ODBC Driver 18 for SQL Server;'
    f'SERVER={serverName};'
    f'DATABASE={databaseName};'
    f'Trusted_Connection=yes;'
    f'Encrypt=no;'
)

try: 
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    print('connection successful')
except Exception as e:
    print(e)
    print('unsuccessful connection')


app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

rows = cursor.execute('select * from Authentications')

for row in rows:
    print(row)

@app.get('/hello')
def helloWorld():
    print('pinged')
    return {'message': 'Hello from fastApi'}

@app.post('/api/login')
def login(request: LoginRequest):
    password_bytes = request.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    hashed_password_string = hashed_password.decode('utf-8')

    print(f'password: {request.password} hashed pw string: {hashed_password_string} raw hashed password: {hashed_password}')

    print(f'{request.username} tried to log in with password {request.password}')
    return {'message': 'login attempt received.' + f'user {request.username} tried to log in with password {request.password} password hash {hashed_password_string}'}


