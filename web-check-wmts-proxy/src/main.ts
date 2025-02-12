import './css/normalize.css'
import './css/skeleton.css'
import './css/style.css'
import logo from '/logo.svg'
import {APP, APP_URL, BACKEND_URL, BUILD_DATE, defaultAxiosTimeout, getLog, VERSION} from "./config";
import {
    baseLayerType,
    Coordinate2D,
    createLausanneMap,
    drawBBox,
    PolygonWithVerticesStyleOptions,
    redrawMarker
} from "./mapLausanne.ts";
import axios from "axios";

const log = getLog(APP, 4, 2);
const placeStFrancoisM95: Coordinate2D = [2538202, 1152364];
const defaultZoom = 6
const posCenterX = 2538202;
const posCenterY = 1152364;
const myPointLayerName = "GoelandPointLayer";
const myBBoxLayerName = "GoelandBBoxLayer";
const defaultBaseLayer: baseLayerType = "fonds_geo_osm_bdcad_couleur";
const getBaseTileUrl = "https://tilesmn95.lausanne.ch/tiles/1.0.0"
const getTileUrl = (layer: baseLayerType, z: number, row: number, col: number) => `/${layer}/default/2021/swissgrid_05/${z}/${row}/${col}.png`

interface tileInfo {
    "zoom": number,
    "col": number,
    "row": number,
    "wms_url": string,
    "bbox": [number, number, number, number],
}

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
<div class="container">
    <section class="header">
        <a href="${APP_URL}" target="_blank" class="u-pull-left">
            <img src="${logo}" class="logo" alt="${APP} logo"/>
        </a>
        <h6>${APP}</h6>
    </section>
    <div class="row">
        <form>
            <div class="six columns">
                <div class="row">
                    <div class="three columns">
                        <label for="xCoordinate">Coordinate X</label>
                        <input class="u-full-width" type="number" placeholder="x coordinate" id="xCoordinate"
                               value="${posCenterX}">
                    </div>
                    <div class="three columns">
                        <label for="yCoordinate">Coordinate Y</label>
                        <input class="u-full-width" type="number" placeholder="y coordinate" id="yCoordinate"
                               value="${posCenterY}">
                    </div>
                    <div class="two columns">
                        <label for="zoomMap">zoom</label>
                        <select class="u-full-width" id="zoomMap">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4" selected>4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                            <option value="8">8</option>
                            <option value="9">9</option>
                        </select>
                    </div>
                    <div class="four columns">
                        <label for="baseLayer">layer</label>
                        <select class="u-full-width" id="baseLayer">
                            <option value="orthophotos_ortho_lidar_2016">orthophotos_ortho_lidar_2016</option>
                            <option value="fonds_geo_osm_bdcad_gris">fonds_geo_osm_bdcad_gris</option>
                            <option value="fonds_geo_osm_bdcad_couleur">fonds_geo_osm_bdcad_couleur</option>
                        </select>
                    </div>
                    <div class="row">
                        <div class="twelve columns">
                            <label for="debugMsg">Message</label>
                            <textarea 
                                class="u-full-width debug" 
                                placeholder="debug messages will appear her …"
                                rows="7"
                                id="debugMsg">
                            </textarea>
                            <input class="button-primary" type="button" value="Hide Map">
                        </div>
                    </div>
                </div>
            </div>
        </form>
        <div class="six columns">
            <div id="map" class="map"></div>
        </div>
    </div>
    <div class="row">
        <div class="six columns">
            <div id="tile-url" class="url-wmts u-pull-right "></div>
        </div>
        <div class="six columns">
            <div id="wms-url" class="url-wmts u-pull-left"></div>
        </div>
    </div>
    <div class="row">
        <div class="six columns">
            <div id="tile-image" class="image-wmts u-pull-right "></div>
        </div>
        <div class="six columns">
            <div id="wms-image" class="image-wmts u-pull-left"></div>
        </div>
    </div>
