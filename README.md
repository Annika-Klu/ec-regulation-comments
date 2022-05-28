# Comments on the European Commission's regulation draft concerning the digital COVID certificate
***a project to practice scraping and evaluating data***

## What this is
When I came across [this page](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13375-Extension-of-EU-Digital-COVID-Certificate-Regulation/feedback_en?p_id=27926341)
by the European Commission concerning the extended use of the COVID certificate, I noticed there were tons of comments on it, some of which have apparently been posted multiple times.
There are comments in many different languages, but certain topics seem to recur. Having been looking for a project to practice scraping data and evaluating it, I decided to go for these comments. 

## How I do it
The project is scripted in Python using some native libraries and these main external ones:
- selenium, which can run a browser driver and extract the pages' source
- bs4 that I'm using BeautifulSoup from, a package that helps extract data from HTML or XML content
- pymongo client for connecting to the database and adding/editing its content
- dotenv so I can import sensitive data from a local .env file.

In order for selenium to be able to run the browser, you will need to download/install
- the broser of your choice (selenium supports many) | for this project: Firefox
- the respective driver to use with automated processes. | for this project: geckodriver

Eventually, I deployed the script to a platform because there are more than 380k comments (10 per page) - and because I wanted to learn about how I can let "someone else" run my script. 😉
The script is now on Heroku with a [worker](https://devcenter.heroku.com/articles/background-jobs-queueing) set so I can start/stop it;
this required different/additional configs for Heroku's linux environment, also I ended up using Chrome there because I kept having issues with Firefox crashing. 
I'll eventually publish the remote scraper script as well, either on a separate branch here or in a different repo.

## Project status and "to do"
- [x] script to scrape the page for all comments ✔️
- [x] make script insert comments into a database ✔️
- [x] deploy script so the scraping & database inserting is automated ✔️
- [ ] write methods for evaluating the comments (for main actions, e. g. "comments_by_page", and helpers, e. g. "group_by") 💡
- [ ] evaluate comments 💡
- [ ] think of a nice way to present results - maybe even visually, adding a frontend to this 💡

***Thanks for stopping by - hope you enjoy this project!***
