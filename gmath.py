import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(view)
    normalize(light[LOCATION])
    a = calculate_ambient(ambient,areflect)
    d = calculate_diffuse(light,dreflect,normal)
    s = calculate_specular(light,sreflect,view,normal)
    i = [a[i] + d[i] + s[i] for i in range(3)]
    i = limit_color(i)
    return i


def calculate_ambient(alight, areflect):
    ans = [-1,-1,-1]
    for i in range(3):
        ans[i] = alight[i] * areflect[i]
    ans = limit_color(ans)
    return ans

def calculate_diffuse(light, dreflect, normal):
    ans = [-1,-1,-1]
    for i in range(3):
        ans[i] = light[COLOR][i] * dreflect[i] * dot_product(light[LOCATION], normal)
    ans = limit_color(ans)
    return ans

#according to "conitec.net" refection is equal to 2 * (N*L)*N L lol
#yeah for this one I might have copied notes badly this is confusing as fudge
# [2n^ (l^ dot n^) - l^] dot v^
def calculate_specular(light, sreflect, view, normal):
    spec = [0,0,0]
    #cos_a = r^ dot v^
    #r^ = 2n^(l^*n^)-l^
    cos_alpha = 2 * dot_product(light[LOCATION],normal)
    for i in range(3):
        spec[i] = (cos_alpha * normal[i]) - light[LOCATION][i]
    cos_alpha = math.pow(cos_alpha,SPECULAR_EXP)
    for i in range(len(spec)):
        spec[i] = light[COLOR][i] * sreflect[i] * cos_alpha
    return limit_color(spec)
        
        
    

def limit_color(color):
    for i in range(len(color)):
        if color[i] > 255:
            color[i] = 255
        if color[i] < 0:
            color[i] = 0
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
