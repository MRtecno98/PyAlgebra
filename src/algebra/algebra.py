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

EXTRACT_PRECISION = 14
def decimal_part(decimal, str_manipulation=False) :
    if not isinstance(decimal, float): return 0
    return round(decimal % 1, EXTRACT_PRECISION) if not str_manipulation \
            else float(".".join(["0", str(decimal).split(".")[1]]))

def decimal_to_number(decimal, reduce=True) :
    decimals = len(str(decimal).split(".")[1]) if isinstance(decimal, float) \
               else 0
    factor = 10 ** decimals

    # n = Number(int(decimal * factor), denominator=factor)
    n = Number(int(str(decimal).replace(".", "")), denominator=factor)
    return n.reduce() if reduce else n


def extract_root(base, n=2) :
    try :
        return base.__radext__(n)
    except:
        try :
            return base**(1/n)
        except Exception as exc :
            if n == 2 :
                return math.sqrt(base)
            raise TypeError("Unsupported operation") from exc

class AlgebricException(Exception) :
    "For Algebric errors"

class Numerical :
    pass

class Number(Numerical) :
    def __init__(self, numerator, denominator=1) :
        numerator = numerator if not isinstance(numerator, float) \
                   else decimal_to_number(numerator)
        denominator = denominator if not isinstance(denominator, float) \
                   else decimal_to_number(denominator)
        
        if isinstance(numerator, Number) :
            if denominator == 1 :
                self.__init__(numerator.num, numerator.den)
                return
            if numerator.den == 1 :
                numerator = int(numerator.real_value())

        if isinstance(denominator, Number) :
            if denominator.den == 1 :
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

    def __radext__(self, n) :
        #TODO Irrationals!
        return self**Number(1, n)
            
    def __int__(self) :
        return int(self.real_value())
    def __float__(self) :
        return float(self.real_value())

    def __str__(self) :
        return ("{}" if not isinstance(self.num, Number) else "({})") \
                        .format(self.num) \
                + (("/{}" if not isinstance(self.den, Number) else "/({})") \
                        .format(self.den) \
                    if self.den != 1 else "")
    
    def __repr__(self) :
        return "Number(" + str(self) + ")"

class Variable() :
    def __init__(self, letter, exponent=1) :
        self.letter = letter
        self.exponent = exponent

    def __str__(self) :
        return "{}^{}".format(str(self.letter), str(self.exponent))
    def __repr__(self) :
        return "Variable({})".format(str(self))

class Monomial(Numerical) :
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

    def __pow__(self, other) :
        if isinstance(other, (Monomial, Polynomial)) :
            raise AlgebricError("Can't raise to a not-number")
        res = self
        for i in range(other - 1) :
            res = res * self
        return res

    def __add__(self, other) :
        mother = other
        if not isinstance(other, Monomial) :
            mother = Monomial(other)
        if self.sign_vars() == mother.sign_vars() \
                or (mother.coefficient == 0 and
                        len(mother.sign_vars()) == 0) :
            return Monomial(self.coefficient + mother.coefficient, \
                            *(self.variables))
        else :
            return Polynomial(self, mother)

    def __radd__(self, other) :
        mother = other
        if not isinstance(other, Monomial) :
            mother = Monomial(other)
        if self.sign_vars() == mother.sign_vars() \
                or (mother.coefficient == 0 and
                        len(mother.sign_vars()) == 0) :
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

class Polynomial(Numerical) :
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

