import React, { useState, useEffect, useContext } from 'react';
import { WebSocketContext } from './WebSocketComponent'

function TimelineComponent() {
    const { ws, messages, locations } = useContext(WebSocketContext);
    return (
        <div>
        </div>
    );
}

export default TimelineComponent;