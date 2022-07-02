from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils.timezone import now


ADD_EXPENSE_CHOICES = [
     ("Expense","Expense"),
     ("Income","Income")
 ]


class User(AbstractUser):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)


class Wallet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wallet_name = models.CharField(max_length=30)
    wallet_amount = models.BigIntegerField()
    budget = models.BigIntegerField() 
    amount_left = models.BigIntegerField()
    
    def __str__(self):
        return self.wallet_name

    # def __str__(self):
    #     return "{0} {1}".format(self.wallet_amount,self.budget)
    

class Add_transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,null=True)
    add_money = models.CharField(max_length = 10 , choices = ADD_EXPENSE_CHOICES )
    category = models.CharField(max_length=30)
    amount = models.BigIntegerField()
    Date = models.DateField(default = now)
    description = models.CharField(max_length=200,null=True)




    
