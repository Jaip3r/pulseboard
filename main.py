from fastapi import FastAPI

# Punto de interacción principal para crear nuestra aplicación
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hola Mundo!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "hostname": "localhost"}
