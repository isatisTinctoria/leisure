WINDOW_W, WINDOW_H = 800, 800
_INFO = \
'''%PDF-1.7
1 0 obj
<<
/Length 2 0 R
>>
stream
'''
INFO_ = \
'''S
endstream
endobj
2 0 obj
1000
endobj
4 0 obj
<<
/Type /Page
/Parent 5 0 R
/Contents 1 0 R
>>
endobj
5 0 obj
<<
/Kids [4 0 R]
/Count 1
/Type /Pages
/MediaBox [0 0 %d %d]
>>
endobj
3 0 obj
<<
/Pages 5 0 R
/Type /Catalog
>>
endobj
xref
0 6
0000000000 65535 f
0000000100 00000 n
0000000200 00000 n
0000000500 00000 n
0000000300 00000 n
0000000400 00000 n
trailer
<<
/Size 6
/Root 3 0 R
>>
startxref
1000
%%EOF''' % (WINDOW_W, WINDOW_H)


import pygame
from pygame.locals import *
from random import randint
pygame.init()
keep_going = True
pygame.display.set_caption("Bezier2D")
SCREEN = pygame.display.set_mode([WINDOW_W, WINDOW_H])


class Trig:
    def __init__(self):
        self.d = 0
        self.c = 0
        self.lft = 0
        self.mid = 0
        self.enter = 0


class renderTools:
    @staticmethod
    def mirror(dot):
        return [int(dot[0]), int(WINDOW_H - dot[1])]
    
    @staticmethod
    def gettblr(rect):
        return [max([rect[1], rect[3]]), min([rect[1], rect[3]]),
                min([rect[0], rect[2]]), max([rect[0], rect[2]])]


class bezier3:
    def __init__(self, dot4):
        self.dot4 = dot4
        self.rgb = [randint(0, 255), randint(0, 255), randint(0, 255)]
        self.bx = self.by = self.cx = self.cy = self.dx = self.dy = None

    def update(self):
        self.bx = 3*(self.dot4[1][0] - self.dot4[0][0])
        self.by = 3*(self.dot4[1][1] - self.dot4[0][1])
        self.cx = 3*(self.dot4[2][0] - self.dot4[1][0]) - self.bx
        self.cy = 3*(self.dot4[2][1] - self.dot4[1][1]) - self.by
        self.dx = self.dot4[3][0] - self.dot4[0][0] - self.bx - self.cx
        self.dy = self.dot4[3][1] - self.dot4[0][1] - self.by - self.cy
    
    def get1Dot(self, t):
        return [int(self.dot4[0][0] + self.bx*t + self.cx*t*t + self.dx*t*t*t),
                int(self.dot4[0][1] + self.by*t + self.cy*t*t + self.dy*t*t*t)]


