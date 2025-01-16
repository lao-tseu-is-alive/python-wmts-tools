import logging
import os
from typing import Annotated

from fastapi import FastAPI, status, HTTPException

from app.wms.wms import get_wms_params
from app.wmts.swisstopogrid28 import SwissTopoGrid28

APP = "wmtsReader"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(APP)

app = FastAPI()

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
             200: {"description": "Returns a tile png image", "content": {"image/png": {}}},
             400: {"description": "ValueError in one of the parameters"}
         },
         )
def read_tiles(
        zoom: Annotated[int, "Zoom level"],
        col: Annotated[int, "Tile Column"],
        row: Annotated[int, "Tile Row"],
        q: str | None = None
):
    ch_grid = SwissTopoGrid28()
    layers = "osm_bdcad_couleur_msgroup,planville_cs_autres_msgroup,planville_cs_bati_pol_sout,planville_marquage_msgroup,planville_od_objets_msgroup,planville_arbres_goeland_msgroup,planville_cs_bati_msgroup,planville_od_labels_msgroup"
    wms_request=f"https://carto.lausanne.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&cache_version=cc690bc896474be1bcacba64275d7b5d&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS={layers}&SERVERTYPE=mapserver&STYLES=&CRS=EPSG%3A2056&WIDTH=2247&HEIGHT=1389&BBOX=2534733.7499999986%2C1152061.2499999998%2C2540351.2499999986%2C1155533.7499999998"
    try:
        bbox = ch_grid.get_tile_bbox(zoom, col, row)
        logger.debug(f"bbox={bbox}")
        params = get_wms_params(bbox, 20, ch_grid.get_width(), ch_grid.get_height())
        logger.debug('Fetching wms image: %s?%s',        get_wms_backend_url(),
        '&'.join([f'{k}={v}' for k, v in params.items()])
                             )
        return {"data": bbox}
    except ValueError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Error: {error}")
