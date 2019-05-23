import csv

washed_content = ""
titles = []
release_years = []
with open('m.tsv', 'r') as movietsv:
    content = movietsv.readlines()

    for entry in content:
        splitted_entry = entry.split('\t')
        release_year = splitted_entry[5]
        if release_year.isdigit():
            release_years.append(release_year)
            titles.append(splitted_entry[3])

with open('washed_movies.tsv', 'w') as movietsv:
    writer = csv.writer(movietsv, delimiter='\t')
    for index, (title, release_year) in enumerate(zip(titles, release_years)):
        writer.writerow([index, title, release_year])
