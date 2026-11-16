"""Check all S015 remainder and interval examples independently."""
assert divmod(37,5)==(7,2)
candidates=[n for n in range(340,350) if n%4==0]
assert candidates==[340,344,348]
assert [n for n in candidates if n%3==0]==[348]
valid=[n for n in range(56,212) if n%4==3 and n%6==5]
shifted=[n for n in range(57,213) if n%12==0]
assert shifted==list(range(60,205,12)) and len(shifted)==13
assert [n+1 for n in valid]==shifted and len(valid)==13
assert valid[0]==59 and valid[-1]==203
assert (204-60)//12==12
print('S015: counter remainder, digit tests, shifted interval and 13 solutions verified')
