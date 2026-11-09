import numpy as np

n_simulations = 10000

profits = []

for _ in range(n_simulations):

    # Revenue uncertainty (15%)
    revenue = np.random.normal(
        loc=10_000_000,
        scale=1_500_000
    )

    # Labor cost uncertainty (10%)
    labor_cost = np.random.normal(
        loc=4_000_000,
        scale=400_000
    )

    # Material cost uncertainty (20%)
    material_cost = np.random.normal(
        loc=2_000_000,
        scale=400_000
    )

    # Delay penalty
    penalty = 500_000 if np.random.rand() < 0.2 else 0

    profit = revenue - labor_cost - material_cost - penalty

    profits.append(profit)

profits = np.array(profits)

# print(f"Average profit: {profits.item:,.0f}")
print(f"Average profit: {profits.mean():,.0f}")
print(f"P10: {np.percentile(profits,10):,.0f}")
print(f"P90: {np.percentile(profits,90):,.0f}")

loss_probability = np.mean(profits < 0)

print(f"Probability of loss: {loss_probability:.2%}")



import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.hist(profits, bins=50, edgecolor='black')
plt.xlabel("Profit (€)")
plt.ylabel("Frequency")
plt.title("Monte Carlo Profit Distribution")
plt.grid(True, alpha=0.3)

plt.show()