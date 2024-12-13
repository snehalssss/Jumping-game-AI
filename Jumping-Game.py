import tkinter as tk
import random

root = tk.Tk()
root.title("Jumping Game")
root.geometry("800x600")

canvas = tk.Canvas(root, width=800, height=600, bg='white')
canvas.pack()

platforms = []
coins = []
enemies = []

score_display = tk.StringVar()
score_display.set("Score: 0")
score_label = tk.Label(root, textvariable=score_display, font=("Times", 20, "bold"), fg='purple')
score_label.place(x=10, y=10)

# Create platforms
def create_platforms():
    platform_width = 120
    platform_height = 10

    last_x = 0
    while last_x < 3000:
        x = random.randint(last_x + 100, last_x + 200)
        y = random.randint(300, 500)
        velocityX = random.uniform(0.5, 1.5)  # Adjust velocity for slower movement
        platforms.append({'x': x, 'y': y, 'width': platform_width, 'height': platform_height, 'velocityX': velocityX})
        last_x = x

# Create coins on platforms
def create_coins():
    for platform in platforms:
        coin_x = random.randint(platform['x'], platform['x'] + platform['width'])
        coin_y = platform['y'] - 20
        coins.append({'x': coin_x, 'y': coin_y, 'radius': 5, 'collected': False})

# Player setup
player = {
    'width': 30,
    'height': 20,
    'velocityX': 0,
    'velocityY': 0,
    'isJumping': False,
    'speed': 4,
    'jumpHeight': 12,
    'score': 0
}

# Function to set player's initial position on a platform
def set_initial_player_position():
    player['x'] = platforms[0]['x'] + 20  # Set player's x position on the platform (offset by 20 units from the left edge)
    player['y'] = platforms[0]['y'] - player['height']  # Set player's y position above the platform

# Bind jump function
def jump(event):
    if not player['isJumping']:
        player['isJumping'] = True
        player['velocityY'] = -player['jumpHeight']

root.bind('<space>', jump)
current_platform_index = 0  # Track the current platform being moved
time_between_platforms = 1000  # Time delay between moving platforms (milliseconds)
platform_speed = 1  # Adjust platform speed
coin_speed = 1  # Adjust coin speed


def move_platforms():
    global current_platform_index
    player_on_platform = False

    if current_platform_index < len(platforms):
        platform = platforms[current_platform_index]
        platform['x'] -= platform_speed

        # Check if the player is on this platform
        if (player['x'] < platform['x'] + platform['width'] and
                player['x'] + player['width'] > platform['x'] and
                player['y'] + player['height'] >= platform['y'] and
                player['y'] + player['height'] <= platform['y'] + platform['height']):
            player_on_platform = True

        if platform['x'] + platform['width'] < 0:
            current_platform_index += 1
            if current_platform_index < len(platforms):
                root.after(time_between_platforms, move_platforms)

    # Move all platforms except the one the player is on
    for index, platform in enumerate(platforms):
        if index != current_platform_index:
            platform['x'] -= platform_speed

    # Move coins along with the platforms
    for coin in coins:
        coin['x'] -= coin_speed

    # Update player's position if not on a stable platform
    if not player_on_platform:
        handle_player_vertical_movement()
# def move_platforms():
#     for platform in platforms:
#         platform['x'] -= platform['velocityX']  # Adjust platform position based on velocityX

def draw_platforms():
    for platform in platforms:
        canvas.create_rectangle(platform['x'], platform['y'], platform['x'] + platform['width'],
                                platform['y'] + platform['height'], fill='blue')

def draw_coins():
    for coin in coins:
        if not coin['collected']:
            canvas.create_oval(coin['x'] - coin['radius'], coin['y'] - coin['radius'],
                                coin['x'] + coin['radius'], coin['y'] + coin['radius'], fill='gold')

def check_coin_collision():
    global player
    for coin in coins:
        if not coin['collected']:
            if (player['x'] < coin['x'] + coin['radius'] and
                    player['x'] + player['width'] > coin['x'] - coin['radius'] and
                    player['y'] < coin['y'] + coin['radius'] and
                    player['y'] + player['height'] > coin['y'] - coin['radius']):
                coin['collected'] = True
def find_next_platform(current_platform):

    # It finds the next platform in the right direction.
    next_platform = None
    for platform in platforms:
        if platform['x'] > current_platform['x']:
            if next_platform is None or platform['x'] < next_platform['x']:
                next_platform = platform
    return next_platform

def move_towards_platform(next_platform):
    if next_platform:
        if player['x'] < next_platform['x']:
            player['velocityX'] = player['speed']
        else:
            player['velocityX'] = -player['speed']
    else:
        player['velocityX'] = 0
class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self):
        self.x += self.speed