class bezierTools:
    def __init__(self):
        self.size = 0
        self.eps = 0.01
        self.speed =0.02
        self.core = None
        self.beziers = []
        self.deleted = []
        self.selected = []
        self.trig = Trig()
        self.showDots = True
        self.showCurs = True
        self.rgbBG = [0, 0, 0]
        self.selectRect = [-1]*4
        self.rgbPen = [255, 255, 255]

    def clearSelected(self):
        for i in range(self.size):
            self.selected[i] = [False]*4

    def deleteSelected(self):
        for i in range(self.size):
            for j in range(4):
                if self.selected[i][j]:
                    self.deleted[i] = True

    def moveSelected(self, mode, mus, offset):
        if mode == 0:
            delta_x = mus[0] - self.beziers[self.core[0]].dot4[self.core[1]][0]
            delta_y = mus[1] - self.beziers[self.core[0]].dot4[self.core[1]][1]
        for i in range(self.size):
            if not self.deleted[i]:
                flag = 0
                for j in range(4):
                    if self.selected[i][j]:
                        flag = 1
                        if mode == 0:
                            self.beziers[i].dot4[j][0] += delta_x
                            self.beziers[i].dot4[j][1] += delta_y
                        else:
                            self.beziers[i].dot4[j][0] += offset[0]
                            self.beziers[i].dot4[j][1] += offset[1]
                if flag:
                    self.beziers[i].update()

    def addSelected(self):
        t, b, l, r = renderTools.gettblr(self.selectRect)
        for i, bezier in enumerate(self.beziers):
            if not self.deleted[i]:
                for j, dot in enumerate(bezier.dot4):
                    if l < dot[0] < r and b < dot[1] < t:
                        self.selected[i][j] = True

    def showSelected(self):
        t, b, l, r = renderTools.gettblr(self.selectRect)
        pygame.draw.rect(SCREEN, [255, 255, 255],
                         renderTools.mirror([l, t]) + [r-l, t-b], 1)

    def addBezier(self, mus):
        self.clearSelected()
        self.size += 1
        self.deleted.append(False)
        self.selected.append([True]*4)
        dot4 = [[mus[0]+k*10, mus[1]] for k in range(4)]
        tar = bezier3(dot4)
        tar.update()
        self.beziers.append(tar)

    def renderBG(self):
        SCREEN.fill(self.rgbBG)
    
    def render1Bezier(self, i, bezier):
        if self.showDots:
            rad = [5, 3, 3, 5]
            pos = [renderTools.mirror(bezier.dot4[k]) for k in range(4)]
            for j in range(4):
                pygame.draw.circle(SCREEN, bezier.rgb, pos[j], rad[j], 0)
                if self.selected[i][j]:
                    pygame.draw.circle(SCREEN, [255, 255, 255], pos[j], rad[j], 1)
        if self.showCurs:
            t, dotw = 0, []
            while 1:
                dotw.append(renderTools.mirror(bezier.get1Dot(t)))
                t += self.eps
                if t > 1:
                    break
            pygame.draw.aalines(SCREEN, self.rgbPen, False, dotw)
    
    def renderBeziers(self):
        for i, bezier in enumerate(self.beziers):
            if not self.deleted[i]:
                self.render1Bezier(i, bezier)

    def getCore(self, mus):
        candidates = []
        for i, bezier in enumerate(self.beziers):
            if not self.deleted[i]:
                for j, dot in enumerate(bezier.dot4):
                    d2 = (mus[0]-dot[0])**2 + (mus[1]-dot[1])**2
                    if d2 < 25:
                        candidates.append(([i, j], d2))
        if len(candidates) == 0:
            self.core = None
        else:
            mind2 = 26
            for can in candidates:
                if can[1] < mind2:
                    mind2 = can[1]
                    self.core = can[0]

    def exportPDF(self):
        with open("font.txt", 'a') as f:
            f.write(_INFO)
            for i, bezier in enumerate(self.beziers):
                if not self.deleted[i]:
                    info = ''
                    for j, dot in enumerate(bezier.dot4):
                        if j == 0:
                            info += '%d %d m\n' % (int(dot[0]), int(dot[1]))
                        else:
                            info += '%d %d ' % (int(dot[0]), int(dot[1]))
                    info += 'c\n'
                    f.write(info)
            f.write(INFO_)
            
    def KD(self):
        global keep_going
        for event in pygame.event.get():
            if event.type == QUIT:
                keep_going = False
        keys = pygame.key.get_pressed()
        lft, mid, rgt = pygame.mouse.get_pressed()
        mus = renderTools.mirror(pygame.mouse.get_pos())

        if lft and not self.trig.lft:
            self.trig.lft = 1
            self.getCore(mus)
            if self.core is None:
                self.clearSelected()
                self.selectRect[0:2] = mus
            else:
                self.selected[self.core[0]][self.core[1]] = True

        if lft and self.trig.lft:
            if self.core is None:
                self.selectRect[2:] = mus
                self.showSelected()
            else:
                self.moveSelected(0, mus, None)

        if not lft and self.trig.lft:
            self.trig.lft = 0
            if self.selectRect[0] != -1:
                self.addSelected()
                self.selectRect[0] = -1

        if rgt and not lft:
            self.deleteSelected()
            self.clearSelected()

        if mid and not self.trig.mid:
            self.trig.mid = 1
            if not lft and not rgt:
                self.addBezier(mus)

        if not mid and self.trig.mid:
            self.trig.mid = 0

        offset = [0, 0]
        if keys[K_UP]:
            offset[1] += self.speed
        if keys[K_DOWN]:
            offset[1] -= self.speed
        if keys[K_LEFT]:
            offset[0] -= self.speed
        if keys[K_RIGHT]:
            offset[0] += self.speed
        self.moveSelected(1, None, offset)

        if keys[K_RETURN] and not self.trig.enter:
            self.trig.enter = 1
            self.exportPDF()
        if not keys[K_RETURN] and self.trig.enter:
            self.trig.enter = 0

        if keys[K_d] and not self.trig.d:
            self.trig.d = 1
            self.showDots = not self.showDots
        if not keys[K_d] and self.trig.d:
            self.trig.d = 0

        if keys[K_c] and not self.trig.c:
            self.trig.c = 1
            self.showCurs = not self.showCurs
        if not keys[K_c] and self.trig.c:
            self.trig.c = 0

    def update(self):
        self.renderBG()
        self.KD()
        self.renderBeziers()


if __name__ == '__main__':
    app = bezierTools()
    while keep_going:
        app.update()
        pygame.display.update()
    pygame.quit()
    exit()