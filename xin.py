from collections import deque

def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [])])  # Queue chứa (đỉnh, đường đi tới đỉnh đó)

    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path + [current]  # Trả về đường đi từ start đến goal

        for neighbor in graph[current]:
            queue.append((neighbor, path + [current]))

    return None  # Không tìm thấy đường đi

# Biểu diễn các ô lưới dưới dạng chỉ số trong danh sách đỉnh
vertex_mapping = {}
index = 0
for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        vertex_mapping[(x, y)] = index
        index += 1

# Tạo danh sách kề cho mỗi đỉnh (ô lưới)
graph = {}
for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        neighbors = []
        # Thêm ô lưới hàng xóm vào danh sách kề nếu không phải là vật cản
        if (x + GRID_SIZE, y) not in list(zip(list_x, list_y)) and x < SCREEN_WIDTH - GRID_SIZE:
            neighbors.append(vertex_mapping[(x + GRID_SIZE, y)])
        if (x - GRID_SIZE, y) not in list(zip(list_x, list_y)) and x >= GRID_SIZE:
            neighbors.append(vertex_mapping[(x - GRID_SIZE, y)])
        if (x, y + GRID_SIZE) not in list(zip(list_x, list_y)) and y < SCREEN_HEIGHT - GRID_SIZE:
            neighbors.append(vertex_mapping[(x, y + GRID_SIZE)])
        if (x, y - GRID_SIZE) not in list(zip(list_x, list_y)) and y >= GRID_SIZE:
            neighbors.append(vertex_mapping[(x, y - GRID_SIZE)])
        graph[vertex_mapping[(x, y)]] = neighbors

# Chạy thuật toán BFS
start_vertex = vertex_mapping[(x_position, y_position)]
exit_vertex = vertex_mapping[exit_position]
path = bfs(graph, start_vertex, exit_vertex)

if path:
    # Duyệt ngược để tạo đường đi
    for i in range(len(path) - 1):
        current_x, current_y = list(vertex_mapping.keys())[list(vertex_mapping.values()).index(path[i])]
        next_x, next_y = list(vertex_mapping.keys())[list(vertex_mapping.values()).index(path[i+1])]
        
        # Di chuyển từ (current_x, current_y) đến (next_x, next_y)
        # Vẽ đường đi tại (next_x, next_y)
else:
    print("No path found")
