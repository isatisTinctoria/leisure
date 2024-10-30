# >>> help(RSL.py)
#
# I'm RSL,
# Rock, Soil & Leave,
# from 2022.1.27 to 2022.2.23,
# A simple, naive version of Minecraft.
# Without
# smooth shades,
# abundant elements,
# adventurous survival,
# and, astonishing efficiency.
# But in me,
# you can still build,
# watch brilliant natural landscape,
# embrace freedom, excitement, and, happiness.
#
# help> HowToPlay()
#
# -------------------------------------------
# |      *EVENTS*      |      *EFFECTS*     |
# -------------------------------------------
# | O                  | parameter          |
# | F11                | fullscreen         |
# | WASD               | move               |
# | SPACE              | jump/ascend        |
# | LSHIFT             | descend            |
# | NUMLOCK            | ghost              |
# | CAPSLOCK           | perspective eye    |
# | MOUSELEFT          | crash              |
# | MOUSERIGHT         | place              |
# | MOUSEWHEEL(press)  | GRAVITY/FLIGHT     |
# | MOUSEWHEEL(scroll) | next type          |
# -------------------------------------------
#
# help> Version()
#
# V.1.0.0. Welcome visit wzb200488@163.com!
#
# help> Settings()
#
import pygame
from pygame.locals import *
from random import random , randint

from numpy import sin as s
from numpy import cos as c
from numpy import array as A
from numpy import zeros as Z
from numpy import arctan , pi , sign , tan

pygame.init()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False) # virtual input mode
pygame.display.set_caption("RSL")
screen = pygame.display.set_mode([800 , 600])
keep_going = True

# basic pygame.draw methods
pdc , pdl , pdp , pdr = pygame.draw.circle , pygame.draw.line , pygame.draw.polygon , pygame.draw.rect


# help> Functions()
#
# Turn ATime into 24-hour 
def ATIME():
        return "%02d : %02d" % divmod((ATime + 90) % 360 * 4 , 60)


# Draw the crosshair
def Aim(W):
        # Using invert colour to adapt to the background  
        C = cReverse(screen.get_at([400 , 300]))
        pdl(screen , C , [400 - W , 300] , [400 + W , 300] , 5)
        pdl(screen , C , [400 , 300 - W] , [400 , 300 + W] , 5)


# Quickview lists
# Warning: Calling the function too many times may reduce performance
def Browse(_list , P):
        return _list[int(P[0])][int(P[1])][int(P[2])]


# Detect collisions (Press [NumLock] to activate or cancel this operation)
# Tip: Leave blocks are penetrable
def CS():
        if not L[K_NUMLOCK]: return

        global E , V , air
        K , _K = Z([3]) , [0] * 6 # deltas , sections
        for i in range(3):
                _K[2 * i]     = int( O[2 * i])
                _K[2 * i + 1] = int(_K[2 * i] + R[i][1] - R[i][0]) + 1 # Adapt to the size of body
        
        for K[0] in range(_K[0] , _K[1]):
                for K[1] in range(_K[2] , _K[3]):
                        for K[2] in range(_K[4] , _K[5]):
                                if not (V[0] or V[1] or V[2]): return              # All dimensions have been checked
                                if IN_WORLD(K) and not Browse(Map , K) in {0 , 3}: # Exclude <air> and <leave>
                                        i , j , k = 2 , 0 , 1
                                        
                                        # Consider each dimension                                        
                                        for _ in range(3):
                                                i , j , k = j , k , i
                                                if not V[i]: continue                 # This dimension has been checked
                                                _V = Z([3]) ; _V[i] = int(sign(V[i])) # Record the direction
                                                
                                                # Predict future situation
                                                if Browse(Map , K - _V) in {0 , 3}:
                                                        if V[i] < 0: _E = E + V * (-R[i][0] + K[i] + 1 - E[i]) / V[i] # backwards
                                                        if V[i] > 0: _E = E - V * ( R[i][1] + E[i] - K[i])     / V[i] # forwards

                                                        # Record criteria frames
                                                        _O  = [_E[j] + R[j][0] , _E[j] + R[j][1] , _E[k] + R[k][0] , _E[k] + R[k][1]] # yours
                                                        _O_ = [ K[j] , K[j] + 1 , K[k] , K[k] + 1]                                    # blocks

                                                        # You will hit this block
                                                        if INTERSECT(2 , _O , _O_):
                                                                E[i] = _E[i]                                    # normal force
                                                                if i == 2 and V[i] < 0:air = Air                # Reset hop count
                                                                if i == 2 and V[i] > 0 and not FM: V[i] = -V[i] # elastic collision 
                                                                else:                              V[i] = 0     # perfect inelastic collision
                                                                break


