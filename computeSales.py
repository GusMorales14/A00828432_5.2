# pylint: disable=invalid-name
"""Compute the total cost
for all sales included in"""
import argparse
import time
import json
from pathlib import Path


def load_json(path: str):
    """Load a JSON file and return the parsed object."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_lookup_table(items,
                       key_field,
                       price_field):
    """
    Docstring for build_lookup_table
    """
    lookup = {}
    for item in items:
        item_name = item.get(key_field)
        item_price = item.get(price_field)
        if item_name is None:
            print(f"Missing '{key_field}' in an item: {item}")
        if item_price is None:
            print(f"Missing '{price_field}' in an item: {item}")
        lookup[item_name] = float(item_price)
    return lookup


def compute_total(sales_list, lookup_list, product, quantity):
    """
    Returns the total of the sale and a list of items missing in the
    cataloge.
    """
    total_sale = 0.0

    for row in sales_list:
        try:
            product = row["Product"]
            quantity = row["Quantity"]

            if product not in lookup_list:
                print(
                    f"Error: Product '{product}' not found in price catalogue"
                      )
                continue

            total_sale += quantity * lookup_list[product]

        except (KeyError, TypeError) as error:
            print(f"Invalid sale record {row}: {error}")
            continue

    return total_sale


def build_output(total_sale, time_elapsed):
    """Build output text"""
    lines = []
    lines.append(f"Total sale: {total_sale:.2f}")
    lines.append(f"ElapsedTimeSeconds\t{time_elapsed}")
    return "\n".join(lines)


def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("priceCataloge",
                        help="JSON catalogue of prices of products")
    parser.add_argument("salesRecord",
                        help="JSON record for all sales in a company")
    args = parser.parse_args()

    start_timer = time.perf_counter()  # Starting time elapsed timer
    cataloge = load_json(args.priceCataloge)
    sales = load_json(args.salesRecord)
    price_lookup = build_lookup_table(cataloge,
                                      key_field="title",
                                      price_field="price"
                                      )

    total = compute_total(sales,
                          price_lookup,
                          product="Product",
                          quantity="Quantity"
                          )

    elapsed_time = time.perf_counter() - start_timer  # End of time counter

    output_text = build_output(total, elapsed_time)
    print(output_text)

    with open(f"SalesResult.txt",
              "w", encoding="utf-8") as out_file:
        out_file.write(output_text)


if __name__ == "__main__":
    main()
