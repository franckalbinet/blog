---
title: LS-SVM for Function Estimation
summary: "Mastering LS-SVMs: From KKT Conditions to Kernel Tricks"
date: June 8, 2025
tags:
  - Machine Learning
  - Kernel Methods
---


## Part 1: Why LS-SVMs Matter

Least Squares Support Vector Machines (LS-SVMs) represent a pivotal advancement in machine learning that bridges classical optimization theory with modern scalable algorithms. While traditional SVMs require solving complex quadratic programming problems with inequality constraints, LS-SVMs elegantly transform the problem into a simple linear system of equations.

This seemingly small change has profound implications. By replacing inequality constraints with equality constraints, we unlock computational efficiency and mathematical elegance that extends far beyond regression and classification. Recent research has shown that this framework provides theoretical foundations for understanding deep learning architectures, in particular self-attention mechanisms through kernel methods and LS-SVM 

In this exploration, we'll build understanding from first principles, starting with the mathematical foundation and working through concrete examples that you can verify by hand.

## Part 2: Mathematical Foundation - The Constrained Formulation

We start with a function estimation model:
$$y(x) = w^T \phi(x) + b$$
where φ(x) is a feature mapping that can be infinite-dimensional.

**The Constrained Problem**
Instead of directly minimizing prediction errors, we formulate:
$$\min_{w,b,e} J(w, e) = \frac{1}{2} w^T w + \gamma \frac{1}{2} \sum_{k=1}^N e_k^2$$
subject to:
$$y_k = w^T \phi(x_k) + b + e_k, \quad k = 1, \ldots, N$$

This introduces error variables e_k as independent optimization variables, connected to the model through equality constraints.

## Part 3: The KKT Conditions - Step by Step Derivation

The constrained formulation allows us to use Lagrangian optimization. We form the Lagrangian:

$$L(w, b, e; \alpha) = \frac{1}{2} w^T w + \gamma \frac{1}{2} \sum_{k=1}^N e_k^2 - \sum_{k=1}^N \alpha_k \{w^T \phi(x_k) + b + e_k - y_k\}$$

The key insight: we treat w, b, e, and α as independent variables in the Lagrangian, even though they're related by constraints.

**Deriving the KKT Conditions:**

Taking partial derivatives and setting them to zero:

1. **$\frac{\partial L}{\partial w} = 0$** → $w = \sum_{k=1}^N \alpha_k \phi(x_k)$
2. **$\frac{\partial L}{\partial b} = 0$** → $\sum_{k=1}^N \alpha_k = 0$  
3. **$\frac{\partial L}{\partial e_k} = 0$** → $\alpha_k = \gamma e_k$
4. **$\frac{\partial L}{\partial \alpha_k} = 0$** → $w^T \phi(x_k) + b + e_k - y_k = 0$

Notice how condition 1 already hints at the dual representation - w becomes a weighted combination of training points in feature space.


## Part 4: he Substitution Dance - Eliminating Primal Variables

Now comes the crucial step: we eliminate the primal variables (w and e) to get a system purely in terms of the dual variables (α and b).

**The Substitution Process:**
Starting with condition: 

(4) $w^T \phi(x_k) + b + e_k - y_k = 0$

We substitute:
- From condition 1: $w = \sum_{l=1}^N \alpha_l \phi(x_l)$
- From condition 3: $e_k = \frac{\alpha_k}{\gamma}$

This gives us for each constraint k:
$$\sum_{l=1}^N \alpha_l \phi^T(x_l)\phi(x_k) + b + \frac{\alpha_k}{\gamma} - y_k = 0$$

**The Kernel Trick Emerges:**
The dot product $\phi^T(x_l)\phi(x_k) = K(x_l, x_k)$ is where kernel functions naturally appear, allowing us to work with infinite-dimensional feature spaces without ever computing $\phi(x)$ explicitly.


**Key Interpretations from the KKT Conditions**:

From condition 3 (α_k = γe_k), we lose the sparsity property of classical SVMs. However, this creates a more nuanced interpretation:

