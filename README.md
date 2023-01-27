# Funx

---

### Programming Language Project, Q1 2022/23

---

Iván Serrano Hernández

`Professor:`  Jordi Petit Silvestre

---

*Funcx*  is an interpreter for a fictional programming language based on expressions and functions. The input and output of this interpreter is done via a web page.  

To define the grammar and building the interpreter for this language `ANTLR4` has been used, and `flask`  and `jinja2` have been used for the web server.  

Both python libraries can be installed with the following commands.

```bash
pip install flask
pip install Jinja2
```

Before invoking the interpreter, it's necessary to compile the grammar and generate the lexer and parser, as well as other necessary files for the normal function of the interpreter.

```bash
antlr4 -Dlanguage=Python3 -no-listener funx.g4
antlr4 -Dlanguage=Python3 -no-listener -visitor funx.g4
```

The following commands must be executed in the terminal to invoke the interpreter.

```bash
export FLASK_APP=funx
flask run
```

The web page will be available in *localhost:5000*, once the previous commands have been executed.

### Funx Specification

---

Funx's instructions are:  

- the assignment with `<-`,  
- the invocation of functions,  
- the conditional with `if` and perhaps `else`,  
- the iteration with `while`,

Written instructions after each other are executed sequentially.

The **allocation** must first evaluate the expression on the right side of the `<-` and then store the result in the local variable on the left. The assignment returns nothing.

Example: `a <- a - b`.

**conditionals** have the usual semantics, with the optional *else* block.

Example:

 `if x = y { z <- 1 } else { z <- 2 }`

Loops using `while` have the usual semantics.

Example: `while a > 0 { a <- a / 2 }`.

Calling a function has the usual semantics. If the number of parameters passed does not correspond to those declared, an error occurs. Functions can be called recursively. Syntax is without parentheses or commas.

Example: `Suma x + y`

### Language Presentation

---

Funx is an expression and function-oriented programming language. With Funx we can define functions and optionally end with an expression.  

An example of a final expression would be as follows.

    # expressions:
    2 + 4 * 2
    
    Out: 10

Funx comments are found after the "#" symbol. The output of the interpreter is the result of the evaluation of the expression.  

In Funx you cannot define programs, only functions (in any order) and a final expression.

Each function has a name, parameters and an associated block. Blocks are inscribed among symbols `{` and `}`.

Functions must start with a capital letter. Variables, on the other hand, start with a lowercase letter.  

Functions pass parameters by copy. They return the value of any expression they find in their block and at that precise moment. Here is an example:

```
# method that takes two parameters and computes its addition
Addition x y
{
  x + y
}

Addition (2 * 3) 4 
```

```
Out: 10
```

The Funx programming language also has recursion. As in the following example.

```
Fibo n
{
    if n < 2 { n }
    (Fibo n-1) + (Fibo n-2)
}

Fibo 4
```

```
Out: 3
```

Variables are local to each function invocation and functions can be communicated through parameters. Functions list the names of their formal parameters, but do not include their types, and parameters are separated with whitespace.  

Another example:

```
# method that takes two parameters and computes its g.c.d.

Euclides a b
{
  while a != b
  {
    if a > b 
    {
      a <- a - b
    }
    else
    {
      b <- b - a
    }
  }
  a
}

Euclides 6 8
```

```
Out: 2
```

Variables must not be declared, in the basic version all are of integer type and no read or write operations exist.  

The comparison operator for equality is `=` and by difference is `!=`. The assignment is done with the `<-` instruction.  

Functions may not have parameters. We can define constant functions like this:  

Example:

```
TWO { 2 }
Addition2 x { TWO + x }
Addition2 3
```

```
Out: 5
```

If a procedure does not have any expression, it returns nothing.

### Additional features

----

Since the base version of this fictional programming language was quite simple, I've decided to implement a few more features to make it a bit richer.

The additional features implemented are the ones following.

- Real numbers. In the basic version of Funx only integers can be used, but the possibility of working with decimal numbers has been implemented, where the decimal part is preceded by a '.'

Example:

```
Func{
    x <- 2.5
    x
} 
Func
    
# The output will be the following
Out: 5.5
```

- for() loop: The basic version of the project had only one way to build loops, so I have decided to implement for loops. They are built in the traditional way, but without parentheses.
  
  The three elements that integrate the loop are separated by ';', as is usually done in other languages, but without using parentheses (following the Funx language line). Iterator increment or decrease must follow assignment format.

Example:

```
For{
    x <- 0
    for i <- 0; i<10; i<- i+1{
        x <- x + i
    }
    x
}
For
# The output will be the following
Out: 45
```

- AND, OR and NOT operators: Since the basic version of Funx does not incorporate logical operators, I have added them with a '&' symbol for the AND, '|' for the OR and '!' for the NOT. Key words **true** and **false** have been introduced also.

Example:

```
Procedure x{ 
    if x < 10 & x > 0 & false{
         x <- 1     
    }     
    if true & false {
        x <- 2     
    } 
    if !false{ 
        x <- 3 
    }     
    x 
}
Procedure 0
# The output will be the following
Out: 3
```

Every single additional feature has its own test. 

- **test-Floats.funx**: test some operations with real numbers. The expected output for this test is 0.

- **test-For.funx**: test a for loop, the expected output for this test is 10.

- **test-LogicOperators.funx**: test all the logic operators implemented. The aditional output for this test is 3.

### Funx limitations

---

Obviously, Funx is a very simple programming language, with many limitations, but there are some that are worth commenting in order to ensure a good user experience.

#### Function calls followed by expressions

Because in a function call the parameters are expressions, and these are not limited by parentheses, it is not possible to execute a function call followed by a conventional expression. One example would be as follows.

```
FuncA x{
    x + 10
}
FuncB x{
    y <- FuncA x
    y + 10        //  An error will raise at this point
}
```

When calling *FuncA*, the compiler will detect the next line as one more parameter, so an error will occur (since the number of parameters in the call will be incorrect, or that y is a non declared variable if it had not been used before). For this reason, it will be necessary to close the function call in parentheses to avoid this error.

```
FuncA x{
    x + 10
}
FuncB x{
    y <- (FuncA x)
    y + 10        //  No error will occur here 
}
```

#### Expression evaluation inside loops and conditionals

The evaluation of expressions in Funx serves as a kind of return, so the execution of any code blocks will return the value of the first expression found, ignoring the rest of the code bellow.

Example:

```
Funx x{
    if x < 20{
        0
    }
    else {
        1
    }
    x <- 10    // This line will never be executed
}
```