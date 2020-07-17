from random import randint
from random import shuffle
import itertools

def makegrid(n):
    a = [[0] * n for i in range(n)]     #make grid of nxn
    for i in range(n):
        for j in range(n):
            if i == 0 or j == 0:
                a[i][j] = 1                #box next to wall is 1
            elif i == (n-1) or j == (n-1):
                a[i][j] = 1
            else:
                a[i][j] = 0               #else zero

    a[2][n-2] = 1          #the two boxes out case
    a[2][n-1] = 'x'
    a[3][n-2] = 1
    a[3][n-1] = 'x'

    #for row in a:
        #print(' '.join([str(elem) for elem in row]))
    return a


def inipop(popsize, stringlength):      # initialize population with random strings
    pop = []
    for i in range(popsize):
        pop.append('')
        for _ in range(stringlength):
            value = randint(0,1)
            pop[i] = pop[i] + str(value)
        #print(pop[i])

    return pop


def fitness(string, grid, is_visited):        # calculate fitness of one string
    length = len(string)
    fitnesscounter=1
    currpos_i=0
    currpos_j=0
    is_visited[0][0]=1
    direction='E'

    for i in range(0,length,2):
        #print("enter loop test")
        if string[i]=='0' and string[i+1]=='0': #do nothing
            #print("do nothing")
            continue
        elif string[i]=='0' and string[i+1]=='1': #turn right
            #print("turn right")
            if direction=='N':
                direction = 'E'
            elif direction == 'E':
                direction = 'S'
            elif direction == 'S':
                direction = 'W'
            elif direction == 'W':
                direction = 'N'

        elif string[i] == '1' and string[i + 1] == '0':  # turn left
            #print("turn left")
            if direction == 'N':
                direction = 'W'
            elif direction == 'W':
                direction = 'S'
            elif direction == 'S':
                direction = 'E'
            elif direction == 'E':
                direction = 'N'

        elif string[i] == '1' and string[i+1] == '1': #move forward
            #print("move forward")
            if direction == 'N':        #if north
                if currpos_i == 0:          #donot move if already on top
                    continue
                elif currpos_i==4 and currpos_j==5:
                    continue
                else:
                    currpos_i = currpos_i -1    #else i--

            elif direction == 'S':      #if south
                if currpos_i == len(grid) - 1:  #donot move if last row
                    continue
                elif currpos_i== 1 and currpos_j==5:
                    continue
                else:
                    currpos_i = currpos_i +1    #else i++

            elif direction == 'E':      #if East
                if currpos_j==5:  #do not move if wall on right
                    continue
                elif currpos_i == 2 and currpos_j == 4:
                    continue
                elif currpos_i == 3 and currpos_j == 4:
                    continue
                else:
                    currpos_j= currpos_j +1          # j++

            elif direction == 'W':       #if West
                if currpos_j == 0:          #donot move if first column
                    continue
                else:
                        currpos_j = currpos_j -1    #else j--

            if grid[currpos_i][currpos_j]==1 and is_visited[currpos_i][currpos_j]==0:
                fitnesscounter = fitnesscounter+1   # if box next to wall then increment fitness
            is_visited[currpos_i][currpos_j] = 1
    return fitnesscounter


def fitnessofpop(population,grid):              #fitness of each string stored into array
    fitness_array = []
    popsize=len(population)
    n=6
    for i in range(popsize):
        isvisited_array = [[0] * n for k in range(n)]
        fitness_array.append(fitness(population[i], grid, isvisited_array))
    # for i in range(popsize):
        # print("The string is: ", population[i])
        # print("with fitness: ", fitness_array[i])
    return fitness_array


def roulette_wheel_selection(population , fitnessarray):
    popsize = len(population)
    totalfitness = sum(fitnessarray)
    probability = []
    new_pop = []
    sp = 0
    for i in range(popsize):
        sp = sp + fitnessarray[i]
        probability.append(sp)
    #print(probability)
    for i in range(popsize):
        value = randint(0,totalfitness-1)
        for j in range(popsize):
            if value < probability[j]:
                new_pop.append(population[j])
                break
    return new_pop


def operate(population):                            # apply mutation or crossover according to the rates
    shuffle(population)                             # shuffle the mating pool
    popsize = len(population)
    mutation_rate=(1/popsize) * 100                 # calculate mutation rate
    for i in range(popsize):
        value=randint(1,100)
        if value<mutation_rate:                     # mutation will occurr
            mutated = mutation(population[i])
            population[i]=mutated
        else:                                       # mutation will not occurr
            continue
    crossover_rate = randint(60,90)                 # calculate crossover rate
    for i in range(0,popsize,2):
        value=randint(1,100)
        if value < crossover_rate:                  # crossover will take place
            twonewstrings = crossover(population[i],population[i+1])
            population[i] = twonewstrings[0]
            population[i+1]=twonewstrings[1]
        else:
            continue                                # crossover will not take place

    return population

