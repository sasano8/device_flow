import React, { useState, useEffect, createContext } from 'react';
import GetWebSocket from '../providers/WebSocketProvider';

export const WebSocketContext = createContext(null);

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
            setMsg(event.data);
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
