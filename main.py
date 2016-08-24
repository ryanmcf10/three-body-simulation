import sys

import pygame
from pygame.locals import *

import math

import planet
import simulation
from colors import *

#GLOBAL GAME VARIABLES
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
MAX_VECTOR = 200


def main():
    pygame.init()
    
    #ADDITIONAL GLOBAL VARIABLES
    global DISPLAYSURF, SMALL_FONT, LARGE_FONT, FPS
    
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Three Body Problem Simulation')

    SMALL_FONT = pygame.font.Font(None, 18)
    LARGE_FONT = pygame.font.Font(None, 36)
    
    FPS = 30
    
    gameclock = pygame.time.Clock()
    
    #initialize the message to display when the simulation is ready
    message = "Press [SPACE] to start the simulation"
    start_message = LARGE_FONT.render(message, 1, WHITE)
    start_message_position = start_message.get_rect(centerx=SCREEN_WIDTH/2, centery=SCREEN_HEIGHT/2)
    
    planets = [planet.Planet(random_color())]
        
    while True:
        gameclock.tick(FPS)
        fps = gameclock.get_fps()
        
        DISPLAYSURF.fill(BLACK)
        
        #Fill the planets list with three planets and set all initial conditions
        if not is_ready(planets):
            if not planets[-1].is_ready():
                mouse_position = pygame.mouse.get_pos()
                set_initial_conditions(planets[-1], mouse_position)
            else:
                planets.append(planet.Planet(random_color()))           
                
        #Draw the planets in the list to the display surface
        for current_planet in planets:
            draw_velocity_vector(current_planet)
            current_planet.draw(DISPLAYSURF)
            
        if is_ready(planets):
            DISPLAYSURF.blit(start_message, start_message_position)

        events = pygame.event.get()
        
        for event in events:
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEBUTTONDOWN:
                #If not all 3 planets are ready, set the initial conditions of the last planet in the list
                if not is_ready(planets):
                    #Click sets the position of the planet
                    if not planets[-1].is_placed == True:
                        planets[-1].is_placed = True     
                    #Click sets the size of the planet
                    elif not planets[-1].is_sized == True:
                        planets[-1].is_sized = True   
                    #Click sets the velocity vector of the planet
                    elif not planets[-1].is_directed == True:
                        planets[-1].is_directed = True
                        
            elif (event.type == KEYUP and event.key == K_SPACE and is_ready(planets)):
                simulation.Simulate(planets[0], planets[1], planets[2])
  
        pygame.display.update()
             
def is_ready(planets):
    """
    Check to see if there are three initialized planets in the 'planets' list
    
    input parameter: planets - list of planets
    return value: result - boolean flag tealling if the planets list is_ready
    """
    result = False
    if len(planets) == 3:
        result = planets[-1].is_ready()
    return result

def set_initial_conditions(current_planet, mouse_position):
    """
    Set the initial conditions of 'current_planet' based on the current 'mouse_position'.
    Sets initial conditions in order -- location first, then size, then direction -- based of the status of indicator flags contained in the planet object.
    
    input parameter: current_planet - the planet object that you want to set the initial conditions for
                     mouse_position - the current positon of the user's mouse
    """
    if not current_planet.is_placed:
        message = "Set the position of the planet."
        set_initial_position(current_planet, mouse_position)
    elif not current_planet.is_sized:
        message = "Set the size of the planet."
        set_size(current_planet, mouse_position)
    elif not current_planet.is_directed:
        message = "Set the velocity of the planet."
        set_initial_velocity(current_planet, mouse_position)
    
    text = LARGE_FONT.render(message, 1, WHITE)
    text_position = text.get_rect(centerx=SCREEN_WIDTH/2, centery=20)
    DISPLAYSURF.blit(text, text_position)

def set_initial_position(current_planet, mouse_position):
    """
    Set the initial position of 'current_planet' to be the current 'mouse_position'.
    
    input parameter: current_planet - the planet object that you want to set the initial position for
                     mouse_position - the current position of the user's mouse
    """
    current_planet.position = mouse_position

def set_size(current_planet, mouse_position):
    """
    Set the initial size (radius and mass) of 'current_planet' based on the current 'mouse_position'.
    Calculates the length of the vector from the center of 'current_planet' to 'mouse_position'.  The vector is then dividided by MAX_VECTOR to calculate the 'multiplier' for setting the mass and radius.
    
    Also draws the current mass of the planet to the display screen.
    
    input parameter: current_planet - the planet object that you want to set the initial size for
                     mouse_position - the current position of the user's mouse
    """
    #calculate the length of the vector from the center of the planet to the current mouse position
    vector_length = math.hypot(current_planet.position[0]-mouse_position[0], current_planet.position[1]-mouse_position[1])
    
    #calculate the multiplier for the radius and mass of the planet
    multiplier = vector_length/MAX_VECTOR
    
    current_planet.radius = multiplier
    current_planet.mass = multiplier
    
    display_string = "Mass: " + "{0:0.1f}".format(current_planet.mass)
    text = SMALL_FONT.render(display_string, 1, WHITE)
    text_position = text.get_rect(centerx=(current_planet.position[0]), centery=(current_planet.position[1]+current_planet.radius+10))
    DISPLAYSURF.blit(text, text_position)
    
def set_initial_velocity(current_planet, mouse_position):
    """
    Set the initial velocity of 'current_planet' based on the current 'mouse_position'.
    Calculates the length of the x and y vectors from the center of 'current_planet' to 'mouse_position'.  The vectors are then dividided by MAX_VECTOR to calculate the multipliers for setting the initial velocity of the planet.
    
    Also draws an arrow from the center of the planet to the users mass to visually represent the velocity vector
    
    input parameter: current_planet - the planet object you want to set the initial velocity for
                     mouse_position - the current positon of the user's mouse
    """
    x_vector = mouse_position[0]-current_planet.position[0]
    y_vector = mouse_position[1]-current_planet.position[1]
    x_multiplier = x_vector/float(MAX_VECTOR)
    y_multiplier = y_vector/float(MAX_VECTOR)
    current_planet.velocity = [x_multiplier, y_multiplier]
    
    draw_velocity_vector(current_planet)
    
    display_string = "Velocity: " + "{0:0.1f}".format(math.hypot(current_planet.velocity[0], current_planet.velocity[1]))
    text = SMALL_FONT.render(display_string, 1, WHITE)
    text_position = text.get_rect(centerx=mouse_position[0], centery=(mouse_position[1]+10))
    DISPLAYSURF.blit(text, text_position)

def draw_velocity_vector(current_planet):
    """
    Draw a representation of the 'current_planet' velocity vector.
    
    TODO: want to update this to draw an arrow instead of a sign
    
    input parameter: current_planet - the planet you want to draw the velocity vector for
    """
    position_1 = current_planet.position
    position_2 = (current_planet.position[0]+int(current_planet.velocity[0]*300),
                  current_planet.position[1]+int(current_planet.velocity[1]*300))
    
    pygame.draw.line(DISPLAYSURF, WHITE, position_1, position_2)
    
if __name__ == '__main__':
    main()

