if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="localhost", port=1234, reload=True)
