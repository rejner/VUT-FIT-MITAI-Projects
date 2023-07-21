'use strict';

/*
* Title:    WAP - Project 1 - Jest tests for Tree module
* Author:   Michal Rein (xreinm00)
* E-mail:   xreinm00@stud.fit.vutbr.cz
* Date:     27.02.2022
* Node:     v16.14.0
*/

import { Tree } from "../tree.mjs";

const exampleInputNumbers = [4, 3, 2.00, 5, 1, 8.00, 12, 6.00, 4];
const exampleInputStrings = ['d', 'c', 'b', 'e', 'a', 'g', 'h', 'f', 'd'];

// simple object constructor for testing
function Item(name, price) {
    this.name = name;
    this.price = price;
}

const exampleInputItems = [new Item("Kniha", 4), new Item("Kobliha", 3), new Item("Rohlík", 2), new Item("Čokoláda", 5)]

describe("Sorting functions, preorder traverse", () => {
    test("(a, b) => a < b ------ (numbers)", () => {
        let t = new Tree((a,b) => a < b);
        exampleInputNumbers.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual([4, 3, 2.00, 1, 5, 4, 8.00, 6.00, 12]);
     });

     test("(a, b) => a > b ------ (numbers)", () => {
        let t = new Tree((a,b) => a > b);
        exampleInputNumbers.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual([4, 5, 8.00, 12, 6.00, 3, 4, 2.00, 1]);
     });

     test("(a, b) => a === b ---- (numbers)", () => {
        let t = new Tree((a,b) => a === b);
        exampleInputNumbers.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual([4, 4, 3, 2.00, 5, 1, 8.00, 12, 6.00]);
     });

     test("(a, b) => a < b ------ (string)", () => {
        let t = new Tree((a,b) => a < b);
        exampleInputStrings.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual(['d', 'c', 'b', 'a', 'e', 'd', 'g', 'f', 'h']);
     });

     test("(a, b) => a > b ------ (string)", () => {
        let t = new Tree((a,b) => a > b);
        exampleInputStrings.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual(['d', 'e', 'g', 'h', 'f', 'c', 'd', 'b', 'a']);
     });

     test("(a, b) => a === b ---- (string)", () => {
        let t = new Tree((a,b) => a === b);
        exampleInputStrings.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual(['d', 'd', 'c', 'b', 'e', 'a', 'g', 'h', 'f']);
     });

     test("(a, b) => a.price < b.price ------ (Item objects)", () => {
        let t = new Tree((a,b) => a.price < b.price);
        exampleInputItems.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n.price);
        }
        expect(out).toEqual([4, 3, 2, 5]);
     });

     test("(a, b) => a.price > b.price ------ (Item objects)", () => {
        let t = new Tree((a,b) => a.price > b.price);
        exampleInputItems.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n.price);
        }
        expect(out).toEqual([4, 5, 3, 2]);
     });

     test("(a, b) => a.price === b.price ---- (Item objects)", () => {
        let t = new Tree((a,b) => a.price === b.price);
        exampleInputItems.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n.price);
        }
        expect(out).toEqual([4, 3, 2, 5]);
     });

});

describe("Traversals for (a, b) => a < b", () => {
    test("Preorder", () => {
        let t = new Tree((a,b) => a < b);
        exampleInputNumbers.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.preorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual([4, 3, 2.00, 1, 5, 4, 8.00, 6.00, 12]);
     });

     test("Inorder", () => {
        let t = new Tree((a,b) => a < b);
        exampleInputNumbers.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.inorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual([1, 2.00, 3, 4, 4, 5, 6.00, 8.00, 12]);
     });

     test("Postorder", () => {
        let t = new Tree((a,b) => a < b);
        exampleInputNumbers.forEach((i) => {
            t.insertValue(i);
        });
        let out = [];
        let pre = t.postorder();
        for (let n of pre) {
            out.push(n);
        }
        expect(out).toEqual([1, 2.00, 3, 4, 6.00, 12, 8.00, 5, 4]);
     });

});

describe("Special cases", () => {
    test("Sorting function not provided", () => {
        let t = new Tree();
        expect(() =>
            exampleInputNumbers.forEach((i) => {
                t.insertValue(i);
            }
        )).toThrow(TypeError);
     });

     test("Sorting function is not a function", () => {
        let t = new Tree(10);
        expect(() =>
            exampleInputNumbers.forEach((i) => {
                t.insertValue(i);
            }
        )).toThrow(TypeError);
     });

     test("Iterating over multiple trees, sequential ([...numbers, ...strings])", () => {
        let t1 = new Tree((a,b) => a < b);
        let t2 = new Tree((a,b) => a < b);
        exampleInputNumbers.forEach((i) => {
            t1.insertValue(i);
        });
        exampleInputStrings.forEach((i) => {
            t2.insertValue(i);
        });
        let out = [];
        let pre1 = t1.preorder();
        let pre2 = t2.preorder();
        for (let n of pre1) {
            out.push(n);
        }
        for (let n of pre2) {
            out.push(n);
        }
        expect(out).toEqual([4, 3, 2.00, 1, 5, 4, 8.00, 6.00, 12, 'd', 'c', 'b', 'a', 'e', 'd', 'g', 'f', 'h']);
     });

     test("Iterating over multiple trees, blended ([number, string, number...])", () => {
        let t1 = new Tree((a,b) => a < b);
        let t2 = new Tree((a,b) => a < b);
        exampleInputNumbers.forEach((i) => {
            t1.insertValue(i);
        });
        exampleInputStrings.forEach((i) => {
            t2.insertValue(i);
        });
        let out = [];
        let pre1 = t1.preorder();
        let pre2 = t2.preorder();
        for (let i = 0; i < exampleInputNumbers.length; i++) {
            let item1 = pre1.next();
            let item2 = pre2.next();
            out.push(item1.value);
            out.push(item2.value);
        }
        expect(out).toEqual([4, 'd', 3, 'c', 2.00, 'b', 1, 'a', 5, 'e', 4, 'd', 8.00, 'g', 6.00, 'f', 12, 'h']);
     });

})
