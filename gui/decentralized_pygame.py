import networkx as nx
import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Define constants for the window size and node radius
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 600
NODE_RADIUS = 15

# Define colors for the nodes and edges
NODE_COLOR = (255, 255, 255)
EDGE_COLOR = (255, 255, 255)

# Set the frame rate
clock = pygame.time.Clock()
fps = 60

#====================================================================================
def get_path_costs(graph,path):
    path_costs = [0]
    next_cost = 0
    for node in path[:-1]:
        edge_data = graph.get_edge_data(path[path.index(node)],path[path.index(node)+1])
        next_cost += int(edge_data.get('weight'))
        path_costs.append(next_cost)
    return path_costs


def draw_graph(screen, graph, path, current_node):
    
    # Draw the edges
    for u, v in graph.edges():
        u_pos = graph.nodes[u]["pos"]
        v_pos = graph.nodes[v]["pos"]
        weight = str(graph[u][v]['weight'])
        label = FONT.render(weight, True, EDGE_COLOR)
        label_pos = ((u_pos[0] + v_pos[0])/2, (u_pos[1] + v_pos[1])/2)
        screen.blit(label, label_pos)
        pygame.draw.line(screen, EDGE_COLOR, u_pos, v_pos)

    # Get the costs in the path to update the count
    costs = get_path_costs(graph,path)

    # Draw the nodes
    for node in graph.nodes():
        pos = graph.nodes[node]["pos"] 
        color = NODE_COLOR
        if node in path:
            if node == current_node:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
        pygame.draw.circle(screen, color, pos, NODE_RADIUS)
        
        # Draw the label
        label = FONT.render(str(node), True, (0,0,0))
        label_pos = (pos[0] - NODE_RADIUS/2, pos[1] - NODE_RADIUS/2)
        screen.blit(label, label_pos)
        
        # Write source and dest nodes in top right corner
        source_label = FONT.render("Source: {}".format(int(path[0])), True, EDGE_COLOR)
        dest_label = FONT.render("Destination: {}".format(int(path[-1])), True, EDGE_COLOR)
        source_pos = (1100,50)
        dest_pos = (1100,80)
        screen.blit(source_label, source_pos)
        screen.blit(dest_label, dest_pos)

        # Write exit instructions in top left
        exit_label = FONT.render("Hit ESC to EXIT".format(int(path[0])), False, EDGE_COLOR)
        exit_pos = (NODE_RADIUS, NODE_RADIUS)
        screen.blit(exit_label, exit_pos)
        
        # Draw the current node label
        if node == current_node:
            label = FONT.render(" Current Node", True, (255, 0, 0))
            label_pos = (pos[0] + NODE_RADIUS, pos[1])
            screen.blit(label, label_pos)
            
            # Draw the cost label
            i = path.index(node) 
            cost = costs[i]
            cost_label = FONT.render("Current Cost: {}".format(cost), True, (255, 0, 0))
            cost_pos = (WINDOW_WIDTH - cost_label.get_width() + NODE_RADIUS, NODE_RADIUS*5)
            screen.blit(cost_label, cost_pos)
            
    # Update the screen
    pygame.display.update()

# ====================================================================================

# Define the main function that will run the game
def decent_main(num_routers, begin, end, dv_start_end, path, cost,graph):
   
    # Define the number of rows in the table
    N = int(num_routers)

    # Initialize Pygame
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Set the font for the title
    title_font = pygame.font.SysFont(None, 35)
    # Set the font for the text in the table
    font = pygame.font.Font(None, 25)

