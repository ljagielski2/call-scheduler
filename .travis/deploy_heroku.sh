#!/bin/sh
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
docker login -u _ --password=$HEROKU_API_KEY registry.heroku.com
#heroku container:push web --app $HEROKU_APP_NAME
docker tag ljagielski2/call-scheduler:latest registry.heroku.com/$HEROKU_APP_NAME/web
docker push registry.heroku.com/$HEROKU_APP_NAME/web
