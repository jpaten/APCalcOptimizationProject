import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics

class President:
    def __init__(self,source, degree, x_space, cap):
        f=open(source,"r")
        self.name = source.split(".")[0]
        self.x=[]
        self.y=[]
        earliest = 0
        try:
            cap = int(cap)
        except:
            pass
        f.readline()
        while True:
            line = f.readline()
            if not cap:
                cap = int(line.split(",")[0])
            cells = line.split(",")
            if line:
                if int(cells[0]) >= cap:
                    continue
                self.x.append(int(cells[0]))
                self.y.append(int(cells[1]))
                earliest = int(cells[0])
            else:
                break
        f.close()
        self.regression = np.polyfit(self.x,self.y,degree)
        print(len(x_space))

        def polynomial_calc(p,x):
            """
            Returns the result of polynomial p, a list where the 0th element is the highest degree coefficient, the 1st the
            second highest degree, and so on, at x
            >>> polynomial_calc([2,1,2,3],2)
            27
            """
            output = 0
            exponent = len(p) - 1
            for i in p:
                if exponent:
                    output += i * (x ** exponent)
                else:
                    output += i
                exponent -= 1
            return output

        def power_rule(p):
            """Takes in a polynomial in the form of a list and applies the power rule to return the derivative
            as a list.
            >>> power_rule([4,2,3])
            [8, 2]
            >>> power_rule([1,2,3,4,5])
            [4, 6, 6, 4]
            >>> power_rule([1.6,3.2,5])
            [3.2, 3.2]
            """
            output = []
            multiplier = len(p)-1
            for i in p:
                output.append(i*multiplier)
                multiplier -= 1
            output.pop(len(output)-1)
            return output

        self.regression_y = []
        self.derivative_y = []
        self.second_derivative_y = []
        self.predicted_y = []
        self.derivative = power_rule(self.regression)
        self.second_derivative = power_rule(self.derivative)
        print(self.derivative)
        #print(derivative_y[1])
        print(self.regression)
        for i in x_space:
            self.regression_y.append(polynomial_calc(self.regression,i))
        for i in x_space:
            self.derivative_y.append(polynomial_calc(power_rule(list(self.regression)),i))
        for i in x_space:
            self.second_derivative_y.append(polynomial_calc(power_rule(power_rule(list(self.regression))), i))
        print(self.x)
        for i in self.x:
            self.predicted_y.append(polynomial_calc(self.regression,i))
        self.days = x_space
        self.maxima = {}
        self.minima = {}
        # Find local extrema
        for i in range(len(self.derivative_y)):
            if -0.0005 < self.derivative_y[i] < 0.0005:
                if not -0.00005 < self.second_derivative_y[i]<0.00005:
                    if self.second_derivative_y[i] < 0:
                        self.maxima[x_space[i]] = self.regression_y[i]
                    elif self.second_derivative_y[i] > 0:
                        self.minima[x_space[i]] = self.regression_y[i]
        def distance_filter(extrema, extrema_type, distance = 5):
            """
            Filters out duplicates of the same extreme value. Type must be max or min.
            """
            assert extrema_type == "max" or extrema_type == "min"
            extrema_x = list(extrema.keys())
            extrema_y = list(extrema.values())
            output = extrema
            for i in range(len(extrema)):
                try:
                    if np.absolute(extrema_x[i]-extrema_x[i-1]) < distance:
                        if extrema_type == "max":
                            if extrema_y[i] > extrema_y[i - 1]:
                                output.pop(extrema_x[i])
                            else:
                                output.pop(extrema_x[i-1])
                        elif extrema_type == "min":
                            if extrema_y[i] < extrema_y[i-1]:
                                output.pop(extrema_x[i])
                            else:
                                output.pop(extrema_x[i-1])
                except KeyError:
                    pass
            return output
        self.maxima = distance_filter(self.maxima, "max")
        self.minima = distance_filter(self.minima, "min")


def write_poly(polynomial, split_point=0):
    equation = ""
    exponent = len(polynomial) - 1
    x_var = "x"
    for i in polynomial:
        j = str(i).split("e")
        coefficient = "%.4f" % float(j[0])
        try:
            ten_value = "* 10^" + "{" + str(j[1]) + "}"
        except IndexError:
            ten_value = ""
        operator = "+"
        if coefficient[0] == "-":
            operator = "-"
        full_coefficient = operator + str(coefficient).split("-")[len(str(coefficient).split("-")) - 1] + ten_value
        if exponent > 1:
            equation += full_coefficient + "*" + x_var + "^" + str(exponent)
        elif exponent == 1:
            equation += full_coefficient + x_var
        else:
            equation += full_coefficient
        if split_point:
            if exponent == split_point:
                equation += "$ \n $"
        exponent -= 1
    return "$" + equation[1:] + "$"

cap = 2922/2
days = np.linspace(5, cap,cap*10)
obama = President("Obama.csv", 9, days, cap)
bush = President("Bush.csv", 9, days, cap)
clinton = President("Clinton.csv", 9, days, cap)
hwbush = President("HWBush.csv", 9, days, cap)
reagan = President("Reagan.csv",9,days,cap)
def plot(days, *presidents):
    colors = ["b","g","r","c","m","y","k"]
    linked_presidents = {}
    counter = 0
    for i in presidents:
        linked_presidents[i] = colors[counter]
        counter += 1
    print(linked_presidents)
    counter = 0
    fig = plt.figure()
    plt.subplot(2,2,1)
    for i in presidents:
        plt.plot(i.x,i.y,"o", color=linked_presidents[i])
    for i in presidents:
        plt.plot(days, i.regression_y, color=linked_presidents[i])
    for i in presidents:
        plt.plot(list(i.minima.keys()), list(i.minima.values()), "o", color=linked_presidents[i])
        plt.plot(list(i.maxima.keys()), list(i.maxima.values()), "o", color=linked_presidents[i])
    plt.xlabel("Time since inauguration (days)\n\n")
    plt.ylabel(r"Net approval rating (percent)")
    plt.title("Net approval rating over time")
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.xlabel("Time since inauguration (days)")
    plt.ylabel("Net approval rating per time (percent/days)")
    plt.title("First derivatives of net approval rating over time")
    plt.grid(True)
    for i in presidents:
        plt.plot(days, i.derivative_y, color=linked_presidents[i])

    plt.subplot(2, 2, 3)
    plt.xlabel("Time since inauguration (days)\n")
    plt.ylabel("Net approval rating per time (percent/days$^{2}$)")
    plt.title("Second derivatives of net approval rating over time")
    for i in presidents:
        plt.plot(days, i.second_derivative_y, color=linked_presidents[i])
    y = 0.45
    for i in linked_presidents:
        plt.text(0.5,y,i.name,color=linked_presidents[i],transform=plt.gcf().transFigure)
        y-=0.03

    plt.show()


plot(days, obama, bush, clinton, hwbush, reagan)
