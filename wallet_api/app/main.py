from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Wallet API")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Wallet API"}