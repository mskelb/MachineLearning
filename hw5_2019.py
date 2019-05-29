# -*- coding: utf-8 -*-
"""Hw5_2019.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KYMkqVwXgbV0enAz-Ab3FticXDXf0RoT



---


General guidelines:
*   All solutions to theoretical and pratical problems must be submitted in this ipynb notebook, and equations wherever required, should be formatted using LaTeX math-mode.
*   All discussion regarding practical problems, along with solutions and plots should be specified in this notebook. All plots/results should be visible such that the notebook do not have to be run. But the code in the notebook should reproduce the plots/results if we choose to do so.
*   Your name, personal number and email address should be specified above.
*   All tables and other additional information should be included in this notebook.
*   **All the answers for theoretical questions must be filled in the cells created for you with "Your answer here" below each question, but feel free to add more cells if needed.**
*   Before submitting, make sure that your code can run on another computer. That all plots can show on another computer including all your writing. It is good to check if your code can run here: https://colab.research.google.com.

# Practical problems

The follwing code might be useful for this excercise.

```python
import scipy.io
mat = scipy.io.loadmat('hw5_p1a.mat')
print (mat.keys())
X = mat['X']
```

## [K-Means Implementation, 8 points]

a. Implement the basic (linear) $k$-means algorithm as described in the lecture, using the euclidean distance. Use (uniformly) random points from the data as initialization for the centroids. Terminate the iterative procedure when the the cluster assignments do not change. [**2 pts**]

b. Run your implementation on the matrix $X$ in **hw5_p1a.mat** with $k=2$. Each row of the matrix is an observation, and each column is a feature. Store the cluster assignment both after 2 iterations, and at convergence. Produce a scatter plot of the data with colors indicating the cluster assignments at convergence and highlight points that have changed assignment after the second iteration. [**2 pts**] 

c. Implement the kernel $k$-means algorithm as described in the lecture, using the Gaussian RBF-kernel. [**2 pts**]

d. Run the linear $k$-means **and** your kernel $k$-means on **hw5_p1b.mat** with $k=2$. For the Gaussian RBF-kernel, use $\sigma=0.2$. Produce scatter plots of the data, with color indicating the cluster assignment at convergence, one plot for each of the algorithms. [**2 pts**]

### Your answer here: (uppload file via: View -> Table of contents -> Files -> Upload)
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from copy import deepcopy
from sklearn.cluster import SpectralClustering
# Euclidian distance between two data points
def Euclidean(a,b, ax=1):
  return np.linalg.norm(a-b, axis=ax) 

def KMeans(X,fig,ax,euclidean):
  colors = ['Magenta','purple']
  # Getting the values and plotting them 
  # Each row is an observation (instances), each column is a feature
  V1 = X[:,0] 
  V2 = X[:,1] 
  data = np.array(list(zip(V1 , V2)))
  plt.scatter(V1, V2, color='b', s=7)
  # Number of clusters 
  k = 2
  # Choose (uniformly) random points from the data as initialization for the centroids
  # X coordinates of random centroids 
  centX = np.random.uniform(0, np.max(data), size=k)
  print(centX)
  # Y coordinates of random centroids 
  centY = np.random.uniform(0, np.max(data), size=k)
  # Initializing centroids
  centroids = np.array(list(zip(centX, centY)), dtype=np.float32)
  # Plot with centroids and datapoints togheter  
  plt.scatter(V1, V2, c='blue', s=7)
  plt.scatter(centX, centY, marker='*', s=80, c=colors[:])
  # List to store past centroids 
  centroidsOld = np.zeros(centroids.shape)
  # Labels 
  clusters = np.zeros(len(data))
  # Distance between new and old centorids 
  error = Euclidean(centroids,centroidsOld, None)
  # Terminate the iterative procedure when the cluster assignments do not change 
  while error != 0:
    # Each value is assigned to its closest cluster
    for i in range(len(data)):
      # Find nearest centroid by taking the Euclidean distance 
      dist = Euclidean(data[i], centroids)
      cluster = np.argmin(dist)
      clusters[i] = cluster
    # Storing the old centroid values
    centroidsOld = deepcopy(centroids)
    # Get the new centroids by taking the average value
    for i in range(k):
      p = [data[j] for j in range(len(data)) if clusters[j] == i]
      # The new centriod -> the mean of all points 
      centroids[i] = np.mean(p, axis=0)
      error = Euclidean(centroids, centroidsOld, None)
    # Scatter plot of clustered data 
    fig, ax = plt.subplots()
    for i in range(k):
      p = np.array([data[j] for j in range(len(data)) if clusters[j] == i])
      ax.scatter(p[:, 0], p[:, 1], s=7)
    ax.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=90, c=colors[:])

import scipy.io
import os
# Task (a) and (b) 
# Importing the dataset 
mat = scipy.io.loadmat('hw5_p1a.mat')
X = mat['X']
fig1, ax1 = plt.subplots()
print("Task (a) and (b)") 
print("Running the implementation on the matrix X with k = 2.")
KMeans(X,fig1, ax1, True)

# Task (c) and (d) 
matb = scipy.io.loadmat('hw5_p1b.mat')
fig2, ax2 = plt.subplots()
Xb = matb['X']
print("Task (c) and (d)") 
print("Running the Linear k-mean on the matrix with k=2:")
KMeans(Xb, fig2, ax2, True)

# Task (d) 
print("Running the kernel on the matrix with k=2 and sigma = 0.2:")

import scipy.io
import numpy as np
import numpy.matlib
import os
from matplotlib import pyplot as plt
# Task (c) and (d) 
matb = scipy.io.loadmat('hw5_p1b.mat')
fig2, ax2 = plt.subplots()
X = matb['X']
# Plot the data 
# Compute the Kernel 
kernel = np.zeros((X.shape[0],X.shape[0]))
N = kernel.shape[0]
gamma = 12.5 # Gamma = 1/(2*sigma^2) = 1/(2*(0.2^2)) = 12.5 
for i in range(kernel.shape[0]):
  for k in range(kernel.shape[1]):
    kernel[i,k] = np.exp(-gamma*sum((X[i,:]-X[k,:])**2)); 
# Assign all into one cluster 
K = 2 
array = [[1,0]]
Z = np.matlib.repmat(array,N,1);
Z = Z.reshape(228,2)
s = np.sum(X**2,1);
position = np.argmin(s)
Z[position] = [0,1]
diagonal = np.zeros((N, K))

col = ['#4682B4','#FFA500']
for i in range(K):
  ass = np.nonzero(Z[:,i])
  plt.scatter(X[ass,0], X[ass,1] , color=col[i], s=20)

converged = 0
while (not converged):
  Nk = [sum(x) for x in zip(*Z)]
  for k in range (K):
    aa = Z[:,k].reshape(228,1)
    n1 = (2/(Nk[k]))
    n2 = ((np.matlib.repmat(aa.conj().transpose(),N,1)*kernel)).sum(axis=1)
    n3 = sum(sum(aa*(aa.conj().transpose())*kernel))
    n4 = (1/(Nk[k]**(2)))
    diagonal[:,k] =  np.diagonal(kernel) - n1 * n2 + n4 *n3
  oldZ = Z
  Z = (diagonal.min(axis=1)).reshape(228,1)
  Z = np.matlib.repmat(Z,1,2)
  Z = (np.in1d(diagonal,Z)*1).reshape(228,2)
  if sum(sum(oldZ !=Z ))==0:
    converged = 1
    
    
for k in range(K):
    pos = np.nonzero(Z[:,k])
    plt.scatter(X[pos,0],X[pos,1],color=col[k], s=7)

"""# GMM [4 pts]

