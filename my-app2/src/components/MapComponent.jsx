import React, { useState, useEffect, useContext } from 'react';
import { WebSocketContext, WebSocketKindHandlers } from './WebSocketComponent'
import { GeoJSON, MapContainer, TileLayer, Marker } from "react-leaflet";
import geohash from "ngeohash";

const geojsonData = {
    "type": "FeatureCollection",
    "features": [
        // {
        //     "type": "Feature",
        //     "properties": {
        //         "title": "Train A",
        //         "popupContent": "Train A",
        //     },
        //     "geometry": {
        //         "type": "Point",
        //         "coordinates": [
        //             139.95027239072502 + 0.01,
        //             36.554560344660054 + 0.01,
        //         ]
        //     }
        // },
        // {
        //     "type": "Feature",
        //     "properties": {
        //         "title": "Train B",
        //         "popupContent": "Train B",
        //         "show_on_map": false
        //     },
        //     "geometry": {
        //         "type": "Point",
        //         "coordinates": [
        //             139.95027239072502 - 0.01,
        //             36.554560344660054 - 0.01,
        //         ]
        //     }
        // },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [139.89844464439608, 36.55870018293028],
                    [139.94128861359127, 36.55672812989238],
                    [139.9616473441539, 36.56880018968707],
                    [139.97738050607467, 36.56557497820353],
                    [139.98350618492697, 36.56710964046614],
                    [139.98468636158583, 36.574466568416895],
                    [139.98401197492296, 36.58101048585654],
                    [139.9866533226854, 36.57943097035752],
                    [139.9883954882293, 36.57897967428006],
                    [139.9981740948362, 36.5784832455477],
                    [139.99929807260827, 36.57807707421047],
                    [140.00002865815787, 36.57726472512594],
                    [140.0014898292614, 36.57812220446485],
                    [140.00300719925173, 36.57992739299627],
                    [140.0070535192266, 36.581236128289575],
                    [140.00845849144122, 36.58444017966819],
                    [140.00930147476868, 36.58489144382568]
                ]
            }
        }
    ]
}

const countryStyle = {
    fillColor: "red",
    fillOpacity: 1,
    color: "black",
    weight: 2
};

// https://codesandbox.io/p/sandbox/basic-usage-with-react-leaflet-v3-forked-2smi9y?file=%2Fsrc%2Findex.tsx%3A5%2C45
function MapComponent() {
    const { ws, messages, locations } = useContext(WebSocketContext);
    const [markers, setMarkers] = useState({});

    const mapid = 'mapid';
    // s: サブドメイン（不可分散に利用） z: ズームレベル x: タイルのx座標 y: タイルのy座標
    const tileurl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    const maxZoom = 19;
    const attribution = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>';
    const centerPoint = [36.554560344660054, 139.95027239072502];
    const zoomlevel = 13;

    const onEachFeature = (country, layer) => {
        const countryName = country.properties.title;
        layer.bindPopup(countryName);
        // layer.options.fillColor = "grey";
    };

    const listenEvent = (event) => {
        const key = 1;

        event.tags.forEach(elm => {
            if (elm[0] === "g") {
                const pos = geohash.decode(elm[1]);
                setMarkers({
                    ...markers,
                    [key]: {lat: pos.latitude, lng: pos.longitude}
                });
            }
        });
    };

    WebSocketKindHandlers[1].push(listenEvent);

    return (
        <div align="center">
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
            <MapContainer
                style={{ height: "1000px", width: "1000px", "color": "blue", "opacity": 0.65 }}
                zoom={zoomlevel}
                center={centerPoint}
                scrollWheelZoom={true}
              >
                <TileLayer
                    attribution={attribution}
                    url={tileurl}
                    maxZoom={maxZoom}
                />
                <GeoJSON
                    style={countryStyle}
                    data={geojsonData}
                    onEachFeature={onEachFeature}
                />
                {Object.entries(markers).map(([key, position]) => (
                    <Marker key={key} position={[position.lat, position.lng]} />
                ))}
          </MapContainer>
        </div>
    );
}

export default MapComponent;