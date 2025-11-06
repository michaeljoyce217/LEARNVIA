# Introduction to Data Structures

## Overview

This module will teach you about data structures. we will cover various topics including arrays, linked lists, stacks, queues, trees, and hash tables. By the end, you will understand how to use them.

## Arrays

Arrays are collection of elements. they are stored in contiguous memory locations. You can access elements using indices.

Here's an example:
```python
arr = [1, 2, 3, 4, 5]
print(arr[0])  # outputs 1
```

The time complexity for accessing an element is O(1), but insertion at arbitrary position requires O(n) because we have got to shift elements.

### Array Operations

The following section examines common operations:

**Insertion**: Add element to array
**Deletion**: Remove element from array
**Search**: Find element in array
**Update**: Change element value

## Linked Lists

Now we will discuss linked lists. Unlike arrays, linked lists do not require contiguous memory. Each node contains data and pointer to next node.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

Linked lists are better than arrays when you need frequent insertions/deletions at beginning.

### Types of Linked Lists

There are several types:
1. Singly linked list
2. Doubly linked list
3. Circular linked list

## Binary Trees

Moving on to trees - they are hierarchical data structures. Binary trees have maximum two children per node. The top node is called root.

Important properties:
- Height: longest path from root to leaf
- Depth: path from root to specific node
- Level: depth + 1

### Tree Traversal

You can traverse trees in different ways:

**Inorder**: Left → Root → Right
**Preorder**: Root → Left → Right
**Postorder**: Left → Right → Root

Here's code for inorder traversal:

```python
def inorder(root):
    if root:
        inorder(root.left)
        print(root.data)
        inorder(root.right)
```

## Binary Search Trees

BSTs are special binary trees where left child < parent < right child. This property makes searching efficient with O(log n) average case.

Operations on BST:
- Search: O(log n) average
- Insert: O(log n) average
- Delete: O(log n) average

But if tree becomes unbalanced, performance degrades to O(n).

## Hash Tables

Hash tables provide O(1) average case for insert, delete, and search operations. They use hash function to map keys to array indices.

### Collision Resolution

When two keys hash to same index, we have collision. Common resolution techniques:

**Chaining**: Store multiple elements at same index using linked list
**Open Addressing**: Find another empty slot using probing

Example of simple hash function:
```python
def hash(key, size):
    return key % size
```

## Stacks and Queues

### Stacks

Stacks follow LIFO principle. Consider stack of plates - you can only add/remove from top.

Operations:
- Push: Add element to top
- Pop: Remove element from top
- Peek: View top element

### Queues

Queues follow FIFO principle. it is like standing in line - first person in line is served first.

Operations:
- Enqueue: Add element to rear
- Dequeue: Remove element from front
- Front: View front element

## Advanced Topics

For those who want to explore further, here are advanced concepts:

### Heaps

Heaps are complete binary trees with heap property. In max heap, parent >= children. In min heap, parent <= children.

they are used for:
- Priority queues
- Heap sort (O(n log n))
- Finding kth largest/smallest element

### Graphs

Graphs consist of vertices and edges. They can be:
- Directed vs undirected
- Weighted vs unweighted
- Cyclic vs acyclic

Common algorithms:
- DFS (Depth First Search)
- BFS (Breadth First Search)
- Dijkstra's shortest path
- Minimum spanning tree

### B-Trees

B-trees are self-balancing trees designed for disk storage. they are used in databases and file systems. Unlike binary trees, B-trees can have multiple children per node.

## Practice Problems

The following problems provide practice:

1. Reverse a linked list
2. Check if binary tree is balanced
3. Implement queue using stacks
4. Find cycle in graph
5. Design LRU cache

## Conclusion

we have covered fundamental data structures. It is important to note that choosing right data structure depends on your use case. Consider time/space complexity trade-offs.

Keep practicing and you will master these concepts!