#!/usr/bin/python3.10.6
# -*- coding: utf-8 -*-
#
# @Time    : 2024/4/25 上午8:41
# @Author  : ASXE

from typing import Any, List


class SerializedInterface:
    """序列化接口"""

    def serialized(self, data):
        ...

    def deserialized(self, data):
        ...


class CompressInterface:
    """压缩"""

    def compress(self, data):
        ...

    def decompress(self, data):
        ...


class BPlusTreeNode:
    def __init__(self, order: int):
        self.order = order
        self.keys: List[Any] = []
        self.children: List[BPlusTreeNode] = []
        self.isLeaf: bool = True

    def split(self):
        midIndex = len(self.keys) // 2
        midKey = self.keys[midIndex]

        leftChild = BPlusTreeNode(self.order)
        rightChild = BPlusTreeNode(self.order)

        leftChild.keys = self.keys[:midIndex]
        rightChild.keys = self.keys[midIndex + 1:]

        if not self.isLeaf:
            leftChild.children = self.children[:midIndex + 1]
            rightChild.children = self.children[midIndex + 1:]
            leftChild.isLeaf = rightChild.isLeaf = False

        return midKey, leftChild, rightChild

    def insertNonFull(self, key, value):
        if self.isLeaf:
            self.keys.append((key, value))
            self.keys.sort(key=lambda x: x[0])
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
                self.keys.sort(key=lambda x: x[0])
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

        if len(self.keys) < (self.order - 1) // 2:
            self.rebalanced()

    def rebalanced(self):
        pass


class BPlusTree:
    def __init__(self, order: int = 4):
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

    def search(self, key):
        currentNode = self.root
        while not currentNode.isLeaf:
            for i in range(len(currentNode.keys)):
                if key < currentNode.keys[i][0]:
                    currentNode = currentNode.children[i]
                    break
            else:
                currentNode = currentNode.children[-1]

        for k, v in currentNode.keys:
            if k == key:
                return v
        return None

    def searchRange(self, keyStart, keyEnd):
        result = []
        currentNode = self.root
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
            currentNode = currentNode.children[-1] if currentNode.children else None

        return result

    def remove(self, key):
        self.root.remove(key)
        if not self.root.keys and self.root.children:
            self.root = self.root.children[0]


def convertType(type: str):
    if type.lower() == 'int':
        return int()
    elif type.lower() == 'float':
        return float()
    elif type.lower() == 'str':
        return str()
