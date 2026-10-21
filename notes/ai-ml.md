# AI and ML Notes

## What A Single Perceptron Can Separate

A 2D perceptron scores a point with `w1x + w2y + b` and uses zero as its decision boundary. That boundary is one straight line. Training changes the line's angle and position; it does not turn the line into a curve.

The XOR and XNOR points alternate labels at the corners of a square, so one line cannot separate them perfectly. The hole-in-the-middle dataset has eight class `1` points around one class `0` point. The center sits inside the ring, so one line cannot isolate it from all eight outer points.

The `88.9%` score in the hole challenge comes from predicting the majority label, `1`, for every point. That gets eight of nine right and misses the center. It is a useful reminder to compare accuracy with a majority-class baseline before assuming the model learned the structure.

Changing the learning rate affects which weights training reaches within its update limit. It cannot make a line represent a pattern that needs a closed or nonlinear boundary.

## 3-Bit Parity In 3D

For 3-bit parity, the eight inputs are the vertices of a cube. The label flips
when any one bit changes, so odd- and even-parity vertices alternate. A single
plane cannot separate both groups perfectly. The challenge's `0.20` run ended
with weights `w1 = 0.60`, `w2 = 0.60`, `w3 = -0.20`, and `b = 0.20`; it
classified six of eight points correctly and reached the accepted `75%`.
This is the 3D version of the XOR/XNOR limit: training can move a linear
boundary, but it cannot make that boundary nonlinear.

## Examples

- [Perceptron Train XOR](../practice/cylabacademy/challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-train-xor/README.md)
- [Perceptron Train XNOR](../practice/cylabacademy/challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-train-xnor/README.md)
- [Perceptron Train Hole in Middle](../practice/cylabacademy/challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-train-hole-in-middle/README.md)
- [Perceptron Train 3-Bit Parity](../practice/cylabacademy/challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-train-3-bit-parity/README.md)
