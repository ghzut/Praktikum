import numpy as np
def weighted_avg_and_std(values, weights):
	average = np.average(values, weights=weights)
	variance = np.average((values-average)**2, weights=weights)
	return (average, np.sqrt(variance))
