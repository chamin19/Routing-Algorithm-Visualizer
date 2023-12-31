import networkx as nx
import os
import pygame
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Define constants for the window size and node radius
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 590
NODE_RADIUS = 15

# Define colors for the nodes and edges
NODE_COLOR = (255, 255, 255)
EDGE_COLOR = (255, 255, 255)

# Initialize the font to none
FONT = None

# Set the frame rate
clock = pygame.time.Clock()
fps = 60


def get_path_costs(graph,path):
    '''Gets the cost of the path at each step of Dijkstra's algorithm'''
    path_costs = [0]
    next_cost = 0
    for node in path[:-1]:
        edge_data = graph.get_edge_data(path[path.index(node)],path[path.index(node)+1])
        next_cost += int(edge_data.get('weight'))
        path_costs.append(next_cost)
    return path_costs

def draw_graph(screen, graph, path, current_node):
    '''Draws the graph on the pygame screen'''
    # Clear the screen
    screen.fill((0, 0, 0))
    
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
        source_pos = (WINDOW_WIDTH - source_label.get_width() + NODE_RADIUS, NODE_RADIUS)
        dest_pos = (WINDOW_WIDTH - dest_label.get_width()+ NODE_RADIUS, NODE_RADIUS*3)
        screen.blit(source_label, source_pos)
        screen.blit(dest_label, dest_pos)

        # Write exit instructions in top left
        title = FONT.render('Shortest path:  {}'.format(" -> ".join(path)), True, (0, 255, 255))
        exit_pos = (NODE_RADIUS, NODE_RADIUS)
        screen.blit(title, exit_pos)
        
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

def draw_game_over_screen(screen, path):
    '''Adds text to the screen when animation is complete'''
    title = FONT.render('Animation complete: Hit ESC key to exit program', True, (0, 255, 255))
    screen.blit(title, (NODE_RADIUS, WINDOW_HEIGHT + NODE_RADIUS*3))
    pygame.display.update()


