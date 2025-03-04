# pset1_q4.py

"""
A fair coin is flipped until the first head occurs. 
Let X denote the number of flips required. Find the 
entropy H(X) in bits. Suppose your friend flips a 
fair coin until the first head is flipped to generate 
a value for X, and now you want to ask a series of 
yes-no questions (of the form “is X contained in the 
following set?”) to determine the value of X generated. 
Describe what questions you ask, determine the expected 
number of questions you ask, and compare your result 
with H(X).
"""

# +++++++++++++++++ Installs/Imports +++++++++++++++++ #



# ++++++++++++++++++++ Functions +++++++++++++++++++++ #



# +++++++++++++++++++ Main Function +++++++++++++++++++ #

if __name__ == "__main__":
    """
    Entropy is the average length of the 
    amount of information in a message, in bits.
    Its equation is ∑ p(i)*log2(1/p(i)) where p(i) is
    the probability of outcome i.  If we want the entropy
    of the first time getting heads, we have many 
    'instances' of probabilities.  For example:

    x = 1       p(1) = 1/2          1st flip is a head
    x = 2       p(1) = (1/2)^2      2nd flip is a head
    ...
    x = inf     p(1) = (1/2)^inf    inf-th flip is a head
    
    Our entropy equation then becomes:

    ∑ p(i)*log2(1/p(i)) where the sum is from i=1 to i=inf
    
    Solving this, we get the sum is 2.  So our entropy is 2.

    We can also think about it statistically.
    A geometric distribution tell us the probability of achieving
    our first success after a certain number of failures.
    If the probability of success is 'p', then the number of 
    times we must repeat our experiment before getting that
    success is simply 1/p.  Therefore, for a fair coin,
    we can expect 1/0.5 = 2 flips before our first head.
    This includes the flip to get the head.
    The number 2 is represented with 2 bits: '10'.  Therefore,
    we need 2 bits to represent the entropy.
    """


    """
    The entropy of the number of questions we ask is 2.
    Suppose we go down the path we took beforehand.
    "Is x=1": did you get a heads on the 1st try
    "Is x=2": did you get a heads on the 2nd try
    ...
    "Is x=inf": did you get a heads on the inf try

    We'll end the question-asking with some probability once the
    person is done flipping their coin.
    "Is x=1": 1/2 of the time, this is all we need/this was the head flip
    "Is x=2": (1/2)^2 of the time, we get here and this is all we need/this was the head flip
    ...

    To find the expected number of questions we'll ask, let's find E(q)
    where q is the number of questions we ask.
    Mathematically, this is 
    ∑ q*(1/2)*q from q=1 to inf
    So if q=2, this means we asked 2 questions, and the 2nd was a yes with (1/2)^2 probability.

    It turns out this is the exact same logic as what we showed up above with finding
    the entropy of H(X), so we can expect to ask around 2 questions.
    """
