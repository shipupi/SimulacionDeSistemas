class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        r = "[{}, {}]".format(self.x, self.y)
        return r

class Particle():
    def __init__(self, ratio, properties):
        self.ratio = ratio
        self.properties = properties
        self.neighbours = []
    
    def dynamic(self, position, velocity):
        self.position = position
        self.velocity = velocity
    
    def set_neighbours(self, neighbours):
        self.neighbours = neighbours
    
    def __str__(self):
        r = "Particle Description\n"
        r += "ratio: {}\n".format(self.ratio)
        r += "properties: {}\n".format(self.properties)
        if self.position or self.velocity:
            r = "Particle Dyanmic Information\n"
            if self.position: r+= "Position: {}\n".format(self.position.__str__()) 
            if self.velocity: r+= "Velocity: {}\n".format(self.velocity.__str__())
        return r
    
    def print_neighbours(self):
        if self.neighbours.__len__() > 0:
            print("Neighbours: {}".format(self.neighbours))
        else:
            print("This particle does not have neighbours at the time")

class SystemConfiguration():
    def __init__(self, config):

        self.config = config
        self.static_configuration()
        self.dynamic_configuration()
        self.neighbours_configuration()

    def static_configuration(self):
        static_path = self.config['paths']['static_path']
        
        f = open(static_path, 'r')
        lines = f.readlines()
        self.t = float(lines[0])
        self.N = float(lines[1])
        self.L = float(lines[2])
        self.M = int(lines[3])
        self.rc = float(lines[4])
        self.B = False if int(lines[5]) == 0 else True

        self.particles = []
        for i in range(6, lines.__len__()):
            particle_info = lines[i].split(',', 1)
            properties = []
            if particle_info.__len__() > 1:
                aux_props = particle_info[1].split(',')
                for prop in aux_props:
                    properties.append(float(prop))
            self.particles.append(Particle(float(particle_info[0]), properties))
        
        f.close()

    def dynamic_configuration(self):
        dynamic_path = self.config['paths']['dynamic_path']
        f = open(dynamic_path, 'r')
        lines = f.readlines()

        self.particles_time = float(lines[0])
        for i in range(1, lines.__len__()):
            coords = lines[i].split(',')
            position = Point(float(coords[0]), float(coords[1]))
            velocity = Point(float(coords[2]), float(coords[3])) if coords.__len__() > 2 else None
            self.particles[i-1].dynamic(position, velocity)

        f.close()
    
    def neighbours_configuration(self):
        interaction_path = self.config['paths']['interaction_path']
        f = open(interaction_path, 'r')
        lines = f.readlines()

        for i in range(0, lines.__len__()):
            neighbours = []
            if lines[i] != '\n':
                aux_neighbours = lines[i].split(',')
                for neigh in aux_neighbours:
                    neighbours.append(int(neigh))
            self.particles[i].set_neighbours(neighbours)
        
        f.close()

    def __str__(self):
        r = "System's static configuration\n"
        r += "t: {}\n".format(self.t)
        r += "N: {}\n".format(self.N)
        r += "L: {}\n".format(self.L)
        r += "M: {}\n".format(self.M)
        r += "rc: {}\n".format(self.rc)
        r += "B: {}\n".format(self.B)
        return r
