class Payslips:
    def __init__(self, name, payment, amount) -> None:
        
        self.name = name
        self.payment = payment
        self.amount = amount

    def pay(self):
        self.payment = "yes"

    def status(self):
        
        if self.payment == "yes":
            return self.name+ " is paid " + str(self.amount)
        
        else:
            return self.name+ " is not paid "
        
noman = Payslips('Nouman','no',13000)
ali = Payslips('Ali','no',20000)

ali.pay()

print(noman.status(), "\n", ali.status())