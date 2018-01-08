'''TSPGAbook3Crossover2.pyde
For the GA Chapter of book
Fixed the glitch January 7, 2018'''

import random

number_of_cities = 30
WHITE = color(255)
PURPLE = color(255,0,255)
mutationRate = 0.02

class City:
    def __init__(self,x,y,num):
        self.loc = PVector(x,y)#random(100),random(100))
        self.number = num #identifying number
        
    def display(self):
        fill(0,255,255)
        ellipse(self.loc.x,self.loc.y,10,10)
        textSize(20)
        text(self.number,self.loc.x-10,self.loc.y-10)
        noFill()
        
class Route:
    def __init__(self,cities,numList):
        self.distance = 0
        #put cities in a list in numList order:
        self.citiesList = [cities[i] for i in numList]

    def display(self,col=PURPLE):
        strokeWeight(3)
        stroke(col)#255,0,255) #purple
        beginShape()
        for city in self.citiesList:
            vertex(city.loc.x,city.loc.y)
        
            #then display the cities and their numbers
            city.display()
        endShape(CLOSE)
        
    def calcLength(self):
        self.distance = 0 #reset to 0
        for i,city in enumerate(self.citiesList):
            #if this is the last city in the list, find the distance
            #from this city to the first city
            if i < len(self.citiesList) - 1:
                self.distance += dist(city.loc.x,
                                      city.loc.y,
                                      self.citiesList[i+1].loc.x,
                                      self.citiesList[i+1].loc.y)
        #finally, add the distance between the first and last city
        self.distance += dist(self.citiesList[-1].loc.x,
                        self.citiesList[-1].loc.y,
                        self.citiesList[0].loc.x,
                        self.citiesList[0].loc.y)
                
        return self.distance

class Genes:
    def __init__(self):
        #random list of numbers representing the order of cities visited
        self.city_nums = random.sample(list(range(number_of_cities)),
                                            number_of_cities)
        #create a route with that order:
        self.route = Route(cities,self.city_nums)

    def mutate(self):
        #swaps two numbers in city numbers list
        index1,index2 = random.sample(list(range(number_of_cities)),2)
        #a,b = b,a to swap
        self.city_nums[index1],self.city_nums[index2] = \
            self.city_nums[index2],self.city_nums[index1]
        #again, after changing the order you have to change the Route, too
        self.route = Route(cities,self.city_nums)
        
    def mutate3(self):
        #swaps 3 numbers in city numbers list
        index1, index2, index3 = random.sample(list(range(number_of_cities)),3)
        self.city_nums[index1],self.city_nums[index2],self.city_nums[index3] = \
            self.city_nums[index2],self.city_nums[index3],self.city_nums[index1]
        
    def crossover(self,partner):
        '''splice together their genes'''
        child = Organism()
        #print("child: ",child.cities)
        index = random.randint(0,number_of_cities-1) #start of slice
        slicesize = random.randint(1,number_of_cities-index) #size of slice
        myslice = self.city_nums[index:index+slicesize]
        #list of numbers not in the slice
        notinslice = [x for x in partner.genes.city_nums if x not in myslice]
        def generateNextCity():
            '''generates next city not in the slice'''
            for n in notinslice:
                yield n
        nextCity = generateNextCity() #a generator!
        #print("slice: ",myslice)
        #put slice in child list
        for i in range(slicesize):
            child.genes.city_nums[index+i] = self.city_nums[index+i]
        #fill in with next parent's cities
        for j,v in enumerate(child.genes.city_nums):
            #if it's not where the slice is
            if j not in range(index,index+slicesize,1):
                #apply numbers from "notinslice" list
                child.genes.city_nums[j] = next(nextCity)
        #once again, after changing the order, you have to update the Route
        child.genes.route = Route(cities,child.genes.city_nums)
    
        #mutate the genes (same as mutate(self))
        if random.random() < mutationRate:
            a = random.randint(0,number_of_cities-1)
            b = random.randint(0,number_of_cities-1)
            child.genes.city_nums[a],child.genes.city_nums[b] = child.genes.city_nums[b],child.genes.city_nums[a]
        return child
    
class Organism:
    def __init__(self):
        self.genes = Genes() #random list of numbers
        self.score = 0
    
    def calcScore(self):
        #the lower the length of the route, the higher the score
        self.score = 100000.0/self.genes.route.calcLength()
        return self.score
    
    def display(self,col=PURPLE):
        self.genes.route.display(col)

cities = []
population = []
number_of_organisms = 1000
        
