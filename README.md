# PyAlgebra
This library provides basic functions to do literal calculations with monomials and polynomials, it's easy to use and completeley open source.
Here there is a small guide for starting using PyAlgebra.
## Numbers
First you need to import the module with the components you need.

    from algebra import Number, Variable, Monomial, Polynomial

The library provides a specific class for representing a Number, it's interchangeable with the classic `int` class.
Here's the usage of the class `Number`

    from algebra import Number
    
    n1 = Number(10)
    print(n1) # 10
	
	n2 = Number(5)
	print(n2) # 5
	
	sum = n1 + n2  # Number(15)
	sub = n1 - n2  # Number(5)
	prod = n1 * n2 # Number(50)
	div = n1 / n2  # Number(2)
	pow = n1 ** n2 # Number(100000)
As you can see, it's very similar to the normal `int` class, but if you prefer the classic way you can always convert it to an int.

    print(int(n1)) # 10

## Monomials
A `Monomial` is a product of variables and a known term(the *coefficient*), in PyAlgebra you can declare a Monomial this way:

    from algebra import Number, Variable, Monomial
	
	m = Monomial(Number(2), Variable("x", exponent=3))
	print(m) # 2x^3
	print(str(m)) # 2x^3
The first argument of the constructor is the coefficient, a `Number` or an `int`, and it can be in any range; the others are Variables, a Variable is an unknown term and is represented by the `Variable` class that takes on constructor a single-character string and, optionally, an exponent for the variable. In a Monomial constructor you can insert only one coefficient and how many Variables you want. A Monomial is represented textually by a string that contains the coefficient and all the variables one after another, you can take it by calling the `str()` function on a Monomial object or by printing it.
