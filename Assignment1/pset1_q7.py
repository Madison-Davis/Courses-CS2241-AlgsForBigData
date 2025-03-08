# pset1_q7.py

"""
For the following, let d = 1024. (You can use higher 
values of d if you wish to test your code, but provide
results for d = 1024.) Write code that first generates 
a random point on the d-dimensional unit sphere, then 
rotates it using a Randomized Hadamard Transform, then 
quantizes coordinates to either -1 or 1 (not stochastic 
quantization, just round by sign), then do the inverse 
rotation, and then finds the mean squared error between 
the resulting point/vector and the original. Have the 
code run 100 times and give the min, mean, and max error. 
For this problem, you may use any libraries or tools 
(such as LLMs) to help generate the code as you wish.
"""

# +++++++++++++++++ Installs/Imports +++++++++++++++++ #
import numpy as np


# ++++++++++++++++++++ Functions +++++++++++++++++++++ #

def make_hadamard_matrix(d):
    """Generate Hadamard matrix of size d."""
    # if d = 1, let H_1 = [1]
    H = np.array([[1]]) 
    # recursively build up Hadamard matrix to size d if d !=1
    while H.shape[0] < d:
        H = np.block([[H, H], [H, -H]]) 
    return H

def conduct_experiment(d=1024):
    """ 
    Perform one iteration of the steps 
    described in the problem above. 
    d: dimension
    """
    # Step 1: generate a random point on the d-dimensional unit sphere
    point = np.random.randn(d)
    point = point / np.linalg.norm(point)

    # Step 2: rotate point using RHT
    # To do RHT, create a Hadamard matrix
    H = make_hadamard_matrix(d)
    rotated_point = H @ point

    # Step 3: quantize point's coordinates to either -1 or 1
    # Do so by rounding sign, not stochastic
    quantized_point = np.sign(rotated_point)

    # Step 4: inverse the rotation using RHT
    # Again, this requires us to inverse our Hadamard matrix
    H_inv = np.linalg.inv(H)
    result_point = H_inv @ quantized_point

    # Step 5: determine MSE between result_point and point
    return np.mean((point - result_point) ** 2)



# +++++++++++++++++++ Main Function +++++++++++++++++++ #

if __name__ == "__main__":
    # Determine variables
    d = 1024
    mse_data = []

    # Run 100 experiments
    for _ in range(100):
        mse_data.append(conduct_experiment(d))

    # Print results
    print(f"Min MSE: \t{np.min(mse_data)}")
    print(f"Mean MSE:\t {np.mean(mse_data)}")
    print(f"Max MSE:\t {np.max(mse_data)}")


    """
    CODE DESCRIPTION:
    - I only needed numpy to run the code.
    - I created one helper function, conduct_experiment, to run the MSE.
    - Each experiment does the following:
        - Step 1: generate a random point on the d-dimensional unit sphere
        - Step 2: rotate point using RHT
        - Step 3: quantize point's coordinates to either -1 or 1
        - Step 4: inverse the rotation using RHT
        - Step 5: determine MSE
    
    - I used the following functions within numpy to help:
        .randn(d)            creates a random-number vector of size d
        .linalg.norm(v)      computes the norm of vector v
        .sign(v)             round values in vector v to either -1 or 1
        .linalg.inv(m)       inverse matrix m
        .mean(data)          find mean value within data   
        .min(data)           find min value within data
        .max(data)           find max value within data
    - Other functions I used:
        @                    allows for matrix multiplication
    """