## Live Betting Data Collection

### Overview
This is a longterm multi-disciplined project I started working on in August 2020.  The main objective is to create a database of live betting data.  I came across many challenges throughout this process, many of which I was unfamiliar with, including selenium, bash scripting, aws ec2 and rds instances.
  
### Structure and Flow
Dynamic live basketball and football data was scraped using a selenium webdriver on a remote AWS ec2 server.  This data was then uploaded to a PostgreSQL database hosted on an aws rds instance.  In order to save money, both the rds and ec2 instances were scheduled to start and stop at specified times using the AWS Cloudwatch service.  
  
The python script to scrape and upload the data is a part of a larger set of bash scripts that runs and checks if the java server running the webdriver is up.
   
Pre and post game data is also scraped for a join later on in the process.
