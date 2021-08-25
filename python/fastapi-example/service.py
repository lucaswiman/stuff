from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root(item: int):
    """
    This is a docstring.
    
    `item` is a variable.
    """
    return {"message": "Hello World"}