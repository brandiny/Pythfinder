import pygame
from queue import PriorityQueue
from collections import deque

def breadthFirstSearch(grid, start, end, draw):
    queue = deque([])
    queue.append(start)

    visited = set()
    parent = dict()

    while queue:
        # pygame.time.wait(100)
        current = queue.popleft()       # Grab the next spot in line to be processed
        visited.add(current)            # Make sure it is not visited again
        
        # In the event it is not start or end - make it negative
        if current != start and current != end:
            current.makeClosed()

        elif current == end:
            path = getPath(start, end, parent)
            for p in path:
                p.makePath()

            end.makeEnd()
            start.makeStart()
            break
            
        
        for n in current.neighbors:
            if n not in visited:
                if n != end:
                    n.makeOpen()
                queue.append(n)
                visited.add(n)
                parent[n] = current
    
        draw()


def depthFirstSearch(grid, start, end, draw):
    stack = []
    stack.append(start)

    visited = set()
    parent = dict()

    while stack:
        current = stack.pop()           # Grab the next spot in line to be processed

        # In the event it is not start or end - make it negative
        if current != start and current != end:
            visited.add(current)            # Make sure it is not visited again
            current.makeClosed()

        elif current == end:
            path = getPath(start, end, parent)
            for p in path:
                p.makePath()

            end.makeEnd()
            start.makeStart()
            break
    
        for n in current.neighbors:
            if n not in visited:
                if n != end:
                    n.makeOpen()
                stack.append(n)
                parent[n] = current
    
        draw()


def aStarSearch(grid, start, end, draw):
    count = 0

    openSet = PriorityQueue()       
    openSet.put((0, count, start))

    parent = {}

    gScore = {spot: float('inf') for row in grid.grid for spot in row}
    gScore[start] = 0

    fScore = {spot: float('inf') for row in grid.grid for spot in row}
    fScore[start] = hScore(start.getPosition(), end.getPosition())

    visited = {start}

    while not openSet.empty():
        # input()
        current = openSet.get()[2]
        visited.remove(current)

        # print(current.getPosition())
        # print("g", gScore[current])
        # print("f", fScore[current])

        # reconstruct path on finding the end point and BREAK
        if current == end:
            path = getPath(start, end, parent)
            for p in path:
                p.makePath()
                draw()
            end.makeEnd()
            start.makeStart()
            break

        for n in current.neighbors:
            gScoreTemp = gScore[current] + 1
            
            if (gScoreTemp < gScore[n]):
                parent[n] = current
                gScore[n] = gScoreTemp
                fScore[n] = gScoreTemp + hScore(n.getPosition(), end.getPosition())
                
                if n not in visited:
                    count += 1

                    # add to need to be visited (open) set and make it open color
                    openSet.put((fScore[n], count, n))
                    visited.add(n)
                    n.makeOpen()

        draw()
        
        if current != start and current != end:
            current.makeClosed()



def getPath(start, end, parentDictionary):
    path = []
    pointer = end

    # Essentially traversing a linkedlist where head=end
    while pointer != start:         
        path.append(pointer)
        pointer = parentDictionary[pointer]

    return path[::-1]
    

def hScore(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # return abs(x1 - x2) + abs(y1 - y2)
    return (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)

    

        

        
