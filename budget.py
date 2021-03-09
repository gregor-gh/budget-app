class Category:

    name = ""
    ledger = []

    # constructor sets the budget category
    def __init__(self, cat):
        self.name = cat


            
        


    # function to deposit an amount into the list variable
    def deposit(self, amount, description=""):
        self.ledger.append({
            "amount": amount,
            "description": description,
        })

    # function to add a withdrawal to the ledger, will return false and do nothing if there is not enough money
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            return False
        else:
            self.ledger.append({
                "amount": -amount,
                "description": description,
            })
            return True

    def get_balance(self):
        balance = 0
        for el in self.ledger:
            balance += el["amount"]
        return balance

    def transfer(self, amount, cat):
        # first check we have nough money to transfer
        if self.check_funds(amount):
            # withdraw from this cat
            self.withdraw(amount, "Transfer to " + cat.name)
            # deposit into other cat
            cat.deposit(amount, "Transfer from " + self.name)

    # function to check whether an amount will use up the remaining budget
    def check_funds(self, amount):
        if amount < self.get_balance():
            return False
        else:
            return True


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)
print(food)
print(clothing)

# def create_spend_chart(categories):
