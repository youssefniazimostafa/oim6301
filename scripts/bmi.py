


def compute_bmi(weight, height):
    bmi_value = weight / (height ** 2)
    return bmi_value

def classify_bmi(bmi):
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    return category

def main():
    weight = float(input("Enter your weight in kilograms: "))
    height = float(input("Enter your height in meters: "))
    bmi_value = compute_bmi(weight, height)
    result = classify_bmi(bmi_value)
    print(f" Your category is: {result}.")

#main()
if __name__ == "__main__":
    main()

