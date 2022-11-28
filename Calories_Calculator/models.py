from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]
LIFE_STYLE_CHOICES = [
    ('Sedentary', 'Sedentary'),
    ('Lightly active', 'Lightly active'),
    ('Moderately active', 'Moderately active'),
    ('Very active', 'Very active'),
    ('Extra active', 'Extra active'),
]


#--------- declare "BMR_Calculate" model(Table)---------
class BMRdata(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male')
    Weight = models.IntegerField()
    Height = models.FloatField(max_length=10)
    Age = models.IntegerField()
    Life_style = models.CharField(max_length=17, choices=LIFE_STYLE_CHOICES, default='Sedentary')
    bmr_result = models.IntegerField(null=True)
    # date = models.DateTimeField(null=True)
    
    def __str__(self):
      return self.Gender

# --------declare "FoodItem" model(Table)--------
MEALS = [
    ('BreakFast', 'Breakfast'),
    ('Lhnch', 'Lunch'),
    ('Dinner', 'Dinner')
]
class addFood(models.Model):
     userID = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     Meals= models.CharField(max_length=9, choices=MEALS, default='BreakFast')
     Food_Name = models.CharField(max_length=12)
     Quantity = models.IntegerField()
     Calories = models.IntegerField()
     Date = models.DateField(null=True)
     
     def __str__(self):   
        return self.Meals