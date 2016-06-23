r1 = [1, 1, 7]
r2 = [2, 3, 4]
r3 = [3, 1, 1]
rot = [r1, r2, r3]
ref = "UKW-A"
plugs = ["AB", "CD", "EF", "GH", "IJ"]
rotors = []
rotors.append([rot[0][0], rot[0][1], rot[0][2]])
rotors.append([rot[1][0], rot[1][1], rot[1][2]])
print(rotors)
