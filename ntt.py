def ntt(a, q, root, inverse=False):
    n = len(a)
    if inverse:
        root = pow(root, q-2, q)  # Calculate the inverse element
    result = [0] * n
    levels = n.bit_length() - 1
    if len(a) != 1 << levels:
        raise ValueError("Length of input vector must be a power of 2")
    
    # Bitwise reverse the input data
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j >= bit:
            j -= bit
            bit >>= 1
        j += bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    
    # NTT main loop
    length = 2
    while length <= n:
        angle = pow(root, (q-1) // length, q)
        for i in range(0, n, length):
            w = 1
            for j in range(length // 2):
                u = a[i + j]
                v = (a[i + j + length // 2] * w) % q
                a[i + j] = (u + v) % q
                a[i + j + length // 2] = (u - v) % q
                w = (w * angle) % q
        length *= 2
    
    # If it is an inverse transform, it is necessary to divide by the modular inverse of n
    if inverse:
        n_inv = pow(n, q-2, q)
        for i in range(n):
            a[i] = (a[i] * n_inv) % q
    
    return a
