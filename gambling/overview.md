## Live Betting Data Collection

### Overview
This is a longterm multi-disciplined project I started working on in August 2020.  The main objective is to create a database of live betting data.  I came across many challenges throughout this process, many of which I was unfamiliar with, including selenium, bash scripting, aws ec2 and rds instances.
  
### Structure and Flow
Dynamic live basketball and football data was scraped using a selenium webdriver on a remote AWS ec2 server.  This data was then uploaded to a PostgreSQL database hosted on an aws rds instance.  In order to save money, both the rds and ec2 instances were scheduled to start and stop at specified times using the AWS Cloudwatch service.  
  
The python script to scrape and upload the data is a part of a larger set of bash scripts that runs and checks if the java server running the webdriver is up.

The scripts are completely automated and uploaded to the EC2 instance and set to run at gametimes.  The output of the cronjobs are logged to ensure ability to check for possible errors.

Pre and post game data is also scraped for a join later on in the process.


Here is a quick snippet with some of the fields for the in game NBA database.
![snippet](./nba_live_db_ex.png)

### Look Ahead
Currently, I only have framework for NBA and NFL games but it would be very simple to extend to other sports and leagues.

In the future, I want to take a stock market approach to live betting.  Whether that be through arbitrage or options trading techniques, I think there is tremendous opportunity to algorithmically explore the live betting world.