We will now consider mixture model. The probability of an observation $x \in \mathbb{R}^D$ is given by: $$p(x) = \sum_{k=1}^{K} \pi_k P(x|\theta_k)$$ where $\pi_k$ are the probabilities a priori and $P(x|\theta_k)$ are multi-dimensional Gaussian characterized by their mean $\mu_k$ and their co-variance matrix $\Sigma_k$
, i.e. $\theta_k = (\mu_k, \Sigma_k)$.

### Q 2.1.
Plot the probability distribution $p(x)$ for D=1 , K = 2, $\pi_1 = \pi_2 = 0.5$ and $\mu_1 = 1$, $\mu_2 = 3$,$\Sigma_1 = 1$,$ \Sigma_2 = 10$. **[2 pts]**

### Q 2.2.

What is the posterior probability that an example $x=1.5$ was produced by the Gaussian $k=1$,i.e. $P(\theta_1| x)$ ? **[2 pts]**

### Your answer here:

Q2.1 

A sample space is made to evaluate the probability, p(x), and plot. A linear spacing of 1000 values from -10 to 15 is chosen to be able to see the peak of p(x) clearly. The value of x=1.5 is stored at x[0] for use in Q2.2 later. The probabilites liklihood probabilities are assumed to be gaussian and can be evaluated as,

\begin{align*}
P(x|\theta_k) &= \mathcal{N}(x, \mu_k, \Sigma_k) = \frac{1}{\Sigma_k \sqrt{2 \pi}} e^{-\frac{(x-\mu_k)^2}{2 \Sigma_k^2}}
\end{align*}

The probability p(x) is then evaluated as,


\begin{align*}
P(x) &= \pi_1 \cdot \mathcal{N}(x, \mu_1, \Sigma_1) + \pi_2 \cdot \mathcal{N}(x, \mu_2, \Sigma_2) \\ 
&= \frac{1}{2 \Sigma_1 \sqrt{2 \pi}} \text{exp} \left \{ -\frac{(x-\mu_1)^2}{2 \Sigma_1^2} \right \} +  \frac{1}{2 \Sigma_2 \sqrt{2 \pi}} \text{exp} \left \{ -\frac{(x-\mu_2)^2}{2 \Sigma_2^2} \right \}
\end{align*}

