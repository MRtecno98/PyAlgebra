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
The `Monomial` class handles three operations, multiplication, division and algebric sum.
You can operate with Monomials by using the normal Python operators

    from algebra import Number, Variable, Monomial
    
    m = Monomial(Number(6), Variable("x", exponent=3), \
							Variable("y", exponent=2))
    m2 = Monomial(Number(2), Variable("y", exponent=2))
	
	print(m * m2) # 12x^3y^4
	print(m / m2) # 3x^3
	
For the algebric sum we need two Monomials with the same Variables, otherwise, we'll get a Polynomial as result.

    m3 = Monomial(Number(4), Variable("y", exponent=2))
    print(m2 + m3) # 6y^2
	
	#If we try adding two non-similar monomials, we get a polynomial
	print(m + m3) # 6x^3y^2 + 4y^2
## Polynomials
When we sum two Monomials with different Variable set, as result we get a `Polynomial`.
We can declare a polynomial this way

    from algebra import Number, Variable, Monomial, Polynomial
	
	m1 = Monomial(3, Variable("x", exponent=2))
	m2 = Monomial(4, Variable("y", exponent=3))
	
	#These two expressions are equivalent
	p1 = Polynomial(m1, m2)
	p2 = m1 + m2

	print(p1 == p2) # True
	print(p1) # 3x^2 + 4y^3

As always, you can operate with these polynomials with the standard Python operators

    print(p1 * Monomial(1, Variable("x"))) # 3x^3 + 4xy^3
    print(p1 + Monomial(1, Variable("x"))) # 3x^2 + 4y^3 + x
  
  Sadly, the division operation is not yet implemented.

## Reduction
The library doesn't automatically reduce the Monomials and Polynomials after operations, although it doesn't make sense right now, it will serve for implementing fractions and scompositions in the future.
So for manually reducing a polynomial/monomial you can use the apposite functions `self.regroup()` for Monomials and `self.minimalize()` for Polynomials.

    from algebra import Number, Variable, Monomial, Polynomial
	
	m = Monomial(1, Variable("x", exponent=2),
					Variable("x", exponent=3))
					
	print(m) # x^2x^3
	m.regroup()
	print(m) # x^5
	
	
	
	p = Polynomial(Monomial(3, Variable("x")),
				   Monomial(5, Variable("x")))
				   
	print(p) # 3x + 5x
	p.minimalize()
	print(p) # 5x

Note that the `minimalize()` function for Polynomials will also reduce all the Monomials contained in it, calling the `regroup()` function for all of them.
					




    
    
    