class Matrix() :
    def __init__(self, raw_matrix) :
        if not equal(*[len(x) for x in raw_matrix]) :
            raise TypeError("Inappropriate raw matrix")
        self.raw_matrix = raw_matrix

    def get_dimensions(self) :
        return len(self.raw_matrix), len(self.raw_matrix[0])

    def is_squared(self) :
        return equal(*self.get_dimensions())

    def get_order(self) :
        return self.get_dimensions()[0] if self.is_squared() else None

    def is_line(self) :
        return self.get_dimensions()[0] == 1

    def is_column(self) :
        return self.get_dimensions()[1] == 1

    @staticmethod
    def get_identity_matrix(lines, columns) :
        return Matrix([[(1 if line==column else 0) \
                 for column in range(1, columns+1)] \
                for line in range(1, lines+1)])
    
    @staticmethod
    def get_null_matrix(lines, columns) :
        return Matrix([[0 for column in range(1, columns+1)] \
                for line in range(1, lines+1)])

    def get_column(self, column) :
        return [line[column-1] for line in self]

    def get_columns(self) :
        return [self.get_column(column+1) \
                for column in range(self.get_dimensions()[1])]

    def get_line(self, line) :
        return self.raw_matrix[line-1]

    def get_algebric_complement(self, line, column) :
        return (-1)**(line+column) * \
            self.get_lower_complementar(line, column)

    def get_determinant(self) :
        if not self.is_squared() :
            raise TypeError("Can't calculate determinant of non-squared matrix")

        if self.get_order() == 2 :
            return (self[1,1]*self[2,2]) - (self[1,2]*self[2,1])
        else :
            det = 0
            column = 1
            for line in range(1, self.get_dimensions()[0]+1) :
                det += self[line, column] * \
                       self.get_algebric_complement(line, column)
            return det

    def get_lower_complementar(self, line, column) :
        dims = self.get_dimensions()
        res = []
        for linei in range(1, dims[0]+1) :
            nline = []
            for columni in range(1, dims[1]+1) :
                if columni != column and linei != line :
                    nline.append(self[linei, columni])
            if nline : res.append(nline)
        return Matrix(res).get_determinant()

    def get_inverse_matrix(self) :
        dims = self.get_dimensions()
        return 1/self.get_determinant() * \
               Matrix([[self.get_algebric_complement(line, column) \
                        for column in range(1,dims[1]+1)] \
                       for line in range(1,dims[0]+1)])

    def __getitem__(self, key) :
        if sum(key) < 2 : raise TypeError("Matrix index can't be 0")
        return self.raw_matrix[key[0]-1][key[1]-1]

    def __setitem__(self, key, value) :
        if sum(key) < 2 : raise TypeError("Matrix index can't be 0")
        self.raw_matrix[key[0]-1][key[1]-1] = value

    def __delitem__(self, key) :
        raise TypeError("Matrix object doesn't support item deletion")

    def __iter__(self) :
        return self.raw_matrix.__iter__()
    
    def __str__(self) :
        SPACE = 2

        values_block = ""
        columns_maxlens = [max([len(str(a)) for a in column]) for column in self.get_columns()]
        for line in self :
            values_block += "|" + " "*SPACE
            
            column = 0
            for a in line :
                values_block += str(a) + " "*(columns_maxlens[column] \
                                              - len(str(a)) + SPACE)
                column+=1

            values_block += "|"
            values_block+="\n"

        line_maxlen = max([len(line) for line in values_block.split("\n")])
        curve = " {0}" + " "*(line_maxlen-4) + "{0}\n"
        
        return "\n" + curve.format("_") + values_block + curve.format("¯")       

    def __repr__(self) :
        dim = self.get_dimensions()
        firstline = "Matrix({}x{}{})\n".format(dim[0],dim[1], \
                                    ", {}th order".format(self.get_order())\
                                           if self.is_squared() else "")
        strself = str(self)
        return firstline + "\n".join([" "*(int((len(firstline) - len(strself.split("\n")[1])) / 2)-1) + line for line in strself.split("\n")])

    def __add__(self, other) :
        if not isinstance(other, Matrix) :
            raise TypeError("Unsupported sum between Matrix and " \
                            + other.__class__.__name__)
        if not self.get_dimensions() == other.get_dimensions() :
            raise TypeError("Unsupported sum between different Matrixes")

        dim = self.get_dimensions()
        return Matrix([[self[i,j] + other[i,j] \
                 for j in range(1, dim[1]+1)] \
                 for i in range(1, dim[0]+1)])
    
    def __radd__(self, other) :
        return self.__add__(other)

    def __mul__(self, other) :
        dim = self.get_dimensions()
        if not isinstance(other, Matrix) :
            return Matrix([[self[i,j] * other \
                     for j in range(1, dim[1]+1)] \
                     for i in range(1, dim[0]+1)])
        else :
            if not dim[1] == other.get_dimensions()[0] :
                raise TypeError("Cannot multiplicate incompatible matrixes")
            res = [[sum([line[i]*column[i] \
                         for i in range(len(line))]) \
                    for column in other.get_columns()] \
                   for line in self]
            return Matrix(res)

    def __pow__(self, exponent) :
        res = 1
        if exponent < 0 :
            exponent = abs(exponent)
            self = Number(1,self)
        for i in range(exponent) :
            res *= self
        return res

    def __rmul__(self, other) :
        return self.__mul__(other)

    def __neg__(self) :
        return self*-1

    def __sub__(self, other) :
        return self + (-other)

    def __rsub__(self, other) :
        return other + (-self)
    
