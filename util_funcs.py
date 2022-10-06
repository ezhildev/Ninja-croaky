import pygame, math

def image_at(spritesheet, rectangle) -> pygame.Surface:
    '''This is used to extract the image from the spritesheet'''
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(spritesheet, (0, 0), rect)
    return image

def lerp(goal_velocity, current_velocity, acceleration) -> float:
    '''Linear interpolation'''
    difference = goal_velocity - current_velocity
    if difference > acceleration:
        return current_velocity + acceleration
    if difference < -acceleration:
        return current_velocity - acceleration
    return goal_velocity

def fade_in(screen, value) -> None:
    '''this used to increase a alpha value'''
    alpha = lerp(255, screen.get_alpha(), value)
    screen.set_alpha(alpha)

def fade_out(screen, value) -> None:
    '''this used to decrease a alpha value'''
    alpha = lerp(0, screen.get_alpha(), value)
    screen.set_alpha(alpha)

def collision_list(rect:pygame.Rect, rect_list) -> list:
    '''this will return a list of collided rects'''
    collided_rects = []
    for r in rect_list:
        if rect.colliderect(r):
            collided_rects.append(r)
    return collided_rects

# this algorithm obtained from here -> https://bit.ly/3CfwfmR. some steps are modified for my convenient
def collide_circle(rect,   # rectangle info
              center_x, center_y, radius):  # circle info
    """ Detect collision between a rectangle and circle. """
    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rect.right < cleft or rect.left > cright or rect.bottom < ctop or rect.top > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rect.left, rect.right):
        for y in (rect.top, rect.bottom):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rect.left <= center_x <= rect.right and rect.top <= center_y <= rect.bottom:
        return True  # overlaid

    return False  # no collision detected