All data points contribute to the model, but with different weights
Large α_k values indicate data points with significant influence
Small α_k values (near zero but not exactly zero) indicate less influential points
This creates a "gray-scale" rather than "black-and-white" support vector interpretation
From condition 2 (Σα_k = 0), we get a centering condition that ensures the mean of the error distribution is zero. This highlights the importance of the bias term b for:

Balancing datasets
Handling prior class probabilities (in classification)
Ensuring proper model calibration
The relationship α_k = γe_k also means that residuals and dual variables are proportional - larger errors correspond to larger influence in the dual representation.


## Part 5: Concrete Reality Check - The 3-Point Toy Example

Let's ground all this theory with a simple example you can verify by hand.

**Our Dataset:**
- (x₁, y₁) = (1, 2)
- (x₂, y₂) = (2, 3) 
- (x₃, y₃) = (3, 5)

**Linear kernel:** K(x,z) = xz, γ = 1

**The Dual Linear System:**
From our derivation, we get the 4×4 system:

```
[ 0 | 1  1  1 ] [ b   ]   [ 0 ]
[ 1 | 2  2  3 ] [ α_1 ] = [ 2 ]
[ 1 | 2  5  6 ] [ α_2 ] = [ 3 ]
[ 1 | 3  6 10 ] [ α_3 ]   [ 5 ]
```

**Solution:** b = 1.33, α = [-0.33, -0.33, 0.67]

Notice how α₃ has the largest magnitude - point (3,5) has the most influence on our model, which makes intuitive sense as it's the "outlier" from a perfect linear trend.

Should we show how this connects back to the primal solution?


**Connecting Back to the Primal**:

When we solved the same problem using the primal formulation (with cvxpy), we got:
- w = 1.0000, b = 1.3333
- Errors: e = [-0.33, -0.33, 0.67]

**The Beautiful Verification:**
Notice that α_k = γe_k with γ = 1, so α_k = e_k exactly! This confirms our theory perfectly.

**Making Predictions:**

Using the dual model y(x) = Σα_k K(x,x_k) + b, for x_new = 2.5:
```
y_new = (-0.33)(2.5×1) + (-0.33)(2.5×2) + (0.67)(2.5×3) + 1.33 = 3.88
```


## Part 6: The Kernel Revelation - Why the Trick Works and When It Matters

**The Computational Magic:**
The kernel trick K(x,z) = φ^T(x)φ(z) allows us to compute infinite-dimensional dot products with simple functions:

- **RBF Kernel:** K(x,z) = exp(-||x-z||²/(2σ²)) - infinite dimensions, finite computation
- **Polynomial Kernel:** K(x,z) = (x^T z + c)^d - avoids explicit high-dimensional expansion

**Example:** For φ(x) = [x₁², √2x₁x₂, x₂²], instead of computing 3D vectors and their dot product, we simply use K(x,z) = (x^T z)².

**The Broader Impact:**
This framework extends beyond regression/classification:
- Provides theoretical foundations for deep learning architectures
- Enables kernel-based interpretations of self-attention mechanisms
- Offers scalable alternatives to traditional SVM approaches

**Your Journey to Mastery:**
You've now derived the complete LS-SVM framework from first principles, verified it with concrete examples, and understand both its computational advantages and theoretical elegance.

## Far-Reaching Applications

The LS-SVM framework's elegance extends well beyond our regression example. This mathematical foundation has spawned a rich family of kernel methods: LS-SVM versions of Principal Component Analysis (Kernel PCA), Singular Value Decomposition, and even modern deep learning components. Recent research has shown how self-attention mechanisms in transformers can be understood through this lens, bridging classical kernel methods with cutting-edge neural architectures. The unifying principle remains the same: transform complex optimization problems into manageable linear systems while leveraging the kernel trick to work in high-dimensional spaces.

This exploration of LS-SVMs is just the beginning - the mathematical tools you've mastered here unlock understanding across a vast landscape of machine learning methods.


## References

1 "Primal-Attention: Self-attention through Asymmetric Kernel SVD in Primal Representation" (https://arxiv.org/abs/2305.19798)