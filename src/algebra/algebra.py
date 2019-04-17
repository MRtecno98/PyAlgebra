"""
Copyright 2019 MRtecno98

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.


TODO:
Implement Fractions

LITERAL CALCULATION LIB BY MRtecno98
Basic math with Polynomials and monomials
"""

from string import ascii_lowercase

class AlgebricError(Exception) :
    '''For errors in algebric calculation'''

class Number :
    def __init__(self, n) :
        #print("hEy Im A lItTlE nUmBeR")
        self.n = float(n)
		
    def __add__(self, other) :
        return self.n + other if type(other) == type(self) else \
                Number(self.n + other)
	
    def __radd__(self, other) :
        return Number(other + self.n)
	    
    def __mul__(self, other) :
        prod = 0
        for i in range(int(other)) :
            prod+=self
        return prod if type(other) == type(self) else \
                Number(prod)
	
    def __rmul__(self, other) :
        prod = 0
        for i in range(int(other)) :
            prod+=self
        return Number(prod)
	    
    def __sub__(self, other) :
        return self.__add__(-other)
	
    def __rsub__(self, other) :
        return self.__radd__(-other)

    def __truediv__(self, other) :
        return self.n / other if type(other) == type(self) else \
                Number(self.n / other)
	
    def __rtruediv__(self, other) :
        return Number(other / self.n)

    def __mod__(self, other) :
        return self.n % other if type(other) == type(self) else \
                Number(self.n % other)
	
    def __rmod__(self, other) :
        return Number(other % self.n)

    def __pow__(self, other) :
        pow_ = 1
        for i in range(int(other)) :
            pow_ = pow_*self
        return pow_ if type(other) == type(self) else \
                Number(pow_)
	
    def __rpow__(self, other) :
        pow_ = 1
        for i in range(int(other)) :
            pow_ = pow_*self
        return Number(pow_)

    def __neg__(self) :
        return Number(-self.n)
	    
    def __str__(self) :
        return str(self.n if self.n % 1 != 0 else int(self.n))

    def __repr__(self) :
        return "Number({0})".format(str(self))

    def __eq__(self, other) :
        if not (type(other) == type(0) or type(other) == type(self)) :
            return False
        on = other.n if type(other) == type(self) else other
        return self.n == on

    def __lt__(self, other) :
        return self.n < float(other)

    def __gt__(self, other) :
        return self.n > float(other)

    def __le__(self, other) :
        return self.n <= float(other)

    def __ge__(self, other) :
        return self.n >= float(other)

    def __abs__(self) :
        return Number(abs(self.n))
	    
    def __int__(self) :
        return int(self.n)

    def __float__(self) :
        return float(self.n)

class Variable :
    def __init__(self, letter:str, exponent=Number(1)) :
        if not ((len(letter) == 1) and letter in ascii_lowercase)  : raise Exception("Illegal variable: {0}".format(letter))
        self.letter = letter
        self.exponent = exponent

    def __eq__(self, other) :
        return self.letter == other.letter and self.exponent == other.exponent

    def __neg__(self) :
        return Variable(self.letter, exponent=-self.exponent)

    def __str__(self) :
        return (self.letter + "^" + str(self.exponent)) \
               if self.exponent != 1 else self.letter

    def __repr__(self) :
        return "Variable({0})".format(str(self))

