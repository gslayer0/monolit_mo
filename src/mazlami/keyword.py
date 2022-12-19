import re, csv

with open("reserved_words_PHP.txt", "r") as f:
    final_result = []
    lines = f.readlines()
    for line in lines:
        if re.match(r"\W*_*[a-zA-Z]", line):
            word = line.strip()
            if word[-1] == ".":
                word = word[:-1]
            final_result.append(word)

print(final_result)

with open("PHP_reserved_words.csv", "w") as f:
    writer = csv.writer(f)
    for word in final_result:
        writer.writerow([word])
