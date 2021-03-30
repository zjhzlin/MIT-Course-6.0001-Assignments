# Problem Set 4A
# Name: Lynn Zhang
# Collaborators:
# Time Spent: 72min
# 2021-03-25 12min 08:43 - 08:55
# 2021-03-26 22min 22:48 - 23:10 stuck in recursive
# 2021-03-27 use function! abstract - get_newsequence put one character into the sequence - different order
# 2021-03-27 38min 07:46 - 08:24 pay attention to the difference between list.append() and list1+list2 (multiple items in list)

def get_newstring(character, string):
    '''
    insert the character into different positions of the string
    Args:
        character:'str' type, the character to insert in to different positions of the string
        string:'str' type

    Returns: the list with different combinations of character + string
    '''
    # get the string's length
    new_list = []
    len_string = len(string)
    # keep track of the index the character is going to insert into, insert character from beginning to end of the string
    for index in range(len_string+1):
        # each loop: update the string into a new string, putting the first character into different positions
        # put the character into the starting position
        if index == 0:
            new_string = character + string
        # put in the end position
        elif index == len_string:
            new_string = string + character
        # when in between
        else:
            new_string = string[0:index] + character + string[index:]
        # update the list with the new string
        new_list.append(new_string)
    return new_list


def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    # keep track of the final list
    final_list =[]
    # base case: for single character, return a singleton list
    if len(sequence) == 1:
        final_list.append(sequence)
    # else recursive case
    else:
        # get the first character,
        # and for each permutation of the rest characters, get new strings
        first_character = sequence[0]
        remaining_characters = sequence[1:] # use index to track the position?
        permutation_list = get_permutations(remaining_characters)
        # fyi: when use append to join two lists with multiple items, permutations is a list with list as element
        # fyi: so then change to using list+list
        # go into the loop -> each permutation
        for string in permutation_list:
            # fyi: wrong code note bofore - for each string in the permutation list, get the new combination list and append to final list
            # fyi: wrong code before, when using append - get the string in the single item(which is a list) of the permutation_list
            # correct way to join two lists with multiple items, use list 1 + list 2
            final_list += get_newstring(first_character, string) # append is used for single item adding.
    return final_list


if __name__ == '__main__':
   #EXAMPLE
   example_input = 'abc'
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output:', get_permutations(example_input))

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)

   # test case 1
   print('Test case 1')
   test_input = 'lyn'
   print('Input:', test_input)
   print('Expected Output:', ['lyn', 'lny', 'yln', 'ynl', 'nly', 'nyl'])
   print('Actual Output:', get_permutations(test_input))

   print('Test case 2')
   test_input = 'cod'
   print('Input:', test_input)
   print('Actual Output:', get_permutations(test_input))
   


