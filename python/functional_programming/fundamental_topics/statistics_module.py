"""
statistics - the standard library's measures of central tendency and spread.

Demonstrates the twelve core measures on one small fixed dataset: mean,
median, mode, and the trimmed variants, plus the distribution measures
variance, standard deviation and quantiles. Every function here takes a data
series and returns a number, with no external state.
"""

import statistics # Investigate more at https://docs.python.org/3/library/statistics.html

ages = [2, 4, 4, 4, 5, 5, 7, 9] # A small fixed dataset used by every demonstration below

# central tendency

arithmetic_mean = statistics.mean(ages) # The plain average: sum divided by count (returns 5)

print(arithmetic_mean)

float_mean = statistics.fmean(ages) # A faster float-based average for large data (returns 5.0)

print(float_mean)

geo_mean = statistics.geometric_mean([4, 9]) # The n-th root of the product, good for growth rates (returns 6.0)

print(geo_mean)

harmonic_mean = statistics.harmonic_mean([1, 2, 3, 6]) # Reciprocal average, used for rates and speeds (returns 2.0)

print(harmonic_mean)

middle_value = statistics.median(ages) # The middle value, robust to outliers (returns 4.5)

print(middle_value)

lower_middle = statistics.median_low(ages) # The lower of the two middle values on an even-sized set (returns 4)

print(lower_middle)

upper_middle = statistics.median_high(ages) # The upper of the two middle values on an even-sized set (returns 5)

print(upper_middle)

most_common = statistics.mode(ages) # The single most frequently occurring value (returns 4)

print(most_common)

all_modes = statistics.multimode(ages) # Every value tied for most frequent (returns [4])

print(all_modes)

# spread

sample_variance = statistics.variance(ages) # Average squared deviation from the mean, denominator n-1 (returns 4.571428571428571)

print(sample_variance)

sample_deviation = statistics.stdev(ages) # Square root of the variance, in the original units (returns 2.138089935299395)

print(sample_deviation)

population_deviation = statistics.pstdev(ages) # Standard deviation of the whole population, denominator n (returns 2.0)

print(population_deviation)