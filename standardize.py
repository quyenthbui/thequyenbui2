import unidecode
def ChuanHoa(n):
    n =n.lower()
    n = n.title()
    n = n.strip()
    for i in range(len(n)):
        n = n.replace('  ', ' ',)
    return n
def ChuanHoa1(n):
    n = unidecode.unidecode(n)
    n =n.lower()
    n = n.title()
    n = n.strip()
    for i in range(len(n)):
        n = n.replace('  ', ' ')
        n = n.replace(' ', '+')
        n = n.replace('-', '+')
        n = n.replace('&', '+')
        n = n.replace(',', '+')
        n = n.replace('.', '+')
    return n
