import math
import os
import pygame

VERSION = "0.4"

MAX_NUMBER_LIVES = 3
BLACK = (0, 0, 0)

RESOURCE_DIR = os.path.abspath(".resources")

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join(RESOURCE_DIR, name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        return image
    except pygame.error:
        print('Cannot load image:', fullname)


def calcnewpos(rect, vector):
    (angle, z) = vector
    (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
    return rect.move(dx, dy)


class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('ball.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect = self.image.get_rect().move(screen.get_width()/2, screen.get_height()-45)
        self.vector = vector
        self.hit = False
        self.score = 0

    def update(self):
        newpos = calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if not self.area.contains(newpos):

            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if (tr and tl) and not bl and not br:
                angle = -angle
            if (tl and bl) or (tr and br):
                angle = math.pi - angle

        elif self.rect.collidelist(bricks.sprites()) != -1:
            hit_brick_index = self.rect.collidelist(bricks.sprites())
            tl = not bricks.sprites()[hit_brick_index].rect.collidepoint(newpos.topleft)
            tr = not bricks.sprites()[hit_brick_index].rect.collidepoint(newpos.topright)
            bl = not bricks.sprites()[hit_brick_index].rect.collidepoint(newpos.bottomleft)
            br = not bricks.sprites()[hit_brick_index].rect.collidepoint(newpos.bottomright)
            if (tr and tl) or (br and bl):
                angle = -angle
            elif (tl and bl) or (tr and br):
                angle = math.pi - angle
            self.score += 1

        else:
            player.rect.inflate(-3, -3)

            if self.rect.colliderect(player.rect) == 1 and not self.hit:
                angle = -angle
                self.hit = True
            elif self.hit:
                self.hit = False
        self.vector = (angle, z)


class Paddle(pygame.sprite.Sprite):
    """Movable tennis 'bat' with which one hits the ball
    Returns: bat object
    Functions: reinit, update, moveup, movedown
    Attributes: which, speed"""

    X = 0
    Y = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('paddle.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.state = "still"
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [0, 0]
        self.rect.midbottom = self.area.midbottom

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveleft(self):
        self.movepos[Paddle.X] = self.movepos[Paddle.X] - self.speed
        self.state = "moveleft"

    def moveright(self):
        self.movepos[Paddle.X] = self.movepos[Paddle.X] + self.speed
        self.state = "moveright"

    def still(self):
        self.movepos = [0, 0]
        self.state = "still"


class Brick(pygame.sprite.Sprite):

    def __init__(self, x, y, brick_type='basic'):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.top_left_x = x
        self.top_left_y = y
        if brick_type == 'med':
            self.image = load_png('med_block.png')
            self.rect = self.image.get_rect().move(self.top_left_x, self.top_left_y)
            self.health = 20
        elif brick_type == 'hard':
            self.image = load_png('hard_block.png')
            self.rect = self.image.get_rect().move(self.top_left_x, self.top_left_y)
            self.health = 30
        else:
            self.image = load_png('basic_block.png')
            self.rect = self.image.get_rect().move(self.top_left_x, self.top_left_y)
            self.health = 10

    def is_brick_hit(self):
        if self.rect.colliderect(ball.rect):
            # print("Brick hit")
            self.rect.inflate(-3, -3)
            ball.update()
            self.brick_hit()

    def brick_hit(self):
        self.health -= 10
        if self.health == 0:
            # print("Brick killed")
            self.kill()
            # print("Brick still alive: ", str(self.alive()))

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(os.path.join(RESOURCE_DIR, image_file))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location







def main():
    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Breakout: v' + str(VERSION))
    # print("Screen initialized")

    # Fill background
    # print(RESOURCE_DIR)
    background = pygame.image.load(os.path.join(RESOURCE_DIR, 'galaxy.png')).convert()


    # Initialize player
    global player
    player = Paddle()
    # print("Player initialized")

    # Initialize ball
    speed = 13
    # rand = 0.1 * random.randint(5, 8)  #never used
    global ball
    ball = Ball((0.47, speed))
    # print("Ball initialized")

    # Initialize bricks
    global bricks
    bricks = pygame.sprite.Group()
    # print("Bricks initialized")

    # Initialize sprites
    playersprites = pygame.sprite.RenderPlain(player)
    ballsprite = pygame.sprite.RenderPlain(ball)
    # print("Sprites initialized")

    # Blit background to screen
    #screen.blit(background, (0, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # print("Blitted background to screen")

    # Initialize clock
    clock = pygame.time.Clock()
    # print("Clock initialized")

    # Initialize pause screen text
    pause_screen = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(),30), "Paused", True,
                                           (255,255,255))
    # print("Pause screen initialized")

    # Initialize game over screen
    game_over_screen = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(),30), "Game Over" , True,
                                               (0, 0, 200))

    # print("Game over screen initialized")

    # Initialize game state variables
    gameover = True
    exitgame = False
    paused = False
    ischange = False
    player_lives = MAX_NUMBER_LIVES
    level = 1
    # print("Game state variables initialized")

    #start music
    pygame.mixer.music.load(os.path.join(RESOURCE_DIR, "lofi2.mp3.mp3"))
    pygame.mixer.music.play(-1)



    # print("Entering game loop...")

    while not exitgame:
        # print("Looping")
        clock.tick(60)
        player_score = ball.score
        score_counter = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), 30),
                                                "Score: {}".format(player_score), True,
                                                (255, 0, 0))
        life_counter = player_lives

        life_counter = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), 30),
                                               "Lives: {}".format(life_counter), True,
                                               (255, 255,0 ))

        level_counter = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), 30),
                                                "Level: {}".format(level), True,
                                                (255, 255, 255))
        screen_top_coords_scorecounter = [255, 12]
        screen_top_coords_lifecounter = [100, 12]
        screen_top_coords_levelcounter = [400, 12]

        # Moved text blitting to after the bricks
        # print(player_score)

        if gameover:  # Game over state, wait until player restarts game or exits
            # print("Game over state")
            screen_center_coords = list(screen.get_rect().center)
            screen_center_coords[0] = screen_center_coords[
                                          0] - game_over_screen.get_width() // 2
            screen_center_coords[1] = screen_center_coords[1] - game_over_screen.get_height() // 2

            screen.fill(BLACK)
            screen.blit(game_over_screen, screen_center_coords)
            screen.blit(score_counter, screen_top_coords_scorecounter)
            screen.blit(life_counter, screen_top_coords_lifecounter)
            screen.blit(level_counter, screen_top_coords_levelcounter)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitgame = True
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        gameover = False
                        level = 1
                        ball.score = 0
                        # print("Emptying brick sprites")
                        # print(bricks.sprites())
                        bricks.empty()
                        # print(bricks.sprites())
                        # print("Regenerating brick sprites")
                        generate_bricksprites(level)
                        # print(bricks.sprites())
                        player_lives = MAX_NUMBER_LIVES
                        # print("Exiting game over state")
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        exitgame = True
                        # print("Exiting game loop")
                        continue

        elif paused:  # Paused state, wait until player resumes or exits game
            # show text "Paused"
            # print("Paused state")
            screen_center_coords = list(screen.get_rect().center)  # These three lines determine the coordinates for
            screen_center_coords[0] = screen_center_coords[0] - pause_screen.get_width() // 2  # the Game Over message
            screen_center_coords[1] = screen_center_coords[1] - pause_screen.get_height() // 2
            screen.fill(BLACK)

            screen.blit(pause_screen, screen_center_coords)
            screen.blit(score_counter, screen_top_coords_scorecounter)
            screen.blit(life_counter, screen_top_coords_lifecounter)
            screen.blit(level_counter, screen_top_coords_levelcounter)
            pygame.display.flip()

            for event in pygame.event.get():
                # print("Event loop entered")
                if event.type == pygame.QUIT:
                    exitgame = True
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                        # print("Exiting paused state")
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        exitgame = True
                        # print("Exiting game loop")
                        continue



        else:
            pygame.display.flip()

            # print("Play state")
            if len(bricks.sprites()) == 0 and not ischange:  # Condition: level cleared, generate next level
                level += 1
                generate_bricksprites(level)

                ball.rect = ball.image.get_rect().move(screen.get_width() / 2, screen.get_height() - 45)
                player.rect.midbottom = player.area.midbottom

                # print("Bricks initialized")

            if ball.rect.topleft[1] > screen.get_height():  # Condition: Ball falls out of screen, decrement life counter, reset ball and paddle
                player_lives -= 1
                ball.rect = ball.image.get_rect().move(screen.get_width() / 2, screen.get_height() - 45)
                player.rect.midbottom = player.area.midbottom
                if player_lives == 0:
                    gameover = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitgame = True
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.moveleft()
                    if event.key == pygame.K_RIGHT:
                        player.moveright()
                    if event.key == pygame.K_SPACE:
                        paused = True
                        continue
                    if event.key == pygame.K_ESCAPE:
                        exitgame = True
                        continue
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.still()

            screen.blit(background, ball.rect, ball.rect)
            screen.blit(background, player.rect, player.rect)
            screen.blit(background, (0, 0))
            screen.blit(score_counter, screen_top_coords_scorecounter)
            screen.blit(life_counter, screen_top_coords_lifecounter)
            screen.blit(level_counter, screen_top_coords_levelcounter)

            for brick in bricks.sprites():  # Update all bricks, check if hit by ball
                brick.is_brick_hit()
                screen.blit(background, brick.rect, brick.rect)

            ballsprite.draw(screen)
            playersprites.draw(screen)
            bricks.draw(screen)

            ballsprite.update()
            playersprites.update()

            screen.blit(score_counter, screen_top_coords_scorecounter)
            screen.blit(life_counter, screen_top_coords_lifecounter)
            screen.blit(level_counter, screen_top_coords_levelcounter)



            pygame.display.flip()

            #screen.fill(BLACK)
            #screen.blit(background, (0, 0))


def generate_bricksprites(level):
    # bricks_list = pygame.sprite.Group()

    if level == 1:
        for i in range(5):
            bricks.add(Brick(i * 125 + 6, 136, brick_type='basic'))
    if level == 2:
        for i in range(5):
            for j in range(3):
                if j == 1:
                    bricks.add(Brick(i * 125 + 6, j * 65 + 6, brick_type='med'))
                    # else:
                elif j == 2:
                    bricks.add(Brick(i * 125 + 6, j * 65 + 6, brick_type='basic'))
    if level >= 3:
        for i in range(5):
            for j in range(3):
                if j == 0:
                    bricks.add(Brick(i * 125 + 6, j * 65 + 6, brick_type='hard'))
                elif j == 1:
                    bricks.add(Brick(i * 125 + 6, j * 65 + 6, brick_type='med'))
                elif j == 2:
                    bricks.add(Brick(i * 125 + 6, j * 65 + 6, brick_type='basic'))


if __name__ == '__main__':
    main()
