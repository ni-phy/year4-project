Here I will be keeping a rough timeline of progress for the project.

11/11/2020:
Fitted GP with a mean function to generated data (predicting rotation given age and BV). Will next be looking into generating my own data set to test the process on. 

12/11/2020
Generated some new sample data (with a slightly different form/shape to the data guy produced) to check if my code worked on other data sets - fit very well :)

--- progress made on new data set ---

30/11/2020

Given the newest data set (Mass, temperature, Rotation and Age), I have been able to make accurate predictions for the rotation period given either age or age and mass. The mean functions for both were power laws A*x^b. If the GP is given total freedom in determining the parameters, it does not work too well. Therefore, I fit rough parameters using SciPy optimize. Using these pre-determined values, I managed to get accurate predictions - tight residuals. 

My mean function is of the form P = A*T^c * B*M^d

Where P is rotational period, A is age, M is mass. A, B, c, d are parameters to be determined by fitting power laws and then improved by using the GP. I collapsed A and B into just one constant A. 

Prior to collapsing A and B into one variable, I was having trouble getting accurate predictions once I allowed the parameters to vary.
Parameters A d and c were determined from normal functions centred on the values determined from the SciPy fitting. 
Once a few bugs were ironed out, I have been able to get a very tidy residual plot.
