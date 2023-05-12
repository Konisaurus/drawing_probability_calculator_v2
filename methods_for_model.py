'''
Contains some basic methods for the model.

Included are:
- faculty()
- biomial_coefficient()
- format_float()
'''

# Methods.
def faculty(n):
    '''
    Calculates the faculty n! and returns it.
    '''
    if n < 0 or type(n) != int:
        raise TypeError("not a positive integer.")
    
    n_fak = 1                   # The smallest possible result of faculty is 1.
    if n != 0:                  # 0! is defined as 1.
        for i in range(2,n+1):  # Increase i by one and multiply it with the result before, until i reaches n.
            n_fak *= i
            
    return n_fak                # return result = n!

def binomial_coefficient(n, k):
    '''
    Calculates the binomial coefficient.

    It is defined as:
    n! / [k! * (n - k)!]

    n: The total of distinct items.
    k: Number of particular items chosen from the total.
    
    Note that n >= k >= 0.

    Because faculties have a lot of same factors, we do not have calculate
    the complete faculties. The following code is a more effiecient implementation
    of the binomial coefficient.
    '''
    if 0 <= k <= n:                             
        dividend = 1
        divisor = 1
        for i in range(1, min(n - k, k) + 1):
            dividend *= n
            divisor *= i
            n -= 1
        return int(dividend / divisor)
    
    else:
        raise ("only positive integers which fulfil n >= k >= 0.")

def check_positive_int(value):
    '''
    Returns True if a value is an integer and positive, else returns False.
    '''
    if type(value) == int and value >= 0:
        return True
    else:
        return False
    
def convert_dict_to_list(dictionary):
    '''
    Converts a dicitionary to a list. Basically, it removes the keys.
    '''
    new_list = []
    try:
        for key in dictionary:
            new_list.append(dictionary[key])
        return new_list
    except:
        raise (TypeError, "convert_dict_to_list needs a dict as an argument.")

def format_float(value, decimals=3, factor=1):
    '''
    Formats a float and returns it as a float
    Percentage: True = multiply the float by 100, False = do nothing.
    Decimals: Number of decimals after the coma.
    Value: Flota you want to format.
    '''
    if type(value) == float and check_positive_int(decimals) and type(factor) == int:
        return float("%.{}f".format(decimals) % value)
    else:
        raise ("Values do not fulfil requirements: \n\
               type(value) == int \n\
               type(decimals) == int and decimals >= 0 \n\
               type(factor) == int")
