import React, { useState, useEffect, useContext } from 'react';
import { WebSocketContext } from './WebSocketComponent'


const geojsonData = {
    "type": "FeatureCollection",
    "features": [{
            "type": "Feature",
            "properties": {
                "popupContent": "Train A",
                "amenity": "Baseball Stadium"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    139.95027239072502 + 0.01,
                    36.554560344660054 + 0.01,
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "popupContent": "Train B",
                "show_on_map": false
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    139.95027239072502 - 0.01,
                    36.554560344660054 - 0.01,
                ]
            }
        },
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


function MapComponent() {
    const { ws, messages, locations } = useContext(WebSocketContext);
    const [markers, setMarkers] = useState(geojsonData);

    return (
        <div>
            <label>layer geojson</label>
            <input
                    type="text"
                    value={markers}
                    onChange={(e) => setMarkers(JSON.parse(e.target.value))}
            />
        </div>
    );
}

export default MapComponent;