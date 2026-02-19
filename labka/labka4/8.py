def gen_primes(n):
    for num in range(2, n + 1):
        is_prime = True
        for d in range(2, int(num ** 0.5) + 1):
            if num % d == 0:
                is_prime = False
                break
        if is_prime:
            yield num


n = int(input())
print(*gen_primes(n))