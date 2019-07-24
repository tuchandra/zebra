# Ideas
This is a mostly throwaway doc where I write down ideas for this project.

## Goals for functionality
I would like this to be able to:
 * solve puzzles (done for specific cases—it was able to solve the original and Quag's puzzles)
 * create puzzles in computer form
 * create puzzles in human-readable form
 * maybe use another solver like [cryptominisat](https://github.com/msoos/cryptominisat)!

## User interaction
Who is the audience of this? Is it just me, generating puzzles for myself / maybe others? What if I turned it into a Flask app for other people to use?

That would be coolest—I'd have to create a utility to generate puzzles, a utility to solve them, and then the Flask code. And templates for this. 

## Representing element classes
I have problems with the data structure to represent groups of elements, like foods being ("pizza", "grilled_cheese", "stew", ...) or colors or others. 
