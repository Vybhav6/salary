

def convert_salaries(input_file):
    columns_to_keep = ['WAGE_RATE_OF_PAY_FROM', 'WAGE_UNIT_OF_PAY']
    conversion_rates = {
        'Year': 1,
        'Month': 12,
        'Hour': 8760,
        'Week': 52,
        'Bi-Weekly': 26
    }
    unit_conversions = {
        'Year': 'year',
        'Month': 'year',
        'Hour': 'year',
        'Week': 'year',
        'Bi-Weekly': 'year'
    }

    with open(input_file, 'r') as infile, open('temp_output.csv', 'w', newline='') as outfile:
        import csv

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        header_indices = {header[i]: i for i in range(len(header))}

        wage_column_index = header_indices['WAGE_RATE_OF_PAY_FROM']
        unit_column_index = header_indices['WAGE_UNIT_OF_PAY']

        writer.writerow(columns_to_keep)

        for row in reader:
            wage_str = row[wage_column_index]
            unit = row[unit_column_index]

            wage_str = wage_str.replace(',', '')

            if unit in conversion_rates:
                wage = float(wage_str) * conversion_rates[unit]
                row[wage_column_index] = wage
                row[unit_column_index] = unit_conversions[unit]

            writer.writerow([row[wage_column_index], row[unit_column_index]])



def calculate_statistics(input_file):
    import csv

    total_records = 0
    total_salary = 0
    salaries = []

    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                wage = float(row['WAGE_RATE_OF_PAY_FROM'])
                unit = row['WAGE_UNIT_OF_PAY']

                if unit == 'hour':
                    wage *= 8760
                elif unit == 'week':
                    wage *= 52
                elif unit == 'month':
                    wage *= 12
                elif unit == 'bi-weekly':
                    wage *= 26

                total_records += 1
                total_salary += wage
                salaries.append(wage)
            except ValueError:
                continue

    salaries.sort()

    median_salary = (salaries[total_records // 2] + salaries[total_records // 2 - 1]) / 2 if total_records % 2 == 0 else salaries[total_records // 2]

    percentile_25 = salaries[int(total_records * 0.25)]

    percentile_75 = salaries[int(total_records * 0.75)]

    mean_salary = total_salary / total_records

    statistics = {
        "Number of results": total_records,
        "Mean salary": mean_salary,
        "Median salary": median_salary,
        "25% percentile salary": percentile_25,
        "75% percentile salary": percentile_75
    }

    return statistics



def combined_model(input_file):
    
    convert_salaries(input_file)
    
    
    statistics = calculate_statistics('temp_output.csv')
    
    return statistics


input_file = 'sample.csv'

result = combined_model(input_file)
print(result)
