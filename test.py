test_data = open("EvaluationSetAllInstances.txt").read().split("\n")
test_data.pop(0)
for line in test_data:
	parts = line.split("\t")
	label = parts.pop(0)
	for clip in parts:
		print find_keywords(clip)
