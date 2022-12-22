import math
import random
import pandas as pd
import os
import numpy


# Генератор РРСЧ Лемера
class LehmerGenerator:
    def __init__(self, seed):
        if seed <= 0 or seed == 2147483647:
            raise Exception('Поменяйте seed!')
        self.seed = seed
        self.a = 16807
        self.m = 2147483647
        self.q = 127773
        self.r = 2836
        self.high_edge = 10
        self.low_edge = 0

    def next(self):
        hi = self.seed / self.q
        lo = self.seed % self.q
        self.seed = (self.a * lo) - (self.r * hi)
        if self.seed <= 0:
            self.seed = self.seed + self.m
        return int((self.high_edge - self.low_edge) * (self.seed / self.m) + self.low_edge)


# Генератор РРСЧ Мультипликативного сравнения
class RndMultiCmpGenerator:
    def __init__(self, x):
        self.x = x
        self.m = 2147483647
        self.a = 65539

    def next(self):
        self.x = (self.a * self.x) % self.m
        return self.x


# встроенный генератор случайных чисел
class BuiltInRnd:
    def __init__(self, x):
        pass

    def next(self):
        return random.randint(0, 2147483647)


class OSRnd:
    def __init__(self, x):
        pass

    def next(self):
        return int.from_bytes(os.urandom(4), "big") % 10


class FrequencyTest:
    def __init__(self, random_numbers, d):
        self.random_numbers = random_numbers
        self.d = d

    def test(self):
        n = len(self.random_numbers)
        ps = 1 / self.d
        nps = n * ps
        y_list = []
        v = 0
        for i in range(self.d):
            count = 0
            for j in range(n):
                if self.random_numbers[j] == i:
                    count += 1
            y_list.append(count)
            v += pow((y_list[i] - nps), 2) / nps
        return round(v, 4)


class SerialTest:
    def __init__(self, random_numbers, d):
        self.random_numbers = random_numbers
        self.d = d

    def test(self):
        n = len(self.random_numbers)
        k = pow(self.d, 2)
        ps = 1 / k
        nps = n * ps
        v = 0
        v_list = []
        for i in range(self.d):
            for j in range(self.d):
                count = 0
                for l in range(n-1):
                    if self.random_numbers[l] == i and self.random_numbers[l+1] == j:
                        count += 1
                v += pow((count - nps), 2) / nps
        return round(v, 4)


class IntervalTest:
    def __init__(self, random_numbers, d):
        self.random_numbers = random_numbers
        self.d = d
    
    def test(self):
        a = 3
        b = 4
        j = -1
        s = 0
        t = 15
        r = 0
        Vi = 0
        v_list = []
        counter = []
        for _ in range(t+1):
            counter.append(0)
        iter = 0
        for i in range(10000):
            if self.random_numbers[i] == a:
                if r > t:
                    r = 15
                counter[r] += 1
                r = 0
                s += 1
            r += 1
 
        p = b/10 - a/10
        vvv = 0
        for i in range(len(counter)):
            Ps = 0.0
            if i < 15:
                Ps = p * pow(1 - p, i)
            else :
                Ps = pow(1 - p, i)
            c = s * Ps
            a = counter[i] - c
            b = pow(a, 2)
            Vi = b/c
            print(i, " : ", counter[i], " : ", Ps)
            vvv += Ps
        print(vvv)
        return round(Vi, 4)


class CollectorTest:
    def __init__(self, random_numbers, d):
        self.random_numbers = random_numbers
        self.d = d
    
    def test(self):
        st = set()
        collectorCount = 0
        t = 0
        counter = []
        Vi = 0
        for _ in range(21):
            counter.append(0)
        for item in self.random_numbers:
            if  collectorCount == 10:
                break
            st.add(item)
            t += 1
            if len(st) == 10:
                if t > 20:
                    t = 20
                counter[t] += 1
                st.clear()
                t = 0
                collectorCount += 1
        Ps = 0
        for i in range(10,len(counter)):
            if i < 20:
                Ps = (math.factorial(self.d) / pow(self.d , i)) * Stirling(i-1, self.d-1)
            else: 
                Ps = 1 - (math.factorial(self.d) / pow(self.d , i-1)) * Stirling(i-1, self.d)
            Vi += pow(counter[i] - collectorCount * Ps, 2) / (collectorCount * Ps)
        return round(Vi, 4)


def Stirling(a, b):
    if a == b:
        return 1
    elif a == 0 or b == 0 or a < b:
        return 0
    else: 
        return Stirling(a-1, b-1) + b * Stirling(a-1, b)

        
# def random_multi_comparison(x):
#     m = 2147483647
#     a = 65539
#     x = (a * x) % m
#     return x


