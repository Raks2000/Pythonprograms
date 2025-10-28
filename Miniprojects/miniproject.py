import csv

def read_csv_file(filepath): #function to read CSV file
    stocks = []  # Empty list to store stock data
    try:
        with open(filepath, 'r') as file: # Open the file in read mode
            reader = csv.DictReader(file)  # Read file line by line as dictionary

            required = ['Stock', 'Sector', 'PriceStart', 'PriceEnd']
            for col in required: #checking for required columns
                if col not in reader.fieldnames: # checking if any required column is missing
                    print(f" Missing required column: '{col}' — skipping analysis.") #printing missing column message
                    return [] #returning empty list

            for row in reader: # Looping through each row
                print("\nNew Row Read From CSV:") # Indicates a new row is being processed
                print(row)  # it will print the full data in the form of dictionary
                # Geting each column value
                stock = row['Stock'] 
                sector = row['Sector'] 
                price_start = float(row['PriceStart'])
                price_end = float(row['PriceEnd'])

                if price_start > 0 and price_end > 0: # checking for positive prices
                    # Adding this stock to the list
                    stocks.append({
                        "Stock": stock,
                        "Sector": sector,
                        "PriceStart": price_start,
                        "PriceEnd": price_end
                    })
                else:
                    print("Skipping row with non-positive price:", row)
                    
    except FileNotFoundError: #handling file not found error
        print(f"Error: The file {filepath} was not found.")
    except Exception as e: #handling any other unexpected exceptions
        print(f"An error occurred: {e}")
    return stocks  # Returnimg the final list of stocks


def compute_return(row): #function to compute return percentage
    price_start = row['PriceStart'] #extracting starting price
    price_end = row['PriceEnd'] #extracting ending price
    return round(((price_end - price_start) / price_start) * 100, 2) #calculating return percentage and rounding to 2 decimal places

def process_all(rows): #function to process all stock data
    results = [] #initializing empty list to store results
    for r in rows: #looping through each row
        r['Return'] = compute_return(r) #computing return for each stock
        results.append(r) #appending processed stock data to results list
    return results #returning the results list

def aggregate_by_sector(results): #function to aggregate data by sector
    summary = {} # Empty dictionary to store each sector’s data
    for item in results: # Go through each stock record one by one
        sector = item['Sector'] # Get the sector name
        ret = item['Return'] # Get the return value

        if sector not in summary: # checking if this sector is not yet in the summary
            summary[sector] = { 
                'total': 0, # Total return for this sector
                'count': 0, # Number of stocks in this sector
                'avg_return': 0  # Added this field
            }

        summary[sector]['total'] += ret # Add this stock’s return to total
        summary[sector]['count'] += 1 # Increase the count by 1

    for sector in summary: # Now calculate average return for each sector
        total = summary[sector]['total'] # Get total return
        count = summary[sector]['count'] # Get count of stocks
        summary[sector]['avg_return'] = round(total / count, 2) # Calculate and round average return and updates avreage return

    return summary # return the summary back

def print_report(results, summary): #printing the final report
    print("Individual Stock Returns:") #printing header for individual stock returns
    print("\n==== All Stock Details ====") #printing header for all stock details
    print(f"{'Stock':<12} {'Sector':<20} {'Start':<10} {'End':<10} {'Return(%)':<10}") #printing table header

    for r in results: #looping through each processed stock data
        print(f"{r['Stock']:<12} {r['Sector']:<20} {r['PriceStart']:<10.2f} {r['PriceEnd']:<10.2f} {r['Return']:<10.2f}") #printing all the details
    
    print("\n==== Top 5 Performing Stocks ====")
    sorted_results = sorted(results, key=lambda x: x['Return'], reverse=True) #sorting stocks by return in descending order
    
    for r in sorted_results[:5]: #printing top 5 performing stocks
        print(f"{r['Stock']} ({r['Sector']}) - {r['Return']}%") #printing stock name, sector and return percentage

    print("\n==== Sector Summary ====")
    print(f"{'Sector':<25} {'Avg Return(%)':<15} {'Count':<10}") #printing sector summary header
    best_sector = None #
    best_return = -float('inf') # Initialize best return to negative infinity(the smallest possible number in Python.)

    for sector, data in summary.items(): #looping through each sector summary
        print(f"{sector:<25} {data['avg_return']:<15.2f} {data['count']:<10}") #printing data of sector name, average return and count of stocks
        if data['avg_return'] > best_return: #checking for best performing sector
            best_return = data['avg_return'] #updating best return
            best_sector = sector #updating best sector

    print(f"\nBest Performing Sector: {best_sector} ({best_return}%)") #printing best performing sector

def export_results_to_csv(results, output_filepath): #function to export results to CSV file
    try:
        with open(output_filepath, 'w', newline='') as file: # Open the file in write mode
            fieldnames = ['Stock', 'Sector', 'PriceStart', 'PriceEnd', 'Return'] # Define the CSV column headers
            writer = csv.DictWriter(file, fieldnames=fieldnames) # Create a DictWriter object

            writer.writeheader() # Write the header row
            for r in results: # Loop through each processed stock data
                writer.writerow(r) # Write each stock's data as a row in the CSV file
        print(f"Results successfully exported to {output_filepath}") # Indicate successful export
    except Exception as e: #handling any exceptions during file writing
        print(f"An error occurred while exporting to CSV: {e}")

def main():
    filepath = "stocks_30rows_4cols.csv" #path to the CSV file
    print(f"Loading data from: {filepath}\n") #printing the file path

    rows = read_csv_file(filepath) #reading the CSV file
    if not rows: # checking if no valid data is returned
        print("No valid data to process. Exiting.")
        #return

    results = process_all(rows) #processing all stock data
    summary = aggregate_by_sector(results) #aggregating data by sector
    print_report(results, summary) #printing the final report
    export_results_to_csv(results, "stocks_30rows_4cols.csv") #exporting results to CSV file

if __name__ == "__main__":
    main()