def cent_main(graph, path, dist_vecs, prev_node):
    '''Define the main function that will run the game'''
    pygame.init()

    # Define the font for the node labels
    global FONT
    FONT = pygame.font.Font(None, 30)

    # Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH+50, WINDOW_HEIGHT+100))
  
    # Display start page
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('DM Sans', 26)
    text_font = pygame.font.SysFont('DM Sans', 23)
    i = 25

    # Display the description of Dijkstra's algorithm
    title = font.render("Centralized Algorithm in Networking: Dijkstra's algorithm", True, (255, 255,0))
    screen.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, 15))

    title = text_font.render( "The centralized algorithm implements Dijkstra's algorithm for finding the shortest path in a network. Each node ", True, (255, 255, 255))
    screen.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*2))
    title1 = text_font.render("represents a router. The cost of each edge represents the cost of sending a packet between routers.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*3))

    title1 = text_font.render("The function takes three arguments: graph, which is a NetworkX graph object representing the weighted graph, ", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*5))
    title1 = text_font.render("start_node, which is the starting node for the shortest path, and end_node, which is the end node for the path.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*6))

    title1 = text_font.render("The function starts by initializing three lists: distances, which keeps track of the shortest distance to each", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*8))
    title1 = text_font.render("node from the start node, parent_nodes, which keeps track of the parent node in the shortest path to each" , True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*9))
    title1 = text_font.render("node, and visited_nodes, which keeps track of visited nodes." , True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*10))

    title1 = text_font.render("The algorithm then loops through all the nodes in the graph until all nodes have been visited. It finds the", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*12))
    title1 = text_font.render("unvisited node with the smallest distance from the start node and marks it as visited. It then updates the", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*13))
    title1 = text_font.render("distances to all the neighboring nodes of the current node.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*14))

    title1 = text_font.render("Once all nodes have been visited, the function backtracks from the end node to the start node to find the ", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*16))
    title1 = text_font.render("shortest path. It starts by appending the index of the end node to the shortest_path list and then iteratively", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*17))
    title1 = text_font.render("adds the parent node of each node in the path until it reaches the start node.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*18))

    title1 = text_font.render("Finally, the function converts the indices in shortest_path to node names using the list(graph.nodes())[i]", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*20))
    title1 = text_font.render("syntax, and returns the resulting list.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*21))

    title1 = text_font.render("Overall, this function provides a simple and efficient way to find the shortest path in a weighted graph", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*23))
    title1 = text_font.render("using Dijkstra's algorithm.", True, (255, 255, 255))
    screen.blit(title1, (WINDOW_WIDTH/2 - title.get_width()/2 + 25, i*24))

    start = font.render("Press any key to continue to the animation", True, (0, 255, 255))
    screen.blit(start, (WINDOW_WIDTH/2 - start.get_width()/2, i*26))
    pygame.display.update()

    # Initilize running to True
    running = True
    start_dijkstras = False
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
                start_dijkstras = True
                running = False

    if start_dijkstras:
        screen.fill((0, 0, 0))

        # Define the size of each cell
        cell_width, cell_height = WINDOW_WIDTH // 4.8 - 20, 25

        # Run the game loop
        time = 0
        running = True
        pressed2 = False
       
        print(graph.number_of_nodes())

        # while running is True, check for events to see if user has pressed ESC, right or left arrow keys
        while running:      
            for event in pygame.event.get():
                # Clear the screen
                screen.fill((0, 0, 0))

                # Quit the game if user has closed the program
                if event.type == pygame.QUIT:
                    running = False

                # If user has pressed a key
                elif event.type == pygame.KEYDOWN:

                    # If user has pressed the left arrow key, decrement the time
                    if event.key == pygame.K_LEFT and time > 0:
                        time = time - 1

                    # If user has pressed the right arrow key, increment the time    
                    elif event.key == pygame.K_RIGHT and time >= 0 and time < graph.number_of_nodes()-1:
                        time = time + 1
                    
                    # IF user has pressed ESC, quit the game 
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        break

                    # Otherwise, set running to false and break the loop 
                    else:
                        pressed2 = True
                        running = False
                        break
            
            # Clear the screen 
            screen.fill((0, 0, 0))

            # Display the graph
            imp = pygame.image.load("gui/graph.png").convert()
            IMAGE_SMALL = pygame.transform.rotozoom(imp, 0, 0.6)
            screen.blit(IMAGE_SMALL, (10, 50))

            # Display the Step number
            text = "Step: " + str(time+1)  # + "\n" +
            title_text = font.render(text, True, (255, 255, 255))

            title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2 + 220, 25))
            
            # Draw the title on the window surface
            screen.blit(title_text, title_rect)
            
            table_font = pygame.font.SysFont('DM Sans', 23)

            # Handle events
            # Loop over each row in the table
            for row in range(graph.number_of_nodes() + 1):  # Add 1 to include the header row
                # Loop over each column in the row
                for col in range(3):
                    # Calculate the position of the cell based on the row and column                   
                    x = col * cell_width + 400
                    y = (row * cell_height) + 50  

                    # Create a Rect object for the cell
                    cell_rect = pygame.Rect(x, y, cell_width, cell_height)

                    # Draw the cell with a white background and a black border
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)

                    # Add text to the cell
                    # Populate the data table 
                    if row == 0:  # This is the header row
                        if col == 0: # First column - Node number
                            text = f"Node"
                        elif col == 1: # Second column - for the distances
                            text = f"Distance from {path[0]}"
                        else: # Third column - for the previous node
                            text = f"Previous node"
                        
                        # Render the header text in bold
                        text_surface = table_font.render(text, True, (0, 0, 0), (255, 255, 255))
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        screen.blit(text_surface, text_rect)

                    else:  # These are the data rows
                        if col == 0:
                            text = f"{row}"
                        elif col == 1 and time < len(dist_vecs):
                            # Get the distance of that node
                            timeat = dist_vecs[time]
                            starting = timeat[row-1]
                            text = str(starting)
                        else:
                            # Get the previous node of that node
                            timeat = prev_node[time]
                            starting = timeat[row-1]
                            text = str(starting)

                        # Print the data
                        text_surface = table_font.render(text, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        screen.blit(text_surface, text_rect)

            # Create a clock object
            clock = pygame.time.Clock()
            # Limit the frame rate to 60 FPS
            clock.tick(60)

            # Update the display
            pygame.display.update()

    # If table is complete, start the animation
    if pressed2:
        # Display text to explain the outcome of the algorithm
        title = FONT.render('Using the resulting table, backtrack from the destination to the start node.', True, (255, 255, 255))
        title1 = FONT.render('The result of backtracking is:  {}'.format(" -> ".join(path[::-1])), True, (255, 255, 255))
        title2 = FONT.render('Therefore, the shortest path is:  {}'.format(" -> ".join(path)), True, (255, 255, 255))
        title3 = FONT.render('Press any key to continue', True, (0, 255, 255))
        screen.blit(title, (NODE_RADIUS, WINDOW_HEIGHT - NODE_RADIUS*6))
        screen.blit(title1, (NODE_RADIUS, WINDOW_HEIGHT - NODE_RADIUS*6 + 35))
        screen.blit(title2, (NODE_RADIUS, WINDOW_HEIGHT - NODE_RADIUS*6 + 35*2))
        screen.blit(title3, (NODE_RADIUS, WINDOW_HEIGHT - NODE_RADIUS*6 + 35*3 + 30))
        pygame.display.update()

        running = True
        # Table screen: Check if key is pressed 
        while running:
            # Handle events
            for event in pygame.event.get():
                # If user exited, quit pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                
                # Stop if any key is pressed
                elif event.type == pygame.KEYDOWN:
                    start_animation = True
                    running = False

    # Display the graph for animating the path
    if start_animation:
        # Set the positions of the nodes based on their degrees
        positions = nx.circular_layout(graph)
        for node in graph.nodes():
            pos = positions[node]
            graph.nodes[node]["pos"] = (int(pos[0]*WINDOW_WIDTH//2.5 + WINDOW_WIDTH//2.5+50),
                                        int(pos[1]*WINDOW_HEIGHT//2.5 + WINDOW_HEIGHT//2.5+100))
        
        # Set the initial state
        current_node = path[0]
        path_index = 0

        # Call the draw_graph function to show the graph
        draw_graph(screen, graph, path, current_node)
        
        # Run the game loop
        running = True
        animation_done = False
        while running:
            # Handle events
            for event in pygame.event.get():
                # If user exited, quit pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    # If left arrow key is pressed, go to prev node
                    if event.key == pygame.K_LEFT:
                        if path_index > 0:
                            path_index -= 1
                            current_node = path[path_index]
                    
                    # If right arrow key is pressed, go to next node
                    elif event.key == pygame.K_RIGHT:
                        # if this is the last node in the path, stop the animation
                        if path_index == len(path) - 1:
                            animation_done = True

                        # if it is not the last node in the graph, go to the next
                        elif path_index < len(path) - 1:
                            path_index += 1
                            current_node = path[path_index]

                    # Quit if ESC is pressed
                    elif event.key == pygame.K_ESCAPE:
                        running = False 
                        break

            # Call game over function if animation is done 
            if animation_done:
                draw_game_over_screen(screen, path)

            if not running:
                break            
            
            # Update the screen
            if not animation_done:
                draw_graph(screen, graph, path, current_node)

        # Quit pygame
        pygame.quit()