## Diagnosing Diabetes

### Overview
We built a model to predict whether or not a patient had diabetes.
This is useful in rural areas where it would be beneficial to efficiently allocate resources and this model could serve as an initial screening for diabetes. 
We used two different types of models: Logistic Regression and Bayesian Logistic Regression.
One of the main advantages of Bayesian Logistic Regression is the ability to set priors on coefficients.
We used the coefficient estimates from our Logistic Regression as priors for our Bayesian model and seeing how they compare.

### Data
The data for this project was taken from [kaggle](https://www.kaggle.com/uciml/pima-indians-diabetes-database).  Many different algorithms have been applied to this data but there was no mention of using Bayesian Logistic Regression anywhere.  
There were a lot of missing values and after some data cleaning there were 392 obvservations of females of Pima Indian descent.  

![Here](./diabetes_correlation_plot.png)

Above is a correlation plot of the data to give an idea of the relationships between variables.

### Model
We used backward selection on a logistic regression model to determine the best predictors for the Bayesian model.  These predictors were  Age, BloodPressure, Glucose, DiabetesPedigreeFunction, and BMI.  The Bayesian model was coded in STAN and ran in R with the rstan package.  The normal logistic regression model ended up having a better accuracy than the Bayesian version on the test data with a 85% to 70% accuracy edge.  The Bayesian model was limited by the correlations built in to the data and the data which was limited to females aged 21 or older of Pima Indian heritage.
