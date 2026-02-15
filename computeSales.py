import argparse
import time

def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("priceCataloge",
                        help= " JSON catalogue of prices of products")
    parser.add_argument("salesRecord",
                        help= "JSON record for all sales in a company")

    start_timer = time.perf_counter()
if __name__ == "__main__":
    main()