def run_rng_test(TestMethod, Generator, x, test_count, number_count, number_size):
    result = 0.0
    step_results = []
    random_generator = Generator(x)
    for i in range(test_count):
        random_numbers = []
        for j in range(number_count):
           x = random_generator.next()
           #random_numbers.append(randrange(10))
           random_numbers.append(x % number_size)
    #for j in range(20):
    #    for k in range(50):
    #        print(random_numbers[j + k], end=" ")
    #    print(" ")

        generator_test = TestMethod(random_numbers, number_size)
        step_results.append(generator_test.test())
        result += generator_test.test()
    result = (result / test_count) * 1.0
    return step_results, result, TestMethod, Generator


def save_to_xlsx( rngTestsResults, salaries ):
    print(rngTestsResults)
    if(len(rngTestsResults) > 0 ): 
        TestMethod = rngTestsResults[0][2]
        step_results = rngTestsResults[0][0]

        testCount = ['№']
        for i in range(len(step_results)):
            testCount.append(i+1)

        testCount.append("Avg")

        salar = {str(TestMethod.__name__) : testCount}

        
        for rngTestResult in rngTestsResults:
            step_results = rngTestResult[0]
            result = rngTestResult[1]
            Generator = rngTestResult[3]

            step_results.insert(0, str(Generator.__name__))
            
            step_results.append(round(result, 4))
            salar[str(Generator.__name__)] = step_results

        salaries[str(TestMethod.__name__)] = pd.DataFrame( salar )
            
    return salaries

def create_xlsx(salaries):
    writer = pd.ExcelWriter('./rngTests.xlsx', engine='xlsxwriter')

    for sheet_name in salaries.keys():
        salaries[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()


if __name__ == '__main__':
    x = 65539
    test_count = 30
    number_count = 10000
    number_size = 10

    frequencyTestResults = []
    frequencyTestResults.append(run_rng_test(FrequencyTest, LehmerGenerator, x, test_count, number_count, number_size))
    #frequencyTestResults.append(run_rng_test(FrequencyTest, RndMultiCmpGenerator, x, test_count, number_count, number_size))
    frequencyTestResults.append(run_rng_test(FrequencyTest, BuiltInRnd, x, test_count, number_count, number_size))
    frequencyTestResults.append(run_rng_test(FrequencyTest, OSRnd, x, test_count, number_count, number_size))

    serialTestResults = []
    #serialTestResults.append(run_rng_test(SerialTest, RndMultiCmpGenerator, x, test_count, number_count, number_size))
    serialTestResults.append(run_rng_test(SerialTest, LehmerGenerator, x, test_count, number_count, number_size))
    serialTestResults.append(run_rng_test(FrequencyTest, BuiltInRnd, x, test_count, number_count, number_size))
    serialTestResults.append(run_rng_test(FrequencyTest, OSRnd, x, test_count, number_count, number_size))

    intervalTestResults = []
    #intervalTestResults.append(run_rng_test(IntervalTest, RndMultiCmpGenerator, x, test_count, number_count, number_size))
    intervalTestResults.append(run_rng_test(IntervalTest, LehmerGenerator, x, test_count, number_count, number_size))
    #intervalTestResults.append(run_rng_test(FrequencyTest, BuiltInRnd, x, test_count, number_count, number_size))
    #intervalTestResults.append(run_rng_test(FrequencyTest, OSRnd, x, test_count, number_count, number_size))

    collectorTestResults = []
    #collectorTestResults.append(run_rng_test(CollectorTest, RndMultiCmpGenerator, x, test_count, number_count, number_size))
    collectorTestResults.append(run_rng_test(CollectorTest, LehmerGenerator, x, test_count, number_count, number_size))
    collectorTestResults.append(run_rng_test(FrequencyTest, BuiltInRnd, x, test_count, number_count, number_size))
    collectorTestResults.append(run_rng_test(FrequencyTest, OSRnd, x, test_count, number_count, number_size))

    # rngTestsResults.append(run_rng_test(FrequencyTest, RndMultiCmpGenerator, x, test_count, number_count, number_size))
    # rngTestsResults.append(run_rng_test(SerialTest, RndMultiCmpGenerator, x, test_count, number_count, number_size))
    # rngTestsResults.append(run_rng_test(IntervalTest, RndMultiCmpGenerator, x, test_count, number_count, number_size))
    # rngTestsResults.append(run_rng_test(CollectorTest, RndMultiCmpGenerator, x, test_count, number_count, number_size))

    salaries = {}

    salaries = save_to_xlsx(frequencyTestResults, salaries)
    salaries = save_to_xlsx(serialTestResults, salaries)
    salaries = save_to_xlsx(intervalTestResults, salaries)
    salaries = save_to_xlsx(collectorTestResults, salaries)

    create_xlsx(salaries)

    # lehmer_generator = LehmerGenerator(1)
    # for i in range(30):
    #     print(lehmer_generator.next())

