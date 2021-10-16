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
        TsvPreparer.wash_tsv(file_path, "downloaded_and_washed.tsv")

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
    def wash_tsv(input_file_name, output_file_name):
        default_img_url = "_"
        output_file = open(output_file_name, "w", encoding="utf-8")
        # output_file = open(output_file_name, "w")
        output_file.write(f"id\ttitle\trelease_year\timdb_id\timg_url\n")
        with open(input_file_name, "r", encoding="utf-8") as input_file:
            internal_id = 0
            for entry in input_file.readlines():
                splitted_entries = entry.split("\t")
                imdb_id = splitted_entries[0]
                title_type = splitted_entries[1]
                title = splitted_entries[3]
                release_year = splitted_entries[5]

                if release_year.isdigit() \
                        and title != "\\N" \
                        and len(title) < 200 \
                        and int(release_year) > 1950 \
                        and title_type == "movie":
                    output_file.write(f"{internal_id}\t{title}\t{release_year}\t{imdb_id}\t{default_img_url}\n")
                    internal_id += 1
        output_file.close()

    @staticmethod
    def add_urls(input_file_name, output_file_name):
        """
        Input file is expected to be a tab separated list with "id, title, release_year":
        tt0015724       Dama de noche   1993
        tt0016906       Frivolinas      2014
        """
        import requests
        from bs4 import BeautifulSoup

        with open(input_file_name, 'r') as input_file:
            lines = input_file.readlines()
        assert lines

        with open(output_file_name, 'w') as output_file:
            for line in lines:
                splitted_lines = line.split("\t")
                movie_id = splitted_lines[0]
                r = requests.get(f'https://www.imdb.com/title/{movie_id}')
                if r:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    if soup:
                        url = soup.img['src']
                        if url.startswith("//fls"):
                            print(f"Only got a pixel for {movie_id}: {url}")
                            url = None
                        title = splitted_lines[1]
                        release_year = splitted_lines[2]
                        output_file.write(f'{movie_id}\t{title}\t{release_year}\t{url}\n')
                    else:
                        print(f"Could not make soup from {movie_id}")
                else:
                    print(f"Did not find {movie_id}")


if __name__ == "__main__":
    # TsvPreparer.run()
    TsvPreparer.wash_tsv("title.basics.tsv", "ws6.tsv")
    # TsvPreparer.add_urls(input_file_name="washed_movies_2.tsv",
    #                      output_file_name="washed_movies_2_with_urls.tsv")
