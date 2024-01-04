import React, { createContext, useState, useEffect } from 'react';

export const WebSocketContext = createContext(null);

class MockWebSocket {
    constructor(url) {
        this.url = url;
        this.readyState = WebSocket.OPEN;
        this.onopen = null;
        this.onmessage = null;
        this.onclose = null;

        setTimeout(() => {
            if (this.onopen) {
                this.onopen();
            }
        }, 100); // 接続を開く
    }

    send(data) {
        console.log(`MockWebSocket send: ${data}`);
        // メッセージを受信するようにシミュレート
        setTimeout(() => {
            if (this.onmessage) {
                this.onmessage({ data });
            }
        }, 100);
    }

    close() {
        this.readyState = WebSocket.CLOSED;
        this.onmessage = null;
        this.onopen = null;
        this.onclose = null;
        console.log('MockWebSocket closed');
        if (this.onclose) {
            this.onclose();
        }
    }
}

function GetWebSocket(wsMode, wsUrl) {
    if (wsMode === 'mock') {
        return new MockWebSocket(wsUrl);
    } else {
        return new WebSocket(wsUrl);
    }
}

export default GetWebSocket;