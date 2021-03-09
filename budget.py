import re
import math


class Category:

    # constructor sets the budget category
    def __init__(self, cat):
        self.name = cat
        self.ledger = []

    def __str__(self):
        output = ""
        # first the title bar
        # need 30 chars so number of stars is 30 minus the name
        stars = 30 - len(self.name)
        # find the middle, add 0.5 if it's an odd numbered name
        middle = stars / 2

        # now loop through adding *s and the cat name
        if len(self.name) % 2 != 0:
            middle += 0.5
            extra = True
        while stars > 0:
            if stars == middle:
                output += self.name
            else:
                output += "*"
            stars -= 1

        output += "*\n"

        # now loop through the ledger adding each entry
        for item in self.ledger:
            # set strdesc
            strdesc = item["description"][:23]

            # add the desc
            output += strdesc

            # set any spaces requried
            spaces = 23-len(strdesc)

            # add any spaces required
            while spaces > 0:
                output += " "
                spaces -= 1

            # get the amount as a string (and only 7 chars due to to fcc req) converting to float too
            floatamount = float(item["amount"])
            stramount = str(floatamount)

            # add an extra leading zero as required
            if re.search("\.\d$", stramount):
                stramount += "0"

            # loop through and add any spaces required
            spaces = 7 - len(stramount)
            while spaces > 0:
                output += " "
                spaces -= 1

            # now add the amount
            output += stramount

            output += "\n"

        # finally adding the the total line
        total = self.get_balance()
        total = str(float(total))  # change to float then string
        if re.search("\.\d$", total):  # add leading zero as required
            total += "0"
        output += "Total: "+total

        return output

    # function to deposit an amount into the list variable

    def deposit(self, amount, description=""):
        self.ledger.append({
            "amount": amount,
            "description": description,
        })

    # function to add a withdrawal to the ledger, will return false and do nothing if there is not enough money
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": -amount,
                "description": description,
            })
            return True
        else:
            return False

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
            return True
        else:
            return False

    # function to check whether an amount will use up the remaining budget
    def check_funds(self, amount):
        balance = self.get_balance()
        if amount > balance:
            return False
        else:
            return True

    def get_withdrawals(self):
        withdrawals = 0
        for el in self.ledger:
            if el["amount"] < 0:
                # subtract the minus to make positive
                withdrawals -= el["amount"]
        return withdrawals


def create_spend_chart(categories):
    output = "Percentage spent by category\n"

    # first calc percentages
    withdrawals = []
    for category in categories:
        withdrawals.append(category.get_withdrawals())

    # calc total
    sum = 0
    for balance in withdrawals:
        sum += balance

    # calc perecents
    withdrawalperc = []
    for balance in withdrawals:
        # balance over sum to get %, then multiply 10 so we can floor (have to always round down), then by 10 again
        withdrawalperc.append(math.floor((balance/sum)*10)*10)

    # now loop through 100-0
    loop = 100
    while loop >= 0:
        strloop = str(loop)
        # need to add spaces to right alignn the numbers
        spaces = 3 - len(strloop)

        while spaces > 0:
            output += " "
            spaces -= 1

        output += strloop + "| "

        # loop through percentages
        for perc in withdrawalperc:
            if perc >= loop:
                output += "o  "
            else:
                output += "   "

        output += "\n"

        loop -= 10

    # add the dashes before the cat names
    output += "    ----------\n"

    # first get the longest cat name so we know the number of times to loop
    maxcat = 0
    for category in categories:
        name = category.name
        if len(name) > maxcat:
            maxcat = len(name)

    # now loop through each line, determined by max cat length
    i = 0
    while maxcat > i:
        # add the initial empty space
        output += "     "

        # loop through each category
        for category in categories:
            char = category.name[i:i + 1]
            if char == "":  # if we're past the end of the category name we still need to add an empty space
                char = " "
            output += char+"  "

        i += 1

        output += "\n"

    # get rid of last newline
    output=output[:len(output)-1]

    return output