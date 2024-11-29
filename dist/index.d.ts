declare class Queue {
    items: any[];
    constructor();
    enqueue(element: any): void;
    dequeue(): any;
    peek(): any;
    isEmpty(): boolean;
    size(): number;
    print(): void;
}
declare const bfs: (graph: object, callback: Function, nodeAndNeighbor?: boolean, startNode?: string | number) => void;
export { Queue, bfs };
