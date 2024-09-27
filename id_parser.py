from bs4 import BeautifulSoup 

# Returns all projects id's on an html page
def find_ids_in_raw_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')

    # Example: Extract project links
    projects = soup.find_all('a', href=True)
    project_ids = set()

    for project in projects:
        href = project['href']
        if "/projects/" in href:
            project_id = href.split("/projects/")[1].split("/")[0]
            if project_id.isdigit():
                project_ids.add(project_id)

    return project_ids
