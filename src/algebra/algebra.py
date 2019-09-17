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

LITERAL CALCULATION LIB 2.0 BY MRtecno98
Basic math with Polynomials and monomials
"""

import math

def equal(*elements) :
    if len(elements) < 2 : return True
    else : return elements[0] == elements[1] \
         and equal(*elements[1:])

def mul(*numbers) :
	if len(numbers) < 1 : return 1
	else : return numbers[0] * mul(*numbers[1:])

def gcd(first, *others) :
    if len(others) < 1 : return first
    return gcd(math.gcd(first, others[0]), *others[1:])

def lcm(first, *others) :
	if len(others) < 1 : return first
	return lcm(int(mul(first, others[0]) / \
                       gcd(first, others[0])), *others[1:])


class AlgebricException(Exception) :
    "For Algebric errors"

class Number() :
    def __init__(self, numerator, denominator=1) :

        if isinstance(numerator, Number) and numerator.den == 1 :
            numerator = int(numerator.real_value())

        if isinstance(denominator, Number) and denominator.den == 1 :
            denominator = int(denominator.real_value())
        
        self.num = numerator
        self.den = denominator

    def real_value(self) :
        return self.num / self.den

    def reduce(self) :
        for i in range(min(self.num, self.den), 0, -1) :
            if self.is_reducible_by(i) :
                   return self.reduce_by(i)

    def reduce_by(self, red) :
        if not self.is_reducible_by(red) :
            raise AlgebricException(repr(self) + " is not reducible by "
                                    + repr(red))
        return Number(int(self.num / red), int(self.den / red))

    def is_reducible_by(self, red) :
        return self.num % red == 0 and \
            self.den % red == 0

    def reduce_to_common(self, *others) :
        others = [self] + [Number(i) \
                  if not isinstance(i,Number) else i for i in others]
        cden = lcm(*[fract.den for fract in others])
        return tuple([Number(int((cden/other.den)*other.num), cden) \
                      for other in others])

    def _get_reduced_numerators(self, *others) :
        return [i.num for i in self.reduce_to_common(*others)]

    def opposite(self) :
        return Number(self.den, self.num)

    def __eq__(self, other) :
        return equal(*self._get_reduced_numerators(other))

    def __lt__(self, other) :
        a,b = self._get_reduced_numerators(other)
        return a < b

    def __le__(self, other) :
        a,b = self._get_reduced_numerators(other)
        return a <= b

    def __gt__(self, other) :
        a,b = self._get_reduced_numerators(other)
        return a > b

    def __ge__(self, other) :
        a,b = self._get_reduced_numerators(other)
        return a >= b

    def __add__(self, other) :
        if not isinstance(other, Number) :
            other = Number(other)
        a,b = self.reduce_to_common(other)
        return Number(a.num + b.num, a.den)

    def __radd__(self, other) :
        return self.__add__(other)

    def __sub__(self, other) :
        return self.__add__(-other)

    def __rsub__(self, other) :
        return (-self).__add__(other)

    def __neg__(self) :
        return Number(-self.num, self.den)

    def __mul__(self, other) :
        if not isinstance(other, Number) :
            other = Number(other)
        return Number(self.num*other.num,
                      self.den*other.den)

    def __rmul__(self, other) :
        return self.__mul__(other)

    def __truediv__(self, other) :
        if not isinstance(other, Number) :
            other = Number(other)
        return self.__mul__(other.opposite())

    def __rtruediv__(self, other) :
        return self.opposite().__mul__(other)

    def __abs__(self) :
        return Number(abs(self.num), abs(self.den))

    def __pow__(self, other) :
        if isinstance(other, Number) :
            other = other.real_value()
        return Number(self.num**other, self.den**other)
        #TODO: Add decimal conversion to number on constructor
            
    def __int__(self) :
        return int(self.real_value())
    def __float__(self) :
        return float(self.real_value())

    def __str__(self) :
        return str(self.num) + (("/" + str(self.den))
                                if self.den != 1 else "")
    def __repr__(self) :
        return "Number(" + str(self) + ")"

    
    
    
