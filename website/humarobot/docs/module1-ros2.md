---
sidebar_position: 2
---

# Module 1: ROS 2 - Robot Operating System

## Introduction to ROS 2

ROS 2 (Robot Operating System) is the most popular middleware for robot software development. It's not actually an operating system, but a framework that provides:

- **Communication** between robot components
- **Hardware abstraction** 
- **Package management**
- **Development tools**

## Why ROS 2?

| Feature | Benefit |
|---------|---------|
| **Distributed** | Components can run on different computers |
| **Modular** | Easy to add/remove components |
| **Open Source** | Free to use with community support |
| **Multi-language** | Python, C++, Java, and more |

## Core Concepts

### 1. Nodes
Nodes are individual processes that perform computation. Each robot component (sensor, motor, AI) runs as a node.

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        self.get_logger().info('Node started!')