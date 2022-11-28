from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages


from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .form import RegisterUserForm, BMR_Calculater
from .models import addFood, BMRdata
# Create your views here.

#----------Registeration-----------------
def register(request):
    context = {

    }
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account created successfully")
            return redirect('loginUser')
        else:
            db_detail = User.objects.get(username=request.POST['username'])
            if db_detail.username == request.POST["username"]:
                messages.error(request, "This username already taken")
            elif db_detail.email == request.POST['email']:
                messages.error(request, "This email already taken")
            elif request.POST['password2'] != request.POST['password1']:
                messages.error(request, "Your password doesn't match")
            return redirect('register')
    else:
        form = RegisterUserForm()
        context["form"] = form
    return render(request, 'Calories/register.html', context)

#----------Login User------------------
def loginUser(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user:
                login(request,user)
                return redirect('calculator')
            else: 
                messages.error(request,'Username or password is wrong!!!')
            return redirect('loginUser')
    else:
        fm = AuthenticationForm()
    return render(request,'Calories/login.html',{'form':fm})
    

#....... BMR Calculation function.............
def calculator(request):
    if request.user.is_authenticated: 
        if request.method == "POST":
            form = BMR_Calculater(request.POST)
            if form.is_valid():
                gender = form.cleaned_data['Gender']
                WInKg = form.cleaned_data['Weight']
                HInCm = form.cleaned_data['Height']
                AgeInYear = form.cleaned_data['Age']
                life_style = form.cleaned_data['Life_style']
                bmr_data = form.save()
                if gender == 'male':
                    BMR = (10 * WInKg) + (6.25 * HInCm) - (5 * AgeInYear) + 5
                elif gender == 'female':
                    BMR = (10 * WInKg) + (6.25 * HInCm) - (5 * AgeInYear) - 161
                    # print(BMR)
                if life_style == 'Sedentary':
                   Total_BMR = BMR * 2.1
                elif life_style == 'Lightly active':
                   Total_BMR = BMR * 1.37
                elif life_style == 'Moderately active':
                   Total_BMR = BMR * 1.55
                elif life_style == 'Very active':
                   Total_BMR = BMR * 1.725
                elif life_style == 'Extra active':
                   Total_BMR = BMR * 1.9
                #   print(Total_BMR)
                bmr_data.bmr_result = int(Total_BMR)
                bmr_data.userID = request.user
                bmr_data.save()
                BMRData = { 
                    "bmr": int(Total_BMR), 
                }
            return render(request, 'Calories/home.html',BMRData)
        elif request.method == "GET":
            form = BMR_Calculater
            context = {
                    }
            userInfo = BMRdata.objects.filter(userID=request.user.id)
            if userInfo:
                return redirect('home')
            else: 
                userID = request.user
                context["form"] = form        
                context["user"] = userID
                context["bmr_info"] = userInfo
                #print(user)
                return render(request, 'Calories/calculator.html', context)
    else:
        context={
            "form": BMR_Calculater
        }
        return render(request, 'Calories/calculator.html', context)


# ...........Dashboard............
def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            Meals = request.POST.get("Meals")
            Food_Name = request.POST.get("Food_Name")
            Quantity = request.POST.get("Quantity")
            Calories = request.POST.get("Calories")
            Date = request.POST.get("Date")
            FoodData = addFood.objects.create(Meals=Meals, Food_Name=Food_Name, Quantity=Quantity, Calories=Calories, Date=Date)
            FoodData.userID = request.user
            FoodData.save()
            bmr = BMRdata.objects.get(userID=request.user.id).bmr_result 
            FoodInfo = addFood.objects.filter(userID_id=request.user.id)
            intake_calories = 0
            for food in FoodInfo:
                intake_calories += food.Calories
            cal_status = bmr - intake_calories
            Food_Data = {
                "FoodInfoo" :FoodInfo,
                "bmr": bmr,
                "cal_status": cal_status,
                "intake_calories": intake_calories,
                }
            return render(request, 'Calories/home.html',Food_Data)
        elif request.method == "GET":
            userInfo = BMRdata.objects.filter(userID=request.user.id)
            if userInfo:
                bmr = BMRdata.objects.get(userID=request.user.id).bmr_result 
                FoodInfo = addFood.objects.filter(userID_id=request.user.id)
                intake_calories = 0
                for food in FoodInfo:
                    intake_calories += food.Calories
                    cal_status = bmr - intake_calories
                    Food_Data = {
                    "FoodInfoo" :FoodInfo,
                    "bmr": bmr,
                    "cal_status": cal_status,
                    "intake_calories": intake_calories,
                    }
                return render(request,'Calories/home.html', Food_Data)
            else:
                bmr = BMRdata.objects.get(userID=request.user.id).bmr_result 
                FoodInfo = addFood.objects.filter(userID_id=request.user.id)
            return render(request,'Calories/home.html', Food_Data)
        
#-----------Update Function-------------------   

def EditBMR(request): 
    if request.user.is_authenticated: 
        context = {}
        update_bmr = BMRdata.objects.get(userID_id=request.user.id)
        context['update_bmr'] = update_bmr
        if request.method == "POST":
            form = BMR_Calculater(request.POST)
            if form.is_valid():
                gender = form.cleaned_data['Gender']
                WInKg = form.cleaned_data['Weight']
                HInCm = form.cleaned_data['Height']
                AgeInYear = form.cleaned_data['Age']
                life_style = form.cleaned_data['Life_style']
                
                update_bmr.Gender = gender
                update_bmr.Weight = WInKg
                update_bmr.Height = HInCm
                update_bmr.Age = AgeInYear
                update_bmr.Life_style = life_style
                update_bmr.save()
                
                if gender == 'male':
                    BMR = (10 * WInKg) + (6.25 * HInCm) - (5 * AgeInYear) + 5
                elif gender == 'female':
                    BMR = (10 * WInKg) + (6.25 * HInCm) - (5 * AgeInYear) - 161
                    # print(BMR)
                if life_style == 'Sedentary':
                   Total_BMR = BMR * 2.1
                elif life_style == 'Lightly active':
                   Total_BMR = BMR * 1.37
                elif life_style == 'Moderately active':
                   Total_BMR = BMR * 1.55
                elif life_style == 'Very active':
                   Total_BMR = BMR * 1.725
                elif life_style == 'Extra active':
                   Total_BMR = BMR * 1.9
                #   print(Total_BMR)
                update_bmr.bmr_result = int(Total_BMR)
                update_bmr.userID = request.user
                update_bmr.save()
                FoodInfo = addFood.objects.filter(userID_id=request.user.id)
                intake_calories = 0
                for food in FoodInfo:
                    intake_calories += food.Calories
                cal_status = update_bmr.bmr_result - intake_calories
                BMRData = { 
                    "bmr": int(Total_BMR), 
                    "FoodInfoo" :FoodInfo,
                    "cal_status": cal_status,
                    "intake_calories": intake_calories,
                    
                }
                return render(request, 'Calories/home.html',BMRData)
        else:
            data= BMRdata.objects.get(userID_id=request.user.id)
            form = BMR_Calculater(instance=data)
        return render(request, 'Calories/update.html', {"form":form})
        
                       
# ......Search Function of  Daily, Weekly and Monthly Record.......
def SearchByDate(request):
    if request.user.is_authenticated:
        if request.method =='POST': 
            if 'date_btn' in request.POST:
                date = request.POST.get("search_date")
                searched = addFood.objects.filter(userID_id=request.user.id, Date=date)
                # print(searched)
            if 'month_btn' in request.POST:
                month = request.POST.get("search_month")
                searched = addFood.objects.filter(userID_id=request.user.id, Date__contains=month)
            if 'week_btn' in request.POST:
                week = request.POST.get("search_week")
                weeek = week[6:]
                searched = addFood.objects.filter(userID_id=request.user.id, Date__week=weeek)
            return render(request, 'Calories/search.html', {"searched": searched})
    return render(request, 'Calories/search.html')

# .......Monthly Graphical report......
def graph(request):
    if request.user.is_authenticated:
        if request.method =='POST':
           month = request.POST.get("month")
           searched = addFood.objects.filter(userID_id=request.user.id, Date__contains=month)
           bmr = BMRdata.objects.get(userID=request.user.id).bmr_result     
           intake_calories = 0
           for food in searched:
                intake_calories += food.Calories
        #    print(searched)
           return render(request, 'Calories/graph.html', {"intake_calories":intake_calories, "month":month, "searched": searched,"bmr":bmr})
    return render(request, 'Calories/graph.html')



def logoutUser(request):
        logout(request)
        return redirect('loginUser')