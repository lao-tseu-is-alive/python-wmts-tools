import  Map from 'ol/Map'
import View from "ol/View";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import {fromLonLat} from "ol/proj";

export type Coordinate2D = [number, number]

export function setupMap(element: HTMLButtonElement, center: Coordinate2D, zoom: number) {
  let map = new Map({
    target: element,
    layers: [
      new TileLayer({
        source: new OSM(),
      }),
    ],
    view: new View({
      center: fromLonLat(center),
      zoom: zoom,
    }),
  })
  map.on('click', (e) => {
    console.log('#click', e)
  })
}
