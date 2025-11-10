class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f'Person {name} created.')
        
    def introduce(self):
        print(f'Name: {self.name}')
        print(f'Age: {self.age}')
        
p = Person('Bob', 30)
p.introduce()