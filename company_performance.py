import csv

def read_csv_safe(filepath):
    stocks = []
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
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
    price_start = row['PriceStart']
    price_end = row['PriceEnd']
    return round(((price_end - price_start) / price_start) * 100, 2)


def process_all(rows):
    results = []
    for r in rows:
        r['Return'] = compute_return(r)
        results.append(r)
    return results


def aggregate_by_sector(results):
    sector_summary = {}
    for r in results:
        sector = r['Sector']
        if sector not in sector_summary:
            sector_summary[sector] = {"total_return": 0, "count": 0}
        sector_summary[sector]['total_return'] += r['Return']
        sector_summary[sector]['count'] += 1

    for sector in sector_summary:
        avg = sector_summary[sector]['total_return'] / sector_summary[sector]['count']
        sector_summary[sector]['avg_return'] = round(avg, 2)

    return sector_summary


def print_report(results, sector_summary):
    print("\n==== All Stock Details ====")
    print(f"{'Stock':<12} {'Sector':<20} {'Start':<10} {'End':<10} {'Return(%)':<10}")
    print("-" * 65)
    for r in results:
        print(f"{r['Stock']:<12} {r['Sector']:<20} {r['PriceStart']:<10.2f} {r['PriceEnd']:<10.2f} {r['Return']:<10.2f}")

    sorted_results = sorted(results, key=lambda x: x['Return'], reverse=True)
    print("\n==== Top 5 Stocks by Return ====")
    for r in sorted_results[:5]:
        print(f"{r['Stock']} ({r['Sector']}) - {r['Return']}%")

    print("\n==== Sector Performance Summary ====")
    print(f"{'Sector':<25} {'Avg Return(%)':<15} {'Count':<10}")
    print("-" * 50)
    best_sector = None
    best_return = float('-inf')

    for sector, data in sector_summary.items():
        print(f"{sector:<25} {data['avg_return']:<15.2f} {data['count']:<10}")
        if data['avg_return'] > best_return:
            best_return = data['avg_return']
            best_sector = sector

    print("\nBest Performing Sector:", best_sector, f"({best_return}%)")


def export_csv(results, filename):
    try:
        with open(filename, 'w', newline='') as file:
            fieldnames = ['Stock', 'Sector', 'PriceStart', 'PriceEnd', 'Return']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"\nResults exported successfully to '{filename}'")
    except Exception as e:
        print("Error exporting CSV:", e)


def main():
    filepath = "stocks_sample.csv"  # Auto-loads CSV file in same folder
    print(f"Loading data from: {filepath}\n")

    rows = read_csv_safe(filepath)
    if not rows:
        print("No valid data to process. Exiting.")
        return

    results = process_all(rows)
    sector_summary = aggregate_by_sector(results)
    print_report(results, sector_summary)

    choice = input("\nDo you want to export the results to 'stock_returns.csv'? (y/n): ").strip().lower()
    if choice == 'y':
        export_csv(results, "stock_returns.csv")


if __name__ == "__main__":
    main()