# def create_enemies():
#     for _ in range(3):
#         x = random.randint(100, 700)
#         y = random.randint(50, 300)
#         speed = random.uniform(1, 2)
#         enemy = Enemy(x, y, 20, 20, speed)
#         enemies.append(enemy)
#
def move_enemies():
    for enemy in enemies:
        enemy.move()
#

def draw_enemies():
    for enemy in enemies:
        canvas.create_rectangle(enemy.x, enemy.y, enemy.x + enemy.width, enemy.y + enemy.height, fill='green')

def create_enemies():
    for _ in range(3):
        platform = random.choice(platforms)  # Choose a random platform
        x = random.randint(platform['x'], platform['x'] + platform['width'] - 20)  # Adjust x position within platform bounds
        y = platform['y'] - 20  # Place enemy above the platform
        speed = random.uniform(1, 2)
        enemy = Enemy(x, y, 20, 20, speed)
        enemies.append(enemy)

def update_game():
    move_platforms()  # Move platforms horizontally
    check_coin_collision()  # Check for coin collection
    next_platform = find_next_platform(player)
    move_towards_platform(next_platform)
    canvas.delete("all")
    move_enemies()
    draw_enemies()
    handle_player_horizontal_movement()
    handle_player_vertical_movement()
    draw_platforms()
    draw_coins()
    draw_player()
    check_game_status()
    update_score()
    root.after(30, update_game)

# Update score function to count collected coins and update the score
def update_score():
    global high_score
    collected_coins = sum(coin['collected'] for coin in coins)
    player['score'] = collected_coins
    score_display.set(f"Score: {player['score']}")
    score_text = f"Score: {player['score']}"
    high_score_text = f"High Score: {high_score}"
    canvas.itemconfig(score_id, text=score_text)
    canvas.itemconfig(high_score_id, text=high_score_text)

    # Position the score and high score text on the right side of the window
    canvas.coords(score_id, 700, 10)
    canvas.coords(high_score_id, 700, 30)

def draw_player():
    canvas.create_rectangle(player['x'], player['y'], player['x'] + player['width'], player['y'] + player['height'],
                            fill='red')

def handle_player_vertical_movement():
    player['velocityY'] += 0.5
    player['y'] += player['velocityY']

    on_platform = False
    for platform in platforms:
        if (player['x'] < platform['x'] + platform['width'] and
                player['x'] + player['width'] > platform['x'] and
                player['y'] + player['height'] >= platform['y'] and
                player['y'] + player['height'] <= platform['y'] + platform['height']):
            on_platform = True
            player['y'] = platform['y'] - player['height']
            player['velocityY'] = 0
            player['isJumping'] = False

            if player['x'] < platform['x']:
                player['x'] = platform['x']
            elif player['x'] + player['width'] > platform['x'] + platform['width']:
                player['x'] = platform['x'] + platform['width'] - player['width']


root.bind('<space>', jump)

def handle_arrows(event):
    if event.keysym == 'Left':
        player['velocityX'] = -player['speed']
    elif event.keysym == 'Right':
        player['velocityX'] = player['speed']
    else:
        player['velocityX'] = 0

root.bind("<Left>", handle_arrows)
root.bind("<Right>", handle_arrows)

def handle_player_horizontal_movement():
    player['x'] += player['velocityX']

# def check_game_status():
#     on_platform = False
#     for platform in platforms:
#         if (player['x'] < platform['x'] + platform['width'] and
#                 player['x'] + player['width'] > platform['x'] and
#                 player['y'] + player['height'] == platform['y']):
#             on_platform = True
#             break
#
#     if not on_platform or (player['y'] + player['height'] >= 600 and not on_platform):
#         game_over()
score_id = canvas.create_text(700, 10, text="", font=("Arial", 14), anchor='ne')
high_score_id = canvas.create_text(700, 30, text="", font=("Arial", 14), anchor='ne')

high_score = 0
def check_game_status():
    global high_score
    on_platform = False
    for platform in platforms:
        if (player['x'] < platform['x'] + platform['width'] and
                player['x'] + player['width'] > platform['x'] and
                player['y'] + player['height'] == platform['y']):
            on_platform = True
            break
    if not on_platform and player['y'] + player['height'] >= 600:
        # if player['score'] > high_score:  # Check if the current score is higher than the high score
        #     high_score = player['score']
        game_over()
        update_score()

    # def update_score():
#     collected_coins = sum(coin['collected'] for coin in coins)
#     player['score'] = collected_coins  # Update score based on collected coins
#     score_display = f"Collected: {collected_coins}"  # Text to display on canvas
#
#     # Update canvas with the score display
#     canvas.itemconfig(score_text, text=score_display, font=("Arial", 20), fill='purple')

def game_over():
    canvas.create_text(400, 300, text="Game Over!", font=("Georgia", 26, "bold"))


create_platforms()
create_coins()
set_initial_player_position()
update_game()
root.mainloop()
