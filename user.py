# define user class 

class User:
    def __init__(self, age, gender, total_income, expenses ):
        self.age = age
        self.gender = gender
        self.total_income = total_income
        self.expenses = expenses

    def __repr__(self):
        return f"User(age={self.age}, gender='{self.gender}', total_income={self.total_income}, expenses='{self.expenses})"