</div>  
`

const inputX = document.querySelector<HTMLInputElement>('#xCoordinate')!;
const inputY = document.querySelector<HTMLInputElement>('#yCoordinate')!;
const inputZoom = document.querySelector<HTMLSelectElement>('#zoomMap')!;
const inputBaseLayer = document.querySelector<HTMLSelectElement>('#baseLayer')!;
const debugMsg = document.querySelector<HTMLTextAreaElement>('#debugMsg')!;
const tileImage = document.querySelector<HTMLDivElement>('#tile-image')!;
const tileInfoUrl = document.querySelector<HTMLDivElement>('#tile-url')!;
const wmsImage = document.querySelector<HTMLDivElement>('#wms-image')!;
const wmsInfoUrl = document.querySelector<HTMLDivElement>('#wms-url')!;


const getTileByXY = async (z: number, x: number, y: number): Promise<tileInfo | null> => {
    const url = `${BACKEND_URL}/getTileByXY/${z}/${x}/${y}`;
    log.l(`getTileByXY url:${url}`);
    try {
        const response = await axios.get(url, {timeout: defaultAxiosTimeout});
        log.l(`getTileByXY response:`, response);
        return response.data;
    } catch (error) {
        log.e(`getTileByXY error:`, error);
        return null;
    }
}


log.t(`✅ starting ${APP}-v${VERSION}  build:${BUILD_DATE}`);
inputBaseLayer.value = defaultBaseLayer;
try {
    const myOlMap = await createLausanneMap(
        document.querySelector<HTMLDivElement>('#map')!,
        placeStFrancoisM95,
        defaultZoom,
        myPointLayerName,
        defaultBaseLayer);
    if (myOlMap !== null) {
        log.l(`✅ map createLausanneMap returned a valid map`);
        myOlMap.getView().setCenter(placeStFrancoisM95);
        myOlMap.getView().setZoom(defaultZoom);
        const imgBBox=[2537000.0,1152000.025,2537999.975,1153000.0];
        const imgBBoxPolygonWithVerticesStyleOptions: PolygonWithVerticesStyleOptions = {
            strokeColor: 'blue',
            strokeWidth: 2,
            fillColor: 'rgba(255, 0, 0, 0.1)',
            vertexFillColor: 'yellow',
            vertexRadius: 3,
        };

        drawBBox(myOlMap, myBBoxLayerName, imgBBox as [number, number, number, number], false, imgBBoxPolygonWithVerticesStyleOptions);
        const tileGridBBox=[2532640.0,1145200.0,2548000.0,1158000.0];
        const tileGridBBoxPolygonWithVerticesStyleOptions: PolygonWithVerticesStyleOptions = {
            strokeColor: 'black',
            strokeWidth: 2,
            fillColor: 'rgba(0, 0, 0, 0.7)',
            vertexFillColor: 'yellow',
            vertexRadius: 3,
        };
        drawBBox(myOlMap, myBBoxLayerName, tileGridBBox as [number, number, number, number], false, tileGridBBoxPolygonWithVerticesStyleOptions);
        myOlMap.on("click", async (evt) => {
            log.t(`map click event`, evt);
            const x = +Number(evt.coordinate[0]).toFixed(2);
            const y = +Number(evt.coordinate[1]).toFixed(2);
            const msg = `map click at [${x},${y}]`;
            log.l(msg);
            debugMsg.value = `map click at [${x},${y}]`;
            inputX.value = x.toString();
            inputY.value = y.toString();
            myOlMap.getView().setCenter([x, y]);
            const currentZoom = Number(inputZoom.value)
            const baseLayer = inputBaseLayer.value as baseLayerType;
            redrawMarker(myOlMap, myPointLayerName, [x, y]);
            const res = await getTileByXY(currentZoom, x, y);
            log.l(`getTileByXY response:`, res);
            if (res !== null) {
                const tileUrl = getTileUrl(baseLayer, res.zoom, res.row, res.col)
                const tileSrc = `${getBaseTileUrl}${tileUrl}`;
                debugMsg.value = `map click at [${x},${y}]\n tileSrc:${tileSrc},\n wms_url:${res.wms_url}`;
                tileImage.innerHTML = `<img src="${tileSrc}" alt="tile image"/>`;
                tileInfoUrl.innerHTML = `${tileUrl}`;
                wmsImage.innerHTML = `<img src="${res.wms_url}" alt="wms image"/>`;
                wmsInfoUrl.innerHTML = `WMS bbox:${res.bbox}`;
                drawBBox(myOlMap, myBBoxLayerName, res.bbox);
            }

        });
        myOlMap.on("moveend", () => {
            log.t(`map moveend event`);
            const newCenter = myOlMap.getView().getCenter() || placeStFrancoisM95;
            const realZoom = myOlMap.getView().getZoom() || defaultZoom;
            log.l(`real zoom: ${realZoom}`);
            const newZoom = Math.round(realZoom);
            inputX.value = newCenter[0].toFixed(2);
            inputY.value = newCenter[1].toFixed(2);
            myOlMap.getView().setZoom(newZoom);
            inputZoom.value = newZoom.toString();
            const msg = `map view changed to [${newCenter[0].toFixed(2)},${newCenter[1].toFixed(2)}] zoom:${newZoom}`;
            log.l(msg);
            debugMsg.value = msg;
        });
    }

} catch (error) {
    log.e(`event [map-error]💥💥 map initialization error: ${error}`);
}
