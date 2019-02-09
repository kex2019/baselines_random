import baselines_random.random_package_random_drop as rprd
print("Starting evaluation")
rprd.evaluate(render=True, robots=5, shelve_width=10, shelve_height=10, steps=1000)
