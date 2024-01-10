# def calculate_transaction_cost(amount):
#     if not amount:
#         return "No amount entered"

#     cost_ranges = [(0, 1000, 3), (1001, 2000, 4), (2001, 3000, 5), (3001, 5000, 6)]

#     for start, end, cost in cost_ranges:
#         if start <= amount <= end:
#             return cost

#     return "No applicable cost for the provided amount"


# # Example usage:
# amount = 150
# cost = calculate_transaction_cost(amount)
# print(f"Transaction cost for {amount}: {cost}")

# class CostGenarator:

#     def __init__(self, amount, range, step):
#         self.amount = amount
#         self.range = range
#         self.step = step

#     def genrate(self):
#         return self.amount


# cost = CostGenarator(100, 200, 2)
# print(cost.genrate())

def calculate_transaction_cost(amount):
    if not amount:
        return "No amount entered"

    cost_ranges = [(0, 1000, 100), (1001, 2000, 200),
                   (2001, 3000, 300), (3001, 5000, 400)]
    if amount > 5000:
        return "you have exceeede the limit"

    for start, end, cost in cost_ranges:
        if start <= amount <= end:
            # cost = calculate_transaction_cost(amount)
            # print(f"Transaction cost for {amount}: {cost}")
            return cost

amount =50000
cost = calculate_transaction_cost(amount)
print(cost)
