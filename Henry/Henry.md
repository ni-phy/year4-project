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


03/12/2020
(_ denotes a parameter I am allowing to vary in GP, no _ means it is fixed.)
I slightly altered my approach to getting the parameters the process is now as follows:
 - fit power-law parameters to the age and rotation relation using scipy, for to get these values I only analyse the data for a small range of masses (0.9 - 0.94)
 - Use a GP to get a more accurate prediction for these parameters, this is mostly to determine the factor out front. I have had the most success using the literature value for the power dependance t^0.52
 - Fit a power-law to the mass and rotation data for a subset of the data where the ages are in the range ( 4.4 > t > 5)Gyrs.
 - Use a GP to get a more accurate prediction for the power dependance. I am still a little uncertain how to best determine the multiplication factor, at the moment I am determining it from a normal function with the mean at the value determined from the age relation but with a fairly large sigma (A * 0.5), the mean function is of the form A_*T^c * M^d_
 
 The residual plot this produces is very nice, it sits dead on the y=x line with a small deviation below at the upper limit. The Z plot is well centered on 0, but there are a few peaks above the N(0,1) plot.
 
 
 # in testing currently # 
 The BV dependance is slightly different, I am using the equation determined by Meibom et.al https://iopscience.iop.org/article/10.1088/0004-637X/695/1/679/pdf, of the form g_(BV - h)^f. Where the parameters are given in the paper and in my notebook. I have chosen to not let d vary, I am also unsure how to handle c at this stage. 
 - I am using a mean function of the form A_*T^c * M^d_ * (BV - d)^f_ ( here A_ is centered on A*g, A from before and g from paper).
 - So far, I have not been able to get as nice plots from this data. The residual plot fits well up to rotations of roughly 35 days (this data only goes up to approx 40 days), but beyond this my GP is over predicting the rotation, not too sure why. 
 
 
 # to determine the values for the hyper parameters (I am unsure if this is a sensible approach...)
 I am currenty using three expential quadratic kernels with 3 different pairs of paramters, l1,sig1, l2,sig2, l3,sig3.
 - I have sort of thought of each kernel as repesenting one of each of the variables: age, mass and BV. Therefore I have chosen ls and sigs that look sensible to that data. i.e for Mass, the mass data spans a  range of roughly 1.4 solar masses, therefore a lengthscale was chosen to be roughly double'ish' that (3.6), looking at the scatter plot of mass vs Prot, at the greatest difference the Prot range spans approximently 40 days, therefore a sigma of 40 has been chosen. A similar approach was then applied to BV and Age. 
 
 I also skim read a few papers where GPs have been used for other Astro problems in the hope that this would help me determine the mean function/hyperparameters, but there wasnt too much useful content on this.
 
