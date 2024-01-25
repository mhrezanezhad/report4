import graphics
from math import factorial
import copy


class Csps:
    def __init__(self, board, forward_checking=False, pruning_filter=False, mlv_ordering=False):
        self.step = 0
        self.constraint = dict()
        self.unassigned_variables = list()
        self.variable_assignments = dict()
        self.domains = dict()
        self.priorities = dict()
        self.board = board

        self.init_variable()
        self.init_constraint()
        self.init_priorities()

        if forward_checking:
            self.forward_checking()

        elif pruning_filter and mlv_ordering:
            self.backtracking_with_mlv_ordering_and_pruning_filter()

        elif pruning_filter:
            self.backtracking_with_pruning_filter()

        elif mlv_ordering:
            self.backtracking_with_mlv_ordering()

        else:
            self.backtracking()

    def init_variable(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == '':
                    self.unassigned_variables.append((i, j))
                    self.domains[(i, j)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def init_constraint(self):
        horizontal_variables = []
        vertical_variables = []
        horizontal_guide = int()
        vertical_guide = int()
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if '\\' in self.board[i][j]:
                    if self.board[i][j].find('\\') != len(self.board[i][j]) - 1:
                        horizontal_guide = int(self.board[i][j][self.board[i][j].find('\\') + 1:])
                        k = j + 1
                        while k < len(self.board[0]) and ('\\' not in self.board[i][k] and self.board[i][k] != 'X'):
                            horizontal_variables.append((i, k))
                            k += 1

                        for variable in horizontal_variables:
                            temp = horizontal_variables.copy()
                            temp.remove(variable)
                            self.constraint[variable] = [[horizontal_guide, temp]]

                        horizontal_variables = []

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if '\\' in self.board[i][j]:
                    if self.board[i][j].find('\\') != 0:
                        vertical_guide = int(self.board[i][j][:self.board[i][j].find('\\')])
                        k = i + 1
                        while k < len(self.board) and ('\\' not in self.board[k][j] and self.board[k][j] != 'X'):
                            vertical_variables.append((k, j))
                            k += 1

                        for variable in vertical_variables:
                            temp = vertical_variables.copy()
                            temp.remove(variable)
                            self.constraint[variable].append([vertical_guide, temp])
                    vertical_variables = []

    def init_priorities(self):
        for variable in self.unassigned_variables:
            if len(self.constraint[variable][0][1]) != 8:
                middle_of_the_interval = (len(self.constraint[variable][0][1]) + 1) * 5
                horizontal_priority = (abs(middle_of_the_interval - self.constraint[variable][0][0])
                                       / (middle_of_the_interval - sum(range(1, len(self.constraint[variable][0][1]) + 2)))
                                       / factorial(middle_of_the_interval))
            else:
                horizontal_priority = 1 / factorial(9)

            if len(self.constraint[variable][1][1]) != 8:
                middle_of_the_interval = (len(self.constraint[variable][1][1]) + 1) * 5
                vertical_priority = (abs(middle_of_the_interval - self.constraint[variable][1][0])
                                       / (middle_of_the_interval - sum(range(1, len(self.constraint[variable][1][1]) + 2)))
                                       / factorial(middle_of_the_interval))
            else:
                vertical_priority = 1 / factorial(9)

            self.priorities[variable] = max(vertical_priority, horizontal_priority)

    def backtracking(self):
        if len(self.unassigned_variables) == 0:
            return True
        variable = self.unassigned_variables.pop(0)
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for value in domain:
            if self.is_consistent(variable, value):
                self.step += 1
                self.variable_assignments[variable] = value
                graphics.write_number_on_screen(variable, value, self.board, (0, 0, 0))

                result = self.backtracking()
                if result: return result

                self.variable_assignments.pop(variable)
                graphics.write_number_on_screen(variable, value, self.board, (255, 255, 255))

        self.unassigned_variables.insert(0, variable)
        return False

    def forward_checking(self):
        if len(self.unassigned_variables) == 0:
            return True
        variable = self.unassigned_variables.pop(0)

        for value in self.domains[variable]:
            if self.is_consistent(variable, value):
                self.step += 1
                self.variable_assignments[variable] = value

                domain = copy.deepcopy(self.domains)
                self.change_domains(variable, value)

                graphics.write_number_on_screen(variable, value, self.board, (0, 0, 0), )
                result = self.forward_checking()
                if result: return result

                self.domains = domain.copy()
                self.variable_assignments.pop(variable)
                graphics.write_number_on_screen(variable, value, self.board, (255, 255, 255))

        self.unassigned_variables.insert(0, variable)
        return False

    def backtracking_with_pruning_filter(self):
        if len(self.unassigned_variables) == 0:
            return True
        variable = self.unassigned_variables.pop(0)

        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for value in domain:
            if self.is_consistent2(variable, value):
                self.step += 1
                self.variable_assignments[variable] = value

                graphics.write_number_on_screen(variable, value, self.board, (0, 0, 0), )
                result = self.backtracking_with_pruning_filter()
                if result: return result

                self.variable_assignments.pop(variable)
                graphics.write_number_on_screen(variable, value, self.board, (255, 255, 255))

        self.unassigned_variables.insert(0, variable)
        return False

    def backtracking_with_mlv_ordering(self):
        if len(self.unassigned_variables) == 0:
            return True

        variable = max(self.priorities, key=self.priorities.get)
        temp = self.priorities[variable]
        self.priorities.pop(variable)
        self.unassigned_variables.remove(variable)

        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for value in domain:
            if self.is_consistent(variable, value):
                self.step += 1
                self.variable_assignments[variable] = value

                priorities = self.priorities.copy()
                self.change_priorities(variable)

                graphics.write_number_on_screen(variable, value, self.board, (0, 0, 0))
                result = self.backtracking_with_mlv_ordering()
                if result: return result

                self.priorities = priorities.copy()
                self.variable_assignments.pop(variable)
                graphics.write_number_on_screen(variable, value, self.board, (255, 255, 255))

        self.unassigned_variables.insert(0, variable)
        self.priorities[variable] = temp
        return False

    def backtracking_with_mlv_ordering_and_pruning_filter(self):
        if len(self.unassigned_variables) == 0:
            return True

        variable = max(self.priorities, key=self.priorities.get)
        temp = self.priorities[variable]
        self.priorities.pop(variable)
        self.unassigned_variables.remove(variable)

        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for value in domain:
            if self.is_consistent2(variable, value):
                self.step += 1
                self.variable_assignments[variable] = value

                priorities = self.priorities.copy()
                self.change_priorities(variable)

                graphics.write_number_on_screen(variable, value, self.board, (0, 0, 0))
                result = self.backtracking_with_mlv_ordering_and_pruning_filter()
                if result: return result

                self.priorities = priorities.copy()
                self.variable_assignments.pop(variable)
                graphics.write_number_on_screen(variable, value, self.board, (255, 255, 255))

        self.unassigned_variables.insert(0, variable)
        self.priorities[variable] = temp
        return False

    def is_consistent(self, variable, value):
        sum = 0
        for neighbor in self.constraint[variable][0][1]:
            if neighbor not in self.unassigned_variables:
                if self.variable_assignments[neighbor] == value:
                    return False
                sum += self.variable_assignments[neighbor]

        if self.is_last_variable(variable)[0] and sum + value != self.constraint[variable][0][0]:
            return False

        sum = 0
        for neighbor in self.constraint[variable][1][1]:
            if neighbor not in self.unassigned_variables:
                if self.variable_assignments[neighbor] == value:
                    return False
                sum += self.variable_assignments[neighbor]

        if self.is_last_variable(variable)[1] and sum + value != self.constraint[variable][1][0]:
            return False

        return True

    def is_consistent2(self, variable, value):
        summation, count = 0, 0
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        domain.remove(value)
        for neighbor in self.constraint[variable][0][1]:
            if neighbor not in self.unassigned_variables:
                if self.variable_assignments[neighbor] == value:
                    return False

                domain.remove(self.variable_assignments[neighbor])
                summation += self.variable_assignments[neighbor]
                count += 1

        number_of_unassigned_variables = len(self.constraint[variable][0][1]) - count
        domain1 = domain[: number_of_unassigned_variables]

        if number_of_unassigned_variables == 0:
            domain2 = []
        else:
            domain2 = domain[number_of_unassigned_variables * -1:]

        if not (summation + value + sum(domain1) <= self.constraint[variable][0][0] <= summation + value + sum(domain2)):
            return False

        summation, count = 0, 0
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for neighbor in self.constraint[variable][1][1]:
            if neighbor not in self.unassigned_variables:
                if self.variable_assignments[neighbor] == value:
                    return False
                domain.remove(self.variable_assignments[neighbor])
                summation += self.variable_assignments[neighbor]
                count += 1

        number_of_unassigned_variables = len(self.constraint[variable][1][1]) - count
        domain1 = domain[: number_of_unassigned_variables]
        if number_of_unassigned_variables == 0:
            domain2 = []
        else:
            domain2 = domain[number_of_unassigned_variables * -1:]

        if not (summation + value + sum(domain1) <= self.constraint[variable][1][0] <= summation + value + sum(domain2)):
            return False

        return True

    def is_last_variable(self, variable):
        result = []
        temp = True
        for neighbor in self.constraint[variable][0][1]:
            if neighbor in self.unassigned_variables:
                temp = False

        result.append(temp)

        temp = True
        for neighbor in self.constraint[variable][1][1]:
            if neighbor in self.unassigned_variables:
                temp = False

        result.append(temp)

        return result

    def change_domains(self, variable, value):
        for neighbor in self.constraint[variable][0][1]:
            if neighbor in self.unassigned_variables and value in self.domains[neighbor]:
                self.domains[neighbor].remove(value)

        for neighbor in self.constraint[variable][1][1]:
            if neighbor in self.unassigned_variables and value in self.domains[neighbor]:
                self.domains[neighbor].remove(value)

    def change_priorities(self, variable):
        count = 0
        for neighbor in self.constraint[variable][0][1]:
            if neighbor in self.unassigned_variables:
                count += 1


        for neighbor in self.constraint[variable][0][1]:
            if neighbor in self.unassigned_variables:
                self.priorities[neighbor] = max(self.priorities[neighbor],
                                                (abs(count * 5 - (self.constraint[variable][0][0]))
                                                 / (count * 5 - sum(range(1, count + 1)))
                                                 / factorial(count)))

        count = 0
        for neighbor in self.constraint[variable][1][1]:
            if neighbor in self.unassigned_variables:
                count += 1

        for neighbor in self.constraint[variable][1][1]:
            if neighbor in self.unassigned_variables:
                self.priorities[neighbor] = max(self.priorities[neighbor],
                                                (abs(count * 5 - (self.constraint[variable][1][0]))
                                                 / (count * 5 - sum(range(1, count + 1)))
                                                 / factorial(count)))
