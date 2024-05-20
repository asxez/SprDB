#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/25 上午8:41
# @Author  : ASXE

from typing import Any, List, Optional


class SerializedInterface:
    """序列化接口"""

    def serialized(self, data):
        """序列化表数据"""
        ...

    def deserialized(self, data):
        """反序列化表数据"""
        ...


class CompressInterface:
    """压缩"""

    def compress(self, data):
        """压缩数据"""
        ...

    def decompress(self, data):
        """解压数据"""
        ...


class BPlusTreeNode:
    def __init__(self, order: int):
        self.order = order
        self.keys: List[Any] = []
        self.children: List[BPlusTreeNode] = []
        self.isLeaf: bool = True
        self.next: Optional[BPlusTreeNode] = None  # 用于叶子节点的链表链接

    def split(self):
        midIndex = len(self.keys) // 2
        midKey = self.keys[midIndex][0]

        leftChild = BPlusTreeNode(self.order)
        rightChild = BPlusTreeNode(self.order)

        leftChild.keys = self.keys[:midIndex]
        rightChild.keys = self.keys[midIndex:]

        if not self.isLeaf:
            leftChild.children = self.children[:midIndex + 1]
            rightChild.children = self.children[midIndex + 1:]
            leftChild.isLeaf = rightChild.isLeaf = False
        else:
            rightChild.next = self.next
            self.next = rightChild

        return midKey, leftChild, rightChild

    def insertNonFull(self, key, value):
        if self.isLeaf:
            self.keys.append((key, value))
            self.keys.sort(key=lambda x: x[0])  # 只对键进行排序
        else:
            for i in range(len(self.keys)):
                if key < self.keys[i][0]:
                    child = self.children[i]
                    break
            else:
                child = self.children[-1]

            if len(child.keys) == self.order - 1:
                midKey, leftChild, rightChild = child.split()
                self.keys.append((midKey, None))
                self.keys.sort(key=lambda x: x[0])  # 只对键进行排序
                self.children = self.children[:self.children.index(child)] + [leftChild, rightChild] + self.children[
                                                                                                       self.children.index(
                                                                                                           child) + 1:]

                if key < midKey:
                    child = leftChild
                else:
                    child = rightChild

            child.insertNonFull(key, value)

    def remove(self, key):
        if self.isLeaf:
            self.keys = [k for k in self.keys if k[0] != key]
        else:
            for i in range(len(self.keys)):
                if key < self.keys[i][0]:
                    self.children[i].remove(key)
                    break
            else:
                self.children[-1].remove(key)

    def search(self, key):
        if self.isLeaf:
            for k, v in self.keys:
                if k == key:
                    return v
            return None
        for i in range(len(self.keys)):
            if key < self.keys[i][0]:
                return self.children[i].search(key)
        return self.children[-1].search(key)

    def searchRange(self, keyStart, keyEnd):
        result = []
        currentNode = self
        while not currentNode.isLeaf:
            for i in range(len(currentNode.keys)):
                if keyStart < currentNode.keys[i][0]:
                    currentNode = currentNode.children[i]
                    break
            else:
                currentNode = currentNode.children[-1]

        while currentNode:
            for k, v in currentNode.keys:
                if keyStart <= k <= keyEnd:
                    result.append(v)
            currentNode = currentNode.next

        return result


class BPlusTree:
    def __init__(self, order: int = 1000):
        self.root = BPlusTreeNode(order)
        self.order = order

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == self.order - 1:
            midKey, leftChild, rightChild = root.split()
            newRoot = BPlusTreeNode(self.order)
            newRoot.keys = [(midKey, None)]
            newRoot.children = [leftChild, rightChild]
            newRoot.isLeaf = False
            self.root = newRoot

        self.root.insertNonFull(key, value)

    def remove(self, key):
        self.root.remove(key)
        if not self.root.keys and not self.root.isLeaf:
            self.root = self.root.children[0]

    def search(self, key):
        return self.root.search(key)

    def searchRange(self, keyStart, keyEnd):
        return self.root.searchRange(keyStart, keyEnd)
