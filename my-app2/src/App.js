import logo from './logo.svg';
import './App.css';
import WebSocketComponent from './components/WebSocketComponent';
import MapComponent from './components/MapComponent';
import PostComponent from './components/PostComponent';
import SendPositionComponent from './components/SendPositionComponent';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

function App() {
  const data = [];
  return (
      <div className="App">
          <h1>WebSocket Demo</h1>
          <WebSocketComponent>
            <SendPositionComponent/>
            <PostComponent/>
          </WebSocketComponent>
      </div>
  );
}

export default App;
