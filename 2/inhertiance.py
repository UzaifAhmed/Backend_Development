class Employees:
    def __init__(self, name, last) -> None:
        
        self.name = name
        self.last = last

class Supervisors(Employees):
    def __init__(self, name, last, password) -> None:
        super().__init__(name, last)
        self.password = password

class Chefs(Employees):
    def leave_request(self, days):
        
        return "May I take a leave for " +str(days)+ " days"
    

adam = Supervisors('Adam', 'A', "asgf2#B1")

bilqees = Chefs("Bilqees", 'B')
tariq = Chefs('Tariq','T')


print(adam.password)
print(tariq.leave_request(3))
print(bilqees.name)

#   Built-in functions
#   issubclass()    and    isinstance()

print(issubclass(Supervisors,Employees))
#               Derived class, Base class  
print(issubclass(Employees,Supervisors))

print(isinstance(tariq,Chefs))
print(isinstance(adam,Employees))