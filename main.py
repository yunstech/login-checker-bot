from fastapi import FastAPI
from redis import Redis
from rq import Queue
from pydantic import BaseModel

class CredentialRequest(BaseModel):
    username: str
    password: str
    product: str
    endpoint: str
    breach_id: int = None

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.post("/check_credential")
async def check_credential(credentials: CredentialRequest):
    redis_conn = Redis(host='localhost', port=6379)
    queue = Queue(connection=redis_conn)
    job = queue.enqueue('services.LoginService.loginCheck',
        credentials.username, 
        credentials.password, 
        credentials.product, 
        credentials.endpoint,
        credentials.breach_id
    )

    return {"job_id": job.get_id()}
