# pset1_q6.py

"""
Compress the string “abracadabraarbadacarba” using the LZ77 approach 
(sliding windows), with a window size of six and a lookahead buffer 
of size six. Similarly, compress it using the LZ78 and LZW approaches. 
For the LZW approach, assume the letters a, b, c, d, and r start in 
the dictionary in alphabetical order.
"""

# +++++++++++++++++ Installs/Imports +++++++++++++++++ #
 


# ++++++++++++++++++++ Functions +++++++++++++++++++++ #

def find_longest_match_search_buffer(search_buffer, lookahead_buffer):
    """ 
    Helper function for LZ77 compression.
    Finds longest prefix match in lookahead buffer with search buffer. 
    Output: (pos, length) of this prefix in the search buffer.
    If no match, returns (-1, -1).
    """
    # Start with longest prefix in lookahead buffer, and continue shortening it
    for length in range(len(lookahead_buffer), 0, -1):
        # See if the prefix exists in the search buffer
        prefix = lookahead_buffer[:length]
        pos = search_buffer.rfind(prefix) 
        # If it does, return because this is the longest match so far
        # indexing for pos starts at 0 by default
        if pos != -1: 
            return pos, length, prefix
    # If no match then return invalid values
    return -1, -1, ""

def compress_LZ77(value, search_buffer_size, lookahead_buffer_size):
    """ 
    Perform LZ77 compression.
    See tutorial:
    https://www.youtube.com/watch?v=jVcTrBjI-eE

    How it works:
    LZ77 works with two datastructures: search buffer and lookahead buffer
    In this implementation, they are strings
    Search buffer acts like a prior dictionary of what we have seen.
    Lookahead buffer is our current index's character, and some later characters.
    Goal: for current lookahead buffer, match its longest prefix of chars with search buffer
    If we find a match, write (offset, length, prefix) 
    If no match, write (0,0,current character)
    Then, move lookahead buffer to go past the prefix we looked at
    Likewise, move the search buffer same amount to be behind current char index

    Exmaple:
    AABABAC
    Let both buffer's sizes be 3, and we're currently at the third 'A'
    Search buffer: [A, A, B]
    Lookahead buffer: [A, B, A]
    Longest prefix-match in search buffer: 'A', starts 2 chars back from curr char
    Output: (2, 1, 'A')
    """

    # Define variables
    output = [] # list of tuples where each tuple (offset, length, char)
    search_buffer = "" 
    lookahead_buffer = value[:lookahead_buffer_size] if len(value) > lookahead_buffer_size else value
    char_index = 0 # what value are we currently looking at

    while char_index < len(value): # NOTE: may be lookahead-buffer
        # Find the longest match
        pos, length, prefix = find_longest_match_search_buffer(search_buffer, lookahead_buffer)
        # If match exists...
        if pos != -1:
            # Step 1: create output
            # for offset, last char = 1 offset, 2nd to last char = 2 offset, etc.
            offset = len(search_buffer) - pos
            curr_output = (offset, length, prefix)
            output.append(curr_output)
            # Step 2: update search buffer
            # make sure search buffer doesn't exceed max search buffer size
            search_buffer += prefix
            if len(search_buffer) > search_buffer_size:
                num_delete = len(search_buffer) - search_buffer_size
                search_buffer = search_buffer[num_delete:]
            # Step 3: update lookahead buffer
            # Either add so we get lookahead_buf_size # of values or add remaining chars
            lookahead_buffer = lookahead_buffer[length:]
            char_index += length    # update the char_index to reflect the match length
            i = char_index          # add each new char one by one
            while len(lookahead_buffer) < lookahead_buffer_size and i + lookahead_buffer_size <= len(value):
                lookahead_buffer += value[char_index+lookahead_buffer_size-1]
                i += 1
        # If match does not exist...
        else:
            # Step 1: create output
            prefix = value[char_index]
            curr_output = (0, 0, prefix)
            output.append(curr_output)     
            # Step 2: update search buffer
            # make sure search buffer doesn't exceed max search buffer size
            search_buffer += prefix
            if len(search_buffer) > search_buffer_size:
                search_buffer = search_buffer[1:]
            # Step 3: update lookahead buffer
            # Either add so we get lookahead_buf_size # of values or add remaining chars
            lookahead_buffer = lookahead_buffer[1:]
            char_index += 1
            if char_index + lookahead_buffer_size <= len(value):
                lookahead_buffer += value[char_index+lookahead_buffer_size-1]
        #print("P", prefix, "OUT", curr_output, "S", pt2, "L", pt1)
    return output



