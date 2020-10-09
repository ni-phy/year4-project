## General matters

There are a handful of ways we can approach our project.

- Here is a good technique and a million problems, how good does this technique work on these 5 scenarios
- focussing on 1 problem and prove that the technique is right is another sensible approach
  - Compare NN and GPs on data that is around the range where GPs are questionable (105) data points.

Most likely we are going to choose a method that suits us best and fit this onto a problem that is somewhat interesting.

We need to begin to narrow down what interests us the most NN, MCMC or GP.

PYMC3 uses a Theano backend which works poorly on google colab. There is a pre-release of PYMC4 which has a TF backend. However, as it is new tech there is not much documentation (There is not much for 3 either…) Luckily, Stan in C++ is similar, look up how to do it in stan and translate to PYMC

## By next week

- Set up a github - me or Nik.
  - github log becomes the project notebook
  - treat it like a front facing public project - useful for jobs
- Look into gaussian processes
- discussion of algorithm

## Gaussian process&#39; (GPs)

Guy suggested GPs as an alternative to neural nets. They are very good at what they do. Neural nets have the issue of being over-confident. For whatever reason, GPs are safe and apparently are just generally better. The flip side is that they are incredibly computationally expensive. As a base they are O(N3). Can be reduced to n2log(n) under certain conditions and can be O(n) for a damped stochastic SHO.

They allow you to integrate over all (infinite number of) models to find the best few. Neural nets tend to GPs as the number of neurons goes to infinity, obviously this is impossible. However, if we have loads and loads, it is not too far off.

talk (important beyond 45mins its crazy)

learn some basics, learn the fundamentals of what it is

https://www.youtube.com/watch?v=92-98SYOdlY

They try every model weighted by how the fit the data and the prior info. They are big new tech and are a major focus of cutting edge-research. Roughly speaking they do the same as NN (both try and learnt he map of input to output) not just training data but general map. They try and describe the underlying process not just the data they are fed, i.e. form a model not just fit a line.

NN are excellent with a tone of data, which is great as lots of data can provide the generalisation.

Although GPs do not scale well, they are much better at filling in the blanks (whilst telling you the uncertainty). When the GP is bad it will let you know. heteroskedastic process (variance of the output variances)

NN are homoscedastic (fixed output variance).

examples (playing the stock market, banks use these algorithms to make decisions on trade, they use NN as there&#39;s loads of data. NNs do not know when they are making bad decisions, they just make the decision and do it.

GP determines the decision and confidence. As soon as the uncertainty goes above a level a human bean can make the decision (NNs can do this but does not have the inbuilt manifestation of uncertainty).

NN are overly confident. GPs, when set up properly, have the correct level of confidence. GPs get more confident with lots of data, but less so with little data.

Could approach the project in the boundary between lots and little data (5-10 thousand). And apply both NN and GPs and compare

Could be part of the project

Spin down of stars
