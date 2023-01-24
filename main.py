""" Main module """

from typing import Callable, Optional, Tuple

from fastapi import FastAPI

import scraper

ACTIONS: dict = {
    "BCV": scraper.get_bcv_rate,
    "PARALELO": scraper.get_paralelo_rate,
}

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    """Root endpoint"""
    return {"message": "Hello world!"}


@app.get("/items")
def read_items() -> dict:
    """Return available items"""
    return {"items": tuple(ACTIONS.keys())}


@app.get("/item/{item}")
def get_item(item: str) -> dict:
    """Get value for a given item"""
    if item not in ACTIONS:
        return {"error": "Invalid item."}
    return {"name": item, "value": ACTIONS[item]()}
