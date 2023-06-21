import math

# Function to calculate the entropy
def entropy(prob_dist):
    # Regular entropy calculation
    entropy_val = -sum([p * math.log2(p) for p in prob_dist.values()])
    
    # Number of distinct outcomes
    # n = len(prob_dist)
    
    # # Normalizing the entropy
    # entropy_val = entropy_val / math.log2(n)
    
    return entropy_val

# The probability distributions
numbers_prob_dist = {
    5: 0.6,
    4.5: 0.2,
    3: 0.2
    # 1155:0.9,   
    # 155: 0.1
}

equations_prob_dist = {
    'x+y': 0.4,
    '1.5x+1.5y': 0.2,
    '1.5x+1.25y': 0.4
}

# Calculating and printing the entropy for the number and equation distributions
print(f'Normalized entropy for numbers: {entropy(numbers_prob_dist):.2f}')
print(f'Normalized entropy for equations: {entropy(equations_prob_dist):.2f}')
