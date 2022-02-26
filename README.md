# simpl

A small stack based programming language originally inspired by [porth](https://gitlab.com/tsoding/porth).

(WORK IN PROGRESS)

## Notes

https://astexplorer.net/

## Goals

- [x] Compiles
- [ ] Turing complete
- [x] Nestable statements
- [x] Flexible spacing
- [x] Standard library
- [x] Errors
  - [x] Syntax errors
  - [x] Run time errors
- [x] Importing files

## Syntax

- Comments
```
# blah
```

- Types
```
"string"   # a string
123        # an integer
123.456    # a float
T          # a boolean (true)
F          # a boolean (false)
```

- Push to the stack
```
"wasd" .
a .        # push a variable called a
..         # push the top of the stack again (duplicate)
```

- Variables
```
"basd" .   # push first
@ b        # pops "basd" into a new variable called b
```

- Math operations
```
# Operate on the top two items on the stack, and push result to the stack
# (pops the original two on the top)
# All are single operations (no input or output variables)
+
-
*
/    # second item divided by first item
%    # modulo (remainder) of second item divided by first item

# Example
2 .
3 .
+
@ a     # a is 5
```


- Boolean operations
```
# Operate on the top two items on the stack, and push the boolean result to the stack
# (pops the original two on the top)
# All are single operations (no input or output variables)
==
!=
>    # second item is greater than the top item
<    # second item is less than the top item
>=   # second item is greater than or equal to the top item
<=   # second item is less than or equal to the top item

# Example
"wasd" .
"basd" .
!=
@ c     # c is T
```

- Conditional checks
```
# Run the code in the curly braces if the top of the stack is T
# (pops the top)
# Otherwise run the code in the second curly brace
? {
  
} : {
}
```

- Loops
```
# Loop what is in the curly braces forever, until it is broken
& {
  ~ # continue (skip to next iteration)
  ^ # break the loop
}
```

- Functions
```
# Function definition
factorial {
  # push the input number on the stack before calling this function

  .. # duplicate the top
  0 .
  <=
  ? {
    "Number must be greater than 0" .
    ->      # stop the function (return)
  }

  # <snip>
  # assume result is the factorial
  result .
}

# Calling a function
5 .
factorial!    # put a ! at the end of the name
@ result      # result should be 120
```

- Input/output
```
# Printing:
'Hello world!' . print!
'Hello world!' . println!

# Text input
'What is your name? ' . print!
input!
'Your name is ' . print! @_
print!
```
