import math
import random
import pandas as pd

class LehmerGenerator:
    def __init__(self, seed):
        if seed <= 0 or seed == 2147483647:
            raise Exception('Поменяйте seed!')
        self.seed = seed
        self.a = 16807
        self.m = 2147483647
        self.q = 127773
        self.r = 2836

    def next(self):
        hi = self.seed / self.q
        lo = self.seed % self.q
        self.seed = (self.a * lo) - (self.r * hi)
        if self.seed <= 0:
            self.seed = self.seed + self.m
        return int(self.seed / self.m)


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
        return v

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
        return v

class GapTest:
    def __init__(self, random_numbers, d):
        self.random_numbers = random_numbers
        self.d = d
    
    def test(self):
        a = 3
        b = 4
        j = -1
        n = 1000
        s = 0 
        t = 20
        r = 0
        Vi = 0
        v_list = []
        counter = []
        for _ in range(t+1):
            counter.append(0)
        iter = 0
        # while s != n and j<999:
        #     r = 0
        #     j += 1
        #     while self.random_numbers[j] < a and self.random_numbers[j] < b:
        #         j += 1
        #         r += 1
        #         if j >= 999:
        #             break
        #     if r >= t:
        #         counter[t] += 1
        #     else:
        #         counter[r] += 1
        #     s += 1;
        for i in range(1000):
            if s == 50:
                break
            r += 1
            if self.random_numbers[i] >= a and self.random_numbers[i] < b:
                if (r-1) > t:
                    r = 20
                counter[r-1] += 1
                r = 0
                s += 1
 
        p = b/10 -a/10
        for i in range(len(counter)):
            Ps = 0.0
            if i < 20:
                Ps = p * pow(1 - p, i)
            else :
                Ps = pow(1 - p, i)
            # Vi += pow(counter[i] - s * Ps, 2) / (s* Ps)
            c = s * Ps
            a = counter[i] - c
            b = pow(a, 2)
            Vi = b/c
        return Vi
                    
class KollekcionerTest:
    def __init__(self, random_numbers, d):
        self.random_numbers = random_numbers
        self.d = d
    
    def test(self):
        st = set()
        kollecionerCount = 0
        t = 0
        counter = []
        Vi = 0
        for _ in range(21):
            counter.append(0)
        for item in self.random_numbers:
            if  kollecionerCount == 10:
                break
            st.add(item)
            t += 1
            if len(st) == 10:
                if t > 20:
                    t = 20
                counter[t] += 1
                st.clear()
                t = 0
                kollecionerCount += 1
        Ps = 0
        for i in range(10,len(counter)):
            if i < 20:
                Ps = (math.factorial(self.d) / pow(self.d , i)) * Stirling(i-1, self.d-1)
            else: 
                Ps = 1 - (math.factorial(self.d) / pow(self.d , i-1)) * Stirling(i-1, self.d)
            Vi += pow(counter[i] - kollecionerCount * Ps, 2) / (kollecionerCount * Ps)
        return Vi


def Stirling (a,b):
    if a == b:
        return 1
    elif a == 0 or b == 0 or a < b:
        return 0
    else: 
        return Stirling(a-1,b-1) + b * Stirling(a-1, b)

        
def random_multi_comparison(x):
    m = 2147483647
    a = 65539
    x = (a * x) % m
    return x


def run_rng_test(TestMethod, x, test_count, number_count, number_size):
    result = 0
    step_results = []
    for i in range(test_count):
        random_numbers = []
        for j in range(number_count):
           x = random_multi_comparison(x)
           #random_numbers.append(randrange(10))
           random_numbers.append(x % number_size)
        generator_test = TestMethod(random_numbers, number_size)
        step_results.append(str(generator_test.test()))
        result += generator_test.test()
    result = result / test_count
    return step_results, result, TestMethod

def saveToXml( rngTestsResults ):
    print(rngTestsResults)

    salaries = {}
    
    for rngTestResult in rngTestsResults:
        step_results = rngTestResult[0]
        result = rngTestResult[1]
        TestMethod = rngTestResult[2]

        testCount = ['№']
        for i in range(len(step_results)):
            testCount.append(i+1)

        step_results.insert(0, "Хуй знает")

        testCount.append("Avg")
        step_results.append(result)

        salaries[str(TestMethod.__name__)] = pd.DataFrame( { str(TestMethod.__name__) : testCount, "" : step_results })
        
    writer = pd.ExcelWriter('./rngTests.xlsx', engine='xlsxwriter')

    for sheet_name in salaries.keys():
        salaries[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()


if __name__ == '__main__':
    x = 65539
    test_count = 30
    number_count = 1000
    number_size = 10

    rngTestsResults = []
    
    rngTestsResults.append(run_rng_test(FrequencyTest, x, test_count, number_count, number_size))
    rngTestsResults.append(run_rng_test(SerialTest, x, test_count, number_count, number_size))
    rngTestsResults.append(run_rng_test(GapTest, x, test_count, number_count, number_size))
    rngTestsResults.append(run_rng_test(KollekcionerTest, x, test_count, number_count, number_size))

    saveToXml(rngTestsResults)
    
    # lehmer_generator = LehmerGenerator(1)
    # for i in range(30):
    #     print(lehmer_generator.next())