# Display a single block
# Warning: Remember not using Browse() & array.all() to slow down your program
def Cube(C , I):
        Is   , Stk  =   [ ]  ,   [0]  # id of 12 apexes , stack for iter_DFS
        _vis , vis_ = Z([8]) , Z([8]) # whether an apex is behind face , whether an apex has been visited in DFS
        
        _G = [[0 , 1 , 3 , 2] , [0 , 1 , 5 , 4] , [0 , 2 , 6 , 4] ,
              [1 , 3 , 7 , 5] , [2 , 3 , 7 , 6] , [4 , 5 , 7 , 6]]   # list of 4 indexes of apexes in 6 faces

        G_ = [[1 , 2 , 4] , [0 , 3 , 5] , [0 , 3 , 6] , [1 , 2 , 7] ,
              [0 , 5 , 6] , [1 , 4 , 7] , [2 , 4 , 7] , [3 , 5 , 6]] # adjacency list for DFS

        # Pick visible apexes
        for i in range(2):
                for j in range(2):
                        for k in range(2):
                                P = I + [i , j , k] ; Is.append(P)
                                _I = ID(P - (P - E) / INF)
                                if not (_I[0] == I[0] and _I[1] == I[1] and _I[2] == I[2]):
                                        _vis[(i << 2) + (j << 1) + k] = 1

        # Draw a face when 4 apexes are all in front of your retina
        if L[K_CAPSLOCK]:
                for Q , _Q , Q_ , _Q_ in _G:
                        if _vis[Q] and _vis[_Q] and _vis[Q_] and _vis[_Q_]:
                                P , _P , P_ , _P_ = Is[Q] , Is[_Q] , Is[Q_] , Is[_Q_]
                                if Vis[P[0]][P[1]][P[2]]:
                                        if Vis[_P[0]][_P[1]][_P[2]]:
                                                if Vis[P_[0]][P_[1]][P_[2]]:
                                                        if Vis[_P_[0]][_P_[1]][_P_[2]]:
                                                                Face(C , [P , _P , P_ , _P_])

        # Draw edges, using DFS to simplify code
        while len(Stk):
                Q = Stk.pop()
                vis_[Q] = 1
                for _Q in G_[Q]:
                        if not vis_[_Q]:
                                Stk.append(_Q)
                                if not L[K_CAPSLOCK] or _vis[Q] and _vis[_Q]:
                                        P , _P = Is[Q] , Is[_Q]
                                        if Vis[P[0]][P[1]][P[2]] and Vis[_P[0]][_P[1]][_P[2]]:
                                                Edge([0 , 0 , 0] , 100 , P , _P)


# Display all the blocks
# Tip: Use bit operations to shorten codes
def Cubes():
        # local variables
        # Ext : Consider a particular point for only one time
        # rg  : boundaries of your sight, [x_lb , x_ub , y_lb , y_ub , z_lb , z_ub]
        # bk  : tuples for sorting, hoping to draw cubes from far to near, [(distance , id)...]        
        bk , I , rg , Ext = [] , ID(E) , [0] * 6 , Z([Vol[0] + 1 , Vol[1] + 1 , Vol[2] + 1])

        # Calculate rg
        for i in range(3):
                rg[2 * i] , rg[2 * i + 1] = I[i] - r_s , I[i] + r_s + 1
                if rg[2 * i + 1] < 1 or rg[2 * i] >= Vol[i]: return
                if rg[2 * i    ] < 0                       : rg[2 * i] = 0
                if rg[2 * i + 1] > Vol[i]                  : rg[2 * i + 1] = Vol[i]

        # Consider cubes in range one by one
        for i in range(rg[0] , rg[1]):
                for j in range(rg[2] , rg[3]):
                        for k in range(rg[4] , rg[5]):
                                if Map[i][j][k]:
                                        d = (i + 0.5 - E[0]) ** 2 + (j + 0.5 - E[1]) ** 2 + (k + 0.5 - E[2]) ** 2
                                        if d < r_s * r_s:
                                                bk.append((d , [i , j , k]))
                                                for n in range(8):
                                                        _i , _j , _k = i + (n & 1) , j + (n >> 1 & 1) , k + (n >> 2 & 1)
                                                        if not Ext[_i][_j][_k]:
                                                                Q , r = M([_i , _j , _k])
                                                                Ext[_i][_j][_k] , Vis[_i][_j][_k] = 1 , 0
                                                                if Q: Vis[_i][_j][_k] , Rto[_i][_j][_k] , Pos[_i][_j][_k] = 1 , r , T(Q)                                                                                 

        # Correct the order for displayment
        if  L[K_CAPSLOCK]: bk.sort(key = lambda B : -B[0])
        for _ , I in bk:
                _C = Clr[Browse(Map , I)]            # Get type
                C_ = cDivide(_C , [255] * 3 , 1 , 2) # Highlight the cube you're aiming at
                Cube(C_ if I == Ib else _C , A(I))


