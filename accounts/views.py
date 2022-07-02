from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,get_user_model, update_session_auth_hash
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from django.db.models import Sum
from django.http import JsonResponse


def dashboard(request):
    return render(request,'base.html')

def index(request):
    return render(request,'index.html')

def signup(request):
    user = get_user_model()
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        if user.objects.filter(email=email).exists():
            messages.info(request,'Email already exists!!')
            return redirect('signup')
        else:
            user = user.objects.create_user(username=username, name=name, email=email,phone=phone,password=password )
            user.save()
            print("User created")
            messages.info(request,'Account created successfully')
            return redirect('login')
    else:
        return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request,username=username, password=password)
        print('USER:',user)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'Logged in successfully')
            return redirect('index')
        else:
            messages.info(request,'Invalid Username or Password!!')
            return redirect('login')

    else:
        return render(request,'login.html')
    

def logout(request):
    auth.logout(request)
    return redirect('login')


def wallet(request):

    if request.method == "GET":
        return render(request,'wallet.html')

    if Wallet.objects.filter(user_id=request.user.id).count()==1:
        messages.info(request,"You already have a wallet, you can only manage one wallet at a time")
    else:    
        if request.method == "POST":
            user_id = request.user.id 
            wallet_name = request.POST['wallet_name']
            wallet_amount = request.POST['wallet_amount']
            budget = request.POST['budget']
            add1 = Wallet.objects.create(user_id = user_id, wallet_name= wallet_name,wallet_amount=wallet_amount, budget=budget, amount_left =budget)
            add1.save()
            messages.info(request,"Wallet added successfully")
            # return render(request,'wallet.html')
            return redirect('transaction')

    return redirect('wallet')


def transaction(request):
    user_id = request.user.id 
    # wallet1 = Wallet.objects.all().get(user_id)
    wallet1 = Wallet.objects.filter(user_id=request.user.id)
    if not Wallet.objects.filter(user_id=request.user.id).exists():
        messages.info(request,"Add a wallet first")
        return redirect('wallet')
   
    context = {
        'wallet1' : wallet1,
        'values' : request.POST
    }

   

    return render(request,'transaction.html',context)
    


def transaction_submit(request):

    if request.method == "POST":
        user_id = request.user.id 
        wallet_name = request.POST['wallet_name']
        add_money = request.POST["add_money"]
        category = request.POST["category"]
        amount = request.POST["amount"]
        Date = request.POST["Date"]
        description = request.POST["description"]
        wallet_id = Wallet.objects.filter(wallet_name=wallet_name).first()
        print("-------------------------------", add_money)
        if (add_money == "Expense" and wallet_id.amount_left >= int(amount)):
            print("-------------------------------", wallet_id.budget)
            wallet_id.amount_left -= int(amount)
            add = Add_transaction.objects.create(user_id = user_id, wallet=wallet_id, add_money=add_money, category=category, amount=amount, Date=Date, description=description)
            add.save()
            wallet_id.save()
        elif(add_money == "Income"):
            add = Add_transaction.objects.create(user_id = user_id, wallet=wallet_id, add_money=add_money, category=category, amount=amount, Date=Date, description=description)
            add.save()
        else:
            messages.warning(request,'Your expenses exceeded your budget')
            return redirect('index')

    return redirect('index')


def history(request):
    history = Add_transaction.objects.filter(user_id=request.user.id)
    context = {
        'history' : history,
        'values' : request.POST
    }
    return render(request,'history.html',context)





def expense_week(request):
    User = get_user_model()
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    user_id = request.user.id
    user1 = User.objects.get(id=user_id)
    addmoney = Add_transaction.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.category
    Category_list = list(set(map(get_Category,addmoney)))


    def get_expense_category_amount(category,add_money):
        amount = 0 
        filtered_by_category = addmoney.filter(category = category,add_money="Expense") 
        for item in filtered_by_category:
            amount+=item.amount
        return amount

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)







