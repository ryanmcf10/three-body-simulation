import pygame
from pygame.locals import *

import numpy as np

#CONSTANTS
MAX_RADIUS = 25
MAX_MASS = 10
STANDARD_VELOCITY = .35

class Planet(object):
    """
    PLANET
    
    One of the planets in the three body orbit simulator.  Contains position and velocity vectors for the planet.
    
    Initial conditions are set by the player.  All initial conditions have been specified when is_ready() returns True
    
    position = [x, y]
    velocity = [x_veleocity, y_velocity]
    radius = radius of display circle
    mass = mass of planets
    
    is_placed, is_sized, is_directed = boolean values to check status of planet
    """
    def __init__(self, color):
        self.color = color
        
        self._position = np.array([0., 0.])
        self._velocity = np.array([0., 0.])
        self._radius = 15
        self._mass = 10.
        
        self.is_placed = False
        self.is_sized = False
        self.is_directed = False
        
    @property
    def position(self):
        """
        returns the current position of the planet as a vector - [x, y]
        """
        x = int(self._position[0])
        y = int(self._position[1])
        return [x, y]
    
    @position.setter
    def position(self, value):
        """
        Set the position of the planet.
                
        input parameters: value - list of x,y coordinates - [x, y]
        """
        self._position[0] = float(value[0])
        self._position[1] = float(value[1])
        
    @property
    def velocity(self):
        """
        returns the current velocity of the planet as a vector - [x_veleocity, y_velocity]
        """
        x_velocity = self._velocity[0]
        y_velocity = self._velocity[1]
        return [x_velocity, y_velocity]
        
    @velocity.setter
    def velocity(self, multipliers):
        """
        Set the velocity of the planet to be the STANDARD_VELOCITY times a multiplier
                
        input parameters: value - list of x,y multipliers - [x_multiplier, y_multiplier]
        """
        self._velocity[0] = STANDARD_VELOCITY*multipliers[0]
        self._velocity[1] = STANDARD_VELOCITY*multipliers[1]

        
    @property
    def radius(self):
        """
        return the radius of the planet
        """
        return self._radius
    
    @radius.setter
    def radius(self, multiplier):
        """
        Set the radius of the planet.  Caps the radius at MAX_RADIUS.
        
        input parameters: multiplier - float to set  radius to MAX_RADIUS*multiplier
        """
        if multiplier > 1:
            multiplier = 1
        self._radius = int(multiplier*MAX_RADIUS)
        
    @property
    def mass(self):
        """
        return the mass of the planet
        """
        return self._mass
    
    @mass.setter
    def mass(self, multiplier):
        """
        return the mass of the planet. Caps the mass at MAX_MASS.
                
        input parameters: multiplier - float to set mass to MAX_MASS*multiplier
        """
        if multiplier > 1:
            multiplier = 1
        
        self._mass = multiplier*MAX_MASS
        
    def is_ready(self):
        return (self.is_placed and self.is_sized and self.is_directed)
        
    def draw(self, surface):
        """
        Draw the planet as a circle with a 2px white outline
        """
        pygame.draw.circle(surface, (255, 255, 255), self.position, self.radius+2)
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        
    
    