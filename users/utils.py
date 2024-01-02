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


