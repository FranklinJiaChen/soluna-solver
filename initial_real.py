"""
This script calculate the distribution that the inital Soluna tiles will land on.
"""


import itertools

def coin_flips_distribution():
    outcomes = list(itertools.product(['A', 'B'], ['A', 'C'], ['A', 'D'],
                                      ['B', 'C'], ['B', 'D'], ['C', 'D'], repeat=2))
    distribution = {}
    for outcome in outcomes:
        start_config = tuple(sorted((outcome.count('A'), outcome.count('B'), outcome.count('C'), outcome.count('D')), reverse=True))
        if start_config in distribution:
            distribution[start_config] += 1
        else:
            distribution[start_config] = 1

    return distribution


# Get the distribution
distribution = coin_flips_distribution()
sorted_distribution = dict(sorted(distribution.items()))

# Print the distribution
for dist, count in sorted_distribution.items():
    print(f'Distribution: {dist}, Count: {count}')
