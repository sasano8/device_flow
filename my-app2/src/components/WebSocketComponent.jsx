import React, { useState, useEffect, createContext } from 'react';
import GetWebSocket from '../providers/WebSocketProvider';
import geohash from "ngeohash";

export const WebSocketContext = createContext(null);
export const WebSocketKindHandlers = {1: []};

export const WebSocketComponent = ({ children }) => {
    const [wsMode, setWsMode] = useState('mock');
    const [wsUrl, setWsUrl] = useState('ws://localhost:8000');
    const [ws, setWs] = useState(null);
    const [recievedAt, setRecievedAt] = useState(new Date().toLocaleString());
    const [delay, setDelay] = useState(3000);
    const [msg, setMsg] = useState("hello my app!");
    const [messages, setMessage] = useState([]);
    const [locations, setLocation] = useState([]);

    // WebSocket接続を開始
    useEffect(() => {
        if (!wsUrl) return;

        const webSocket = GetWebSocket(wsMode, wsUrl);

        webSocket.onopen = () => {
            console.log('WebSocket connection established');
        };

        webSocket.onmessage = (event) => {
            setRecievedAt(new Date().toLocaleString());
            const message = JSON.parse(event.data);
            switch (message[0]) {
                case "EVENT":
                    // ["EVENT", subscription_id, {}]

                    if (message[1]) {
                    } else {
                    }

                    const event = message[2];
                    if (event.kind in WebSocketKindHandlers) {
                        const funcs = WebSocketKindHandlers[event.kind];
                        funcs.forEach((func) => {
                            func(event);
                        });
                    } else {
                    }
                    break;
                case "EOSE":
                    // ["EOSE", subscription_id]
                    break;
                case "NOTICE":
                    // ["NOTICE", "message"]
                    break;
                case "OK":
                    // ["OK", event_id, true || false, "message"]
                    break;
                case "CLOSED":
                    // ["CLOSED", subscription_id, "message"]
                    break;
            }
        };

        webSocket.onclose = () => {
            console.log('WebSocket connection closed');
            setWs(null);
        };

        setWs(webSocket);

        return () => {
            webSocket.close();
        };
    }, [wsUrl]);

    const value = {
        ws,
        messages,
        locations
    };

    return (
        <div>
            <div>
                <label>mode</label>
                <input
                    type="text"
                    value={wsMode}
                    onChange={(e) => setWsMode(e.target.value)}
                />
            </div>
            <div>
                <label>url</label>
                <input
                    type="text"
                    value={wsUrl}
                    onChange={(e) => setWsUrl(e.target.value)}
                />
            </div>
            <div>
                <button onClick={() => setWsUrl(wsUrl)}>Connect</button>
            </div>
            <div>
                {recievedAt}
                {msg}
            </div>
            <WebSocketContext.Provider value={value}>
                {children}
            </WebSocketContext.Provider>
        </div>
    );
}

export default WebSocketComponent;
