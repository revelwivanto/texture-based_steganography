from math import isclose

def parse_ratio(ratio_str):
    return list(map(float, ratio_str.split(':')))

def normalize_ratio(ratio):
    total = sum(ratio)
    return [x / total for x in ratio]

def calculate_similarity(ratio1, ratio2):
    normalized_ratio1 = normalize_ratio(ratio1)
    normalized_ratio2 = normalize_ratio(ratio2)
    return sum(abs(a - b) for a, b in zip(normalized_ratio1, normalized_ratio2))

def find_most_similar_ratio(target_ratio_str, *ratios_str):
    target_ratio = parse_ratio(target_ratio_str)
    ratios = [parse_ratio(r) for r in ratios_str]
    
    similarities = [calculate_similarity(target_ratio, r) for r in ratios]
    
    most_similar_index = similarities.index(min(similarities))
    
    return most_similar_index

# Example usage
a = "75:12.5:12.5"
b1 = "74.25:13.5:12.25"
b2 = "75:12.3:12.7"

most_similar_index = find_most_similar_ratio(a, b1, b2)

if most_similar_index == 0:
    print(f"Input bit a is more similar to input bit b 1st")
elif most_similar_index == 1:
    print(f"Input bit a is more similar to input bit b 2nd")
else:
    print(f"Input bit a is not similar to any of the input bits b")
