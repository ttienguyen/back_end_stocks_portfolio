# Description of the application:
This is a back-end API service designed to support a webapp,"Personal Stock Portfolio". The webapp itself is designed for a single user who wants to know the values of their stocks and the value of the entire stock porfolio. It also plots historical prices and percentage gains(percentage loss) over the past year for a selected stock so that the user can see trends over time. This back-end implements an API to retrieve price information for stocks from an external API server from Alpha Vantage. It stores information about stocks in the user's portfolio and price information retrieved from Alpha Vantage in a Postgres database.

This app was created by Thuytien Nguyen (C17)as a Capstone project for Ada Development Academy.

# Dependencies:
1. This service has been deployed on Heroku.
2. This service relies on an external API server from Alpha Vantage (https://www.alphavantage.co).
3. It needs to have an API key for Alpha Vantage.
4. The implementation depends on various Python packages such as Flask and SQLAlchemy.


# App setup:
As mentioned above, this application has been deployed on Heroku, so it can just be reached via the URL: https://personal-stocks-portfolio.herokuapp.com.

To run from source:
1. Clone the git repository (https://personal-stocks-portfolio.herokuapp.com).
2. cd into the local directory.
3. Required libraries are all in requirements.txt.
4. Run flask server using standard command after all required libraries have been installed with pip.
