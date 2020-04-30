
docker build -t perosa/worldcapitalschatbot .


docker run -p 3978:3978 --rm -it --name worldcapitalschatbot perosa/worldcapitalschatbot


docker tag perosa/worldcapitalschatbot registry.heroku.com/worldcapitalschatbot/web
docker push registry.heroku.com/worldcapitalschatbot/web
heroku container:release web -a worldcapitalschatbot


https://worldcapitalschatbot.herokuapp.com/webhook/status


     