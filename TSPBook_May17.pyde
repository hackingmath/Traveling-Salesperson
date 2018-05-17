#travelingSalesperson.pyde

import random

N_CITIES = 50

class City:
    def __init__(self,x,y,num):
        self.x = x
        self.y = y
        self.number = num #identifying number
        
    def display(self):
        fill(0,255,255) #sky blue
        ellipse(self.x,self.y,10,10)
        textSize(20)
        text(self.number,self.x-10,self.y-10)
        noFill()

class Organism:
    def __init__(self):
        self.distance = 0
        #put cities in a list in numList order:
        self.genes = random.sample(list(range(N_CITIES)),N_CITIES)
        
    def display(self):
        strokeWeight(3)
        stroke(255,0,255) #purple
        beginShape()
        for i in self.genes:
            vertex(cities[i].x,cities[i].y)
            #then display the cities and their numbers
            cities[i].display()
        endShape(CLOSE)

    def calcLength(self):
        self.distance = 0
        for i in range(N_CITIES):
        # find the distance to the previous city
            self.distance += dist(cities[self.genes[i]].x,
                                cities[self.genes[i]].y,
                                cities[self.genes[i-1]].x,
                                cities[self.genes[i-1]].y)
        return self.distance
    
    def mutate(self):
        index1,index2 = random.sample(list(range(N_CITIES)),2)
        self.genes[index1],self.genes[index2] = self.genes[index2],\
        self.genes[index1] #this works!
        
    def mutateN(self,num):
        indices = random.sample(list(range(N_CITIES)),num)
        child = Organism()
        child.genes = self.genes[::]
        for i in range(num-1):
            child.genes[indices[i]],child.genes[indices[(i+1)%num]] = \
            child.genes[indices[(i+1)%num]], child.genes[indices[i]]
        return child
    
    def crossover(self,partner):
        '''Splice together genes with partner's genes'''
        child = Organism()
        #randomly choose slice point
        index = random.randint(1, N_CITIES - 2)
        #add numbers up to slice point
        child.genes = self.genes[:index]
        #half the time reverse them
        if random.random()<0.5:
            child.genes = child.genes[::-1]
        #list of numbers not in the slice
        notinslice = [x for x in partner.genes if x not in child.genes]
        #add the numbers not in the slice
        child.genes += notinslice
        return child

'''cities = [City( 146 , 467 , 0 ),
City( 426 , 399 , 1 ),
City( 201 , 173 , 2 ),
City( 67 , 340 , 3 ),
City( 65 , 109 , 4 ),
City( 168 , 231 , 5 ),
City( 339 , 536 , 6 ),
City( 430 , 199 , 7 ),
City( 318 , 344 , 8 ),
City( 282 , 154 , 9 ),
City( 196 , 467 , 10 ),
City( 229 , 472 , 11 ),
City( 101 , 168 , 12 ),
City( 454 , 211 , 13 ),
City( 417 , 355 , 14 ),
City( 387 , 76 , 15 ),
City( 269 , 165 , 16 ),
City( 329 , 136 , 17 ),
City( 180 , 52 , 18 ),
City( 294 , 382 , 19 ),
City( 341 , 321 , 20 ),
City( 395 , 162 , 21 ),
City( 250 , 138 , 22 ),
City( 532 , 358 , 23 ),
City( 80 , 194 , 24 ),
City( 136 , 342 , 25 ),
City( 337 , 102 , 26 ),
City( 411 , 117 , 27 ),
City( 65 , 439 , 28 ),
City( 197 , 55 , 29 ),
City( 194 , 463 , 30 ),
City( 546 , 159 , 31 ),
City( 504 , 218 , 32 ),
City( 275 , 197 , 33 ),
City( 198 , 78 , 34 ),
City( 280 , 388 , 35 ),
City( 513 , 316 , 36 ),
City( 379 , 128 , 37 ),
City( 378 , 108 , 38 ),
City( 475 , 502 , 39 ),
City( 86 , 52 , 40 ),
City( 537 , 435 , 41 ),
City( 500 , 364 , 42 ),
City( 181 , 443 , 43 ),
City( 319 , 387 , 44 ),
City( 546 , 366 , 45 ),
City( 53 , 200 , 46 ),
City( 270 , 221 , 47 ),
City( 279 , 455 , 48 ),
City( 134 , 226 , 49 )]'''
cities = []
population = [] #list for Organisms
POP_N = 10000 #number of Organisms in population

def setup():
    global best, record_distance,first,population
    size(800,800)
    for i in range(N_CITIES):
        cities.append(City(random.randint(50,width-50),
                           random.randint(50,height-50),i))
    #put organisms in population list
    for i in range(POP_N):
        population.append(Organism())
    best = random.choice(population)
    record_distance = best.calcLength()
    first = record_distance
    
def draw():
    global best, record_distance,population
    background(0)
    best.display()
    population.sort(key=Organism.calcLength)
    population = population[:POP_N]
    matingPool = population[::]
    # now sort it from shortest route to longest route
    
    # the first Organism has the shortest route 
    #org1 = matingPool[0]    
    length1 = matingPool[0].calcLength()
    #print("length1:"+str(length1))
    if length1 < record_distance:
        best = matingPool[0]
        record_distance = length1
    matingPool = matingPool[:1000]
    
    
    #do crossover on mating pool
    for i in range(POP_N):#len(matingPool)):
        parentA, parentB = random.sample(matingPool,2)

        #reproduce:
        child = parentA.crossover(parentB)
        index = random.randint(0,POP_N-1)
        population.append(child)
        
    for i in range(3,25):
        if i < N_CITIES:
            neworg = matingPool[0].mutateN(i)
            index = random.randint(0,POP_N-1)
            population.append(neworg)
   
    for i in range(3,25):
        if i < N_CITIES:
            index = random.randint(0,len(matingPool)-1)
            neworg = matingPool[index].mutateN(i)
            index = random.randint(0,POP_N-1)
            population.append(neworg)
            
            #println("Mutate")
    
    textSize(30)
    text(first,30,50)
    text(record_distance,300,50) 
    
    println(best.genes)
