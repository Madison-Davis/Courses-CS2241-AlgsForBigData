# pset1_q1.py

"""
Determine Pagerank scores and Hub and Authority scores for 
the following graph (given by the transition matrix). 
State whatever assumptions you make in calculating the 
scores (for example, what scaling methods you are using, if any).
"""

# +++++++++++++++++ Installs/Imports +++++++++++++++++ #
import numpy as np



# ++++++++++++++++++++ Functions +++++++++++++++++++++ #
A = np.array([      [0,0,1,1,0,1],
                    [0,0,1,0,0,1],
                    [0,0,0,1,0,1],
                    [0,1,1,0,0,0],
                    [1,0,0,0,0,0],
                    [0,0,0,0,1,0]], dtype=float)



# +++++++++++++++++ Helper Functions +++++++++++++++++ #
def compute_pagerank(A, d=0.95, e=1e-8, max_iter=100):
    """
    Compute PageRank from adjacency matrix.
    Follows from tutorial: https://www.youtube.com/watch?v=P8Kt6Abq_rM
    One can also follow the logic from 2.6 of PageRank paper, then add damping for scalability
    A:          adjacency matrix where A[j][i] = 1 if j points to i
    d:          damping parameter, set to 0.95 (= 1 makes little difference)
    e:          epsilon, for quick-stop convergence
    max_iter:   if we're not converging fast enough, stop after this # iterations
    """
    # Step 1: set the initial PageRank to 1/N for each page
    N = A.shape[0]  # number of pages/nodes
    PR = np.ones(N) / N
    # Step 2: iterate for a maximum number of iterations or until convergence
    for _ in range(max_iter):
        # create a new PR vector to store updated values
        new_PR = np.zeros(N)
        # for each page...
        for i in range(N):
            # sum of the PageRank contributions from all pages pointing to page i
            for j in range(N):
                # if page j points to page i...
                if A[j][i] == 1:  
                    # A[j] sums up all 1s in that row, where A[j][i] = 1 if j points to i
                    # This includes this page so that the sum is >= 1 (no division by 0)
                    new_PR[i] += PR[j] / np.sum(A[j])
            # apply the damping factor (d)
            new_PR[i] = (1 - d) / N + d * new_PR[i]
        # check for convergence
        # if the difference between new PR and old PR is below tolerance, no need to continue
        if np.linalg.norm(new_PR - PR, 1) < e:
            break
        # update PR for the next iteration
        PR = new_PR
    return PR

def compute_hubsauthorities(A, e=1e-8):
    """
    Compute Hub and Authority weights from adjacency matrix.
    Follow from personal lecture notes.
    A:          adjacency matrix where A[j][i] = 1 if j points to i
    e:          epsilon, for quick-stop convergence
    """
    # Initialize hub (h) and authority (a) scores uniformly
    # In paper, they're called y and x, but let's just use intuitive notation
    n = A.shape[0]
    h = np.ones(n)
    a = np.ones(n)
    # As per the paper, normalize vectors so that sum of their squares is 1
    h /= np.linalg.norm(h, 2)
    a /= np.linalg.norm(a, 2)
    # Keep track of iteration value for output-purposes
    iteration = 0
    while True:
        # Update authority scores: a = A^T h
        # Normalize weights to allow for convergence
        a_new = A.T @ h
        a_new /= np.linalg.norm(a_new, 2)
        # Update hub scores: h = A a
        # Normalize weights to allow for convergence
        h_new = A @ a_new
        h_new /= np.linalg.norm(h_new, 2)
        # If convergence, return
        if np.linalg.norm(a_new - a, 2) < e and np.linalg.norm(h_new - h, 2) < e:
            break
        # If no convergence, update for next iteration
        a, h = a_new, h_new
        iteration += 1
    return h, a



# +++++++++++++++++++ Main Functions +++++++++++++++++++ #

if __name__ == "__main__":
    pagerank_scores = compute_pagerank(A)
    print("PageRank Scores:", pagerank_scores)
    hub_weights, authority_weights = compute_hubsauthorities(A)
    print(f"\nHub Weights: {hub_weights}")
    print(f"\nAuthority weights: {authority_weights}")