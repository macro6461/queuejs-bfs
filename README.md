# queuejs-bfs v1.0.38

This package offers Queue support for JavaScript (a language that does not have it's own built-in queue data structure), and associated libraries and frameworks. It also offers a built-in Breadth First Search (BFS) method that can be used for efficient graph node exploration.

## Installation

To install, you can simply run the below command in your JavaScript, React, React Native, etc. terminal.

```javascript
// using NPM
npm install queuejs-bfs

// using yarn
yarn add queuejs-bfs
```

## Usage

After you have installed `queuejs-bfs`, you can import it into your JavaScript application like so.

```javascript
import { Queue, bfs } from "queuejs-bfs";
```

### Queue

Once imported, you can create a `Queue` instance like so.

```javascript
const queue = new Queue();

queue.enqueue("A");
queue.enqueue("B");
queue.enqueue("C");

queue.print();

// > "A"
// > "B"
// > "C"
```

Other methods that are permitted when using a Queue are below.

- `dequeue`: remove the element from the front of the queue.
- `peek`: View the element at the front of the queue without removing it.
- `isEmpty`: Quickly determine if the queue itself is empty.
- `size`: Get the size of the queue.

### bfs

To use the `bfs` method, you will need to provide one required argument, and then one optional argument. The required argument is a `graph`, the second argument is a `callback` function to handle the nodes/neighbors. Next is `nodeAndNeighbor` which is a boolean, defaulted to true, if you want the callback to handle both the node and the neighbors in the `bfs` method. The final, _optional_ argument, is `startNode`.

The `graph` is an object that looks something like the below.

```javascript
const graph = {
  user1: ["user2", "user3"],
  user2: ["user1", "user4", "user5"],
  user3: ["user1", "user6"],
  user4: ["user2"],
  user5: ["user2"],
  user6: ["user3"],
};
```

For `callback` you can pass a function to handle the neighbors and nodes how you want. I'll show an example in a moment.

For `startNode`, you can pass either a number or a string. This parameter tells the `bfs` method which node to start from. If left empty, it will start from the first node of the graph. See an example of `bfs` implementation below.

```javascript
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
        // here we want both the node and the neighbor, so we don't pass anything for `nodeAndNeighbor`. It defaults to true.
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
```

If you have your own BFS algorithm and just want a quick `Queue` instance, you can simply import `Queue` and use as need be.

**Note: The full example React app can be found in the `example` directory on [GitHub](https://github.com/macro6461/queuejs-bfs/tree/main/example).**