# Core function of DisPlaying, including cubes and nature
def DP():
        # proper index of colour bar, which adapts to smo 
        IDX  = int(phi / pi * smo * 180)

        # current colours of different elements in nature
        global SKY , SUN , SEA , SUNG , MOON
        SKY , SUN , SEA , SUNG , MOON = cSky[IDX] , cSun[IDX] , cSea[IDX] , cSung[IDX] , cMoon[IDX]

        # RSL.display(all)
        Sky() ; Stars() ; Sung(80) ; Sun(70 / e) ; MoonPlus(70 / e) ; Hor(40) ; Cubes() ; Aim(15) ; Info()


# Specific method of displaying edges of cubes
# Warning: You'd better NOT use Browse() in this function
def Edge(C , W , P , _P):
        pdl(screen,C,Pos[P[0]][P[1]][P[2]],Pos[_P[0]][_P[1]][_P[2]],int((Rto[P[0]][P[1]][P[2]]+Rto[_P[0]][_P[1]][_P[2]])/2*W))


# Specific method of displaying faces of cubes
# Warning: You'd better NOT use Browse() in this function
def Face(C , Ps):
        pdp(screen , C , [Pos[Ps[i][0]][Ps[i][1]][Ps[i][2]] for i in range(4)] , 0)


# Normal method of displaying planar polygon on the screen
def Flat(C , Ps): # colour , list of practical points (need sorting)
        Ts = []
        for P in Ps:
                Q = next(M(P))
                if not Q: return
                Ts.append(T(Q))        
        pdp(screen , C , Ts , 0)


# Provide a list of gradients between two colours
def Gradient(_C , C_ , n):
        Delta = (A(C_) - _C) / (n + 1)
        for _ in range(n):
                _C += Delta
                yield list(_C)


# Smooth the sharp boundary between sky and sea
def Hor(H):
        th = arctan(300 / (e * f))
        if a < th:
                sl = int(e * f * tan(a) + 300) # y of skyline
                if sl < 0: sl = 0              # It's not necessary to display parts out of view
                pdr(screen , SEA , [0 , sl , 800 , 600 - sl])
                if a > -th:                    # equal to 'if abs(a) < th'. Why there's no '0.2'? No height
                        _C_ = Gradient(SKY , SEA , H)
                        for i in range(40):
                                pdr(screen , next(_C_) , [0 , sl + i , 800 , 1] , 0)


# Assign unique indexes to a practical point
def ID(P):
        return [int(P[0]) , int(P[1]) , int(P[2])]


# Judge whether two areas have common parts
def INTERSECT(D , O , _O):
        for i in range(0 , D * 2 , 2):
                if O[i + 1] - _O[i] <= 0 or _O[i + 1] - O[i] <= 0:
                        return False
        return True


# Judge whether a practical point is out of range
# Tip: The total number of times this func is called only depends on R & S
# Warning: Do not replace IN_WORLD() with try: ... except IndexError: pass,
#          as negative indexes were allowed in python list
def IN_WORLD(P):
        for i in range(3):
                if P[i] < 0 or P[i] >= Vol[i]: return False
        return True

# Prepare necessary variables for DP()
def IV():
        global ATime , F , L , MOON , ex , ey , ph , phi , vm , vn

        # for Cube Series
        vm = A([c(b) , s(b) , 0])
        vn = A([c(a) * c(b) , c(a) * s(b) , s(a)])
        
        ex = A([s(b) , -c(b) , 0])
        ey = A([-s(a) * c(b) , -s(a) * s(b) , c(a)])

        F = E + f * vn

        # for Nature Series
        # Control the rise & fall of the sun
        phi += eps
        if phi > 2 * pi: phi = 0

        # Turn 'phi'(rad) into 'ATime'(deg)
        ATime = phi / pi * 180

        # Automatically change the moonphase
        if L[K_TAB] and 85 < ATime < 95:
                L[K_TAB] , ph = 0 , (ph + 1) % 8
        if not (L[K_TAB] or 85 < ATime < 95): L[K_TAB] = 1


# Show vital information about the game
# Tip: Press [I] to show or hide information
def Info():
        if not INFO: return
        C = cReverse(SKY) # adaptation
        if   Clr[0] == 1:  q  = "Rock"
        elif Clr[0] == 2:  q  = "Soil"
        elif Clr[0] == 3:  q  = "Leave"
        if   FM         : _FM = "Flight"
        else            : _FM = "Gravity"
        Msg("Mode: %s"     % _FM , 0 , 40 , 20 , C)
        Msg("Time: %s" % ATIME() , 0 , 80 , 20 , C)
        Msg("Material: %s" %  q  , 0 , 60 , 20 , C)
        Msg("Angle: α = %.2f , β = %.2f" % (180 * a / pi , 180 * b / pi) , 0 , 20 , 20 , C)
        Msg("Pos: x = %.2f , y = %.2f , z = %.2f" % (E[0] , E[1] , E[2]) , 0 ,  0 , 20 , C)


