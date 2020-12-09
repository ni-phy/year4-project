Here I will be keeping a rough timeline of progress for the project.

# 11/11/2020: #
Fitted GP with a mean function to generated data (predicting rotation given age and BV). Will next be looking into generating my own data set to test the process on. 

# 12/11/2020 #
Generated some new sample data (with a slightly different form/shape to the data guy produced) to check if my code worked on other data sets - fit very well :)

--- progress made on new data set ---

# 30/11/2020 #

Given the newest data set (Mass, temperature, Rotation and Age), I have been able to make accurate predictions for the rotation period given either age or age and mass. The mean functions for both were power laws A*x^b. If the GP is given total freedom in determining the parameters, it does not work too well. Therefore, I fit rough parameters using SciPy optimize. Using these pre-determined values, I managed to get accurate predictions - tight residuals. 

My mean function is of the form P = A*T^c * B*M^d

Where P is rotational period, A is age, M is mass. A, B, c, d are parameters to be determined by fitting power laws and then improved by using the GP. I collapsed A and B into just one constant A. 

Prior to collapsing A and B into one variable, I was having trouble getting accurate predictions once I allowed the parameters to vary.
Parameters A d and c were determined from normal functions centred on the values determined from the SciPy fitting. 
Once a few bugs were ironed out, I have been able to get a very tidy residual plot.


# 03/12/2020 #
(_ denotes a parameter I am allowing to vary in GP, no _ means it is fixed.)
I slightly altered my approach to getting the parameters the process is now as follows:
 - fit power-law parameters to the age and rotation relation using SciPy, for to get these values I only analyse the data for a small range of masses (0.9 - 0.94)
 - Use a GP to get a more accurate prediction for these parameters, this is mostly to determine the factor out front. I have had the most success using the literature value for the power dependence t^0.52
 - Fit a power-law to the mass and rotation data for a subset of the data where the ages are in the range (4.4 > t > 5) Gyrs.
 - Use a GP to get a more accurate prediction for the power dependence. I am still a little uncertain how to best determine the multiplication factor, at the moment I am determining it from a normal function with the mean at the value determined from the age relation but with a fairly large sigma (A * 0.5), the mean function is of the form A_*T^c * M^d_
 
 The residual plot this produces is very nice, it sits dead on the y=x line with a small deviation below at the upper limit. The Z plot is well centred on 0, but there are a few peaks above the N (0,1) plot.
 
 
 # in testing currently # 
 The BV dependence is slightly different, I am using the equation determined by Meibom et.al https://iopscience.iop.org/article/10.1088/0004-637X/695/1/679/pdf, of the form g_ (BV - h) ^f. Where the parameters are given in the paper and in my notebook. I have chosen to not let d vary; I am also unsure how to handle c at this stage. 
 - I am using a mean function of the form A_*T^c * M^d_ * (BV - d)^f_ ( here A_ is centred on A*g, A from before and g from paper). I have found that there is not too much difference in the result when I let d vary, but the plot does seem to fit best when it is not allowed to. 
 - So far, I have not been able to get as nice plots from this data. The residual plot fits well up to rotations of roughly 35 days (this data only goes up to approx. 40 days), but beyond this my GP is over predicting the rotation, not too sure why. 
 - This could be evidence that my mean function is not optimised for this data or it COULD be evidence of the Kraft break in the data. My model does not take this into account and therefore if this is the case, over predicting is expected. 
 
 
 # to determine the values for the hyper parameters (I am unsure if this is a sensible approach...)
 I am currently using three exponential quadratic kernels with 3 different pairs of parameters, l1, sig1, l2, sig2, l3, sig3.
 - I have sort of thought of each kernel as representing one of each of the variables: age, mass, and BV. Therefore, I have chosen ls and sigs that look sensible to that data. i.e. for Mass, the mass data spans a  range of roughly 1.4 solar masses, therefore a length scale was chosen to be roughly double'ish' that (3.6), looking at the scatter plot of mass vs Prot, at the greatest difference the Prot range spans approximately 40 days, therefore a sigma of 40 has been chosen. A similar approach was then applied to BV and Age. 
 
 I also skim read a few papers where GPs have been used for other Astro problems in the hope that this would help me determine the mean function/hyperparameters, but there was not too much useful content on this.


# Semester 1 recap
As semester one comes to a close, I have made good progress on the project. I now have a reliable initial model that can accurately predict ages using generated data as the training data. Our aims for this semester were to be able to produce a model to make accurate predictions for the rotational period given mass and age. I have achieved this and taken this one step further and can include temperature (or BV) in our predictions. I have read literature on the underlying physics of gyrochronology and where Gaussian processes have been used in examples related (and not related) to astrophysics. 

I am on track with the Gantt chart outlined in the project plan. Although I have not kept a complete log of where I am, the regular commits to the github repository and discussions made in weekly meetings, with my supervisor Guy Davies, acts as the evidence that continuous work has been made on the project. 

Evidence of to show the accuracy of predictions made from my trained model can be found in year4-project/Henry/good-fit-images/ under the names 3d good predictions (1&2). The figures were generated for the model where I have used Age, mass, and BV to predict rotation, the mean function used is the product of three power laws (one for each variable) where approximate values where determined by SciPy line fitting and more accurate values where determined by the Gaussian process.



The next step in the project will be to slowly increase the realism of the generated training data. The main hurdle to overcome will be to introduce latent parameter prescription, this challenging concept is something I will first have to read into before attempting to introduce this to the current model. Once this is functional, I will be very close to being able to train my model on real data.


