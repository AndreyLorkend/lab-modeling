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
        step_results.append(generator_test.test())
        result += generator_test.test()
    result = result / test_count
    return step_results, result

if __name__ == '__main__':
    x = 65539
    test_count = 30
    number_count = 1000
    number_size = 10

    
    print(run_rng_test(FrequencyTest, x, test_count, number_count, number_size))
    print(run_rng_test(SerialTest, x, test_count, number_count, number_size))
    
    # lehmer_generator = LehmerGenerator(1)
    # for i in range(30):
    #     print(lehmer_generator.next())

