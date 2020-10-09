# Week 3

## Ideas for the context:

Use GPs in a couple of scenarios. In the plan keep it straightforward with one task (e.g. gyro-chronology) but can expand on later:

- GPs to estimate the age of stars using gyro-chronology (rotation of stars and their age). Spinning creates a mag field, As the stars are hot, they give off stellar wind. The hot charged particle emitted from star get caught in wind. This causes the spin to reduce over time.
- An outstanding report – sets up GPS, apply to a few astro problems (gyro chronology, another problem, …)

Read a paper on gyro-chronology

## Github

Keep notes of git, any work should be kept on the log. Notes, code, everything. If in doubt, whack it up there. Read article, make notes. Spend an afternoon reading, make notes add them commit. Commit messages 5-6 words

## Project plan

Week 4 – do not forget. Will have a literature review, use the 2 papers.

## Gaussian Processes

Prior is the kernel (bible equation 2.28). start reading bible (C. E. Rasmussen &amp; C. K. I. Williams GPs for machine learning) in Jan-Feb

## Bayes

P(set of parameters | data) α P(set of parameters) \* prop(data| set of parameters)

P(set of parameters) – **prior** : what do we think are sensible parameters, a distribution of likely parameters that we think are sensible. Probably gaussian between some sensible values N(mean, variance (or squared std dev))

P(data| set of parameters or model) - **likelihood** : P(D|M(parameters)) Model could map surface temperature(measurable) to core temperature (not measurable). Will have uncertainty. Probably a normal distribution. Normal(Model(parameter) – measure, variance). Very dependent on model if that&#39;s wrong you won&#39;t get a good answer

P(set of parameters| data) – **posterior** :

## By next week:

Read a paper on gyro chronology

Develop understanding of GPs

Apply a GP to a basic problem

Develop git understanding (create a repository, learn push, pull, commit, issue and add)

Make our own trivial data set 100 points. Np and RNG to generate some data set. Y = mx +c + noise or Y = X\*sin(X). 1 parameter. Try and fit a GP. Write from scratch in np (ideal) or a package:

tf gpyflow / sklearn more beginner friendly / pymc3 / stan / anything.