def setup():
    global best_genes,record_distance,first_best,cities
    global population,org1
    size(800,800)
    background(0)
    #create a cities list randomly or from an
    #already generated list of cities for testing/comparison
    cities = [City(454.0,648.0,0),
City(706.0,474.0,1),
City(301.0,595.0,2),
City(602.0,700.0,3),
City(391.0,426.0,4),
City(396.0,36.0,5),
City(264.0,51.0,6),
City(359.0,409.0,7),
City(696.0,754.0,8),
City(521.0,789.0,9),
City(531.0,70.0,10),
City(694.0,299.0,11),
City(231.0,215.0,12),
City(616.0,202.0,13),
City(599.0,655.0,14),
City(429.0,382.0,15),
City(632.0,348.0,16),
City(141.0,686.0,17),
City(90.0,323.0,18),
City(99.0,494.0,19),
City(108.0,766.0,20),
City(34.0,480.0,21),
City(243.0,634.0,22),
City(266.0,603.0,23),
City(771.0,744.0,24),
City(393.0,387.0,25),
City(337.0,191.0,26),
City(318.0,696.0,27),
City(147.0,733.0,28),
City(434.0,471.0,29)]
    #uncomment this out to generate Cities in random locations
    '''
    for i in range(number_of_cities):
            cities.append(City(random.randint(20,width-20),
                            random.randint(20,height-20),i))
    #This prints out the list of cities for future use
    for city in cities:
        println("City("+str(city.loc.x)+','+ \
        str(city.loc.y)+','+str(city.number)+"),")'''
    #put the organisms in the population list
    for i in range(number_of_organisms):
        population.append(Organism())
    #choose a random Organism to be the first best one
    org1 = random.choice(population)
    #best Genes 
    best_genes = org1.genes
    #first best route length
    first_best = best_genes.route.calcLength()
    record_distance = first_best
    
    #println(record_distance)
    
    
def draw():
    global best_genes, record_distance,org1
    global population, number_of_organisms
    background(0)
    
    #uncomment to add random new organisms
    '''for i in range(50):
        new_org = Organism()
        population.append(new_org)'''
    
    #uncomment to limit the population
    '''if len(population) > 10000:
        while len(population) > 10000:
            index = random.randint(0,len(population)-1)
            population.remove(population[index])'''
    #println("pop: "+str(len(population)))
    for org in population:
        new_length = org.genes.route.calcLength()
        if new_length >= record_distance:
            continue
        if new_length < record_distance:
            println("org: "+str(org.score))
            best_genes = org.genes
            #best_genes.city_nums = org.genes.city_nums[::]
            record_distance = new_length
            displayResults(best_genes, record_distance, first_best)
            '''for i in range(5):
                new_org = Organism()
                new_org.genes.city_nums = best_genes.city_nums[::]
                new_org.genes.mutate()
                population.append(new_org)
            for i in range(5):'''
            #do a 3-mutate on one organism
            new_org = Organism()
            new_org.genes.city_nums = best_genes.city_nums[::]
            new_org.genes.mutate3()
            population.append(new_org)
                
        #else: #delete inferior organisms
            #del(org)
            
    #display first best distance
    
    fill(255)
    textSize(24)
    text(first_best,30,30)
    
    #display record distance so far
    fill(255,0,255)
    textSize(24)
    text(record_distance,450,30)
    noFill()
    
    #draw first guess in white if you want to see it
    #org1.display(WHITE) 
            
    #create mating pool
    matingPool = []
    for org in population:
        score = org.calcScore()
        #get score as integer
        num = int(score)
        #put that many copies of the Organism in
        #the mating pool
        for i in range(num):
            matingPool.append(org)
    #println("matingpool: "+str(len(matingPool)))
    #println("population: "+str(len(population)))
    
    for i in range(number_of_organisms):
        #choose 2 organisms from mating pool:
        parentA = random.choice(matingPool)
        parentB = random.choice(matingPool)
        
        #reproduce:
        child = parentA.genes.crossover(parentB)
        population[i] = child
        
    #mutate the best ever:
    child = Organism()
    child.genes.city_nums = best_genes.city_nums[::]
    child.genes.mutate()
    #put it in the population
    population.append(child)
    
    #display the best route in purple            
    best_genes.route.display(PURPLE)
    #println("Pop: "+str(len(population)))
    
def displayResults(best_genes, record_distance, first_best):
    '''prints the stats in the console'''
    println("first: "+str(first_best) + " record: "+ str(record_distance))
    println(best_genes.city_nums)
    #println("improvement: "+ \
              #str(round(100*(first_best - record_distance)/first_best,1)) +"%")
    
    