#====================================================================================

 # Define the font for the node labels
    global FONT
    FONT = pygame.font.Font(None, 30)

    # Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH+50, WINDOW_HEIGHT+100))
  
    # Display start page
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('DM Sans', 30)
    text_font = pygame.font.SysFont('DM Sans', 25)
    i = 25

    title = font.render("This algorithm finds the shortest path between a given start and end node in a network, without requiring any central authority", True, (255, 255, 255))
    screen.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2, i*2))
    title1 = font.render("or global knowledge of the network topology. Each node represents a router in the network, and each edge cost represents the", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*3))
    title1 = font.render("cost of sending a packet between two routers. ", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*4))

    title1 = font.render("The algorithm begins by initializing a dictionary called dist_vecs, which represents the distance vector of each node in the ", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*6))
    title1 = font.render("network. The distance vector is a dictionary that contains the distance from a given node to every other node in the network." , True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*7))

    title1 = font.render("Next, the code initializes the distance vectors of all nodes by setting the distance from each node to itself to 0, and the" , True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*9))
    title1 = font.render("distance to all other nodes to infinity. Then, for each edge in the graph, the code updates the distance vectors of both nodes", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*10))
    title1 = font.render("by setting the distance between them to the weight of the edge.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*11))

    title1 = font.render("The algorithm then enters a loop, where it repeatedly updates the distance vectors of each node in the network based on the  ", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*13))
    title1 = font.render("distance vectors of its neighbors.  During each iteration of the loop, the code computes the new distance vectors for each node by ", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*14))
    title1 = font.render("considering the distance vectors of its neighbors, and updates the notify_neighbors dictionary to indicate which nodes need to ", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*15))
    title1 = font.render("be notified of the changes. The loop continues until all nodes have been notified and their distance vectors have converged.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*16))

    title1 = font.render("Finally, the algorithm uses the converged distance vectors to find the shortest path between the start and end nodes.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*18))
    title1 = font.render("It starts at the start node and iteratively chooses the neighbor with the lowest cost path to the end node, until it ", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*19))
    title1 = font.render("reaches the end node.", True, (255, 255, 255))
    
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*20))
    title1 = font.render("The algorithm returns three values: dv_start_end, which is a list of dictionaries containing the distance vectors of the", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*22))
    title1 = font.render("start and end nodes at each iteration of the loop; path, which is a list of nodes representing the shortest path from", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*23))
    title1 = font.render("the start node to the end node; and cost, which is the total cost of the shortest path.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*24))
    
    
    
    title1 = font.render("", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2, i*12))


    start = font.render("Press any key to continue to the animation", True, (0, 255, 255))
    screen.blit(start, (WINDOW_WIDTH/2 - start.get_width()/2, (WINDOW_HEIGHT/2 + start.get_height()/2)+340))
    start = font.render("Decentralized Algorithm in Networking: Bellman-Ford's Algorithm", True, (255, 255,0))
    screen.blit(start, ((WINDOW_WIDTH/2 - start.get_width()/2), (WINDOW_HEIGHT/2 + start.get_height()/2)-295))
    pygame.display.update()

    running = True
    start_bell = False
    start_animation = False

    # Start screen: Check if key is pressed 
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            
            # stop if any key is pressed
            elif event.type == pygame.KEYDOWN:
                start_bell = True 
                running = False

    if start_bell:
        screen.fill((0, 0, 0))

        # Define the size of each cell
        cell_width, cell_height = WINDOW_WIDTH // 5.8 - 30, 30

