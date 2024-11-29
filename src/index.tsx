interface NodeAndNeighbor {
  node: any;
  neighbor?: any;
}

class Queue {
  items: any[];
  constructor() {
    this.items = [];
  }

  // Enqueue: Add an element to the end of the queue
  enqueue(element: any) {
    this.items.push(element);
  }

  // Dequeue: Remove the element from the front of the queue
  dequeue() {
    if (this.isEmpty()) {
      return "Queue is empty!";
    }
    return this.items.shift(); // shift removes the first element
  }

  // Peek: View the element at the front without removing it
  peek() {
    if (this.isEmpty()) {
      return "Queue is empty!";
    }
    return this.items[0];
  }

  // Check if the queue is empty
  isEmpty() {
    return this.items.length === 0;
  }

  // Get the size of the queue
  size() {
    return this.items.length;
  }

  // Print the queue
  print() {
    console.log(this.items.toString());
  }
}

const bfs = (
  graph: object,
  callback: Function,
  startNode?: string | number
) => {
  const queue = new Queue();
  const visited = new Set();
  let first = startNode || Object.keys(graph)[0];

  queue.enqueue(first);
  visited.add(first);

  while (!queue.isEmpty()) {
    const node = queue.dequeue();
    if (graph[node]) {
      // Add all unvisited neighbors to the queue
      graph[node].forEach((neighbor) => {
        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          queue.enqueue(neighbor);
          callback({ node, neighbor } as NodeAndNeighbor);
        }
      });
    }
  }
};

export { Queue, bfs };
