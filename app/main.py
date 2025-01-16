from fastapi import FastAPI, status, HTTPException
from app.wmts.swisstopogrid28 import SwissTopoGrid28

app = FastAPI()


@app.get("/")
def read_root():
    return {"docs": "World"}


@app.get("/tiles/{zoom}/{col}/{row}")
def read_tiles(zoom: int, col: int, row: int, q: str = None):
    ch_grid = SwissTopoGrid28()
    try:
        bbox = ch_grid.get_tile_bbox(zoom, col, row)
        return {"data": bbox}
    except ValueError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Error: {error}")
