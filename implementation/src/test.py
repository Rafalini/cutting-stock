import random

def random_sum_to_n(N):
    remaining_sum = N
    result = []

    while remaining_sum > 0:
        # Generate a random number between 1 and the remaining sum
        random_num = random.randint(1, remaining_sum)
        
        # If the remaining sum is greater than the random number, append the random number
        if remaining_sum > random_num:
            result.append(random_num)
            remaining_sum -= random_num
        else:
            # If the remaining sum is less than or equal to the random number, append the remaining sum
            result.append(remaining_sum)
            break

    return result

# Example usage:
N = 20  # Replace this number with the desired value of N
random_numbers = random_sum_to_n(N)
print(f"Random numbers summing up to {N}: {random_numbers}")
print(f"Sum: {sum(random_numbers)}")
