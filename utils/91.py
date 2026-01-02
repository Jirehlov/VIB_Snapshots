import json
import argparse

def compare_json(json1, json2):
    keys1, keys2 = set(json1), set(json2)
    print("\nJSON1 独有字段:", {k: json1[k] for k in keys1 - keys2})
    print("\nJSON2 独有字段:", {k: json2[k] for k in keys2 - keys1})
    print("\n共有但值不同的字段:", {k: (json1[k], json2[k]) for k in keys1 & keys2 if json1[k] != json2[k]})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json1", type=str, help="Path to first JSON file")
    parser.add_argument("json2", type=str, help="Path to second JSON file")
    args = parser.parse_args()
    
    with open(args.json1) as f1, open(args.json2) as f2:
        compare_json(json.load(f1), json.load(f2))

if __name__ == "__main__":
    main()
