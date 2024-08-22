import requests
from bs4 import BeautifulSoup
from bin import download_subtitle
from uwar import get_subtitles
from rase import sanitize_filename


def search_movie_subtitles(movie_name):
    search_url = f"https://www.opensubtitles.org/en/search2/sublanguageid--ara,eng,fre/moviename-{movie_name.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        movie_rows = soup.select('tbody tr.change')
        movie_list = []
        for row in movie_rows:
            movie_title_element = row.find('strong').find('a')
            if movie_title_element:
                movie_title = movie_title_element.text.strip()
                movie_link = "https://www.opensubtitles.org" + movie_title_element.get('href')
                movie_year = movie_title.split()[-1].strip('()')
                imdb_rating_element = row.find('td', align='center').find('a')
                imdb_rating = imdb_rating_element.text.strip() if imdb_rating_element else 'N/A'

                movie_list.append({
                    'title': movie_title,
                    'year': movie_year,
                    'link': movie_link,
                    'imdb_rating': imdb_rating
                })
        return movie_list
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return None



# Main program flow
movie_name = input("Enter the movie name: ")
movies = search_movie_subtitles(movie_name)

if movies:
    print("\nFound Movies:")
    for idx, movie in enumerate(movies, start=1):
        print(f"{idx}. {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
        print(f"   Link: {movie['link']}\n")

    movie_choice = int(input("Select a movie by number to see available subtitles: "))
    if 1 <= movie_choice <= len(movies):
        movie_url = movies[movie_choice - 1]['link']
        subtitles = get_subtitles(movie_url)

        if subtitles:
            print("\nAvailable Subtitles:")
            for idx, subtitle in enumerate(subtitles, start=1):
                print(f"{idx}. {subtitle['title']} ({subtitle['language']}) - {subtitle['file_type']} - Rating: {subtitle['rating']}")
                print(f"   Upload Date: {subtitle['upload_date']}")
                print(f"   Download Link: {subtitle['download_link']}\n")

            subtitle_choice = int(input("Select a subtitle by number to download: "))
            if 1 <= subtitle_choice <= len(subtitles):
                selected_subtitle = subtitles[subtitle_choice - 1]
                download_url = selected_subtitle['download_link']
                filename = sanitize_filename(f"{selected_subtitle['title'].replace(' ', '_')}_{selected_subtitle['upload_date'].replace(' ', '_').replace('/', '-')}.srt")
                
                # Ensure the filename does not include newline characters
                filename = filename.replace('\n', '')

                download_subtitle(download_url, filename)
            else:
                print("Invalid subtitle choice.")
        else:
            print("No subtitles found.")
    else:
        print("Invalid movie choice.")
else:
    print("No movies found.")
