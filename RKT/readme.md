One of the projects I have been focused on is the Dial Prioritization models for unallocated leads.  Specifically, the purchase and refinance retention models.

The project started out with the question: how can we better call potential clients?  What seemed like a simple question becomes more complicated when considering the many different types of clients that we call.  Purchase differs from refinance and both differ from leads that are escalated.  What happens if a banker has clients from different groups in their same pipeline?

The architecture I designed for these models is below
![arch](./dp_architecture.JPG)
Due to the difference in distributions, the values outputted from different models are not comparable.  In order to address this problem, there was a calibration to get the true probability of a loan closing based on the original distribution of the dataset.  This allows us to compare loans across models and accurately organize a banker's pipeline.  We tried different calibration methods, including a Beta correction on undersampled data, Isotonic Regression, and Platt Calibration.

Another key area of this project was the production ready preprocessing.  The processors were designed and tested to be able to handle hourly batch scoring.
