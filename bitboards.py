"""

# You can create bitboards and shift them around:

B = fromList([[1,0,0],
              [1,0,0],
              [0,0,0],
              [0,0,0]])

shiftFunction = shift(boardShape=(4,3), shiftVector=(1,1))

pp((4,3), shiftFunction(B))
pp((4,3), shiftFunction(B) | B)

L = toList((4,3), B)

# You can use the last coordinate for bit depth:

B = fromList([[1,2,3],
              [0,1,4]], bitDepth=4) # entries are from 0 to 15
C = fromList([[0,4,3],
              [1,1,5]], bitDepth=4)

greaterThanFunction = gte((2,3,4))

pp((2,3,4), B+C)
pp((2,3,4), greaterThanFunction(B, C))

# NOTE: using the greaterThanFunction requires that B and C don't use the
# most significant bit in any entry. The function checks this for you
# (costing like 2 extra bitops) unless you pass checkSignificantBit=False.

L = toList((2,3,4), B+C, bitDepth=True)

"""

import numpy as np
from functools import reduce

def shift(boardShape, shiftVector):
    """ e.g. shift a shape (7,5) board by (-3,1).
    Returns a function to apply to your bitboards. """
    shiftAmount = position(boardShape, shiftVector)
    filledMask = rectangle(
        boardShape,
        [(v,d) if v>=0 else (0,d+v) for v,d in zip(shiftVector, boardShape)]
    ) # AND by this at the end
    if shiftAmount > 0:
        def shifted(bitboard):
            return (bitboard << shiftAmount) & filledMask
        return shifted
    else:
        shiftAmount *= -1
        def shifted(bitboard):
            return (bitboard >> shiftAmount) & filledMask
        return shifted

def gte(boardShape):
    """ returns a function (board1, board2) -->
    board with ones in the slots where board1 >= board2.
    Assumes the final coordinate is used for bit depth.

    Entries of board1 and board2 CANNOT use most significant bit. """
    #raise NotImplementedError
    # todo: implement this and eq
    ones = np.zeros(boardShape,dtype="bool"); ones[...,0] = 1
    ones = fromList(ones)
    bigs = ones << (boardShape[-1]-1)
    def greaterThanOrEqual(board1, board2, checkSignificantBit=True):
        if checkSignificantBit:
            assert board1 & bigs == 0
            assert board2 & bigs == 0
        return (((board1 | bigs) - board2) & bigs) >> (boardShape[-1]-1)
    return greaterThanOrEqual

def toList(boardShape, bitboard, bitDepth=None):
    realShape = tuple(boardShape) + (bitDepth,) if bitDepth else boardShape
    L = list(map(int, bin(bitboard)[2:]))
    L = [0]*(reduce(lambda x,y:x*y, realShape) - len(L)) + L
    L = np.reshape(L[::-1], realShape)
    if not bitDepth: return L
    else:
        result = L[...,0]
        for i in range(1,boardShape[-1]): result += (2**i) * L[...,i]
        return result

def fromList(L, bitDepth=None):
    if bitDepth:
        shape = np.array(L).shape+(bitDepth,)
        def leftpad(s,length): return "0"*(length-len(s))+s
        bitstring = "".join(leftpad(bin(b)[2:],bitDepth)[::-1]
                            for b in np.reshape(L,(-1,)))
        return int(bitstring[::-1], 2)
    shape = np.array(L).shape
    bitstring = "".join("1" if b else "0" for b in np.reshape(L,(-1,)))
    return int(bitstring[::-1], 2)

def product(lists, bitDepth=None):
    """ For example, product([[1,0,1],[1,1,1,1]]) is
        [[1,1,1,1],
         [0,0,0,0],
         [1,1,1,1]]. """
    N = [1]
    for L in lists: N = np.multiply.outer(N, L)
    return fromList(N, bitDepth)

def pp(boardShape, bitboard):
    """ 2D boards only.
    Use a 3rd coordinate of boardShape for bit depth, if applicable. """
    L = toList(boardShape, bitboard, bitDepth=None)
    for row in L:
        if len(boardShape)==2:
            print("".join("x" if thing else "." for thing in row))
        elif len(boardShape)==3:
            def char(thing):
                # thing is like (1,1,0,0,1)
                a = 0
                for b in thing[::-1]:
                    a *= 2; a += b
                try:
                    return ".123456789Tabcdefghijklmnopqrstuvwxyz"[a]
                except IndexError:
                    return "@"
            print("".join(char(thing) for thing in row))

### HELPER FUNCTIONS ###

def geom(start, factor, terms):
    """ Sum of geometric series. """
    return start * (factor**terms - 1)//(factor - 1)

def position(boardShape, coordinates):
    """ e.g. on a board of shape (7,5), cell (1,2) is the 8th cell. """
    #assert all(x < d for x,d in zip(coordinates, boardShape))
    total, stride = 0, 1
    for dim, coord in zip(boardShape[::-1], coordinates[::-1]):
        total += stride * coord
        stride *= dim
    return total

def rectangle(boardShape, bounds):
    total, stride = 1, 1
    for dim, (start, stop) in zip(boardShape[::-1], bounds[::-1]):
        total *= geom(1 << stride*start, 1 << stride, stop-start)
        stride *= dim
    return total
