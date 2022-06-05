import argparse
from pprint import pprint

from csvcomparer import CsvCompare

def main() -> None:
    def handle_args() -> argparse.Namespace:

        parser = argparse.ArgumentParser(
            description="Compare delimited files that share a common key."
        )
        parser.add_argument(
            "left_csv_filepath",
            metavar="left_csv_filepath",
            type=str,
            help="Filepath to the 'left' file for compare.",
        )
        parser.add_argument(
            "right_csv_filepath",
            metavar="right_csv_filepath",
            type=str,
            help="Filepath to the 'right' file for compare.",
        )
        parser.add_argument(
            "key",
            metavar="key",
            nargs="+",
            help="Common key(s) between the left and right csv files.",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Convert csv compare results into JSON format."
        )
        parser.add_argument(
            "-o", "--output",
            metavar="output",
            type=str,
            help="Output file for csv compare results."
        )

        return parser.parse_args()

    cli_args = handle_args()

    diffs = CsvCompare(
        cli_args.left_csv_filepath, cli_args.right_csv_filepath, cli_args.key
    ).diffs
    
    diffs = diffs.to_json() if cli_args.json else diffs.to_dict()

    if cli_args.output:
        with open(cli_args.output, 'w') as f:
            f.write(str(diffs))
    else:
        print(diffs)
    

if __name__ == "__main__":
    main()
