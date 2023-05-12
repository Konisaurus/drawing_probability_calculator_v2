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
        self.defined_groups = {}        # Each element is a group (type = list). {"number": [card_count, min_in_sample, max_in_sample], "number": [...], etc.]
        self.group_key = 0
        self.unassigned_cards = 0       # Number of cards that are in no group
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
             self.notify("invalid deck size")
        
    def set_sample_size(self, integer):
        '''
        Sets self.sample_size to integer.
        '''
        if check_positive_int(integer) and integer <= self.deck_size:
            self.sample_size = integer
        else:
            self.notify("invalid sample size")

    def add_defined_group(self, card_count=0, min_in_sample=0, max_in_sample=0):
        '''
        Adds a new group to self.defined_groups. Needs three integers.
        self.unassigned_cards >= card_count >= max_in_sample >= min_in_sample
        Updates self.unassigned_cards. 
        '''
        if check_positive_int(card_count) and check_positive_int(min_in_sample) and check_positive_int(max_in_sample) \
                                          and self.unassigned_cards >= card_count >= max_in_sample >= min_in_sample:
            self.defined_groups[self.group_key] = [card_count, min_in_sample, max_in_sample]
            self.group_key += 1
            self.update_unassigned_cards()
        else:
            self.notify("invalid_pool")
        
    def set_defined_group_size(self, key, card_count):
        try:
            if check_positive_int(card_count) and card_count <= self.unassigned_cards and card_count >= (self.defined_groups[key][1] and self.defined_groups[key][2]):
                self.defined_groups[key][0] = card_count
                self.update_unassigned_cards()
            else:
                self.notify("invalid group size", group_key=key)
        except:
            pass

    def set_defined_group_min(self, key, min_in_sample):
        try:
            if check_positive_int(min_in_sample) and min_in_sample <= self.defined_groups[key][2]:
                self.defined_groups[key][1] = min_in_sample
            else:
                self.notify("invalid group min", group_key=key)
        except:
            pass

    def set_defined_group_max(self, key, max_in_sample):
        try:
            if check_positive_int(max_in_sample) and max_in_sample >= self.defined_groups[key][1] and max_in_sample <= self.defined_groups[key][0]:
                self.defined_groups[key][2] = max_in_sample
            else:
                self.notify("invalid group max", group_key=key)
        except:
            pass
            
    def del_defined_group(self, key):
        '''
        Deletes a group from self.defined_groups. index = integer for accessing the group.
        '''
        try:
            self.defined_groups.pop(key)
            self.update_unassigned_cards()
        except:
            pass

    def update_unassigned_cards(self):
        '''
        Updates self.unassigned_cards.
        '''
        self.unassigned_cards = self.deck_size
        for key in self.defined_groups:
            self.unassigned_cards -= self.defined_groups[key][0]

    def calculate_combinations(self):
        '''
        Get a list with all possible slot sizes of each group (also lists) and return it.
        '''
        slot_sizes = []
        for key in self.defined_groups:                 # Get a list with all possible slot sizes of each group.
            size_list = []
            group = self.defined_groups[key]
            size_list = list(range(group[1], min(group[0], group[2], self.sample_size) + 1))
            slot_sizes.append(size_list)

        combination_table = list(product(*slot_sizes))  # The combination_table is a list containing tuples. Every tuple of product() contains exactly one element from each sublist of slot_sizes. product() contains all possible combinations.
        return combination_table
    

    def calculate(self):
        '''
        Calculate the probability of drawing the configured hand in the deck_manager() and return it.
        '''
        self.notify("start calculate")                                              # Notifiy the Observers that the calculation will start, so the last parameters can be set before calculation.
        defined_groups = convert_dict_to_list(self.defined_groups)                  # Convert dict to list (index not needed).
        binomial_list_table = []                                                    # Stores multiple lists which themself contain binomial coeffiecents. Each sublist contains a set of binomial coeffiecents that are needed for one hypgeo_pdf.
        combination_table = self.calculate_combinations()                           # Raw data from the groups for calculating binomial coeffiecents.                      
        for combination in combination_table:
            size_sum = sum(combination)                                             # How many slots of sample_size are in a defined group.
            size_rest = self.sample_size - size_sum                                 # Not all slots of the sample hand must be occupied by a group. Here, the size of the rest slot is calculated and stored in size_rest.
            if size_sum <= self.sample_size and size_rest <= self.unassigned_cards: # All slot sizes added up must not exceed the self.sample_size (You can't draw more cards than self.sample_size.). Also, there must be enough unassigned cards to fill size_rest.
                index = 0                                                           # index count variable which we need for accessing certain elements in group_lists.
                binomial_list = []                                                  # Store the binomial coefficient of each in_sample in one combination.
                for in_sample in combination:                                       # in_sample = we select that many cards from that group. The binomial coeffiecent is calcualted with n = (total cards in the group) and k = in_sample.
                    binomial_list.append(binomial_coefficient(defined_groups[index][0], in_sample))
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
    
    def get_defined_groups(self):
        return self.defined_groups
    
    def get_unassigned_cards(self):
        return self.unassigned_cards
    
    def get_group_size(self, key):
        return self.defined_groups[key][0]
    
    def get_group_min(self, key):
        return self.defined_groups[key][1]
    
    def get_group_max(self, key):
        return self.defined_groups[key][2]

    def get_result(self):
        return self.result

# Testing this model class.
if __name__ == "__main__":
    hypgeo = Model_Hypgeo()
    hypgeo.set_deck_size(40)
    hypgeo.set_sample_size(5)
    hypgeo.add_defined_group(3, 1, 3)
    hypgeo.add_defined_group(5, 2, 3)
    hypgeo.add_defined_group(5, 2, 3)
    hypgeo.del_defined_group(1)
    hypgeo.calculate()
