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
matrix = np.array([ [0,0,1,1,0,1],
                    [0,0,1,0,0,1],
                    [0,0,0,1,0,1],
                    [0,1,1,0,0,0],
                    [1,0,0,0,0,0],
                    [0,0,0,0,1,0]], dtype=float)



# +++++++++++++++++ Helper Functions +++++++++++++++++ #

def compute_pagerank(delta, epsilon, A, E, S):
    """
    Compute PageRank from adjacency matrix.
    Follow from Section 2.6 of PageRank
    delta:      user-tuned parameter
    epsilon:    user-tuned parameter
    A:          adjacency matrix
    E:          typically, a uniform vector over all pages with value epsilon
    S:          any vector over pages (can be E)
    """
    # Initialize R
    R = S.copy() / np.linalg.norm(S, ord=1)
    iteration = 0

    # While True and break mimic a 'do-while' loop to model pseudocode from paper
    while True:
        R_next = (A @ R) 
        d = np.linalg.norm(R, ord=1) - np.linalg.norm(R_next, ord=1)
        R_next = R_next + d * E
        # Normalize R_next to allow for better convergence
        R_next = R_next / np.linalg.norm(R_next, ord=1)  
        delta = np.linalg.norm(R_next - R, ord=1)
        # If converged, stop
        if delta < epsilon:
            print(f"PageRank conversion reached after {iteration} iterations!")
            break
        # Detect blow-up case
        if np.isnan(delta):
            print("PageRank NaN detected! Stopping.")
            break
        # If not converged, update R for next iteration
        R = R_next
        iteration += 1
    return R

def compute_hubsauthorities(A, epsilon):
    """
    Compute Hub and Authority weights from adjacency matrix.
    Follow from personal lecture notes.
    A:          adjacency matrix
    epsilon:    user-tuned parameter
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
        if np.linalg.norm(a_new - a, 1) < epsilon and np.linalg.norm(h_new - h, 1) < epsilon:
            print(f"Hubs Authorities conversion reached after {iteration} iterations!")
            break
        # If no convergence, update for next iteration
        a, h = a_new, h_new
        iteration += 1
    return a, h



# +++++++++++++++++++ Main Functions +++++++++++++++++++ #

if __name__ == "__main__":
    # Establish variables
    # Assumptions:
        # E is uniform over pages with value of epsilon
        # S = E
        # epsilon is some small number
        # delta starts off high with some dampening-effect (ie != 1)
    delta = 0.85        
    epsilon = 0.002
    A = matrix
    N = matrix.shape[0]  # Number of pages
    E = np.full(matrix.shape[0], epsilon)
    S = E
    pageranks = compute_pagerank(delta, epsilon, A, E, S)
    print(f"PageRank ranks:\n{pageranks}\n\n")
    hub_weights, authority_weights = compute_hubsauthorities(A, epsilon)
    print(f"Hub weights:\n{hub_weights}\nAuthority weights:\n{authority_weights}")
