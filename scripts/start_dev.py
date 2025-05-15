import uvicorn


def main():

    uvicorn.run(
        "src.main:api",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
