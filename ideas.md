# Ideas
This is a mostly throwaway doc where I write down ideas for this project.

## Goals for functionality
I would like this to be able to:
 * solve puzzles (done for specific cases—it was able to solve the original and Quag's puzzles)
 * create puzzles in computer form
 * create puzzles in human-readable form
 * maybe use another solver like [cryptominisat](https://github.com/msoos/cryptominisat)!
 * read puzzles from a file
 * generate puzzle files

## User interaction
Who is the audience of this? Is it just me, generating puzzles for myself / maybe others? What if I turned it into a Flask app for other people to use?

That would be coolest—I'd have to create a utility to generate puzzles, a utility to solve them, and then the Flask code. And templates for this. 

## Representing element classes
I have problems with the data structure to represent groups of elements, like foods being ("pizza", "grilled_cheese", "stew", ...) or colors or others. Technically speaking, I can use a namedtuple factory function that creates a namedtuple instance, initializes it, then returns it; but this messes with all kinds of static type checking and linting. But I'm not trying to initialize the puzzle in code, am I? I probably want some kind of text representation that I can then parse and solve.

So what does that mean? Specify the puzzle in text, then read it into Python as a puzzle class. Or something.