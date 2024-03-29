## Rocket Mortgage Work

### Dial Prioritization

One of the projects I have been focused on is the Dial Prioritization models for unallocated leads.  Specifically, the purchase and refinance retention models.

The project started out with the question: how can we better call potential clients?  What seemed like a simple question becomes more complicated when considering the many different types of clients that we call.  Purchase differs from refinance and both differ from leads that are escalated.  What happens if a banker has clients from different groups in their same pipeline?

The architecture I designed for these models is below
![arch](./dp_architecture.JPG)
Due to the difference in distributions, the values outputted from different models are not comparable.  In order to address this problem, there was a calibration to get the true probability of a loan closing based on the original distribution of the dataset.  This allows us to compare loans across models and accurately organize a banker's pipeline.  We tried different calibration methods, including a Beta correction on undersampled data, Isotonic Regression, and Platt Calibration.

Another key area of this project was the production ready preprocessing.  The processors were designed and tested to be able to handle hourly batch scoring.  The processors needed to be able to execute on all leads for the hour within the 15 minute lambda timeout window.  These functions did things like clean outliers, fix datatypes, and create new features from the raw data.  After going through the processors, the data was preprocessed by a sklearn preprocessor fitted on the training data for imputation and one hot encoding of categorical variables.

I trained different models and Bayesian hyperparameter tuning jobs to determine the best model.  In order to calibrate the model outputs, I trained another model using Platt Calibration which is a Logistic Regression model trained on the output of the XGBoost model. The data for this second model was the validation set and a portion of the test set, leaving out a portion of the test set to be unseen by either model.  This second model gave us the true probabilities and allowed us to compare different populations of leads against one another.

The result of this process was a 75% conversion lift in the top 3 deciles of leads and an improvement of 47% in our net lead to allocate metric, meaning more leads were getting assigned to bankers.

### Prioritization Engine Model (PEM)

While the dial priority model focused on leads before they reach bankers, the PEM project focused on loans after they were in the bankers pipeline.  Our business partners wanted to know if we could identify loans that had been neglected and apply an escalation treatment to gain conversion.  This process had been in play for post-credit pull when we know a lot more about the client, but the business had struggled with pre-credit treatment for a long time.

After a move to a new operations system, the Revenue Operations team lost the ability to set up a system based test.  This forced me to design a complex SQL query to identify loans in the control group that would have been eligible for treatment since not all loans get neglected.  This query captured 95% of all eligible for escalation loans.  We ensured that the test and control group had an even distribution of lead grade.

We then built a model to identify loans most likely to reach PAL, the next step after a credit pull.  The loans at the top deciles from this model converted at over 2x the conversion of the non treated loans, meaning our model was identifying that portion of neglected loans that should be escalated and keeping out the neglected loans that would be a waste of time.
