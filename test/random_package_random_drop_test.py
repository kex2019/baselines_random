import baselines_random.random_package_random_drop as rprd
print("Starting evaluation")
rprd.evaluate(render=True, robots=2, spawn=10, capacity=2, shelve_length=5, shelve_width=2, shelve_height=2, steps=1000, periodicity_lower=200, periodicity_upper=700, collect=True)

