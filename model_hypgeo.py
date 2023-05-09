'''
This module contains a model that calculates the probability of drawing 
a sample hand from a deck with the hypergeometric cumulative distribution function.
'''

# Imports.
from itertools import product
from methods_for_model import *
from observer_subject import Subject

# Classes.
class Model_Hypgeo(Subject):
    '''
    Model which calculates the probability of drawing a sample hand 
    from a deck with the hypergeometric cumulative distribution function.
    '''
    def __init__(self):
        Subject.__init__(self)          # Inheritance of Observer pattern.
        self.deck_size = 0              # Number of cards in deck.
        self.sample_size = 0            # Size of the sample of cards drawn.
        self.defined_pools = []         # Each list element is a pool (type = list). [[card_count, min_in_sample, max_in_sample], [...], [...], etc.]
        self.unassigned_cards = 0       # Number of cards that are in no pool
        self.result = None              # Store the result of the last calculation.

    # Set functions
    def set_deck_size(self, integer):
        '''
        Sets self.deck_size to integer, updates self.unassigned_cards.
        '''
        if check_positive_int(integer):
            self.deck_size = integer
            self.update_unassigned_cards()
        else:
             self.notify("invalid_deck_size")
        
    def set_sample_size(self, integer):
        '''
        Sets self.sample_size to integer.
        '''
        if check_positive_int(integer) and integer <= self.deck_size:
            self.sample_size = integer
        else:
            self.notify("invalid_sample_size")

    def add_defined_pool(self, card_count, min_in_sample, max_in_sample):
        '''
        Adds a new pool to self.defined_pools. Needs three integers.
        self.unassigned_cards >= card_count >= max_in_sample >= min_in_sample
        Updates self.unassigned_cards. 
        '''
        if check_positive_int(card_count) and check_positive_int(min_in_sample) and check_positive_int(max_in_sample) \
                                          and self.unassigned_cards >= card_count >= max_in_sample >= min_in_sample:
            self.defined_pools.append([card_count, min_in_sample, max_in_sample])
            self.update_unassigned_cards()
        else:
            self.notify("invalid_pool")
        

    def remove_defined_pool(self, index):
        '''
        Removes a pool from self.defined_pools. index = integer for accessing the pool.
        '''
        list_length = len(self.defined_pools)
        if type(index) == int and index < list_length and index >= -(list_length):
            self.defined_pools.pop(index)
        else:
            self.notify("invalid_removal_index")

    def update_unassigned_cards(self):
        '''
        Updates self.unassigned_cards if self.deck size != None.
        '''
        self.unassigned_cards = self.deck_size
        for li in self.defined_pools:
            self.unassigned_cards -= li[0]

    def calculate_combinations(self):
        '''
        Get a list with all possible slot sizes of each pool (also lists) and return it.
        '''
        slot_sizes = []
        for pool in self.defined_pools:                 # Get a list with all possible slot sizes of each pool.
            size_list = []
            size_list = list(range(pool[1], min(pool[0], pool[2], self.sample_size) + 1))
            slot_sizes.append(size_list)

        combination_table = list(product(*slot_sizes))  # The combination_table is a list containing tuples. Every tuple of product() contains exactly one element from each sublist of slot_sizes. product() contains all possible combinations.
        return combination_table

    def calculate(self):
        '''
        Calculate the probability of drawing the configured hand in the deck_manager() and return it.
        '''
        self.notify("start calculate")                                              # Notifiy the Observers that the calculation will start, so the last parameters can be set before calculation.
        binomial_list_table = []                                                    # Stores multiple lists which themself contain binomial coeffiecents. Each sublist contains a set of binomial coeffiecents that are needed for one hypgeo_pdf.
        combination_table = self.calculate_combinations()                           # Raw data from the pools for calculating binomial coeffiecents.                      
        for combination in combination_table:
            size_sum = sum(combination)                                             # How many slots of sample_size are in a defined pool.
            size_rest = self.sample_size - size_sum                                 # Not all slots of the sample hand must be occupied by a pool. Here, the size of the rest slot is calculated and stored in size_rest.
            if size_sum <= self.sample_size and size_rest <= self.unassigned_cards: # All slot sizes added up must not exceed the self.sample_size (You can't draw more cards than self.sample_size.). Also, there must be enough unassigned cards to fill size_rest.
                index = 0                                                           # index count variable which we need for accessing certain elements in pool_lists.
                binomial_list = []                                                  # Store the binomial coefficient of each in_sample in one combination.
                for in_sample in combination:                                       # in_sample = we select that many cards from that pool. The binomial coeffiecent is calcualted with n = (total cards in the pool) and k = in_sample.
                    binomial_list.append(binomial_coefficient(self.defined_pools[index][0], in_sample))
                    index += 1                                          
                binomial_list.append(binomial_coefficient(self.unassigned_cards, size_rest))    # Calculate the binomial coefficient of the rest, n = self.unassigned_cards, k = size_rest.
                binomial_list_table.append(binomial_list)                                       # Add the rest binomial coefficient to the list. Now, all slots of the sample hand are occupied by something.

        divisor = binomial_coefficient(self.deck_size, self.sample_size)                        # All possible samples that a deck can produce which includes successes and failures. It is the divisor of the probability.   

        dividend = 0                            # All successfull, possible samples that this deck can produce. It is the dividend of the probability.
        for binomial_list in binomial_list_table:                                                                         
            temp_factor = 1
            for value in binomial_list:         # If we multiply all binomial coefficients of one combination, we get the number of successful samples that one combination adds to the overall probability (the dividend of the hypergeometric probability distribution function of this exact combination).
                temp_factor *= value                
            dividend += temp_factor             # We add all dividends of the hypgeo. pdfs together and get the number of all possible successfull samples(the dividend of the hypergeometric cumulative distribution function).
        hypgeo_cdf = dividend / divisor         # We get the hypgeo. cdf by dividing (successful samples) / (possible samples).
        self.result = hypgeo_cdf                # Set self.result.
        self.notify("end calculte")             # Notify the Observers that the caluclation has finished.
    
    # Get methods.
    def get_deck_size(self):
        return self.deck_size
    
    def get_sample_size(self):
        return self.sample_size
    
    def get_defined_pools(self):
        return self.defined_pools
    
    def get_unassigned_cards(self):
        return self.unassigned_cards

    def get_result(self):
        return self.result


# Testing this model class.
if __name__ == "__main__":
    hypgeo = Model_Hypgeo()
    hypgeo.set_deck_size(40)
    hypgeo.set_sample_size(5)
    hypgeo.add_defined_pool(10, 1, 5)
    hypgeo.remove_defined_pool(0)
    hypgeo.add_defined_pool(3, 1, 3)
    hypgeo.calculate()
    print(hypgeo.result)
