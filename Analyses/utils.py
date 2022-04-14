from tqdm import tqdm
import random

def bootstrap_resampling(values):

    seed = 20
    random.seed(seed)

    resample_results = []
    N = 10000

    K = len(values)
    ave = sum(values) / K

    print("Beginning bootstrap resampling")
    for i in tqdm(range(N)):
        samples = random.choices(values, k=K)
        # tie_highest_samples = random.choices(tie_highest_values, k=K)
        
        prop = sum(samples) / K
        resample_results.append(prop)


    sorted_vals = sorted(resample_results)
    lower_bound = int(N * .025)
    upper_bound = int(N * .975)

    lower_error = ave - sorted_vals[lower_bound]
    upper_error = sorted_vals[upper_bound] - ave
    return ave, lower_error, upper_error