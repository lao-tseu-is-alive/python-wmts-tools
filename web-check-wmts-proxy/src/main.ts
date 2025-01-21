import './css/normalize.css'
import './css/skeleton.css'
import './css/style.css'
import logo from '/logo.svg'
import { setupMap, Coordinate2D } from './map.ts'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="container">
      <section class="header">
        <a href="https://vite.dev" target="_blank" class="u-pull-left">
            <img src="${logo}" class="logo" alt="Vite logo" />
        </a>
        <h4>wmts-proxy</h4>
      </section>
      <div class="row">
          <div class="six columns">
            <div id="map" class="map"></div>
          </div>
          <div class="six columns">
            <div id="map-wmts" class="map"></div>
          </div>
  </div>
`
const posCenter:Coordinate2D = [6.63332, 46.51971]
const zoom = 12
setupMap(document.querySelector<HTMLButtonElement>('#map')!, posCenter, zoom)
