import { useEffect, useState } from "react";
import "./App.css";
import { Queue, bfs } from "queuejs-bfs";

const graph = {
  user1: ["user2", "user3"],
  user2: ["user1", "user4", "user5"],
  user3: ["user1", "user6"],
  user4: ["user2"],
  user5: ["user2"],
  user6: ["user3"],
};

function App() {
  const [userConnections, setUserConnections] = useState([]);

  useEffect(() => {
    initQueueWithBfs();
  }, []);

  const initQueueWithBfs = () => {
    let mutualConnections = [];
    bfs(
      graph,
      ({ node, neighbor }) => {
        console.log(neighbor);
        mutualConnections.push(node);
      },
      "user1"
    );
    setUserConnections(mutualConnections);
  };

  return (
    <div className="App">
      <h1>Mutual Connections</h1>
      <ul>
        {userConnections.map((user, index) => (
          <li key={index}>{user}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