This is accomplished in the code below.
"""

# %matplotlib inline  # Make it possible to show plots in the notebooks.
import numpy as np
import matplotlib.pyplot as plt

# create a sample space in R1 
N = 500
x = np.linspace(-10, 15, N)
x[0] = 1.5 # point of interest for later

sig = np.array((1, 10)) # standard deviations
mu = np.array((1, 2)) # means

# initialize normal distributions p(theta_k)
Normal = np.zeros((2, N)) 

Normal[0] = (np.sqrt(2*np.pi) *sig[0])**-1 * np.exp(- (x-mu[0])**2 / (2*sig[0]**2))
Normal[1] = (np.sqrt(2*np.pi) *sig[1])**-1 * np.exp(- (x-mu[1])**2 / (2*sig[1]**2))

# p(x)
p = 0.5*Normal[0] + 0.5*Normal[1]

fig= plt.figure(figsize=(16, 5))
plt.scatter(x, p, s = 4);
plt.title('Probability distribution p(x)');
plt.show()

"""Q2.2 - The posterior probability can be evaluated using Bayes thereom. Directly applying Bayes thereom gives the following.

\begin{align*}
 P(\theta_1 | x = 1.5) = \frac{P(x = 1.5 | \theta_1) P(\theta_1)}{P(x = 1.5)}
\end{align*}

The following is known from the previous step.

\begin{align*}
P(\theta_1) &= \pi_1 = 0.5 \\
P(x) &= \sum_{k=1}^K \pi_k P(x|\theta_k) \\
P(x|\theta_1) &= \mathcal{N}(x, \mu_1, \Sigma_1)
\end{align*}

The point of interest x = 1.5 was added to the original sample space in step one at index 0. This allows the probabilites to be evaulated at x=1.5 by indexing at 0. This is done in the code below and the posterior probability, the probability that the data point x=1.5 belongs to the class k=1, is calculated to be 89.8 %.
"""

posterior = np.zeros((2, 1))
posterior[0] = Normal[0][0] * 0.5 / p[0]
posterior[1] = Normal[1][0] * 0.5 / p[0]

print("The posterior probability is %2.1f %%" % (posterior[0]*100))

"""# EM algorithm for GMM [8 pts]

Assume that the property prices of Gotheburg follow a mixture of 2 Gaussians, of respective parameters $(\mu_1, \sigma_1^2)$ and $(\mu_2, \sigma_2^2)$.

The table below lists the prices in million SEK of some real estate transactions:
$$\begin{array}{|c|c|c|c|}
\hline
8& 1 & 4 & 3 & 4 & 5 & 7 & 5 & 3 & 5 \\ \hline
\end{array}$$

We will call $\pi_1$ and $\pi_2$ the coefficients of the two Gaussians in the mixture.

### Q 3.1.

Sort the items of the sample in ascending order and use the 5 smallest values for
estimate by maximum likelihood $(\mu_1, \sigma_1^2)$ and 5 larger ones to estimate $(\mu_2, \sigma_2^2)$. Under these conditions, what values should logically be assigned to the weights $\pi_1$ and $\pi_2$? **[2 pts]**

### Q 3.2.

Starting from $\theta^0 = \{\mu_1, \sigma^2_1, \pi_1, \mu_2, \sigma^2_2, \pi_2\}$ obtained from the previous question, estimate the value of responsibilities $\gamma(z_{nk})$ according to the EM algorithm. **[3 pts]**

### Q 3.3.
Re-estimate the parameters i.e. calculate $\theta^1$, using the current responsibilities.**[3 pts]**

### Your answer here:
"""

import numpy as np

prices = np.array([8, 1, 4, 3, 4, 5, 7, 5, 3, 5])

# initialize
like = np.zeros((2,5)) # liklihood
mu = np.zeros((2,1)) # mean
variance = np.zeros((2,1)) # standard deviation

prices.sort(axis=0) # sort
like[0] = prices[0:5] # smallest 5
like[1] = prices[5:] # other 5

mu[0] = np.mean(like[0])
mu[1] = np.mean(like[1])

variance[0] = np.std(like[0][:])**2
variance[1] = np.std(like[1][:])**2

"""3.1. 

In maximizing the likelihood function the coefficients in the Guassian Mixture Model are determined by:

\begin{align*}
  \pi_k = \frac{N_k}{N}
\end{align*}

In both cases, 1 and 2, the number of items in the class k, $N_k$, is 5 and the total items, $N$, is 10. So, both $\pi_1$ and $\pi_2$ should be estimated as 0.5.
"""

# above cell needs run first

# initialize normal distributions p(theta_k)
Normal = np.zeros((2, 10)) 
gamma = np.zeros((2, 10))

Normal[0] = (np.sqrt(2*np.pi*variance[0]))**-1 * np.exp(-(prices-mu[0])**2 / (2*variance[0]))
Normal[1] = (np.sqrt(2*np.pi*variance[1]))**-1 * np.exp(-(prices-mu[1])**2 / (2*variance[1]))

# # calculate responsibilities
p = 0.5*Normal[0] + 0.5*Normal[1]

gamma[0] = Normal[0]/p
gamma[1] = Normal[1]/p

print(gamma)
