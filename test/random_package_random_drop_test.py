import baselines_random.random_package_random_drop as rprd
print("Starting evaluation")
rprd.evaluate(render=True, robots=20, spawn=100, shelve_length=5, shelve_width=5, shelve_height=5, steps=1000, collect=True)

