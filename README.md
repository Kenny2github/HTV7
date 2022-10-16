# HTV7
Project for Hack the Valley 7

## Inspiration
A team member once was required to take a "cognitive test" as part of a job application. The test involved being given a list of species and their interactions, and balancing it to avoid the extinction of any of them. We built BEST based on this idea.

## What it does
The _**Biological Ecosystem Simulator and Tweaker**_ (or BEST) application takes in the initial population of different animal species in an ecosystem, then simulates their interactions using predefined rules. We display the population trends as a graph and recommend preemptive actions if needed.

## How we built it
The application was built by a team of three 2nd-year University of Toronto Computer Engineering students using Python and related libraries such as [Qt](https://qt.io) (for UI), [numpy](https://numpy.org) (for fast array operations), and [scipy](https://scipy.org) (for solving differential equations). We also used development tools such as VSCode and GitHub.

## Challenges we ran into
The main issue we spent the most time on was how to model the relationships between the populations of various species in the ecosystem, as there are many factors to how two different species may interact in a real-world setting. We ultimately decided on using the [Generalized Lotka-Volterra model](https://en.wikipedia.org/wiki/Generalized_Lotka%E2%80%93Volterra_equation), which is expressed as a system of differential equations, as the logic behind it was much easier to implement.

## Accomplishments that we're proud of
We had previously learned how to solve differential equations as well as matrix equations through courses, and we were able to make use of what we learned in a programming setting. We are also proud of the speed with which we did the actual programming - the vast majority of the time was spent elsewhere (mostly on tuning ecosystem parameters).

## What we learned
* We learned that not only are ecosystems complex, but they are also chaotic - very sensitive to the parameters you put into them.
* We learned scientific differential-equation models for species interactions within an ecosystem, particularly the Lokta-Volterra models, of which we used the generalized version.
* We learned how to use scipy to compute solutions to systems of differential equations (for the purposes of predicting the evolution of the ecosystem based on the aforementioned models we learned about).

## What's next for Biological Ecosystem Simulator and Tweaker
* Support more ecosystems
* Give more detailed recommendations