# ++++++++++++++++++++ Functions +++++++++++++++++++++ #

def find_longest_match_dict(dictionary, lookahead_buffer):
    """
    Helper function for LZ78 compression.
    Finds the longest match of the prefix in the dictionary.
    Returns (index, length) of this match in the dictionary.
    If no match, returns (-1, -1)
    """
    # Start with longest prefix in lookahead buffer, and continue shortening it
    # Once we find a match, return that dictionary's index and length of prefix
    for length in range(len(lookahead_buffer), 0, -1):
        prefix = lookahead_buffer[:length]
        for index, entry in dictionary.items():
            if entry == prefix:
                return index, length
    return -1, -1

def compress_LZ78(value, lookahead_buffer_size):
    """ 
    Perform LZ78 compression.
    Example:
    https://www.researchgate.net/figure/Example-of-compression-process-of-LZ78-for-the-text-data-AABABCAABBAC_fig1_337580417

    How it compares to LZ77:
    Very similar, but instead of using a sliding window, we use a dictionary
    Output: list of tuples, where each is (dict index, next char in dict)
    """
        
    # Define variables
    output = []                 # list of tuples (dict index, next char in dict)
    dictionary = {}             # 'dict' of substrings (keys = indices starting at 1)
    lookahead_buffer = value    # initialize with value, update to relevant part as we go
    char_index = 0              # what char we're looking at (start at 0)

    # While we're not yet at the end of the value string...
    while char_index < len(value): 
        # Find the longest match in the dictionary
        index, length = find_longest_match_dict(dictionary, lookahead_buffer)
        # If we found a match...
        if index != -1:
            # Step 1: create output (index, next character)
            next_char = lookahead_buffer[length] if length < len(lookahead_buffer) else ''
            curr_output = (index, next_char)
            output.append(curr_output)
            # Step 2: update dict
            # add the matched prefix + next char to the dictionary
            new_key = len(dictionary) + 1
            dictionary[new_key] = lookahead_buffer[:length + 1]
            # Step 3: Update the lookahead buffer (advance by the matched length + 1)
            lookahead_buffer = lookahead_buffer[length + 1:]
            char_index += length + 1
        # If no match found...
        else:
            # Step 1: create output (0, current character)
            next_char = lookahead_buffer[0]
            curr_output = (0, next_char)
            output.append(curr_output)
            # Step 2: Update the dictionary (add the current character)
            new_key = len(dictionary) + 1
            dictionary[new_key] = next_char
            # Step 3: move lookahead buffer forward by 1
            lookahead_buffer = lookahead_buffer[1:]
            char_index += 1
    return output

def compress_LZW(value):
    """
    LZW compression algorithm.
    Source:
    https://www.geeksforgeeks.org/lzw-lempel-ziv-welch-compression-technique/
    """

    # Define variables
    # Initialize table with predefined single-character entries
    # let index i represent each value, starting at i=0
    # output made as list of numbers to allow for discrepancy (ex. 1, 0, and 10)
    table = ["a", "b", "c", "d", "r"]
    output = []
    p = value[0]

    for i in range(1, len(value)):
        c = value[i]
        # If p=p+c in table, continue adding to p
        # Goal: see if we can get a bigger prefix to later add
        if p + c in table:
            p = p + c
        # if p+c not in table, make new table entry for p+c and start over with p=c
        else:
            output.append(table.index(p))
            table.append(str(p+c))
            p = c
    # append any residual accumulation from p to output
    output.append(table.index(p))
    return output




# +++++++++++++++++++ Main Function +++++++++++++++++++ #

if __name__ == "__main__":
    # aababcaabbac
    # abracadabraarbadacarba
    # radradra
    str_to_compress = "radradra"
    window_size = 6
    lookahead_buffer_size = 6
    LZ77_compressed = compress_LZ77(str_to_compress, window_size, lookahead_buffer_size)
    LZ78_compressed = compress_LZ78(str_to_compress, lookahead_buffer_size)
    LZW_compressed = compress_LZW(str_to_compress)
    print("LZ77", LZ77_compressed)
    print("LZ78", LZ78_compressed)
    print("LZW", LZW_compressed)

