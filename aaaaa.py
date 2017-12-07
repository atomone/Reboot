import sys, pygame

pygame.init()
window_size = (320, 256)
bg_color = (0, 0, 255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(window_size)

img_bg = pygame.image.load('chip.png')
num_chips_per_line = int(img_bg.get_width() / 32)

map_data = [
1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
1, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 1,
1, 0, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 0, 1,
1, 0, 1, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 1, 0, 1,
1, 0, 1, 3, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 2, 3, 1, 0, 1,
1, 0, 1, 3, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 3, 1, 0, 1,
1, 0, 1, 3, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 2, 3, 1, 0, 1,
1, 0, 1, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 1, 0, 1,
1, 0, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 0, 1,
1, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 1,
1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
]

camera_x = 0
camera_y = 0

end_game = False
while not end_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        camera_y = max(camera_y - 8, 0)
    if pressed[pygame.K_LEFT]:
        camera_x = max(camera_x - 8, 0)
    if pressed[pygame.K_DOWN]:
        camera_y = min(camera_y + 8, 32 * 15 - 256)
    if pressed[pygame.K_RIGHT]:
        camera_x = min(camera_x + 8, 32 * 20 - 320)

    for y in range(0, 15):
        for x in range(0, 20):
            i = y * 20 + x
            c = map_data[i]
            dx = c % num_chips_per_line
            dy = int(c / num_chips_per_line)
            # カメラからの相対位置
            pos_x = x * 32 - camera_x
            pos_y = y * 32 - camera_y
            # 画面外の描画はスキップ
            if pos_x < -32 or pos_y < -32 or pos_x > 320 or pos_y > 256:
                continue
            screen.blit(img_bg, (pos_x, pos_y), (32 * dx, 32* dy, 32,32))
clock = pygame.time.Clock()
screen = pygame.display.set_mode(window_size)
img_char = pygame.image.load('animation.png')

frame = 0  # フレーム
x = 0  # 表示位置X

end_game = False
while not end_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True

    x = (x + 1) if x < 320 else -32  # 画面右に出たら左から出てくる

    screen.fill(bg_color)

    # ループあり
    loop_anim_index = int(frame / 3) % 5
    screen.blit(img_char, (x, 104), (32 * loop_anim_index, 0, 32, 32))

    # ループなし
    anim_index = min(int(frame / 15), 5)
    screen.blit(img_char, (144, 104), (32 * anim_index, 32, 32, 32))


    # フレーム更新
    frame += 1
    pygame.display.flip()
    clock.tick(60)
sys.exit(0)
