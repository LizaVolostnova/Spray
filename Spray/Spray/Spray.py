import pygame
import numpy as np
import random
import math
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cluster = None
        self.visited = False
    
    def color(self):
        colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]
        if self.cluster is None:
            return (200,200,200)
        elif self.cluster == -1:
            return (100,100,100)
        else:
            return colors[self.cluster % len(colors)]

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def get_neighbors(points, idx, eps):
    neighbors = []
    for i in range(len(points)):
        if i != idx and distance(points[idx], points[i]) <= eps:
            neighbors.append(i)
    return neighbors

def dbscan(points, eps=30, min_pts=3):
    if len(points) < min_pts:
        return
    
    for p in points:
        p.visited = False
        p.cluster = None
    
    cluster_id = 0
    
    for i in range(len(points)):
        if points[i].visited:
            continue
        
        points[i].visited = True
        neighbors = get_neighbors(points, i, eps)
        
        if len(neighbors) < min_pts:
            points[i].cluster = -1
        else:
            cluster_id += 1
            points[i].cluster = cluster_id
            
            j = 0
            while j < len(neighbors):
                curr_idx = neighbors[j]
                
                if not points[curr_idx].visited:
                    points[curr_idx].visited = True
                    curr_neighbors = get_neighbors(points, curr_idx, eps)
                    
                    if len(curr_neighbors) >= min_pts:
                        for n in curr_neighbors:
                            if n not in neighbors:
                                neighbors.append(n)
                
                if points[curr_idx].cluster is None:
                    points[curr_idx].cluster = cluster_id
                
                j += 1

def generate_spray_points(x, y, count=5, radius=20):
    points = []
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, radius)
        new_x = x + dist * math.cos(angle)
        new_y = y + dist * math.sin(angle)
        if 0 <= new_x <= 800 and 0 <= new_y <= 600:
            points.append(Point(new_x, new_y))
    return points

def plot_clusters(points):
    if not points:
        return
    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]
    colors = []
    for p in points:
        if p.cluster is None or p.cluster == -1:
            colors.append('gray')
        else:
            colors.append(plt.cm.tab10(p.cluster % 10))
    plt.figure(figsize=(8,6))
    plt.scatter(x_coords, y_coords, c=colors, s=50)
    plt.title('DBSCAN Clustering')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, alpha=0.3)
    plt.show()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("DBSCAN Clustering")
    clock = pygame.time.Clock()
    points = []
    drawing = False
    font = pygame.font.Font(None, 24)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
                points.extend(generate_spray_points(event.pos[0], event.pos[1], 8, 25))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                points.extend(generate_spray_points(event.pos[0], event.pos[1], 3, 20))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    dbscan(points, 30, 3)
                elif event.key == pygame.K_c:
                    points = []
                elif event.key == pygame.K_p:
                    plot_clusters(points)
        
        screen.fill((30,30,30))
        for p in points:
            pygame.draw.circle(screen, p.color(), (int(p.x), int(p.y)), 8)
        
        texts = [f"Points: {len(points)}", "R - DBSCAN", "C - Clear", "P - Plot"]
        y = 10
        for text in texts:
            surf = font.render(text, True, (255,255,255))
            screen.blit(surf, (10, y))
            y += 25
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()