"""Independently verify the token, chalk and reverse-working examples."""
assert len([(group,item) for group in range(3) for item in range(5)])==15
assert 15//3==5 and 15-5==10 and 10+5==15
assert len([(group,item) for group in range(3) for item in range(10)])==30
assert 30-30//3==20 and 20-20//2==10
solutions=[]
for start in range(1,1001):
    if start%3:continue
    after_first=start-start//3
    new_whole=after_first+4
    if new_whole%2==0 and new_whole-new_whole//2==12:
        solutions.append(start)
assert solutions==[30]
assert 12*2==24 and 24-4==20 and 20//2*3==30
assert 30-10==20 and 20+4==24 and 24-12==12
assert 30//3==10 and 20//2==10
print('S022: exact group sizes, changed wholes, inverse and forward checks verified')
