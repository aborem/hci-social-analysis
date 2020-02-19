def multiple_texting(filepath):
	import csv
	from datetime import datetime

	file = open(filepath)
	reader = csv.reader(file)
	messages = list(reader)

	formatted_messages = {}
	actual_messages = []
	for row in messages:
		sent = row[1] == "sent"
		name = row[3]
		raw_time = row[0] if len(row[0]) == 19 else row[0][:20]
		time = datetime.strptime(raw_time, '%Y-%m-%d %H:%M:%S')
		if name not in formatted_messages:
			formatted_messages[name] = []
		formatted_messages[name].append((time, sent))
		actual_messages.append((name, time, sent))
		
	actual_messages.sort(key = lambda x : x[1])

	max_messages = max([len(v) for v in formatted_messages.values()])
	scores = {name : len(messages) for name, messages in formatted_messages.items()}

	i = 0
	while i < len(actual_messages) - 4:
		name, current_time, sent = actual_messages[i]
		j = i + 1
		multiplier = 0
		while j < i + 4:
			if actual_messages[i][2] != sent:
				break
			new_time = actual_messages[j][1]
			time_diff = new_time - current_time
			if time_diff.total_seconds() <= 60:
				multiplier += 1
				j += 1
			else:
				break
		weight = 0.3 if sent else 0.2
		scores[name] += (1 + weight*multiplier)
		i = j

	max_score = max(scores.values())
	return {n : (scores[n] / max_score) for n in scores}

print(multiple_texting('arthur_borem_data.csv'))
