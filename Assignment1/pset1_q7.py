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
    # To do RHT, create random permutation of binary Hadamard matrix
    H = np.random.choice([1, -1], size=(d, d))  
    np.random.shuffle(H)
    rotated_point = H @ point

    # Step 3: quantize point's coordinates to either -1 or 1
    # Do so by rounding sign, not stochastic
    quantized_point = np.sign(rotated_point)

    # Step 4: inverse the rotation using RHT
    # Again, we'll create random permutation of binary Hadamard matri
    H_inv = np.random.choice([1, -1], size=(d, d)) 
    np.random.shuffle(H_inv)
    result_point = np.linalg.inv(H_inv) @ quantized_point

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
    print(f"Min MSE: {np.min(mse_data)}")
    print(f"Mean MSE: {np.mean(mse_data)}")
    print(f"Min MSE: {np.max(mse_data)}")


    """
    RESULTS:
    For d=1024, my result is:
    Min MSE:    0.1130352042854703
    Mean MSE:   7429.64817612989
    Min MSE:    736573.9641994352

    Rounded to the nearest hundredths:
    Min MSE:    0.11
    Mean MSE:   7429.65
    Min MSE:    736573.96
    """

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
        .choice([], axb)     creates a matrix of size axb whose cells are randomly chosen among the [] items
        .shuffle(m)          shuffle entries within matrix m
        .sign(v)             round values in vector v to either -1 or 1
        .linalg.inv(m)       inverse matrix m
        .mean(data)          find mean value within data   
        .min(data)           find min value within data
        .max(data)           find max value within data
    - Other functions I used:
        @                    allows for matrix multiplication
    """