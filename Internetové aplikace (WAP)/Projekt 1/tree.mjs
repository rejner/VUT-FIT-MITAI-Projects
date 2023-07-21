"use strict";
/*
* Title:    WAP - Project 1 - Binary Tree Library
* Author:   Michal Rein (xreinm00)
* E-mail:   xreinm00@stud.fit.vutbr.cz
* Date:     27.02.2022
* Node:     v16.14.0
*/

/** @module tree */

/**
 * Represents a binary tree data structure.
 * @constructor
 * @param {Function} sortingFunction - Function which defines rules for adding
 * new value into the tree structure. If sorting function returns true, the new
 * value will be pushed into the left sub-tree (right sub-tree otherwise).
 */
export function Tree(sortingFunction) {
    this.sortingFunction = sortingFunction;

    /**
     * Root Node object of the binary tree structure.
     * @type {Node}
     */
    this.root = null;
    
    /**
     * Function handling requests for inserting new values into the tree.
     * Starts the cascade of recursive calls on Node objects.
     * @param {Function} newValue
     */
    this.insertValue = function (newValue) {
        if (this.root === null) {
            this.root = new Node(newValue);
            return;
        }
        this.root.insert(newValue, this.sortingFunction);
    }

    /**
     * Function creating generator object for preorder traversal of the tree structure.
     * @returns {Generator} - Generator like object for traversing the tree. 
     */
    this.preorder = function () {
        return this.preorder.prototype.next(this.root);
    }

    /**
     * Function creating generator object for inorder traversal of the tree structure.
     * @returns {Generator} - Generator like object for traversing the tree. 
     */
    this.inorder = function () {
        return this.inorder.prototype.next(this.root);
    }

    /**
     * Function creating generator object for postorder traversal of the tree structure.
     * @returns {Generator} - Generator like object for traversing the tree. 
     */
    this.postorder = function () {
        return this.postorder.prototype.next(this.root);
    }

    this.preorder.prototype.next = function* (root) {
        if (root === null) {
            return;
        } 
        yield root.value;
        yield* this.next(root.leftChild);
        yield* this.next(root.rightChild);
    }

    this.inorder.prototype.next = function* (root) {
        if (root === null) {
            return;
        } 
        yield* this.next(root.leftChild);
        yield root.value;
        yield* this.next(root.rightChild);
    }

    this.postorder.prototype.next = function* (root) {
        if (root === null) {
            return;
        } 
        yield* this.next(root.leftChild);
        yield* this.next(root.rightChild);
        yield root.value;
    }
}

/**
 * Represents a node of the binary tree data structure.
 * This node can be either root, parent or leaf node.
 * @constructor
 * @param {any} value - Value stored inside created node. 
 */
function Node(value) {
    /**
     * Value stored in the Node object.
     * @type {any}
     */
    this.value = value;
    /**
     * Reference to the left child Node object.
     * @type {Node}
     */
    this.leftChild = null;
    /**
     * Reference to the right child Node object.
     * @type {Node}
     */
    this.rightChild = null;

    /**
     * Function which perform inserting new value into binary tree structure.
     * Based on the sorting function provided by Tree object, recursive call
     * is made to find the first empty slot where the new Node object will be
     * created containing the new value.
     * @param {Function} newValue
     */
    this.insert = function (newValue, sortingFunction) {
        if (sortingFunction(newValue, this.value)) {
            this.leftChild === null ? this.leftChild = new Node(newValue) : this.leftChild.insert(newValue, sortingFunction);
        } else {
            this.rightChild === null ? this.rightChild = new Node(newValue) : this.rightChild.insert(newValue, sortingFunction);
        }
    }
}


