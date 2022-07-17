print("Hi to our cube solver, please follow the input method." )
print("""Notice that the colors for each side should inputed as
red --> r
green --> g
blue --> b
orange --> o
white --> w
yellow --> y
""")

face1 = []
face2 = []
face3 = []
face4 = []
face5 = []
face6 = []

def red_center():
    face = c1, c2, c3, c4, c5, c6 = input("Enter the colors for the face with red center : ").split()
    return face1.append(face)

def green_center():
    face = c1, c2, c3, c4, c5, c6 = input("Enter the colors for the face with green center : ").split()
    return face2.append(face)

def blue_center():
    face = c1, c2, c3, c4, c5, c6 = input("Enter the colors for the face with blue center : ").split()
    return face3.append(face)

def white_center():
    face = c1, c2, c3, c4, c5, c6 = input("Enter the colors for the face with white center : ").split()
    return face4.append(face)

def orange_center():
    face = c1, c2, c3, c4, c5, c6 = input("Enter the colors for the face with orange center : ").split()
    return face5.append(face)

def yellow_center():
    face = c1, c2, c3, c4, c5, c6 = input("Enter the colors for the face with yellow center : ").split()
    return face6.append(face)

red_center()
green_center()
blue_center()
white_center()
orange_center()
yellow_center()

print(face1)
print(face2)
print(face3)
print(face4)
print(face5)
print(face6)
