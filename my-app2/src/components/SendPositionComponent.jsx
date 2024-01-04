import React, { useState, useEffect, useContext } from 'react';
import { WebSocketContext } from './WebSocketComponent'

function SendPositionComponent() {
    const { ws, messages, locations } = useContext(WebSocketContext);
    const [watchId, setWatchId] = useState(null);
    const [mode, setMode] = useState('real');

    // 定期的にデータを送信
    useEffect(() => {
        if (!ws) return;
        if (watchId) {
            navigator.geolocation.clearWatch(watchId);
            setWatchId(null);
        }

        if (mode === 'real') {
          const _watchId = navigator.geolocation.watchPosition(
              (position) => {
                const { latitude, longitude, altitude } = position.coords;
                ws.send(JSON.stringify({ latitude, longitude, altitude }));
              },
              (error) => {
                console.error('Error getting location', error);
              },
              {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
              }
          );
          setWatchId(_watchId);
          return () => navigator.geolocation.clearWatch(watchId); // 値は現在のスコープに束縛されている
        } else {
          let index = 0;
          const array = [ { latitude: 36.554560344660054 + 0.01, longitude: 139.95027239072502 + 0.01,  altitude: null }, {latitude: 36.554560344660054 - 0.01, longitude: 139.95027239072502 - 0.01, altitude: null }];

          const intervalId = setInterval(() => {
            if (ws && ws.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify(array[index]));
              index = (index + 1) % array.length; // 配列の末尾に達したら最初に戻る
            }
          }, 1000); // 3秒ごと

          return () => clearInterval(intervalId); // 値は現在のスコープに束縛されている
        }
    }, [ws, mode]);

    return (
        <div>
          <div>
            <label>位置情報モード</label>
            <input
                type="text"
                value={mode}
                onChange={(e) => setMode(e.target.value)}
            />
          </div>
        </div>
    );
}

export default SendPositionComponent;