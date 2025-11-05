import csv

def read_csv_safe(filepath):
    # read stock data from a CSV file and validate input
    stocks = []
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)

            required = ['Stock', 'Sector', 'PriceStart', 'PriceEnd']
            # Validate required columns
            for col in required:
                if col not in reader.fieldnames:
                    print(f"Missing required column: '{col}' — skipping analysis.")
                    return []

            # Process each row and validate data
            for row in reader:
                try:
                    stock = row['Stock'].strip()
                    sector = row['Sector'].strip()
                    price_start = float(row['PriceStart'])
                    price_end = float(row['PriceEnd'])

                    if price_start <= 0 or price_end <= 0:
                        print(f"Skipping invalid row (non-positive price): {row}")
                        continue

                    stocks.append({
                        "Stock": stock,
                        "Sector": sector,
                        "PriceStart": price_start,
                        "PriceEnd": price_end
                    })
                except ValueError:
                    print(f"Skipping invalid row (non-numeric price): {row}")
                    continue
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"Unexpected error while reading file: {e}")

    return stocks


def compute_return(row):
    # """Compute percentage return for a single stock."""
    price_start = row['PriceStart']
    price_end = row['PriceEnd']
    return round(((price_end - price_start) / price_start) * 100, 2)


def process_all(rows):
    # """Compute returns for all valid stocks."""
    results = []
    for r in rows:
        r['Return'] = compute_return(r)
        results.append(r)
    return results


def aggregate_by_sector(results):
    # """Aggregate stock returns by sector and compute average returns."""
    summary = {}
    for item in results:
        sector = item['Sector']
        ret = item['Return']

        if sector not in summary:
            summary[sector] = {'total': 0, 'count': 0, 'avg_return': 0}

        summary[sector]['total'] += ret
        summary[sector]['count'] += 1

    # Compute average returns
    for sector in summary:
        total = summary[sector]['total']
        count = summary[sector]['count']
        summary[sector]['avg_return'] = round(total / count, 2)

    return summary


def print_report(results, summary):
    # Display full stock report and sector-wise summary
    print("\n==== All Stock Details ====")
    print(f"{'Stock':<12} {'Sector':<20} {'Start':<10} {'End':<10} {'Return(%)':<10}")

    for r in results:
        print(f"{r['Stock']:<12} {r['Sector']:<20} {r['PriceStart']:<10.2f} "
              f"{r['PriceEnd']:<10.2f} {r['Return']:<10.2f}")

    # Top 5 performing stocks
    print("\n==== Top 5 Performing Stocks ====")
    sorted_results = sorted(results, key=lambda x: x['Return'], reverse=True)
    for r in sorted_results[:5]:
        print(f"{r['Stock']} ({r['Sector']}) - {r['Return']}%")

    # Sector summary
    print("\n==== Sector Summary ====")
    print(f"{'Sector':<25} {'Avg Return(%)':<15} {'Count':<10}")

    best_sector, best_return = None, -float('inf')
    for sector, data in summary.items():
        print(f"{sector:<25} {data['avg_return']:<15.2f} {data['count']:<10}")
        if data['avg_return'] > best_return:
            best_sector, best_return = sector, data['avg_return']

    print(f"\nBest Performing Sector: {best_sector} ({best_return}%)")


def export_csv(results, output_filepath):
    # Export processed stock data to a CSV file.
    try:
        with open(output_filepath, 'w', newline='') as file:
            fieldnames = ['Stock', 'Sector', 'PriceStart', 'PriceEnd', 'Return']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Results successfully exported to {output_filepath}")
    except Exception as e:
        print(f"An error occurred while exporting to CSV: {e}")


def main():
    #Main program
    filepath = input("Enter path to CSV file (e.g., stocks_sample.csv): ").strip()
    print(f"Loading data from: {filepath}\n")

    rows = read_csv_safe(filepath)
    if not rows:
        print("No valid data to process. Exiting.")
        return

    results = process_all(rows)
    summary = aggregate_by_sector(results)
    print_report(results, summary)

    choice = input("\nDo you want to export the results to CSV? (y/n): ").strip().lower()
    if choice == 'y':
        output_filepath = input("Enter output CSV file path (e.g., output.csv): ").strip()
        export_csv(results, output_filepath)


if __name__ == "__main__":
    main()
