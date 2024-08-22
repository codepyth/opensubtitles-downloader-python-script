import requests
from bs4 import BeautifulSoup


def get_subtitles(movie_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(movie_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        subtitle_rows = soup.select('tbody tr.change')
        subtitles_list = []

        for row in subtitle_rows:
            subtitle_title_element = row.find('strong')
            if subtitle_title_element:
                subtitle_title = subtitle_title_element.find('a').text.strip()

                # Find the correct <td> that contains the <span class="p">srt</span> and extract the download link
                subtitle_td = row.find(lambda tag: tag.name == 'td' and tag.find('span', class_='p') and tag.find('span', class_='p').string == 'srt')
                download_link_element = subtitle_td.find('a', href=True) if subtitle_td else None
                download_link = download_link_element.get('href') if download_link_element else None

                language_element = row.find('td', align='center').find('div', class_='flag')
                language = language_element.get('title') if language_element else 'N/A'

                file_type = subtitle_td.find('span', class_='p').text.strip() if subtitle_td else 'N/A'
                upload_date = row.find('time').get('title') if row.find('time') else 'N/A'
                rating = row.find('span', title=lambda x: x and 'votes' in x).text.strip() if row.find('span', title=lambda x: x and 'votes' in x) else 'N/A'

                subtitles_list.append({
                    'title': subtitle_title,
                    'download_link': "https://www.opensubtitles.org" + download_link if download_link else "No download link found",
                    'language': language,
                    'file_type': file_type,
                    'upload_date': upload_date,
                    'rating': rating,
                })

        return subtitles_list
    else:
        print(f"Failed to retrieve subtitles. Status code: {response.status_code}")
        return None
