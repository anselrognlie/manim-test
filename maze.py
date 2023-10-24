from manim import *

# generate with
# manim -ql --disable_caching --format png maze.py MazeScene
# generates numbered images in media/images/maze/MazeScene*.png
# must have py3cairo installed from homebrew
# brew install py3cairo

PINK = rgb_to_color(c / 100 for c in (100, 90.2, 92.9))
FUCHSIA = rgb_to_color(c / 100 for c in (90.6, 9, 34.1))
DK_BLUE = rgb_to_color(c / 100 for c in (5.9, 20.8, 36.9))
LT_CYAN = rgb_to_color(c / 100 for c in (85.1, 97.6, 100))
LT_GRAY = rgb_to_color(c / 100 for c in (85.1, 85.1, 85.1))
WT_REGULAR = 4
WT_HEAVY = 12
WT_BORDER = 24
WT_PATH = WT_HEAVY
WT_BACKTRACK = WT_BORDER
STEP_TIME = 2
RUN_TIME = .5
WAIT_TIME = STEP_TIME - RUN_TIME
MONO_FONT = "Monaco"
MONO_SIZE = DEFAULT_FONT_SIZE * 0.75
REGULAR_FONT = "Verdana"
REGULAR_SIZE = DEFAULT_FONT_SIZE * 0.75

config.pixel_height = 204
config.pixel_width = 1000
config.frame_height = 35
config.frame_width = 35

class Node(Group):
    def __init__(self, text):
        circ = Circle(color=DK_BLUE)
        circ.set_fill(color=PINK, opacity=1)
        lbl = Text(text, color=BLACK)
        super().__init__(circ, lbl)
        self.circle = circ
        self.text = lbl

    def visit(self):
        return self.circle.animate.set_stroke(color=FUCHSIA, width=WT_HEAVY),

    def restore(self):
        return (
            self.circle.animate.set_stroke(color=DK_BLUE, width=WT_REGULAR).
                set_fill(color=PINK), 
            self.text.animate.set_fill(color=BLACK), 
        )
    
    def leave(self):
        return (
            self.circle.animate.set_stroke(color=FUCHSIA, width=WT_REGULAR), 
            self.text.animate.set_fill(color=FUCHSIA), 
        )
    
    def backtrack(self):
        return (
            self.circle.animate.set_stroke(color=FUCHSIA, width=WT_REGULAR)
                .set_fill(color=FUCHSIA), 
            self.text.animate.set_fill(color=PINK), 
        )

class Edge(Line):
    def __init__(self, start, end):
        super().__init__(start.get_center(), end.get_center())
        self.set_stroke(color=DK_BLUE)

    def visit(self):
        return self.animate.set_stroke(color=FUCHSIA, width=WT_HEAVY),

    def restore(self):
        return self.animate.set_stroke(color=DK_BLUE, width=WT_REGULAR),

    def leave(self):
        return self.animate.set_stroke(color=FUCHSIA, width=WT_REGULAR),

class LabeledArea(Group):
    def __init__(self, text):
        text_area = RoundedRectangle(width=9, height=2.5)
        (text_area.
            set_stroke(width=0).
            set_fill(color=LT_CYAN, opacity=1)
            # to_edge(UP, buff=0).
            )
        label = (Text(text, font=MONO_FONT, font_size=MONO_SIZE).
                 next_to(text_area, LEFT).
                 set_fill(color=BLACK).
                 align_to(text_area, UP).
                 shift([0, -0.5, 0])
        )
        super().__init__(text_area, label)
        self.text_area = text_area
        self.label = label

class MazeArrow(VGroup):
    def __init__(self, width):
        tip = width / 4
        super().__init__(LinePath([
            [0, 0, 0], [width, 0, 0]
        ]), LinePath([
            [width - tip, tip, 0], [width, 0, 0],
            [width - tip, -tip, 0],
        ]))
        self.set_stroke(width=WT_REGULAR, color=BLACK)

class LinePath(VMobject):
    def __init__(self, points):
        super().__init__()
        points = [points[i] for n in range(1, len(points)) for i in (n-1, n-1, n, n)]
        self.set_points(points)