class Monomial :
    def __init__(self, coefficient:Number, *variables:Variable) :
        self.coefficient = coefficient if isinstance(coefficient, Number) \
                           else Number(coefficient)
        self.variables = variables

    def __str__(self) :
        return (str(self.coefficient) if self.coefficient != 1 \
                or self.sign_vars() == [] else "") \
               + "".join([str(i) for i in self.variables])

    def __repr__(self) :
        return "Monomial({0})".format(str(self))

    def sign_vars(self) :
        return [i for i in self.variables if i.exponent != 0]

    def __abs__(self) :
        return Monomial(abs(self.coefficient), *(self.variables))
    
    def reduce(self) :
        varia = {}
        letters = []
        reduced_vars = []
        for i in self.variables :
            if i.letter in varia.keys() :
                varia[i.letter].exponent += i.exponent
            else :
                varia[i.letter] = Variable(i.letter, exponent=i.exponent)
                letters.append(i.letter)
        letters.sort()
        for i in letters :
            reduced_vars.append(varia[i])
        self.variables = reduced_vars

    def minimalize(self) :
        self.variables = self.sign_vars()

    def regroup(self) :
        self.reduce()
        self.minimalize()

    def __mul__(self, other) :
        if isinstance(other, Monomial) :
            prod = Monomial(self.coefficient * other.coefficient, \
                            *(list(self.variables) + list(other.variables)))
        else :
            prod = Monomial(self.coefficient * other, *(self.variables))
        prod.reduce()
        return prod

    def __rmul__ (self, other) :
        if isinstance(other, Monomial) :
            prod = Monomial(other.coefficient * self.coefficient , \
                            *(other.variables + self.variables))
        else :
            prod = Monomial(other * self.coefficient, *(self.variables))
        prod.reduce()
        return prod

    def __add__(self, other) :
        mother = other
        if not isinstance(other, Monomial) :
            mother = Monomial(other)
        if self.sign_vars() == mother.sign_vars() :
            return Monomial(self.coefficient + mother.coefficient, \
                            *(self.variables))
        else :
            return Polynomial(self, mother)

    def __radd__(self, other) :
        mother = other
        if not isinstance(other, Monomial) :
            mother = Monomial(other)
        if self.sign_vars() == mother.sign_vars() :
            return Monomial(mother.coefficient + self.coefficient, \
                            *(self.variables))
        else :
            return Polynomial(mother, self)

    def __sub__(self, other) :
        return self + (-other)

    def __rsub__(self, other) :
        return other + (-self)

    def __truediv__(self, other) :
        mother = other if isinstance(other, Monomial) else Monomial(other)
        mother.reduce()
        varia = {i.letter : i for i in self.variables}
        for i in mother.variables :
            if i.letter in varia.keys() :
                varia[i.letter].exponent -= i.exponent
            else :
                varia[i.letter] = -i
        return Monomial(int(self.coefficient / mother.coefficient), \
                        *(list(varia.values())))

    def __rtruediv__(self, other) :
        mother = other if isinstance(other, Monomial) else Monomial(other)
        mother.reduce()
        varia = {i.letter : i for i in mother.variables}
        for i in self.variables :
            if i.letter in varia.keys() :
                varia[i.letter].exponent -= i.exponent
            else :
                varia[i.letter] = -i
        return Monomial(int(mother.coefficient / self.coefficient), \
                        *(list(varia.values())))

    def __neg__(self) :
        return Monomial(-self.coefficient, *(self.variables))

class Polynomial :
    def __init__(self, *monomials:Monomial) :
        self.monomials = monomials

    def __add__(self, other) :
        mother = other
        if not isinstance(other, Polynomial) :
            if not isinstance(other, Monomial) :
                mother = Monomial(mother)
            mother = Polynomial(mother)
        sum_ = Polynomial(*(list(self.monomials) + list(mother.monomials)))
        return sum_

    def __radd__(self, other) :
        mother = other
        if not isinstance(other, Polynomial) :
            if not isinstance(other, Monomial) :
                mother = Monomial(mother)
            mother = Polynomial(mother)
        sum_ = Polynomial(*(list(mother.monomials) + list(self.monomials)))
        return sum_

    def __mul__(self, other) :
        mother = other
        if not isinstance(other, Polynomial) :
            if not isinstance(other, Monomial) :
                mother = Monomial(mother)
            mother = Polynomial(mother)
        mons = []
        for m in self.monomials :
            for m2 in mother.monomials :
                mons.append(m*m2)
        return Polynomial(*(mons))

    def __rmul__(self, other) :
        mother = other
        if not isinstance(other, Polynomial) :
            if not isinstance(other, Monomial) :
                mother = Monomial(mother)
            mother = Polynomial(mother)
        mons = []
        for m in mother.monomials :
            for m2 in self.monomials :
                mons.append(m*m2)
        return Polynomial(*(mons))

    def __pow__(self, other) :
        if not isinstance(other, (Monomial, Polynomial)) :
            n = Number(other)
            total = self
            for i in range(int(n - 1)) :
                total *= self
            total.minimalize()
            return total
        else :
            raise AlgebricError("Cannot solve a power with non-numeric exponent")
        
    def sign_mons(self) :
        return [i for i in self.monomials if i.coefficient != 0]
    
    def reduce(self) :
        p.monomials = p.sign_mons()
        for i in self.monomials :
            i.reduce()
            i.variables = i.sign_vars()

    def regroup(self) :
        mania = {}
        letters = []
        for i in self.monomials :
            identifier = "".join([str(i) for i in i.variables]) \
                         if len(i.variables) > 0 \
                         else str(i.coefficient)
            mania[identifier] = i if not identifier in mania.keys() else \
                                mania[identifier] + i \
                                if not isinstance(mania[identifier] + i, Polynomial) \
                                else i
            if not identifier in letters : letters.append(identifier)
        letters.sort()
        self.monomials = [mania[i] for i in letters]

    def minimalize(self) :
        self.reduce()
        self.regroup()

    def __str__(self) :
        str_pol = str()
        for s in self.monomials :
            if self.monomials.index(s) > 0 :
                str_pol += (" + " if s.coefficient > 0 else " - ")
                str_pol += str(abs(s))
            else :
                str_pol += str(s)
        return str_pol

    def __repr__(self) :
        return "Polynomial({0})".format(str(self))

    
    
    
