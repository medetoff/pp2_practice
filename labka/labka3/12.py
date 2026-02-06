class Employee:
    def __init__(self,name,base_salary):
        self.name=name
        self.base_salary=base_salary
    def total_salary(self):
        return float(self.base_salary)
class Manager(Employee):
    def __init__(self,name,base_salary,bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent=bonus_percent
    def total_salary(self):
        return self.base_salary*(1+self.bonus_percent/100)
class Developer(Employee):
    def __init__(self,name,base_salary,completed_projects):
        super().__init__(name,base_salary)
        self.completed_projects=completed_projects
    def total_salary(self):
        return self.base_salary+self.completed_projects*500
class Intern(Employee):
    pass

d=input().split()
r=d[0]
if r=="Manager":
    name=d[1]
    base_salary=int(d[2])
    bonus_percent=int(d[3])
    e=Manager(name,base_salary,bonus_percent)
elif r=="Developer":
    name=d[1]
    base_salary=int(d[2])
    completed_projects=int(d[3])
    e=Developer(name, base_salary, completed_projects)
elif r=="Intern":
    name=d[1]
    base_salary=int(d[2])
    e=Intern(name, base_salary)
t=e.total_salary()
print(f"Name: {e.name}, Total: {t:.2f}")