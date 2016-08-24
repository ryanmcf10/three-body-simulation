from visual import *
import planet


class Simulate(object):
    """
    SIMULATION
    
    Class to initialize a VPython simulation of the three body problem.
    
    Takes three 'planet' objects as arguments.  'planet' objects are formatted for use on a pygame pygame display, so some changes must be made before the planets can be initialized as VPython Spheres:
        -both x and y coordinates are divided by 20 to scale from 800x800 PyGame display to 800x800 VPython display
        -sign of y coordinate and y velocity are flipped
        -color values are divided by 255 -- in PyGame, colors are in the range 0-255, in VPython colors are in the range 0-1
    """
    window = display(title = "Three Body Problem Simulation", 
                     autoscale = True, 
                     center = (20, -20), 
                     width=800, 
                     height=800)
    
    def __init__(self, planet_1, planet_2, planet_3):
        self.planet_1 = planet_1
        self.planet_2 = planet_2
        self.planet_3= planet_3
        
        #convert the data saved as planets to VPython Spheres
        self.sphere_1 = sphere(pos = vector(self.planet_1.position[0]/20, -self.planet_1.position[1]/20), 
                               vel = vector(self.planet_1.velocity[0], -self.planet_1.velocity[1]), 
                               mass = self.planet_1.mass, 
                               color = (self.planet_1.color[0]/255., self.planet_1.color[1]/255., self.planet_1.color[2]/255.),
                               make_trail = True, 
                               interval=2, 
                               retain=1000)
        
        self.sphere_2 = sphere(pos = vector(self.planet_2.position[0]/20, -self.planet_2.position[1]/20), 
                               vel = vector(self.planet_2.velocity[0], -self.planet_2.velocity[1]), 
                               mass = self.planet_2.mass,
                               color = (self.planet_2.color[0]/255., self.planet_2.color[1]/255., self.planet_2.color[2]/255.),
                               make_trail = True, 
                               interval=2, 
                               retain=1000)

        self.sphere_3 = sphere(pos = vector(self.planet_3.position[0]/20, -self.planet_3.position[1]/20), 
                               vel = vector(self.planet_3.velocity[0], -self.planet_3.velocity[1]), 
                               mass = self.planet_3.mass, 
                               color = (self.planet_3.color[0]/255., self.planet_3.color[1]/255., self.planet_3.color[2]/255.),
                               make_trail = True, 
                               interval=2, 
                               retain=1000)
        
        self.spheres = [self.sphere_1, self.sphere_2, self.sphere_3]
        
        #calculate the center of mass
        vcentre=(self.sphere_1.mass*self.sphere_1.vel + self.sphere_2.mass*self.sphere_2.vel + self.sphere_3.mass*self.sphere_3.vel)/(self.sphere_1.mass + self.sphere_2.mass + self.sphere_3.mass)
        
        for a in self.spheres:
            a.vel -= vcentre
            a.radius = 0.5*a.mass**(1.0/3.0)

        dt = 0.1
        
        #calculate and update the display
        while True:
            rate(100)
            ## solve using forth-order Runge Kutta approximation method
            y = [self.sphere_1.pos, self.sphere_1.vel, self.sphere_2.pos, self.sphere_2.vel, self.sphere_3.pos, self.sphere_3.vel]
            k1 = dt*self.dydt(y)
            k2 = dt*self.dydt(y+k1/2.0)
            k3 = dt*self.dydt(y+k2/2.0)
            k4 = dt*self.dydt(y+k3)
            dy = k1/6.0 + k2/3.0 +k3/3.0 + k4/6.0
            ## update the animation
            self.sphere_1.pos += dy[0]
            self.sphere_1.vel += dy[1]
            self.sphere_2.pos += dy[2]
            self.sphere_2.vel += dy[3]
            self.sphere_3.pos += dy[4]
            self.sphere_3.vel += dy[5]
        
    def dydt(self, y):
    ## determine the derivative of the state vector y
        deriv = zeros((6,3), dtype=vector)
        r12=y[0]-y[2]; r23=y[2]-y[4]; r31=y[4]-y[0]
        r12c=r12/mag(r12)**3; r23c=r23/mag(r23)**3; r31c=r31/mag(r31)**3
        deriv[1] = -self.sphere_2.mass*r12c + self.sphere_3.mass*r31c
        deriv[3] = -self.sphere_3.mass*r23c + self.sphere_1.mass*r12c
        deriv[5] = -self.sphere_1.mass*r31c + self.sphere_2.mass*r23c
        deriv[0:5:2] = y[1:6:2] 
        return deriv
