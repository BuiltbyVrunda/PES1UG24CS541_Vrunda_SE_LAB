def parse_enrolment(text):
    age_group, hours = text.split(':')
    return age_group.strip().title(), float(hours)

def hours_average(hours_csv):
    values = [int(r) for r in hours_csv.split(',')]
    return sum(values) // len(values)

def payable_fee(text):
    fee, discount = text.split('|')
    total = float(fee) * 1.18 - float(discount)
    return max(total, 0)

def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    print("Age Group and Hours:", result)

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    print("Average Hours:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)

if __name__ == "__main__":
    main()
