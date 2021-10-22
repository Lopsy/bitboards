# You can create bitboards and shift them around:

```
B = fromList([[1,0,0],
              [1,0,0],
              [0,0,0],
              [0,0,0]])

shiftFunction = shift(boardShape=(4,3), shiftVector=(1,1))

pp((4,3), shiftFunction(B))
pp((4,3), shiftFunction(B) | B)

L = toList((4,3), B)
```

# You can use the last coordinate for bit depth.
Bit depth n means each cell stores a number from 0 to 2^n-1.

```
B = fromList([[1,2,3],
              [0,1,4]], bitDepth=4) # entries are from 0 to 15
C = fromList([[0,4,3],
              [1,1,5]], bitDepth=4)

greaterThanFunction = gte((2,3,4))

pp((2,3,4), B+C)
pp((2,3,4), greaterThanFunction(B, C))
```

# NOTE: using the greaterThanFunction requires that B and C don't use the
# most significant bit in any entry. The function checks this for you
# (costing like 2 extra bitops) unless you pass checkSignificantBit=False.

```
L = toList((2,3,4), B+C, bitDepth=True)
```
