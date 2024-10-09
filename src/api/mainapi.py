from fastapi import FastAPI
from api.views import get_logs, get_user_logs

app = FastAPI()

app.get("/logs")(get_logs)
app.get("/logs/{user_id}")(get_user_logs)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
