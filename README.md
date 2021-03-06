# You can create bitboards and shift them around:

```
from bitboards import fromList, shift, pp, toList

B = fromList([[1,0,0],
              [1,0,0],
              [0,0,0],
              [0,0,0]])

shiftFunction = shift(boardShape=(4,3), shiftVector=(1,1))

pp((4,3), shiftFunction(B))
pp((4,3), shiftFunction(B) | B)

L = toList((4,3), B)
```

Note: the pp function only pretty-prints a 2D bitboard (or a 3D bitboard where the 3rd dimension is bit depth, see below).

Note: `shift` does a bunch of math. Don't call it in a tight loop. Instead, call it once for each shift function you need.

# You can use the last coordinate for bit depth.
Bit depth n means each cell stores a number from 0 to 2^n-1.

```
from bitboards import gte

B = fromList([[1,2,3],
              [0,1,4]], bitDepth=4) # entries are from 0 to 15
C = fromList([[0,4,3],
              [1,1,5]], bitDepth=4)

greaterThanFunction = gte((2,3,4))
# now greaterThanFunction compares two bitboards of shape (2,3,4)
# where the last coordinate 4 is the bit depth. It returns a
# bitboard of shape (2,3) computing the boolean >= of the inputs.

pp((2,3,4), B+C)
pp((2,3,4), greaterThanFunction(B, C))

L = toList((2,3,4), B+C, bitDepth=True)
```

NOTE: Just like `shift`, the function `gte` does a bunch of math. Don't call it in a tight loop. Instead, call it once for each shape of >= function you need.

NOTE: using the greaterThanFunction requires that B and C don't use the most significant bit in any entry. The function checks this for you (costing like 2 extra bitops) unless you pass checkSignificantBit=False.

NOTE: for bitboards with bit depth, the `shift` and `gte` functions expect the bit depth to be included as the last coordinate of the first argument `boardShape`.