class ExploredPath(Group):
    def __init__(self, size):
        super().__init__(
            LinePath([
                [0, 0, 0], [size, 0, 0], [size, size / 2 + 2 * size / 3, 0], 
                [2 * size + size / 3, size / 2 + 2 * size / 3, 0],
                [2 * size + size / 3, size / 2 + size / 3, 0],
                [size + size / 3, size / 2 + size / 3, 0],
                [size + size / 3, -size, 0],
                [2 * size + size / 3, -size, 0],
                ]).
                set_stroke(color=DK_BLUE, width=WT_PATH),
            Triangle().
               scale(.25).
               rotate(-90*DEGREES).
               set_stroke(width=0).
               set_fill(color=DK_BLUE, opacity=1).
               set_x(2 * size + size / 3).
               set_y(-size),
           LinePath([
                [2 * size + size / 3, size, 0],
                [2 * size + size / 3, size / 2 + size / 3, 0],
                [size + size / 3, size / 2 + size / 3, 0],
                [size + size / 3, 0, 0],
                ]).
                set_stroke(color=FUCHSIA, width=WT_BACKTRACK),
            )

class Maze(Group):
    def __init__(self):
        SIZE = 6.75
        CELLS = 3
        GRID = SIZE / CELLS
        maze = (Square(side_length=SIZE).
                set_stroke(width=0).
                set_fill(color=LT_GRAY, opacity=1))
        
        walls = []
        walls.append(Square(side_length=GRID).
                set_stroke(width=0).
                set_fill(color=FUCHSIA, opacity=1).
                align_to(maze, LEFT).
                align_to(maze, UP)
                )
        walls.append(Square(side_length=GRID).
                set_stroke(width=0).
                set_fill(color=FUCHSIA, opacity=1).
                align_to(maze, LEFT).
                align_to(maze, DOWN)
                )
        walls.append(Square(side_length=GRID).
                set_stroke(width=0).
                set_fill(color=FUCHSIA, opacity=1).
                align_to(maze, RIGHT)
                )
        
        borders = (VGroup(LinePath([
            [GRID, 0, 0], [GRID, -GRID, 0], [0, -GRID, 0], [0, 0, 0], 
            [SIZE, 0, 0], [SIZE, -2 * GRID, 0], [2 * GRID, -2 * GRID, 0],
            [2 * GRID, -GRID, 0], [SIZE, -GRID, 0], [SIZE, 0, 0]
        ]), LinePath([
            [GRID, -SIZE, 0], [GRID, -2 * GRID, 0], 
            [0, -2 * GRID, 0], [0, -SIZE, 0], [SIZE, -SIZE, 0]
        ])).
            set_stroke(width=WT_BORDER, color=DK_BLUE).
            align_to(maze, LEFT).
            align_to(maze, UP)
        )

        ARROW_WIDTH = GRID * 0.5
        start = (MazeArrow(ARROW_WIDTH).
                 align_to(maze, LEFT).
                 shift([-ARROW_WIDTH, 0, 0])
                 )
        exit = (MazeArrow(ARROW_WIDTH).
                 align_to(maze, RIGHT).
                 shift([ARROW_WIDTH, -GRID, 0])
                 )
        
        explored = (ExploredPath(GRID).
                 align_to(maze, LEFT).
                 shift([GRID / 3, 0, 0])
                    )

        super().__init__(maze, *walls, borders, start, exit, explored)

class LocationText(Text):
    def __init__(self, text):
        super().__init__(text, font=MONO_FONT, font_size=MONO_SIZE)
        self.set_fill(color=BLACK, opacity=1)
        self.strike_thru = None
        self.group = None

    def animate_crossout(self):
        minx = self.get_extremum_along_dim(dim=0, key=-1)
        maxx = self.get_extremum_along_dim(dim=0, key=1)
        miny = self.get_extremum_along_dim(dim=1, key=-1)
        maxy = self.get_extremum_along_dim(dim=1, key=1)
        l = Line(start=[minx, miny, 0], end=[maxx, maxy, 0])
        l.set_stroke(color=FUCHSIA, width=WT_HEAVY)
        self.strike_thru = l

        return (Create(l),)
    
    def fade_out(self):
        anims = [self.animate.set_opacity(0)]
        if self.strike_thru:
            anims.append(self.strike_thru.animate.set_opacity(0))

        return tuple(anims)

def get_locations(node):
    text = node.text.original_text
    lbl1 = LocationText(text).move_to(node).set_opacity(0)
    lbl2 = LocationText(text).move_to(node).set_opacity(0)
    return [lbl1, lbl2]

class LocationManager:
    def __init__(self, sibling):
        self.prev = [sibling]

    def next_animation(self, loc, sibling=None, dir=RIGHT, buff=0.4):
        if sibling is None:
            sibling = self.prev[-1]

        anim = (loc.animate.
            next_to(sibling, dir, buff=buff).
            set_opacity(1),)
        self.prev.append(loc)
        return anim
    
    def rollback(self):
        self.prev.pop()

class MazeScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        nodes = []
        node11 = Node("(1, 1)")
        rel = node11
        node10 = Node("(1, 0)")
        node10.next_to(rel, LEFT)
        node01 = Node("(0, 1)")
        node01.next_to(rel, UP)
        top = node01
        node02 = Node("(0, 2)")
        node02.next_to(rel, UR)
        node21 = Node("(2, 1)")
        node21.next_to(rel, DOWN)
        node22 = Node("(2, 2)")
        node22.next_to(rel, DR)
        nodes = (node10, node11, node01, node02, node21, node22)
        for n in nodes:
            n.scale(0.8)

        edge1011 = Edge(node10, node11)
        edge1101 = Edge(node11, node01)
        edge0102 = Edge(node01, node02)
        edge1121 = Edge(node11, node21)
        edge2122 = Edge(node21, node22)
        edges = (edge1011, edge1101, edge0102, edge1121, edge2122)

        visited = LabeledArea("visited:")
        (visited.
            to_edge(RIGHT, buff=1.5).
            align_to(top, UP).
            shift([0, -0.25, 0])
            )
        self.add(visited)

        path = LabeledArea("path:")
        (path.
            next_to(visited, DOWN).
            shift([0, -0.5, 0]).
            to_edge(RIGHT, buff=1.5)
            )
        self.add(path)

        vloc = LocationManager(visited.label)
        ploc = LocationManager(path.label)

        maze = Maze()
        maze.to_edge(LEFT, buff=3)
        self.add(maze)

        self.add(*edges)
        self.add(*nodes)

        found = Text("Found Exit!", font=REGULAR_FONT, font_size=REGULAR_SIZE, color=FUCHSIA)
        found.next_to(node22, UP).shift((found.get_right() - found.get_left()) / 2 * 0.8)

        complete = Text("Path Complete!", font=REGULAR_FONT, font_size=REGULAR_SIZE, color=FUCHSIA)
        complete.move_to(path.text_area).align_to(path.text_area, DOWN).shift([0, 0.5, 0])

        self.wait(STEP_TIME)
        # return  # uncomment to check basic layout

        #############################################################################
        # start animations
        #############################################################################
        self.play(*node10.visit(), 
                  run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        lbl1, lbl2 = get_locations(node10)
        first_visited = lbl1
        self.play(
            *vloc.next_animation(lbl1, buff=0.75),
            *ploc.next_animation(lbl2, buff=0.75),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(*edge1011.visit(), run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *node10.leave(),
            *edge1011.leave(),
            *node11.visit(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        lbl1, lbl2 = get_locations(node11)
        self.play(
            *vloc.next_animation(lbl1),
            *ploc.next_animation(lbl2),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(*edge1101.visit(), run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *node11.leave(),
            *edge1101.leave(),
            *node01.visit(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        lbl1, lbl2 = get_locations(node01)
        self.play(
            *vloc.next_animation(lbl1),
            *ploc.next_animation(lbl2),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(*edge0102.visit(), run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *node01.leave(),
            *edge0102.leave(),
            *node02.visit(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)
        to_be_crossed = lbl2

        lbl1, lbl2 = get_locations(node02)
        self.play(
            *vloc.next_animation(lbl1),
            *ploc.next_animation(lbl2),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)
        ploc.rollback()
        ploc.rollback()

        self.play(
            *node02.backtrack(),
            *lbl2.animate_crossout(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *lbl2.fade_out(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *node01.visit(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *node01.backtrack(),
            *to_be_crossed.animate_crossout(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *to_be_crossed.fade_out(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *node11.visit(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(*edge1121.visit(), run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *node11.leave(),
            *edge1121.leave(),
            *node21.visit(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        lbl1, lbl2 = get_locations(node21)
        self.play(
            *vloc.next_animation(lbl1, sibling=first_visited, dir=DOWN, buff=0.5),
            *ploc.next_animation(lbl2),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(*edge2122.visit(), run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(
            *node21.leave(),
            *edge2122.leave(),
            *node22.visit(),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        lbl1, lbl2 = get_locations(node22)
        self.play(
            *vloc.next_animation(lbl1),
            *ploc.next_animation(lbl2),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME)

        self.play(Write(found),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME * 2)

        self.play(
            FadeOut(found),
            Write(complete),
            run_time=RUN_TIME)
        self.wait(WAIT_TIME * 2)

        self.play(
            FadeOut(complete),
            run_time=RUN_TIME)

        self.play(
            *(anim for n in nodes for anim in n.restore()),
            *(anim for e in edges for anim in e.restore()),
            *(FadeOut(p) for p in vloc.prev[1:]),
            *(FadeOut(p) for p in ploc.prev[1:]),
            run_time=2, lag_time=0.25)
        self.wait(2)
