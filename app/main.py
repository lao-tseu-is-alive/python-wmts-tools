import logging
import os
from typing import Annotated, Optional
from dotenv import load_dotenv

from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conlist
from starlette.responses import JSONResponse

from app.wms.wms import get_wms_params
from app.wmts.lausanneGrid import LausanneGrid
from app.wmts.utils import BBox

APP = "wmtsReader"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(APP)

load_dotenv()
app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # List of allowed methods
    allow_headers=["*"],  # List of allowed headers
)

class TileInfo(BaseModel):
    zoom: int
    col: int
    row: int
    wms_url: str
    bbox: conlist(float, min_length=4, max_length=4)


def get_wms_backend_url():
    wms_backend = os.getenv("WMS_BACKEND")
    if wms_backend is None:
        raise ValueError("WMS_BACKEND environment variable not set")
    return wms_backend

@app.get("/")
def read_root():
    return {"app": APP, "docs_url": "/docs", "redoc_url": "/redoc"}


@app.get("/tiles/{zoom}/{col}/{row}",
         responses={
             #200: {"description": "Returns a tile png image", "content": {"image/png": {}}},
             200: {"description": "Returns url of wms request"},
             400: {"description": "ValueError in one of the parameters"}
         },
         )
def read_tiles(
        zoom: Annotated[int, "Zoom level"],
        col: Annotated[int, "Tile Column"],
        row: Annotated[int, "Tile Row"],
        q: str | None = None
):
    ch_grid = LausanneGrid()
    layers = "osm_bdcad_couleur_msgroup,planville_cs_autres_msgroup,planville_cs_bati_pol_sout,planville_marquage_msgroup,planville_od_objets_msgroup,planville_arbres_goeland_msgroup,planville_cs_bati_msgroup,planville_od_labels_msgroup"
    try:
        bbox = ch_grid.get_tile_bbox(zoom, col, row)
        logger.debug(f"bbox={bbox}")
        params = get_wms_params(bbox, layers,20, ch_grid.get_tile_width(), ch_grid.get_tile_height())
        wms_url = f"{get_wms_backend_url()}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        logger.debug('Fetching wms image: %s?%s',        wms_url)
        return {"data": wms_url}
    except ValueError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Error: {error}")

@app.get("/getTileByXY/{zoom}/{x}/{y}",
            responses={
                200: {"description": "Returns col and row of the tile and url of wms request"},
                400: {"description": "ValueError in one of the parameters"}
            },
            )
def get_tile_info_by_xy(
        zoom: Annotated[int, "Zoom level"],
        x: Annotated[float, "X coordinate (SwissGrid LV95)"],
        y: Annotated[float, "Y coordinate (SwissGrid LV95)"],
        gutter: Optional[int] = 0
):
    ch_grid = LausanneGrid()
    layers = "osm_bdcad_couleur_msgroup,planville_cs_autres_msgroup,planville_cs_bati_pol_sout,planville_marquage_msgroup,planville_od_objets_msgroup,planville_arbres_goeland_msgroup,planville_cs_bati_msgroup,planville_od_labels_msgroup"
    try:
        col, row = ch_grid.get_tile(x, y, zoom)
        logger.debug(f"col={col}, row={row}")
        bbox = ch_grid.get_tile_bbox(zoom, col, row)
        logger.debug(f"bbox={bbox}")
        params = get_wms_params(bbox, layers,gutter, ch_grid.get_tile_width(), ch_grid.get_tile_height())
        wms_url = f"{get_wms_backend_url()}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        logger.debug('Fetching wms image: %s?%s',        wms_url)
        my_tile_info = TileInfo(zoom=zoom, col=col, row=row, wms_url=wms_url, bbox=bbox.bbox)
        json_my_tile_info = jsonable_encoder(my_tile_info)
        return JSONResponse(content=json_my_tile_info)
    except ValueError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Error: {error}")