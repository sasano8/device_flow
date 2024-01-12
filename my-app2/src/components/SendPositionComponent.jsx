import React, { useState, useEffect, useContext } from 'react';
import { WebSocketContext } from './WebSocketComponent'
import geohash from "ngeohash";

// https://github.com/nbd-wtf/nostr-tools

// デバイスを特定するためにデバイスidが必要。pubkeyでは同一ユーザーによるログインが生じる可能性がある
// gタグが複数きた場合は、deveic_idに紐づく位置情報はリストで持たせて、それぞれマーカーと紐づける。初めから複数を想定しておく。
const sampleData = [
  // ["REQ","test",{"kinds":[1],"limit":50,"authors":["9f77d173dcd94cc4243d36883b157f8c3283051dc6bd237b1c5ac400fb90cecb"]}],  // test をサブスクリプションidとして購読
  ["EVENT","test",{"created_at":1704460227,"content":"現在の位置はa","id":"d5cfb505bd7da4c5a633307fd66c9ae6ca4d319765cf9ba3792b69a63d47c314","kind":1,"pubkey":"9f77d173dcd94cc4243d36883b157f8c3283051dc6bd237b1c5ac400fb90cecb","sig":"eb55a38f406ae15c116294f0a82656740bbd3914242ff3ac1d485a17633f0c6c2f9eaacd1810688c9f2b51c6b27a6f333949086b0071989f1530916d5b70f522","tags":[["e","ef8cf6bc046b2e145450bdcc80a211603eaa58347aa733c2a8550fc77143c8d5","","root"],["e","800c0f941125f1d9f6b4b630208a329559a18e73cd92c9ce5b59a87ea47ffe2a","","reply"],["p","9f77d173dcd94cc4243d36883b157f8c3283051dc6bd237b1c5ac400fb90cecb"], ["g", "xne80b7un8p4"]]}],
  ["EVENT","test",{"created_at":1704460207,"content":"現在の位置はb","id":"800c0f941125f1d9f6b4b630208a329559a18e73cd92c9ce5b59a87ea47ffe2a","kind":1,"pubkey":"9f77d173dcd94cc4243d36883b157f8c3283051dc6bd237b1c5ac400fb90cecb","sig":"af6d0e05b654f887c0a09cfe058c60c3543e9767a87a684a1403fc99d21608d6334d9fa44a3644896c35967bc240e4a680ff5f9a2bae034b6210a509cf660ea7","tags":[["e","ef8cf6bc046b2e145450bdcc80a211603eaa58347aa733c2a8550fc77143c8d5","","root"],["e","ff573087d27a1d697ec5365e523e861b991ee3daf19c96da433db428918e5077","","reply"],["p","9f77d173dcd94cc4243d36883b157f8c3283051dc6bd237b1c5ac400fb90cecb"], ["g", "xn7xbktrkxy1"]]}],
  //["EOSE","test"]
]

class NostrApp {
  constructor() {
    this.relays = {};
    this.subscriptions = {};
    this.handlers = {};
  }

  add_relay(url, ...kwargs) {
    const _kwargs = Object.assign({}, ...kwargs);
  }

  delete_relay(){
  }

  add_hander(){}
  delete_hander(){}

  broadcast(){
  }

  subscribe(subscription_id, request){
    request = {"kinds":[1],"limit":50,"authors":["9f77d173dcd94cc4243d36883b157f8c3283051dc6bd237b1c5ac400fb90cecb"]};
    const req = ["REQ", subscription_id, request];
    return subscription_id;
  }
  unsubscribe(subscription_id){
    const req = ["CLOSE", subscription_id];
  }
}

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
                const encoded = geohash.encode(latitude, longitude, 12);
                const event = ["EVENT","test_1",{"content":"現在の位置はb","created_at":1704460207, "kind": 1, "tags":[["g", encoded]]}];
                ws.send(JSON.stringify(event));
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
          // const geohash_array = ["xne80b7un8p4", "xn7xbktrkxy1"];

          const intervalId = setInterval(() => {
            if (ws && ws.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify(sampleData[index]));
              index = (index + 1) % sampleData.length; // 配列の末尾に達したら最初に戻る
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