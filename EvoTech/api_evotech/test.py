liste_introduite = [
    13, 46, 31, 27, 22, 20, 29, 48, 2, 38, 14,
    42, 44, 26, 17, 51, 9, 16, 35, 15, 6, 34, 10, 28,
    18, 25, 21, 23, 36, 41, 24, 4, 19, 5, 40, 12, 7, 57, 43,
    39, 30, 33, 55, 56,
    45, 8, 38, 32, 37, 52,
    3, 32, 47, 11, 1, 53, 54, 50, 49, 58
]


tous_les_nombres = set(range(1, 59))
nombres_manquants = tous_les_nombres - set(liste_introduite)

print("Les nombres manquants dans la liste sont :")
print(sorted(nombres_manquants))
