import secrets
def is_prime(n, k = 20):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    
    # n-1 = d*2^s
    d, s, = n - 1, 0
    
    while d % 2 == 0:
        s += 1
        d //= 2
    
    for _ in range(k): 
        a = secrets.randbelow(n - 3) + 2       
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
            
        for _ in range(s - 1):
            x = pow(x, 2, n)
            
            if x == n - 1:
                break
                
        else:
            return False
    return True
    
def generate_poly(p, s, n, k):
    if not is_prime(p):
        raise ValueError("p mast be prime")
    if not 0 <= s < p:
        raise ValueError(f"secret must be in [0; {p-1}]")
    if not 1 <= k <= n:
        raise ValueError(f"k mast be in [1; {n}]")
    if n >= p:
        raise ValueError(f"n must be less than p = {p}")    
    
    coeffs = [s] + [secrets.randbelow(p) for _ in range(k - 1)]
    while k > 1 and coeffs[-1] == 0:
        coeffs[-1] = secrets.randbelow(p) 
    return coeffs
 
def gorner(coeffs, x, p):
    in_point = 0
    for c in reversed(coeffs):
        in_point = (in_point*x + c) % p
    return in_point
        
def gen_part_secret(n, s, p, k):
    coeffs = generate_poly(p, s, n, k)
    return {i: gorner(coeffs, i, p) for i in range(1, n+1)}
    


def recover_secret(shares, p): # через лагранжа
    
    secret = 0
    for xi, yi in shares.items():
        
        num = 1 
        den = 1
        for xj, yj in shares.items():
            if xi == xj:
                continue
                
            num = (num * -xj) % p
            den = (den * (xi - xj)) % p
        
        lagrange_basis = (num * pow(den, -1, p)) % p
        secret = (secret + yi * lagrange_basis) % p
        
    return secret
    
if __name__ == "__main__":

    # пример из первой задачи
    p = 127; s = 123; n = 3; k = 3
    known = gen_part_secret(n, s, p, k)
    secret = recover_secret(known, p)
    print(f"доли: {known}")
    print(f"секрет a = f(0) = {secret}")
 