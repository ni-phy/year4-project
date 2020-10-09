# Project plan

|Can we measure lots of rotations and lots of colours/temperatures we can get lots of ages. Which is useful for exoplanets and space archaeology.

Explain gyrochronology referencing existing literature

Explain GPS may want to use someone else&#39;s examples (look at appendix of paper in figure a1 and a2). Does not have to be real data, but try and relate it to rotation and age of star

Do the plots of GP work have to be related to gyrochronology, when we write the section may want to use a plot form one of the papers, (Cite it)

Good to include evidence (Gantt charts, give times to plan all the way from now to may – good for marks) Discuss Gantt charts but should look different, same timescale etc. (NOT identical, different colours at a bare minimum)

Understand Gyrochronology have a handle on GPs understand where project is going in short and medium term

# Science

Membership probability for a star in a cluster

When stars form, big gas cloud that collapses and forms stars, most stars form in some association (not too many individual). They are born together at the same time from the same cloud of gas, all the same age and similar chemical composition, over time most stars orbit galaxy and lots of these stellar associations get disrupted, the collection get disturbed and become no longer gravitationally bound. By chance there are some clusters that have not been disturbed (NGC6098), there are not that many older open clusters, this one is good as it has not been too disturbed. Within the cluster the orbit around the COM of the cluster. If you can work out where the stars are travelling at the moment or watch the progress of time can work out if they&#39;re still bound by the cluster or a transient star passing through the cluster (or one in foreground).

Cluster membership probability, they are clustered by position and depth. If the stars are co-moving it is a high chance, they are a member of the cluster. The probabilities are reasonably tricky to calculate, that is why we get different levels of probability for different stars (a transient star may appear to be co-moving). Is there a threshold for if the star is in the cluster of not? Most people apply a threshold, though this might not be super.

## Gyrochronology

Stars greater than 1.2 solar masses will being to slow down rotation (spin down) after about 0.5Gyr. We generally consider that stars cannot spin up. The rate at which they slow down follows the Skumanich relation . Derived theoretically but seems reasonably accurate. Time is not the only factor; mass will also affect and also metallicity along with some others. A star with a different mass will have a different breaking relation.

Stars have magnetic fields and magnetic winds, as the wind moves away from the star its torque gets a lot larger and so as that happens it can no longer keep the same period, same ang mom but different P. But the star is still rotating with the same period.

Couple the fast-rotating star and the slow rotating wind (charged particles), if we pass a mag field through this sea of charged particles the field will attempt to drag the charged particles with it, this creates a coupling. The mag field rotates with the star quickly, these lines pass through the wind (which is rotating slower) the fast-moving mag field torques the wind to spin faster and in doing so spins down the star.

The mass dependency comes from the fact that stars with different masses have different characteristics, the most important factor is the depth of the convection zone (on the outer shell, like 30%ish in the sun). We get convective cells as they rise and get cooler then fall back down. Rossby number depends on convective time scale and rotational period. Low mass stars have deeper convective zones than high mass star, this changes the convective time scale and therefore changes how strong or structed the magnetic field of star is.

Are we interested in the time or the velocity of the convective cells? **We think of the period of rotation of days and the period of the convection in days.** We will not be too concerned with this as we are totally data driven.

With our project, using a GP where the GP will marginalize over all the functional forms that are sensible for the magnetic breaking, is interesting as we can get a data driven picture of how stars slow down.

# Gaussian processes

By studying fake data, we can determine if our GP is doing the right job

Guy: write your own piece of code that does it (in a simple way) in the worksheets straightforward code, but understanding is difficult, once we have the toy we throw that away and use the professional code.

To be good need to play around and understand the basics, once we have that feel use the professional level code.

# Next week

Have a plan by next week, that guy can review.

Guy has model data and some work sheets to be sent. Use the GP on model data to put in plan, we have a 50% chance of making it work.

Fit a GP to fake data, and work through worksheets (need to understand maths, in the appendix of the paper we can find all the maths we will need)

- Will have to choose the Kernel function (radial basis/squared exponential), choose the hyper parameters (length scale and the variance), very possible that we will need to choose a good mean function ( as our problem is very specific, i.e. we don&#39;t expect stars to spin up (so prediction of GP will continue to slow down forever ( linear ))).
