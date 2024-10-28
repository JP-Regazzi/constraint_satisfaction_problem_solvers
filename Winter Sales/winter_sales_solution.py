"""

The person who bought the TV is Joey.


Name:João Pedro
Surname: REGAZZI FERREIRA DA SILVA
Email: joao-pedro.regazzi-ferreira-da-silva@student-cs.fr


Description:
This code solves a logic puzzle involving students with various attributes
(name, shirt color, age, juice preference, discount received, and item bought)
placed in ordered positions. The constraints enforce unique attributes for each
student and relative conditions (e.g., "Rachel is 25 years old" or "The student
with a black T-shirt is to the right of Rachel").

To solve this, the code uses Python's constraint library to define the problem and
apply constraints for each attribute and their relations. It ensures each constraint
is met across all positions to find a unique solution that matches all specified conditions.
If a unique solution exists, it outputs the name of the student who bought the TV.


Usage:
To run this script, ensure Python is installed with the constraint module available.
Execute the script from the command line using:
python ./winter_sales_solution.py

"""


from constraint import Problem, AllDifferentConstraint

# Define the problem and positions
problem = Problem()
positions = [1, 2, 3, 4, 5]

# Possible attributes
names = ["Joey", "Ross", "Monica", "Rachel", "Phoebe"]
colors = ["black", "blue", "green", "red", "white"]
ages = [21, 22, 23, 24, 25]
juices = ["apple", "peach", "grape", "lemon", "orange"]
discounts = [40, 50, 60, 70, 80]
items = ["razor", "console", "computer", "smartphone", "TV"]

# Add variables for each position and attribute
for position in positions:
    problem.addVariable(('name', position), names)
    problem.addVariable(('color', position), colors)
    problem.addVariable(('age', position), ages)
    problem.addVariable(('juice', position), juices)
    problem.addVariable(('discount', position), discounts)
    problem.addVariable(('item', position), items)

# Define variables for each position and attribute
for attribute in ['name', 'color', 'age', 'juice', 'discount', 'item']:
    problem.addConstraint(AllDifferentConstraint(), [ (attribute, position) for position in positions ])

# Constraint 1: Orange juice is immediately to the right of 70% discount
for p in positions:
    if p == 1:
        problem.addConstraint(lambda juice_p: juice_p != 'orange', [('juice', p)])
    else:
        problem.addConstraint(
            lambda juice_p, discount_p_minus1: (juice_p != 'orange') or (discount_p_minus1 == 70),
            [('juice', p), ('discount', p - 1)]
        )

# Constraint 2: Rachel is 25 years old.
for p in positions:
    problem.addConstraint(
        lambda name_p, age_p: (name_p != 'Rachel') or (age_p == 25),
        [('name', p), ('age', p)]
    )

# Constraint 3: The student who bought a TV is immediately to the left of the student wearing a red T-shirt
for p in positions:
    if p == 5:
        problem.addConstraint(lambda item_p: item_p != 'TV', [('item', p)])
    else:
        problem.addConstraint(
            lambda item_p, color_p_plus1: (item_p != 'TV') or (color_p_plus1 == 'red'),
            [('item', p), ('color', p + 1)]
        )

# Constraint 4: The student in the middle obtained a 50% discount
problem.addConstraint(lambda discount_p: discount_p == 50, [('discount', 3)])

# Constraint 5: Rachel is next to the student wearing a white T-shirt
for p in positions:
    neighbors = []
    if p > 1:
        neighbors.append(('color', p - 1))
    if p < 5:
        neighbors.append(('color', p + 1))
    if neighbors:
        def constraint(name_p, *neighbor_colors):
            if name_p != 'Rachel':
                return True
            return 'white' in neighbor_colors
        problem.addConstraint(constraint, [('name', p)] + neighbors)

# Constraint 6: The student who is 21 years old is somewhere between the student who is 23 and the student who is 24
def constraint6(*ages):
    age_pos = {}
    for idx, age in enumerate(ages):
        age_pos[age] = positions[idx]
    if 23 in age_pos and 21 in age_pos and 24 in age_pos:
        return age_pos[23] < age_pos[21] < age_pos[24]
    else:
        return False
problem.addConstraint(constraint6, [('age', p) for p in positions])

# Constraint 7: The student who drank apple juice bought a smartphone
for p in positions:
    problem.addConstraint(
        lambda juice_p, item_p: (juice_p != 'apple') or (item_p == 'smartphone'),
        [('juice', p), ('item', p)]
    )

