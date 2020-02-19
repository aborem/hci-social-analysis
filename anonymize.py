import csv
from random import randint

def anonymize(filepath):
	file = open(filepath)
	reader = csv.reader(file)
	messages = list(reader)

	messages = [message for message in messages if message[3].count(',') < 2]

	contacts = []
	while len(contacts) < 4:
		contact = messages[randint(0, len(messages))][3]
		if contact not in contacts:
			contacts.append(contact)

	print(pseudonyms)

	to_write = []
	for row in messages:
		if row[3] not in pseudonyms:
			continue
		modified_date = row[0][:19]
		modified_content = "#"*len(row[2])
		to_write.append([modified_date] + [row[1]] + [modified_content] + [pseudonyms[row[3]]] + row[4:])
	write_file = open("anonymized.csv", 'w')
	writer = csv.writer(write_file)
	writer.writerows(to_write)

# replace with name of file
anonymize('0.csv')