# The MOST basic function above all: initialize the globals
def Init():
        # These globals were sorted in dictionary order
        global   AJ   , ATime ,  Air  ,  Bud  ,  Clr  ,   E   ,   F   ,  FM   , \
                 FULL ,  INF  ,  Ib   ,  Ip   ,   L   ,  MOON ,  Map  ,   O   , \
                 Pos  ,   R   ,  Rto  ,   S   ,  SEA  ,  SKY  ,  SUN  ,  SUNG , \
                 V    ,  Vis  ,  Vol  ,   a   ,  air  ,   b   , cMoon ,  cSea , \
                 cSky ,  cSun , cSung ,   e   ,  eps  ,   ex  ,   ey  ,   f   , \
                 g    ,  ph   ,  phi  ,  r_b  ,  r_s  ,  scl  ,  smo  , stars , \
                 v    ,  vm   ,  vn   ,  INFO

        # help> Meanings()
        #
        # AJ   : initial Vz(s) corresponding to 'air'
        # ATime: game clock, the deg version of 'phi'
        #        -------------------------------------------
        #        |     phi     |    ATime    |   24-hour   |
        #        -------------------------------------------
        #        |      0      |      0      |     6:00    |
        #        -------------------------------------------
        #        |    1/2pi    |      90     |    12:00    |
        #        -------------------------------------------
        #        |     pi      |     180     |    18:00    |
        #        -------------------------------------------
        #        |    3/2pi    |     240     |     0:00    |
        #        -------------------------------------------
        # Air  : maximum of the times you can jump when hovering (standard = 2)
        # Bud  : criteria frames of cubes (only used in Init() & shoot())
        # Clr  : list of colour info, [current type , ROCK , SOIL , LEAVE]
        #        -------------------------------------------
        #        |      1      |      2      |      3      |
        #        -------------------------------------------
        #        |    ROCK     |    SOIL     |    LEAVE    |
        #        -------------------------------------------
        # E    : absolute coordinate of your Eye
        # F    : original point of your retina, F = E + f * vn
        # FM   : game mode
        #        -------------------------------------------
        #        |         0          |         1          |
        #        -------------------------------------------
        #        |      Gravity       |       Flight       |
        #        -------------------------------------------
        # FULL : mode of screen
        #        -------------------------------------------
        #        |         0          |    -2147483648     |
        #        -------------------------------------------
        #        |       NORMAL       |     FULLSCREEN     |
        #        -------------------------------------------
        # INF  : fake infinity = 1024, used in displays of sun, moon & stars
        # Ib   : id of the block you want to break
        # Ip   : id of the block you want to place
        # L    : list of bools, recording press-only pulse
        # MOON : current colour of the moon (so as SEA, SKY, SUN, SUNG)
        # Map  : binary array of the world, visit Map[x][y][z] to check block-type
        #        -------------------------------------------
        #        |         0          |       1, 2, 3      |
        #        -------------------------------------------
        #        |       none         |    same as 'Clr'   |
        #        -------------------------------------------
        # O    : criteria frame of your body
        # Pos  : screen x-y sites of each point
        # R    : size of your body, [[x_lb , x_ub] , [y_lb , y_ub] , [z_lb , z_ub]]
        # Rto  : ratios of each point, r = |EQ| / |EP|
        # S    : precision of shoot(), standard = 10
        # V    : velocity, unit vector
        # Vis  : bool list, whether a certain point is in front of your retina
        # Vol  : size of the world, [x_w , y_w , z_w], standard = [100 , 100 , 100]
        # a    : angle of elevation, range from [-pi , pi]
        # air  : rest of the times you can jump when hovering, range from [0 , Air]
        # b    : angle of horizon, range from [0 , 2pi]
        # cMoon: moon's colour bar of the whole day (so as cSea, cSky, cSun, cSung)
        # e    : ratio of screen x-y and practical deltas, standard = 10000
        # eps  : minimum unit of time, phi += eps
        # ex   : x-direction head vector of your retina (so as ey)
        # f    : focal length
        # g    : absolute value of gravity
        # ph   : current moon phase, range from [0 , 8)
        # phi  : game clock, rad version
        # r_b  : the farthest distance you can build, standard = 10
        # r_s  : visual field, standard = 15 (Warning: the larger, the slower)
        # scl  : number of stars
        # smo  : density of colour bar, len(cX) == smo * 360
        # stars: list of basic information for star displayment
        #        example: [[angle of evevation, angle of horizon, radius, colour], ...]
        # v    : norm of V, standard = 0.05
        # vm   : unit vector of horizontal direction of view
        # vn   : normal vector of your retina

        # Avoid raising IndexError
        K_RSHIFT  , K_LSHIFT   = 303 , 304 # K_RSHIFT  , K_LSHIFT   = 1073742053 , 1073742049
        K_NUMLOCK , K_CAPSLOCK = 300 , 301 # K_NUMLOCK , K_CAPSLOCK = 1073741907 , 1073741881

        # Large arrays
        Vol = [100 , 100 , 100]
        Bud = Z([Vol[0]     , Vol[1]     , Vol[2] , 6])
        Vis = Z([Vol[0] + 1 , Vol[1] + 1 , Vol[2] + 1])
        Rto = Z([Vol[0] + 1 , Vol[1] + 1 , Vol[2] + 1])
        Pos = Z([Vol[0] + 1 , Vol[1] + 1 , Vol[2] + 1 , 2] , dtype = int)
        Map = Z([Vol[0]     , Vol[1] ,     Vol[2]        ] , dtype = int)

        # Basic variables
        INF                               =  1024
        a    ,   b                        =     0  ,   0
        Air  ,  air  ,  FM                =     2  ,   2   ,  1
        e    ,   f   ,   g   ,   v        = 10000  ,   0.1 ,  0.005 ,  0.05
        FULL , INFO  ,  r_b  ,  r_s  ,  S =     0  ,   0   , 10     , 15     , 10

        # Small arrays        
        AJ                                = [   0  ,   0.1 ,  0.13]
        V   ,  vm ,  vn                   = Z([3]) , Z([2]),  A([0 , 0 , 1])
        L   ,  R                          = [1] * 323 , [[-0.5 , 0.5] , [-0.5 , 0.5] , [-1.5 , 0.5]]
        E                                 = A([Vol[0] // 2 - 2 , Vol[1] // 2 + 0.5, Vol[2] // 2 + 0.5])
        Clr                               = [1 , [112 , 128 , 105] , [237 , 189 , 101] , [61 , 145 , 64]]

        # Mark centre block
        mark([Vol[0] // 2 , Vol[1] // 2 , Vol[2] // 2] , 1)

        # Calculate criteria frames of blocks (a waste of time, but necessary)
        for x in range(Vol[0]):
                for y in range(Vol[1]):
                        for z in range(Vol[2]):
                                Bud[x][y][z] = [x , x + 1 , y , y + 1 , z , z + 1]

        # core vars for ATime calculation 
        ph                =  0
        stars , scl       = [ ] , 200
        ATime , phi , eps =  0  ,   0 , 0.0002

        # Initialize attributes of stars randomly
        for _ in range(scl):
                stars.append((random()*pi, random()*2*pi, randint(1,2), cDivide([255]*3, [127]*3, 1, random())))

        # Initialize colour bars
        smo = 8
        cSun_In  = list(A([  0 ,  10 , 170 , 180]             , dtype = int) * smo)
        cSea_In  = list(A([  0 ,  10 , 170 , 180 , 185 , 355] , dtype = int) * smo) 
        cSky_In  = list(A([  0 ,  10 , 170 , 180 , 185 , 355] , dtype = int) * smo)
        cSung_In = list(A([  0 ,  10 , 170 , 180 , 185 , 355] , dtype = int) * smo)
        cMoon_In = list(A([180 , 190 , 240 , 300 , 350 ,   0] , dtype = int) * smo)

        cSun_Cu  = [[255 , 255 ,   0] , [255 , 255 , 255] , [255 , 255 , 255] , [255 , 255 ,   0]]
        cSea_Cu  = [[ 30 ,   0 ,  30] , [160 , 160 , 204] , [160 , 160 , 204] , [ 30 ,   0 ,  30] , [  0 ,   0 ,  30] , [  0 ,   0 ,  30]]
        cSky_Cu  = [[  0 ,   0 ,  50] , [200 , 200 , 255] , [200 , 200 , 255] , [  0 ,   0 ,  50] , [  0 ,   0 ,   0] , [  0 ,   0 ,   0]]
        cSung_Cu = [[139 ,   0 ,   0] , [200 , 200 , 255] , [200 , 200 , 255] , [139 ,   0 ,   0] , [  0 ,   0 ,   0] , [  0 ,   0 ,   0]]
        cMoon_Cu = [[255 , 127 ,  80] , [255 , 215 ,   0] , [214 , 236 , 240] , [214 , 236 , 240] , [255 , 215 ,   0] , [255 , 127 ,  80]]

        cSun     = cInterpolation(360 * smo , cSun_In  , cSun_Cu )
        cSea     = cInterpolation(360 * smo , cSea_In  , cSea_Cu )
        cSky     = cInterpolation(360 * smo , cSky_In  , cSky_Cu )
        cSung    = cInterpolation(360 * smo , cSung_In , cSung_Cu)
        cMoon    = cInterpolation(360 * smo , cMoon_In , cMoon_Cu)


# Detect keyboard/mouse events and run gravity
def KD():
        global Clr ,  E  ,   FM  ,  FULL ,   INFO     ,   L   , \
                V  ,  a  ,  air  ,   b   , keep_going ,  phi

        # observer of keyboard,
        # responds when KEYDOWN changes from 0 to 1
        def Trig(K_GIVEN , CMD , BOOL = True):
                if not(keys[K_GIVEN] or  L[K_GIVEN]):
                        L[K_GIVEN] = 1
                if     keys[K_GIVEN] and L[K_GIVEN] and BOOL:
                        L[K_GIVEN] = 0 ; exec(CMD , globals()) # globals() is necessary

        # Get ready for mark() operation
        shoot()

        # events of interface-quit & mouse-click
        for event in pygame.event.get():
                        if event.type == QUIT:
                                keep_going = False
                        if event.type == MOUSEBUTTONDOWN:
                                if event.button == 2:
                                        FM = not FM
                                if event.button == 1:
                                        if Ib: mark(Ib , 0)
                                if event.button == 3:
                                        if Ip: mark(Ip , Clr[0])
                                if event.button == 4:
                                        Clr[0] = (Clr[0] + 1) % 3 + 1
                                if event.button == 5:
                                        Clr[0] =     Clr[0]   % 3 + 1

        # Reset velocity in x, y directions
        V[0] , V[1] = 0 , 0

        # mouse polling, deltas of mouse
        keys = pygame.key.get_pressed()
        _w , w_ = pygame.mouse.get_rel()
        
        # Use rel as omegas
        a -= w_ / 300
        b -= _w / 300

        # Keep both angles in range
        if a < -pi / 2:  a = -pi / 2
        if a >  pi / 2:  a =  pi / 2
        if b <       0:  b =  pi * 2
        if b >  pi * 2:  b =       0

        # Press [Esc] to quit this game
        if keys[K_ESCAPE]  : keep_going = False

        # Transparent of not?
        if keys[K_CAPSLOCK]: L[K_CAPSLOCK] = 0
        else               : L[K_CAPSLOCK] = 1

        # Penetrable or not?
        if keys[K_NUMLOCK] : L[K_NUMLOCK]  = 0
        else               : L[K_NUMLOCK]  = 1

        # WASD system, controlling horizontal movement
        if keys[K_w]: V += v * A([vm[0] ,  vm[1] , 0.]) 
        if keys[K_s]: V -= v * A([vm[0] ,  vm[1] , 0.])
        if keys[K_d]: V += v * A([vm[1] , -vm[0] , 0.])
        if keys[K_a]: V -= v * A([vm[1] , -vm[0] , 0.])
        
        # Refresh Vz
        if FM: # flight mode
                V[2] = 0
                if keys[K_SPACE] : V[2] += v
                if keys[K_LSHIFT]: V[2] -= v
        else: # gravity mode
                V[2] -= (g + 0.1 * sign(V[2]) * V[2] ** 2) # air friction: dv/dt = -Cv^2
                Trig(K_SPACE , "V[2] , air = AJ[air] , air - 1" , air)

        # Show vital information, set fullscreen
        Trig(K_o   , "INFO = not INFO")
        Trig(K_F11 , "FULL = FULLSCREEN if not FULL else 0 ; screen = pygame.display.set_mode([800,600],FULL)")

        # Prepare for CS() operation
        E += V ; re_Outline()


# auxiliary function to T(Q)
# Turn practical site into relative deltas
# Warning: Don't use array.sum() to slow down this function
def M(P):
        # Calculate distance & ratio
        D = vn * (P - F)
        d = D[0] + D[1] + D[2]
        r = f / (f + abs(d))   # Without abs(), sometimes numpy would raise ZeroDivision Warning
        if d >= 0:             # The object is in front of your retina
                vEQ = r * (P - E)
                x , y = vEQ * ex , vEQ * ey
                yield [x[0] + x[1] + x[2] , y[0] + y[1] + y[2]]
        else:
                yield []
        yield r        


# Old version of MoonPlus(), but faster
def Moon(W):
        r = (INF * W) / (4 * f)
        rh = A([-c(phi) ,  0 , -s(phi)])
        xh = A([   0    , -1 ,    0   ])
        yh = A([-s(phi) ,  0 ,  c(phi)])
        _C_ = [cDivide(MOON , SKY , 3 , 1) , MOON]
        
        def _M(x , y):
                return E + INF * rh + x * r * xh + y * r * yh
        def _core(q):
                Flat(_C_[q] , [_M( 0 , 1) , _M(-1 , 1) , _M(-1 , -1) , _M( 0 , -1)])
        def core_(q):
                Flat(_C_[q] , [_M( 0 , 1) , _M( 1 , 1) , _M( 1 , -1) , _M( 0 , -1)])
        def _crescent(q):
                Flat(_C_[q] , [_M(-2 , 2) , _M( 0 , 2) , _M( 0 ,  1) , _M(-1 ,  1) , _M(-1 , -1) , _M(0 , -1) , _M(0 , -2) , _M(-2 , -2)])
        def crescent_(q):
                Flat(_C_[q] , [_M( 2 , 2) , _M( 0 , 2) , _M( 0 ,  1) , _M( 1 ,  1) , _M( 1 , -1) , _M(0 , -1) , _M(0 , -2) , _M( 2 , -2)])
                
        if ATime > 160 or ATime < 20:
                lu = [0 , 0 , 0 , 0 , 1 , 1 , 1 , 1 , 0 , 0 , 0][ph : ph + 4]
                _crescent(lu[0]) ; _core(lu[1]) ; core_(lu[2]) ; crescent_(lu[3])


# Recommended method to better show the moon
# Warning: This may reduce speed performance
def MoonPlus(W):
        # night only
        if 20 < ATime < 160: return

        # Avoid large numbers in screen x-y (speed reduction)
        if abs(abs(abs(phi-1.5*pi)-pi)-pi/2-a)>arctan(300/(e*f))+0.1: return
        if abs(abs(abs( b -1.5*pi)-pi)-pi/2)  >arctan(400/(e*f))+0.1: return 
        
        # basic vectors
        r = (INF * W) / (8 * f)
        rh = A([-c(phi) ,  0 , -s(phi)])
        xh = A([-s(phi) ,  0 ,  c(phi)])
        yh = A([   0    , -1 ,    0   ])
        op = E + INF * rh - 4 * r * (xh + yh) # Don't forget to plus 'E'
        
        # scroll array for shade changement
        moonphase = '00001111000'[ph : ph + 4]

        # compact information of pixels in 8 * 8 scales
        # _list[rank] <==> _list[raw][col] when (raw , col) = divmod(rank , 8)
        lunarmare = '1001110113212212222123313213131213221121111301100110001111110011'
        _crescent = '1111000011110000110000001100000011000000110000001111000011110000'
        _core     = '0000000000000000001100000011000000110000001100000000000000000000'
        core_     = '0000000000000000000011000000110000001100000011000000000000000000'
        crescent_ = '0000111100001111000000110000001100000011000000110000111100001111'

        _C_       =  [cDivide(MOON , SKY , 3 , 1) , MOON] # [DARK sides , BRIGHT sides]
        _G_       = _crescent + _core + core_ + crescent_ # more convenient for coding & bit operations

        # auxiliary function to Pixel()
        # Locate certain points in 8 * 8 board
        def _M(x , y):
                return op + x * r * xh + y * r * yh

        # Display a single large pixel of moon surface
        def Pixel(C , ra , co):
                Flat(C , [_M(ra , co) , _M(ra , co + 1) , _M(ra + 1 , co + 1) , _M(ra + 1 , co)])                

        # local main loop
        for rank in range(64):
                IDX       = 0
                raw , col = divmod(rank , 8)
                magnitude = int(lunarmare[rank])
                for i in range(4): # Decide whether this pixel is visible, 1 yes 0 no
                        IDX |= int(moonphase[i]) & int(_G_[i * 64 + rank])
                Pixel(cDivide(_C_[IDX] , SKY , magnitude , 3) , raw , col)


# Display texts on the screen     
def Msg(text , x , y , size , color = (0 , 0 , 0)):
        font = pygame.font.SysFont('Consolas' , size)
        img  = font.render(text , True , color)
        screen.blit(img , (x , y))


# Fill the sky
def Sky():
        screen.fill(SKY)


# Draw the stars
def Stars():
        if 185 < ATime < 355:
                for i in range(scl): # standard scale: 200
                        _a , _b , _si , C = [stars[i][j] for j in range(4)]
                        _vn = A([c(_a) * c(_b) , c(_a) * s(_b) , s(_a)])
                        Q = next(M(E + INF * _vn))
                        if Q:
                                _T = T(Q)
                                if 0 < _T[0] < 800 and 0 < _T[1] < 600:
                                        # Keep the light-balance between sky and stars
                                        if   185 < ATime < 190: _C = cDivide([0] * 3 , C , ATime - 185 , 190 - ATime)
                                        elif 350 < ATime < 355: _C = cDivide([0] * 3 , C , 355 - ATime , ATime - 350)
                                        else:                   _C = C
                                        pdc(screen , _C , T(Q) , _si , 0)


# Display the sun
def Sun(W):
        # day only
        if 200 < ATime < 340: return

        # Avoid large numbers in screen x-y (speed reduction)
        if abs(pi/2-abs(abs(phi-1.5*pi)-pi)-a)>arctan(300/(e*f))+0.1: return
        if abs(abs(abs( b -1.5*pi)-pi)-pi/2)  >arctan(400/(e*f))+0.1: return

        # local main loop
        Ps = []
        rh = A([c(phi) , 0 ,  s(phi)])
        xh = A([s(phi) , 0 , -c(phi)])
        yh = A([   0   , 1 ,    0   ])
        i , j , r  = 1 , 1 , (INF * W) / (2 * f)
        for _ in range(4):
                Ps.append(E + INF * rh + i * r * xh + j * r * yh) # Don't forget to plus 'E' because you can never reach the sun
                i , j = j , -i
        Flat(SUN , Ps)
        

# Render the rosy clouds during dawn & dusk
def Sung(H):
        if ATime < 10 or ATime > 355 or 170 < ATime < 185:
                # You CANNOT see the sea if angle of elevation is bigger than 'th'
                th = arctan(300 / (e * f))

                # You can see the rosy clouds
                if abs(a) < th + 0.2:                  # Plus '0.2' to deal with error posed by height
                        sl = int(tan(a) * f * e + 300) # y of SkyLine

                        # A simple strategy to increase realism
                        _r , r_ = abs(b - pi) , pi - abs(b - pi) # When you face the sun, sung is lighter
                        if 170 < ATime < 185: _r , r_ = r_ , _r

                        # Fill in the sung with gradient
                        _C_ = Gradient(cDivide(SKY , SUNG , _r , r_) , SKY , H)
                        for i in range(H):
                                pdr(screen , next(_C_) , [0 , sl - 3 * i , 800 , 3] , 0)


# TURN practical, relative deltas into screen, x-y sites
# Q comes from the return value of M(P), P is a practical site
def T(Q):
        # Do NOT forget to use int() for pixel display
        return [int(e * Q[0] + 400) , int(-e * Q[1] + 300)]


# Find the correct colour between two given ones according to ratio
# _C(left colour) --- _r(left length) --- GOAL --- r_(right length) --- C_(right colour)
def cDivide(_C , C_ , _r , r_):
        return [(_r * C_[i] + r_ * _C[i]) / (_r + r_) for i in range(3)]


# Connect break points with gradient
def cInterpolation(si , In , Co):                    # size , indexs , colours
        i , j , n , ans = 0 , 1 , len(In) , [0] * si
        lo , hi = In[i] , In[j]                      # boundaries of cur-sec
        for _ in range(n):
                cur , ans[lo] = lo , Co[i]           
                _n = ((hi - lo - 1) + si) % si       # size of cur-sec (in cycle)
                _C_ = Gradient(Co[i] , Co[j] , _n)   # mould for filling
                for __ in range(_n):
                        cur = (cur + 1) % si
                        ans[cur] = next(_C_)
                i , j = (i + 1) % n , (j + 1) % n
                lo , hi = In[i] , In[j]
        return ans


# Return the invert colour of the given one
def cReverse(C):
        return [255 - C[i] for i in range(3)]


# Revise <Map>
# Tip: You CANNOT crash rock in gravity mode
def mark(I , q):
        if FM or Map[I[0]][I[1]][I[2]] != 1:
                 Map[I[0]][I[1]][I[2]]  = q


# Return the criteria frame of your body
def re_Outline():
        global O
        O = [E[i] + R[i][j] for i in range(3) for j in range(2)]
       

# Use crosshair to place or crash blocks
def shoot():
        # Refresh your criteria frame immediately
        re_Outline()

        # Prepare for mouse events in KD()
        global Ib , Ip
        Ib , Ip = [] , []

        # Stimulate the ray of light
        P , D = E.copy() , (1 / S) * vn
        for _ in range(S * r_b):
                if not IN_WORLD(P): break # Photon moves out of this world
                I = ID(P)                 # id of the block which contains photon

                # You are aiming at a block
                if Map[I[0]][I[1]][I[2]]:
                        Ib = I                        # Record crash site with CURRENT id
                        _I = ID(P - D)                # Step backward to save PREVIOUS id
                        _O = Bud[_I[0]][_I[1]][_I[2]] # criteria frame for PREVIOUS block

                        # Judge whether you will get stuck
                        if not INTERSECT(3 , O , _O): Ip = _I # successful placement
                        break
                
                P += D # spread


# help> MainLoop()
#
if __name__ == '__main__':
        Init()
        while keep_going:
                KD() ; CS() ; IV() ; DP()
                pygame.display.update()
                
pygame.quit()
exit()


# help> quit
#
# You are now leaving help for your homework.
# Wish you good luck,
# and expect you to expect for update.
