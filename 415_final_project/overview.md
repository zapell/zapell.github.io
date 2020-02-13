## NBA Salary Analysis

### Overview
The first part of this project was using the 2017-2018 NBA season advanced player statistics to predict salary.  This type of model can be useful for determining free agent value and applied to players on rookie contracts.  The data was taken from [kaggle](https://www.kaggle.com/aishjun/nba-salaries-prediction-in-20172018-season).  A lot of preprocessing had to be done for this dataset including deleting players with very little playing time, injured players, and splitting rookie and veteran contracts.  The veteran dataset was then split into train and test sets.

### Data Visualization
Using Tableau I made a visualization of salary vs draft position.  

![visual](./draft_position_vs_salary.png)  
The blue points are players under 25, the majority of whom are on rookie contracts.  The reason there is a veteran/rookie split is there is a clear trend by draft pick for rookie contracts and it is clear that the only determining factors for their deals are draft position and draft year.  The few players under 25 not on rookie deals were moved to the veteran dataset as well as the few players over 25 who were on rookie deals still.