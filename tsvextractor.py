"""
Downloads the latest list with information from imdb and washes it to extract a
unique id, title, and release year.

The resulting file can be imported into the database of this project.
"""
import sys
import csv
import gzip
import shutil


class TsvPreparer:
    @staticmethod
    def run():
        file_path = "."
        TsvPreparer.download(
            url="https://datasets.imdbws.com/title.basics.tsv.gz", file_path=file_path
        )
        TsvPreparer.unzip(file_path)
        TsvPreparer.wash_tsv(file_path)

    @staticmethod
    def download(url, file_path):

        return file_path

    @staticmethod
    def unzip(file_path):
        """Overwrite file_name.tsv.gz with file_name.tsv"""
        with gzip.open(file_path, "rb") as f_in:
            with open(file_path[:-3], "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

    @staticmethod
    def wash_tsv(input_file, output_file):
        pass

    washed_content = ""
    titles = []
    release_years = []
    tsv_file_path = sys.argv[1]
    with open(tsv_file_path, "r") as movietsv:
        content = movietsv.readlines()

        for entry in content:
            splitted_entry = entry.split("\t")
            identifier = splitted_entry[0]
            title = splitted_entry[3]
            release_year = splitted_entry[5]

            if release_year.isdigit() and title != "\\N" and len(title) < 200:
                release_years.append(release_year)
                titles.append(splitted_entry[3])

    with open("washed_movies.tsv", "w") as movietsv:
        writer = csv.writer(movietsv, delimiter="\t")
        for index, (title, release_year) in enumerate(zip(titles, release_years)):
            writer.writerow([index, title, release_year])


if __name__ == "__main__":
    TsvPreparer.run()
