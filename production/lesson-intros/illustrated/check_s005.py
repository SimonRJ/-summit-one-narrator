"""Independent arithmetic and counting checks for lesson S005."""
assert sum(int(d) for d in '5724') == 18 and 5724 % 9 == 0
assert sum(str(n).count('4') for n in range(1, 66)) == 17
multiples = [n for n in range(1, 251) if n % 9 == 0]
assert [n for n in multiples if n % 10 == 2] == [72, 162]
assert [n for n in multiples if (n // 10) % 10 == 2] == [27, 126, 225]
assert [n for n in multiples if n // 100 == 2] == [207, 216, 225, 234, 243]
assert sum(str(n).count('2') for n in multiples) == 10
assert str(225).count('2') == 2 and 252 % 9 == 0 and 252 > 250
print('S005: digit sum, positions, exclusions and double counting verified')
