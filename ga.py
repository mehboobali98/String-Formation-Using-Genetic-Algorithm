from random import randint as rn
from random import sample
import random

string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890, .-;:_!\"#%&/()=?@${[]}"
target = "This is a sample string"


class Item:

    def __init__(self, Id, value):
        self.Id = Id
        self.value = value


class Individual:

    def __init__(self):
        self.genes = ''
        self.fitness = 0

    def calculate_fitness(self):
        for x, y in zip(self.genes, target):
            if x != y:
                self.fitness += 1

    def get_fitness(self):
        return self.fitness

    def init_individual(self):
        for i in range(len(target)):
            self.genes = self.genes + string[rn(0, len(string) - 1)]

    def print_individual(self):
        for x in self.genes:
            print(x, end=" ")

    def __lt__(self, other):
        return self.fitness < other.fitness

    def uniform_crossover(self, other):
        off_spring = Individual()

        for j in range(len(target)):
            p = random.random()
            if p < 0.45:
                off_spring.genes = off_spring.genes + self.genes[j]
            elif p < 0.90:
                off_spring.genes = off_spring.genes + other.genes[j]
            else:
                off_spring.genes = off_spring.genes + string[rn(0, len(string) - 1)]

        off_spring.calculate_fitness()
        return off_spring

    def mutate(self):
        index = rn(0, self.genes - 1)
        self.genes[index] = string[rn(0, len(string) - 1)]
        self.fitness = 0
        self.calculate_fitness()


population = []
p_size = 500  # population size
elitism_rate = 20
generation_count = 0
tournament_size = 5
mutation_rate = 0.50

for i in range(p_size):
    population.insert(i, Individual())

for i in range(p_size):
    population[i].init_individual()
    population[i].calculate_fitness()


def tournament_selection():
    pop = sample(population, len(population))
    tournament = []

    for i in range(tournament_size):
        tournament.append(pop[i])

    tournament.sort()
    return tournament[0]


while population[0].get_fitness() > 0:
    generation_count += 1
    population.sort()
    new_pop = []

    s = (elitism_rate * p_size) / 100

    for i in range(0, int(s)):
        new_pop.append(population[i])  # elitism

    s = p_size - s
    p_half = p_size / 2
    for i in range(0, int(s)):
        r = rn(0, int(p_half))
        parent1 = population[r]
        # parent1 = tournament_selection()
        r = rn(0, int(p_half))
        parent2 = population[r]
        # parent2 = tournament_selection()
        offspring = parent1.uniform_crossover(parent2)
        if mutation_rate > random.random():
            offspring.mutate
        new_pop.append(offspring)

    population = new_pop

    print("Generation Count: " + str(generation_count) + " Fittest: " + str(population[0].fitness))
    print("String: " + population[0].genes)
