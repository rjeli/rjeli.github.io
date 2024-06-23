---
layout: post
title: 'Maxylla: an experimental symbolic programming notebook in the browser'
---

I wrote a little thing and put it up at [maxyl.la](http://maxyl.la). It's a symbolic programming language written entirely in javascript. Right now it obviously is very similar to Mathematica, but that's just because I've been focused more on implementation details than syntax or semantics.

Generally, the goal is a fusion of Mathematica, Haskell, and a little bit of J. Personally, whenever I want to run some quick calculations I open an IPython shell or notebook, and I'd like Maxylla to be a better version of that, with symbolic capabilities. It should allow for easy composition of functions, the choice of either verbosity or the tight tacit symbols of APL/J, and a closely integrated debugging environment. I think symbolic (and logic) languages need some kind of graphical execution tracer or they can easily become too hard to reason about.

Various goals:
  - Functional style
    - Efficient closures and TCO are necessary
    - Currying would be *really* nice, but it's not immediately obvious how to reconcile it with the variadic argument matching that is so useful in a CAS
 - Make it easier to write functions that don't fit on one line (Mma. and J fail at this)
 - Provide Mma. compatibility "layer" or "mode", which is just sufficient to run [Rubi, a comprehensive suite of symbolic integration rules](https://rulebasedintegration.org/)

Right now the majority of language features are implemented in Maxylla itself, but that may change if performance becomes an issue. I'm not currently doing anything fancy with expression caching -- in fact, comparing expressions and using them as dictionary keys is implemented by stringifying them! But v8 and spidermonkey don't struggle too much yet.