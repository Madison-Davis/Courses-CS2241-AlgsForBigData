# pset1_q5.py

"""
Consider arithmetic coding for the string abcbaab when the 
probability of an a is 0.2, a b is 0.3, and a c is 0.5. 
Show each step for idealized arithmetic coding, with real 
number arithmetic. Now suppose someone gave you the real 
number 0.63215699. Decode a sequence of length 10 corresponding 
to the above model. For both problems, you should take the 
real interval [0, 1] as broken up into subintervals 
[0, 0.2],[0.2, 0.5] and [0.5, 1], and similarly recursively.
"""

# +++++++++++++++++ Installs/Imports +++++++++++++++++ #
import random 



# ++++++++++++++++++++ Functions +++++++++++++++++++++ #

def arithmetic_encoding(str_to_encode, probs, chars):
    # original window that we focus on
    window = [0, 1]  
    for i, char in enumerate(str_to_encode):
        # find index of char so that we compute window there
        char_index = chars.index(char)
        window_length = window[1] - window[0]
        # compute start for however many levels we've gone down so far
        start = window[0] + sum(window_length * probs[i] for i in range(char_index))
        # the end is simply where we start times the 'width'/prob of that range
        # and finally multiplied by window length
        end = start + window_length * probs[char_index]
        # update window to this new location
        window = [start, end]
        print(f"Step {i}, Window {window}")
    return random.uniform(window[0], window[1])

def arithmetic_decoding(val_to_decode, num_levels, probs, chars, decoded_str = ""):
    # once done with recursion, return the value
    if num_levels == 0:
        return decoded_str
    # compute probability ranges for this level
    sub_windows = {}
    start = 0
    for char, prob in zip(chars, probs):
        sub_windows[char] = (start, start + prob)
        start += prob
    print(f"Level {num_levels}, Value {val_to_decode}, String {decoded_str}")
    print(f"Subwindows for Level {num_levels}: {sub_windows}")
    # identify what character we should append at this level based on sub_windows and val_to_decode
    for char, (window_start, window_end) in sub_windows.items():
        # if the value is in one of the sub_windows
        if window_start <= val_to_decode < window_end:
            new_encoded_val = (val_to_decode - window_end) / (window_start - window_end)
            return arithmetic_decoding(new_encoded_val, num_levels - 1, probs, chars, decoded_str + char)



# +++++++++++++++++++ Main Function +++++++++++++++++++ #

if __name__ == "__main__":
    str_to_encode = "bac"
    str_to_decode = 0.63215699
    chars = ["a", "b", "c"]
    probs = [0.2, 0.3, 0.5]
    print(f"Encoding {str_to_encode}...")
    print(arithmetic_encoding(str_to_encode, probs, chars)) # we find values between [0.23, 0.26 to be sufficient]
    print(f"\nDecoding {str_to_decode}...")
    print(arithmetic_decoding(str_to_decode, 10, probs, chars))