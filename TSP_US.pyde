'''TSP with state capitals
5/7/17
'''

import random
import urllib

url = 'http://peterf.coderbootcamp.org/capitals.txt'

statedata = urllib.urlopen(url).read().split()

cities = [];
totalCities = 48;
population_size = 5000
nums = [x for x in range(totalCities)]
mutationRate = 0.02
first = True #the first "best" route
firstBest = []
firstDist = 0
generations = 0

class City:
    def __init__(self,x,y):
        global cities
        self.pos = PVector(x,y)
        cities.append(self)
        print("length of cities list")
        print(len(cities))

class Organism:
    def __init__(self):
        self.score = 0
        self.length = 0
        self.cities = nums[:]
        random.shuffle(self.cities)
            
    def calculateLength(self):
        for i,c in enumerate(self.cities):
            if i < totalCities - 1:
                d = dist(cities[c].pos.x,
                         cities[c].pos.y,
                         cities[self.cities[i+1]].pos.x,
                         cities[self.cities[i+1]].pos.y)
                self.length += d
                #add distance from last to first city
                self.length += dist(cities[self.cities[0]].pos.x,
                                    cities[self.cities[0]].pos.y,
                                    cities[self.cities[-1]].pos.x,
                                    cities[self.cities[-1]].pos.y)

        return self.length
            
    def calcScore(self):
        myLength = self.calculateLength()
        self.score = 1000000.0/myLength
        return self.score

    def crossover(self,partner):
        '''splice together their genes'''
        child = Organism()
        #print("child: ",child.cities)
        index = random.randint(0,totalCities-1) #start of slice
        slicesize = random.randint(1,totalCities-index)
        myslice = self.cities[index:index+slicesize]
        notinslice = [x for x in partner.cities if x not in myslice]
        def generateNextCity():
            '''generates next city not in the slice'''
            for n in notinslice:
                yield n
        nextCity = generateNextCity()

        #put slice in child list
        for i in range(slicesize):
            child.cities[index+i] = self.cities[index+i]
        #fill in with next parent's cities
        for j,v in enumerate(child.cities):
            #if it's not where the slice is
            if j not in range(index,index+slicesize,1):
                #apply numbers from "notinslice" list
                child.cities[j] = next(nextCity)
        #mutate the genes
        for g in child.cities:
            if random.random() < mutationRate:
                a = random.randint(0,totalCities-1)
                b = random.randint(0,totalCities-1)
                child.cities[a],child.cities[b] = child.cities[b],child.cities[a]
        return child
    
    def swap(self):
        #swap a random number of cities in the best list
        ran = random.randint(1,10)
        for i in range(ran):
            a = random.choice(self.cities)
            b = random.choice(self.cities)
            a,b = b,a


def setup():
    global population_size,cities,totalCities,recordDistance,bestEver,population
    size(800,600);
    population = []
    #get info from txt file
    capitals = []
    for row in range(48):
        capitals.append(statedata[4*row:4*row+4])

    for c in capitals:
        fill(255)
        x = map(float(c[3]),-125,-65,-400,400)
        y = map(float(c[2]),25,50,300,-300)

        City(x,y) #create City, put in cities list.
    #put organisms in population
    for i in range(population_size):
        population.append(Organism());
    for c in cities:
        println(c.pos)
    recordDistance = 1000000 #big number
    bestEver = cities[:];

def draw():
    global cities,totalCities,recordDistance,bestEver,population,first,firstBest,firstDist, generations
    background(0);
    translate(width/2,height/2)
    #Draw the cities
    
  
    #the best path so far
    for org in population:
        fill(255); #white ellipses for cities
        for c in cities:
            ellipse(c.pos.x,c.pos.y,8,8);
        
        
        tourlength = org.calculateLength()
        if tourlength < recordDistance:
            recordDistance = tourlength
            bestEver = org.cities[:]
            
    #println("Record: "+str(recordDistance))
    #println(bestEver)
    
    if first == True: #for the first "best" tour
        firstBest = bestEver[:]
        firstDist = recordDistance
        first = False
    
    
    #display first best distance
    
    fill(255)
    textSize(24)
    text(firstDist,-300,-250)
    
    #display record distance so far
    fill(255,0,255)
    textSize(24)
    text(recordDistance,200,-250)
    noFill()
    
    stroke(255,0,255);
    strokeWeight(4);
    beginShape();
    for t in range(totalCities):
        vertex(cities[bestEver[t]].pos.x,cities[bestEver[t]].pos.y);
    endShape(CLOSE);
    
    #create mating pool
    matingPool = []
    for org in population:
        score = org.calcScore()
        #println(score)
        num = int(score)
        for i in range(num):
            matingPool.append(org)
            
    random_org = random.choice(population)
    #draw the continuing attempts
    '''stroke(255);
    strokeWeight(1);
    noFill();
    beginShape();
    for t in random_org.cities:
        vertex(cities[t].pos.x,cities[t].pos.y);
    endShape(CLOSE);'''
            
    for i in range(population_size):
        #choose 2 organisms from mating pool:
        parentA = random.choice(matingPool)
        parentB = random.choice(matingPool)
        
        #reproduce:
        child = parentA.crossover(parentB)
        population[i] = child
    
    #println(generations)
    generations += 1
    #every hundred generations
    if generations % 100 == 0:
        #save a screenshot
        saveFrame('best####.jpg')
    #after 300 generations
    if generations >300:
        for i in range(20): #20 of you
            #swap cities around
            random_organism = random.choice(population)
            random_organism.cities = bestEver[:]
            random_organism.swap()
    