def mutation(string):
    length=len(string)
    number_of_mutations=randint(1,10)
    for i in range(number_of_mutations):
        temp = ""
        position= randint(0,length-1)
        #print("Mutation has occurred at position: ", position)
        for i in range(length):
            if (i!=position):
                temp=temp + string[i]
            else:
                if string[position]=='0':
                    temp=temp + '1'
                else:
                    temp = temp + '0'
        string=temp


    return string

def crossover(string1, string2):
    length=len(string1)
    position = randint(0,length-1)
    #print("Crossover has occurred at position: ", position)
    twonewstrings= ["",""]
    for i in range(length):
        if i <= position:
            twonewstrings[0]=twonewstrings[0] + string1[i]
            twonewstrings[1] = twonewstrings[1] + string2[i]
        elif i > position:
            twonewstrings[0] = twonewstrings[0] + string2[i]
            twonewstrings[1] = twonewstrings[1] + string1[i]
    return twonewstrings

def traversal(string, grid):        # calculate fitness of one string
    length = len(string)
    currpos_i=0
    currpos_j=0
    grid[currpos_i][currpos_j]= '>'
    direction='E'

    for i in range(0,length,2):
        #print("enter loop test")
        if string[i]=='0' and string[i+1]=='0': #do nothing
            #print("do nothing")
            continue
        elif string[i]=='0' and string[i+1]=='1': #turn right
            #print("turn right")
            if direction=='N':
                direction = 'E'
            elif direction == 'E':
                direction = 'S'
            elif direction == 'S':
                direction = 'W'
            elif direction == 'W':
                direction = 'N'

        elif string[i] == '1' and string[i + 1] == '0':  # turn left
            #print("turn left")
            if direction == 'N':
                direction = 'W'
            elif direction == 'W':
                direction = 'S'
            elif direction == 'S':
                direction = 'E'
            elif direction == 'E':
                direction = 'N'

        elif string[i] == '1' and string[i+1] == '1': #move forward
            #print("move forward")
            if direction == 'N':        #if north
                if currpos_i == 0:          #donot move if already on top
                    continue
                elif currpos_i==4 and currpos_j==5:
                    continue
                else:
                    currpos_i = currpos_i -1    #else i--

            elif direction == 'S':      #if south
                if currpos_i == len(grid) - 1:  #donot move if last row
                    continue
                elif currpos_i== 1 and currpos_j==5:
                    continue
                else:
                    currpos_i = currpos_i +1    #else i++

            elif direction == 'E':      #if East
                if currpos_j==5:  #do not move if wall on right
                    continue
                elif currpos_i == 2 and currpos_j == 4:
                    continue
                elif currpos_i == 3 and currpos_j == 4:
                    continue
                else:
                    currpos_j= currpos_j +1          # j++

            elif direction == 'W':       #if West
                if currpos_j == 0:          #donot move if first column
                    continue
                else:
                        currpos_j = currpos_j -1    #else j--

            if direction=='N':
                grid[currpos_i][currpos_j]='^'
            elif direction=='S':
                grid[currpos_i][currpos_j]='v'
            elif direction=='E':
                grid[currpos_i][currpos_j]='>'
            elif direction=='W':
                grid[currpos_i][currpos_j]='<'

    for row in grid:
        print(' '.join([str(elem) for elem in row]))

    return



n = 6  # nxn grid
popsize= 20
optimal_fitness = 16
grid = makegrid(n)
population = inipop(popsize, 56)
optimal_string="11010000101100111101001111110011001101111111110111111111"
found = 0
gen = 1
while (gen<100000 and found==0):
    print("Generation ", gen)
    print("Population: ", population)
    fitness_array = fitnessofpop(population,grid)
    print("Fitness values: ", fitness_array)
    for i in range(popsize):
        if fitness_array[i] > 16:
            optimal_string = population[fitness_array.index(max(fitness_array))]
            optimal_fitness = max(fitness_array)
            found = 1
    pre_generation = roulette_wheel_selection(population,fitness_array)
    #print(len(pre_generation))
    offspring = operate(pre_generation)
    population = offspring
    gen=gen+1


print("------------------------------------------------")
print("Optimal solution has been reached in generations: ", gen)
print("Optimal solution is: ", optimal_string)
print("with fitness = ", optimal_fitness)
print("The path taken by the robot was: ")
print("--------------")
traversal(optimal_string,grid)
print("--------------")

