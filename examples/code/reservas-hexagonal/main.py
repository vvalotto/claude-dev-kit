"""Punto de entrada de la app Reservas (BC Reservas — hexagonal-ddd-bc)."""

from fastapi import FastAPI

from reservas.api.router import router as reservas_router

app = FastAPI(title="Reservas API", version="1.0.0")
app.include_router(reservas_router)


@app.get("/")
def health() -> dict:
    """Endpoint de salud, usado también como precondición BDD."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