# Constraint 8: The student who is 22 is immediately to the left of the student who bought the razor
for p in positions:
    if p == 5:
        problem.addConstraint(lambda age_p: age_p != 22, [('age', p)])
    else:
        problem.addConstraint(
            lambda age_p, item_p_plus1: (age_p != 22) or (item_p_plus1 == 'razor'),
            [('age', p), ('item', p + 1)]
        )

# Constraint 9: Phoebe is the youngest
for p in positions:
    problem.addConstraint(
        lambda name_p, age_p: (name_p != 'Phoebe') or (age_p == 21),
        [('name', p), ('age', p)]
    )

# Constraint 10: The student who got a 40% discount is exactly to the right of the student who bought the razor
for p in positions:
    if p == 1:
        problem.addConstraint(lambda discount_p: discount_p != 40, [('discount', p)])
    else:
        problem.addConstraint(
            lambda discount_p, item_p_minus1: (discount_p != 40) or (item_p_minus1 == 'razor'),
            [('discount', p), ('item', p - 1)]
        )

# Constraint 11: Ross is 24 years old
for p in positions:
    problem.addConstraint(
        lambda name_p, age_p: (name_p != 'Ross') or (age_p == 24),
        [('name', p), ('age', p)]
    )

# Constraint 12: Phoebe wore a black T-shirt
for p in positions:
    problem.addConstraint(
        lambda name_p, color_p: (name_p != 'Phoebe') or (color_p == 'black'),
        [('name', p), ('color', p)]
    )

# Constraint 13: The penultimate student got the biggest discount
problem.addConstraint(lambda discount_p: discount_p == 80, [('discount', 4)])

# Constraint 14: Joey got a 60% discount
for p in positions:
    problem.addConstraint(
        lambda name_p, discount_p: (name_p != 'Joey') or (discount_p == 60),
        [('name', p), ('discount', p)]
    )

# Constraint 15: The student who was drinking lemon juice is exactly to the right of the student who was drinking grape juice
for p in positions:
    if p == 1:
        problem.addConstraint(lambda juice_p: juice_p != 'lemon', [('juice', p)])
    else:
        problem.addConstraint(
            lambda juice_p, juice_p_minus1: (juice_p != 'lemon') or (juice_p_minus1 == 'grape'),
            [('juice', p), ('juice', p - 1)]
        )

# Constraint 16: Rachel bought a game console
for p in positions:
    problem.addConstraint(
        lambda name_p, item_p: (name_p != 'Rachel') or (item_p == 'console'),
        [('name', p), ('item', p)]
    )

# Constraint 17: The student who got an 80% discount is exactly to the left of the student wearing a blue T-shirt
for p in positions:
    if p == 5:
        problem.addConstraint(lambda discount_p: discount_p != 80, [('discount', p)])
    else:
        problem.addConstraint(
            lambda discount_p, color_p_plus1: (discount_p != 80) or (color_p_plus1 == 'blue'),
            [('discount', p), ('color', p + 1)]
        )

# Constraint 18: The student who was drinking grape juice bought an electric razor
for p in positions:
    problem.addConstraint(
        lambda juice_p, item_p: (juice_p != 'grape') or (item_p == 'razor'),
        [('juice', p), ('item', p)]
    )

# Constraint 19: The student wearing a black T-shirt is somewhere to the right of Rachel
def constraint19(*args):
    name_positions = args[:5]
    color_positions = args[5:]
    pos_rachel = None
    pos_black = None
    for idx, name in enumerate(name_positions):
        if name == 'Rachel':
            pos_rachel = positions[idx]
    for idx, color in enumerate(color_positions):
        if color == 'black':
            pos_black = positions[idx]
    if pos_rachel and pos_black:
        return pos_black > pos_rachel
    else:
        return False
problem.addConstraint(constraint19, [('name', p) for p in positions] + [('color', p) for p in positions])

# Constraint 20: The student who bought the smartphone is next to the student wearing a black T-shirt
for p in positions:
    neighbors = []
    if p > 1:
        neighbors.append(('color', p - 1))
    if p < 5:
        neighbors.append(('color', p + 1))
    if neighbors:
        def constraint(item_p, *neighbor_colors):
            if item_p != 'smartphone':
                return True
            return 'black' in neighbor_colors
        problem.addConstraint(constraint, [('item', p)] + neighbors)

# Solve the problem
solutions = problem.getSolutions()

# Check if there is only one solution
if len(solutions) == 1:
    solution = solutions[0]
    # Find who bought the TV
    for position in positions:
        if solution[('item', position)] == 'TV':
            buyer = solution[('name', position)]
            print(f"The person who bought the TV is {buyer}.")
else:
    print("No unique solution found.")
