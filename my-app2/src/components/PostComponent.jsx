// メッセージ投稿用コンポーネント
import React, { useState, useEffect, useContext } from 'react';
import { WebSocketContext } from './WebSocketComponent'

function PostComponent() {
    const { ws, messages, locations } = useContext(WebSocketContext);
    const [msg, setMsg] = useState('');
    return (
        <div>
            <div>
                <label>送信するメッセージ</label>
                <input
                    type="text"
                    value={msg}
                    onChange={(e) => setMsg(e.target.value)}
                />
            </div>
            <div>
                <button onClick={() => ws?.send(msg)}>Send</button>
            </div>
        </div>
    );
};

export default PostComponent;
