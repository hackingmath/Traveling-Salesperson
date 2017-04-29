'''From Coding Train
https://youtu.be/BAejnwN4Ccw 
3/2/2017
Added Genetic Algorithm
4/27/2017
'''

import random

cities = [];
totalCities = 20;
population_size = 1000
nums = [x for x in range(totalCities)]
mutationRate = 0.02
first = True #the first "best" route
firstBest = []
firstDist = 0

class City:
    def __init__(self,number):
        global cities
        self.number = number
        self.pos = PVector(random.randint(0,width),random.randint(0,height))
        cities.append(self)

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
        #println(self.length)
        #println(10000.0/self.length)
        return self.length
            
    def calcScore(self):
        myLength = self.calculateLength()
        self.score = 1000000.0/myLength
        #println("Mylength:"+str(myLength))
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
        #print("slice: ",myslice)
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

def setup():
    global population_size,cities,totalCities,recordDistance,bestEver,population
    size(600,600);
    population = []
    for c in range(totalCities):
        City(c) #create City, put in cities list.
    #put organisms in population
    for i in range(population_size):
        population.append(Organism());
    for c in cities:
        println(c.pos)
    recordDistance = 1000000 #big number
    bestEver = cities[:];

def draw():
    global cities,totalCities,recordDistance,bestEver,population,first,firstBest,firstDist
    background(0);
    #Draw the cities
    fill(255); #white ellipses for cities
    for c in cities:
        ellipse(c.pos.x,c.pos.y,8,8);
    noFill();
  
    #the best path so far
    for org in population:
        tourlength = org.calculateLength()
        if tourlength < recordDistance:
            recordDistance = tourlength
            bestEver = org.cities[:]
    println("Record: "+str(recordDistance))
    println(bestEver)
    
    if first == True: #for the first "best" tour
        firstBest = bestEver[:]
        firstDist = recordDistance
        first = False
    stroke(255);
    strokeWeight(1);
    beginShape();
    for t in range(totalCities):
        vertex(cities[firstBest[t]].pos.x,cities[firstBest[t]].pos.y);
    endShape(CLOSE);
    
    #display first best distance
    
    fill(255)
    textSize(24)
    text(firstDist,30,30)
    
    #display record distance so far
    fill(255,0,255)
    textSize(24)
    text(recordDistance,450,30)
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
            
    println("matingpool: "+str(len(matingPool)))
    println("population: "+str(len(population)))
            
    for i in range(population_size):
        #choose 2 organisms from mating pool:
        parentA = random.choice(matingPool)
        parentB = random.choice(matingPool)
        
        #reproduce:
        child = parentA.crossover(parentB)
        population[i] = child
