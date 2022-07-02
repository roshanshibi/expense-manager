from . views import *
from django.urls import path

urlpatterns = [
    path('dashboard/',dashboard,name="dashboard"),
    path('index/',index,name="index"),
    path('signup/',signup,name="signup"),
    path('login/',login,name="login"),
    path('logout/',logout,name="logout"),
    path('wallet/',wallet,name="wallet"),
    path('transaction/',transaction,name="transaction"),
    path('transaction_submit/',transaction_submit,name="transaction_submit"),
    path('history/',history,name="history"),
    path('weekly/',weekly,name="weekly"),
    path('expense_week/',expense_week, name='expense_week'),
    path('profile/',profile,name="profile"),
    path('<int:id>/profile_update/',profile_update,name="profile_update"),
    path('<int:id>/profile_edit/',profile_edit,name="profile_edit"),
    path('change_password/',change_password,name="changepassword"),
    path('deletransaction/<int:id>', deletetransaction,name="deletetransaction"),
    path('mywallet/',mywallet,name="mywallet"),
    path('deletewallet/<int:id>', deletewallet,name="deletewallet"),
    path('info/',info,name="info"),
    path('info_year/',info_year,name="info_year"),
    path('expense_edit/<int:id>',expense_edit,name='expense_edit'),
    path('addmoney_update/<int:id>', addmoney_update, name="addmoney_update") ,
    # path('wallet_update/<int:id>',wallet_update,name="wallet_update"),
    # path('wallet_edit/<int:id>',wallet_edit,name="wallet_edit"),

]