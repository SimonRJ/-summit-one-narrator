"""Finite models used by the independent computations in the lesson audit."""
from functools import lru_cache
from itertools import combinations, permutations, product


def only(values):
    values = list(values)
    if len(values) != 1:
        raise ValueError(f'Expected one answer, found {values!r}')
    return values[0]


def yn(condition):
    return 'yes' if condition else 'no'


def digits(options, length):
    return [int(''.join(map(str, p))) for p in permutations(options, length) if p[0]]


def pals(length):
    return [n for n in range(10**(length-1), 10**length) if str(n)==str(n)[::-1]]


def divisors(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def prime(n):
    return n > 1 and len(divisors(n)) == 2


def last_under_print_budget(start, digit, budget):
    for n in range(start, start + 10000):
        budget -= str(n).count(str(digit))
        if budget < 0:
            return n - 1
    raise ValueError('Digit budget did not run out')


def last_under_digit_budget(values, budget):
    last = None
    for n in values:
        budget -= len(str(n))
        if budget < 0:
            break
        last = n
    return last


def rect(width, height):
    return set(product(range(width), range(height)))


def shift(cells, dx, dy):
    return {(x + dx, y + dy) for x, y in cells}


def grid_perimeter(cells):
    return sum((x+dx,y+dy) not in cells for x,y in cells
               for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))


def cube_surface(cells):
    return sum((x+dx,y+dy,z+dz) not in cells for x,y,z in cells for dx,dy,dz
               in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)))


def surface(dims):
    return 2 * sum(a*b for a,b in combinations(dims,2))


def count_in_cuboid(dims, painted, target, keep):
    marked = set(painted)
    return sum(sum((2*i in marked and v==0) + (2*i+1 in marked and v==dims[i]-1)
                   for i,v in enumerate(p))==target
               for p in product(*(range(n) for n in dims)) if keep(*p))


def paint_count(dims, painted, target):
    return count_in_cuboid(dims,painted,target,lambda *_:True)


def small_angle(a,b):
    angle = (a-b) % 360
    return min(angle,360-angle)


def triangle_area(vertices):
    from fractions import Fraction
    return abs(sum(x*b-y*a for (x,y),(a,b) in zip(vertices,vertices[1:]+vertices[:1]))) * Fraction(1,2)


def rotations(marks):
    return [k for k in range(len(marks)) if marks[k:]+marks[:k]==marks]


def reflections(marks):
    n=len(marks)
    return [k for k in range(n) if all(marks[i]==marks[(k-i)%n] for i in range(n))]


def switched_states(n, count, moves):
    masks = [sum(1 << i for i in indices) for indices in combinations(range(n),count)]
    states = {0}
    for _ in range(moves):
        states = {state ^ mask for state in states for mask in masks}
    return states


def reachable(start, steps, moves):
    states = {start}
    for _ in range(moves):
        states |= {state + step for state in states for step in steps}
    return states


def flips_3x3():
    masks = [sum(1 << (3*(r+i)+c+j) for i,j in product(range(2),repeat=2))
             for r,c in product(range(2),repeat=2)]
    states = {0}
    for mask in masks:
        states |= {m ^ mask for m in states}
    return states


def iterate(value, times, step):
    for _ in range(times):
        value = step(value)
    return value


@lru_cache(None)
def chains(length, steps):
    if length == 0:
        return ((),)
    return tuple((step,*tail) for step in steps if step <= length for tail in chains(length-step,steps))


def up_paths(x,y):
    for ups in combinations(range(x+y),y):
        a=b=0
        path=[(a,b)]
        for i in range(x+y):
            if i in ups:
                b += 1
            else:
                a += 1
            path.append((a,b))
        yield path


def trail_ends(edges, start):
    if not edges:
        yield start
    for i,(a,b) in enumerate(edges):
        if start in (a,b):
            yield from trail_ends(edges[:i]+edges[i+1:],b if start==a else a)


def prob(outcomes, condition):
    from fractions import Fraction
    outcomes=list(outcomes)
    return Fraction(sum(map(condition,outcomes)),len(outcomes))


def domino_possible(cells):
    if not cells:
        return True
    x,y=min(cells)
    return any((a,b) in cells and domino_possible(cells-{(x,y),(a,b)})
               for a,b in ((x+1,y),(x,y+1)))


def line_flips_3x3():
    masks = [sum(1 << i for i in line) for line in ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8))]
    states = {0}
    for mask in masks:
        states |= {m ^ mask for m in states}
    return states
