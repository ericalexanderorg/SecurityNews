FROM python:3

LABEL "com.github.actions.name"="Get RSS Feeds"
LABEL "com.github.actions.description"="Pulls RSS feeds, converts to json dict, and saves to repo."
LABEL "com.github.actions.icon"="message-square"
LABEL "com.github.actions.color"="gray-dark"

LABEL "repository"="https://github.com/ericalexanderorg/SecurityNews/ACTIONS/GET-RSS"
LABEL "homepage"="https://github.com/ericalexanderorg/SecurityNews/ACTIONS/GET-RSS"
LABEL "maintainer"="Eric Alexander"

COPY "entrypoint.py" "/entrypoint.py"
RUN chmod +x /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]