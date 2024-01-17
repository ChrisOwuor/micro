import random
import hashlib


def generate_account_number(birthdate):
    # Prefix: Concatenate user-related information
    prefix = str(birthdate)[:2]

    # Random Number Component: Generate a random number
    random_number = str(random.randint(100000, 999999))

    # Combine components
    account_number = prefix + random_number

    # Checksum: Use hashlib to create a checksum
    checksum = hashlib.sha256(account_number.encode()).hexdigest()[:3]

    # Finalize the account number
    final_account_number = account_number + checksum

    return final_account_number


def calculate_transaction_cost(amount, type):
    if not amount:
        return "No amount entered"

    cost_ranges = [(0, 1000, 100), (1001, 2000, 200),
                   (2001, 3000, 300), (3001, 5000, 400)]
    if type == "withdraw":
        if amount > 5000:
            return "you have exceeeded the limit"

        for start, end, cost in cost_ranges:
            if start <= amount <= end:
                return cost
    elif type == "deposit":
        return 0