#====================================================================================

    # Run the game loop
    time = 0
    running = True
    pressed = 1
    animation_done = False
    while running:
        for event in pygame.event.get():
            # Clear the screen
            screen.fill((0, 0, 0))

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and time > 0:
                    time = time - 1

                elif event.key == pygame.K_RIGHT and time >= len(dv_start_end)-1:
                    animation_done = True
                elif event.key == pygame.K_RIGHT and time >= 0 and not (time == len(dv_start_end) ):
                    time = time + 1
                   

                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break
                else:
                    # do nothing
                    time


        if animation_done:
            screen.fill((0, 0, 0))
            text = "Time: " + str(time)  # + "\n" +
            title_text = title_font.render(text, True, (255, 255, 255))
            text2 = "Path: " + str(path)
            title_text2 = title_font.render(text2, True, (0, 255, 0))
            text3 = "Cost: " + str(cost)
            title_text3 = title_font.render(text3, True, (255, 255, 255))

            # SIZEs for displaying the time cost and path
            title_rect = title_text.get_rect(center=(900, 60)) #sizing for time
            title_rect3 = title_text.get_rect(center=(900, 90)) #sizing for cost
            title_rect2 = title_text.get_rect(center=(900, 120)) #sizing for path
            
            # Draw the title on the window surface
            screen.blit(title_text, title_rect)
            screen.blit(title_text2, title_rect2)
            screen.blit(title_text3, title_rect3)
            # Handle events

            # Loop over each row in the table
            for row in range(N + 1):  # Add 1 to include the header row
                # Loop over each column in the row
                for col in range(4):
                    # Calculate the position of the cell based on the row and column
                    x = (col * cell_width) + 30
                    y = (row * cell_height) + 40

                    # Create a Rect object for the cell
                    cell_rect = pygame.Rect(x, y, cell_width, cell_height)

                    # Draw the cell with a white background and a black border
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)

                    # Add text to the cell
                    if row == 0:  # This is the header row
                        if col == 0:
                            text = f"DV in Source"
                        elif col == 2:
                            text = f"DV in Destination"
                        else:
                            text = "Distance"
                        # Render the header text in bold
                        text_surface = font.render(text, True, (0, 0, 0), (255, 255, 255))
                        # Center the header text in the cell
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        # Draw the header text to the screen
                        screen.blit(text_surface, text_rect)
                    else:  # These are the data rows
                        if col == 0:
                            text = f"{begin} --> {row}"
                            
                        elif col == 1:
                            timeat = dv_start_end[time]
                            starting = timeat['dv_start']
                            text = f"{starting[f'{row}']}"
                        elif col == 2:
                            text = f"{end} --> {row}"
                        else:
                            timeat = dv_start_end[time]
                            ending = timeat['dv_end']
                            text = f"{ending[f'{row}']}"
                        # Render the data text
                        text_surface = font.render(text, True, (0, 0, 0))
                        # Center the data text in the cell
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        # Draw the data text to the screen
                        screen.blit(text_surface, text_rect)
            # Set the positions of the nodes based on their degrees
            positions = nx.circular_layout(graph)
            for node in graph.nodes():
                pos = positions[node]
                graph.nodes[node]["pos"] = (int(pos[0]*WINDOW_WIDTH//5.5 + WINDOW_WIDTH//5.5+850),
                                            int(pos[1]*WINDOW_HEIGHT//5.5 + WINDOW_HEIGHT//5.5+270))
            draw_graph(screen, graph, path, 1)
            # ..........................................................................
        else:
            screen.fill((0, 0, 0))

            text = "Time: " + str(time)  # + "\n" +
            title_text = title_font.render(text, True, (255, 255, 255))
            text2 = "Path: " + str(path)
            title_text2 = title_font.render(text2, True, (255, 255, 255))
            text3 = "Cost: " + str(cost)
            title_text3 = title_font.render(text3, True, (255, 255, 255))

            title_rect = title_text.get_rect(center=(60, 35))
            title_rect3 = title_text.get_rect(center=(170, 35))
            title_rect2 = title_text.get_rect(center=(280, 35))
            
            # Draw the title on the window surface
            screen.blit(title_text, title_rect)
            screen.blit(title_text2, title_rect2)
            screen.blit(title_text3, title_rect3)
            # Handle events

            # Loop over each row in the table
            for row in range(N + 1):  # Add 1 to include the header row
                # Loop over each column in the row
                for col in range(4):
                    # Calculate the position of the cell based on the row and columns
                    x = (col * cell_width) + 10
                    y = (row * cell_height) + 60

                    # Create a Rect object for the cell
                    cell_rect = pygame.Rect(x, y, cell_width, cell_height)

                    # Draw the cell with a white background and a black border
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)

                    # Add text to the cell
                    if row == 0:  # This is the header row
                        if col == 0:
                            text = f"DV in Source"
                        elif col == 2:
                            text = f"DV in Destination"
                        else:
                            text = "Distance"
                        # Render the header text in bold
                        text_surface = font.render(text, True, (0, 0, 0), (255, 255, 255))
                        # Center the header text in the cell
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        # Draw the header text to the screen
                        screen.blit(text_surface, text_rect)
                    else:  # These are the data rows
                        if col == 0:
                            text = f"{begin} --> {row}"
                            
                        elif col == 1:
                            timeat = dv_start_end[time]
                            starting = timeat['dv_start']
                            text = f"{starting[f'{row}']}"
                        elif col == 2:
                            text = f"{end} --> {row}"
                        else:
                            timeat = dv_start_end[time]
                            ending = timeat['dv_end']
                            text = f"{ending[f'{row}']}"
                        # Render the data text
                        text_surface = font.render(text, True, (0, 0, 0))
                        # Center the data text in the cell
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        # Draw the data text to the screen
                        screen.blit(text_surface, text_rect)

            # Create a clock object
            clock = pygame.time.Clock()
            # Limit the frame rate to 60 FPS
            clock.tick(60)

            # Update the display
            pygame.display.update()