def weekly(request):
    User = get_user_model()
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    user_id = request.user.id 
    user1 = User.objects.get(id=user_id)
    addmoney_info =Add_transaction.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    sum = 0 
    for i in addmoney_info:
        if i.add_money == 'Expense':
            sum=sum+i.amount
    addmoney_info.sum = sum
    sum1 = 0 
    for i in addmoney_info:
        if i.add_money == 'Income':
            sum1 =sum1+i.amount
    addmoney_info.sum1 = sum1
    # x= Wallet.budget+addmoney_info.sum1  - addmoney_info.sum
    # y= Wallet.budget+addmoney_info.sum1 - addmoney_info.sum

    week = Wallet.objects.filter(user=user_id).first()
    print("-------------------------------", week.amount_left)    
    
    # x= ght.budget - Add_transaction.add_money
    # x=0
    # y=0
    # if x<0:
    #     messages.warning(request,'Your expenses exceeded your budget')
    #     x = 0
    # if x>0:
    #     y = 0
    # addmoney_info.x = abs(x)
    # addmoney_info.y = abs(y)
    return render(request,'weekly.html',{'addmoney_info':addmoney_info,'week': week}) 
      





def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')

def profile_edit(request,id):
    if request.user.is_authenticated:
        User = get_user_model()
        add = User.objects.get(id=id)
        return render(request,'profile_edit.html',{'add':add})
    return redirect("/home")

def profile_update(request,id):
    if request.user.is_authenticated:
        User = get_user_model()
        if request.method == "POST":
            user = User.objects.get(id=id)
            user.username = request.POST["username"]
            user.name = request.POST["name"]
            user.email = request.POST['email']
            user.phone = request.POST['phone']
            user.save()
            return redirect('profile')
    return redirect('index') 



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changepassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })


# def deletetransaction(request,id):
#     deletetrans = Add_transaction.objects.get(pk=id)
#     deletetrans.delete()
#     context = {"object":deletetrans}
#     return redirect('history')

def deletetransaction(request,id):
    if request.user.is_authenticated:
        addmoney_info = Add_transaction.objects.get(id=id)
        addmoney_info.delete()
        return redirect("history")
    return redirect("index") 

def mywallet(request):
    mywallet1 = Wallet.objects.filter(user_id=request.user.id)
    context = {
        'mywallet1' : mywallet1,
        'values' : request.POST
    }
    return render(request,'mywallet.html',context)

def deletewallet(request,id):
    if request.user.is_authenticated:
        wallet_info = Wallet.objects.get(id=id)
        wallet_info.delete()
        return redirect("mywallet")
    return redirect()


def info_year(request):
    User = get_user_model()
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=30*12)
    user_id = request.user.id 
    user1 = User.objects.get(id=user_id)
    addmoney = Add_transaction.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.category
    Category_list = list(set(map(get_Category,addmoney)))


    def get_expense_category_amount(category,add_money):
        amount = 0 
        filtered_by_category = addmoney.filter(category = category,add_money="Expense") 
        for item in filtered_by_category:
            amount+=item.amount
        return amount

    for x in addmoney: 
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def info(request):
    User = get_user_model()
    stats = Add_transaction.objects.filter(user_id=request.user.id)
    context ={
        'stats': stats,
        'values': request.POST
    }
    return render(request,'info.html',context)


def addmoney_update(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            User = get_user_model()
            add  = Add_transaction.objects.get(id=id)
            add.wallet_name = request.POST["wallet_name"]
            add.add_money = request.POST["add_money"]
            add.category = request.POST["category"]
            add.amount = request.POST["amount"]
            add.Date = request.POST["Date"]
            add.description = request.POST["description"]
            add.save()
            return redirect("index")
    return redirect("history")        

def expense_edit(request,id):
    if request.user.is_authenticated:
        User = get_user_model()
        addmoney_info = Add_transaction.objects.get(id=id)
        user_id = request.user.id 
        user1 = User.objects.get(id=user_id)
        return render(request,'expense_edit.html',{'addmoney_info':addmoney_info})
    return redirect("history")  


# def wallet_update(request,id):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             User = get_user_model()
#             wlt  = Wallet.objects.get(id=id)
#             wlt.wallet_name = request.POST["wallet_name"]
#             wlt.wallet_amount = request.POST["wallet_amount"]
#             wlt.budget = request.POST["budget"]
#             wlt.save()
#             return redirect("index")
#         return redirect("mywallet")

# def wallet_edit(request,id):
#     if request.user.is_authenticated:
#         User = get_user_model()
#         user_id = request.user.id 
#         wlt1 = Wallet.objects.get(id=id)
#         user1 = User.objects.get(id=user_id)
#         return render(request,'expense_edit.html',{'wlt1':wlt1})
#     return redirect("mywallet") 