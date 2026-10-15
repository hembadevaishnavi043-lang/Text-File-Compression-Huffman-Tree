
import heapq
from collections import Counter


# Node of Huffman Tree
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# Build Huffman Tree
def build_tree(text):
    frequency = Counter(text)
    heap = []

    for char, freq in frequency.items():
        heapq.heappush(heap, Node(char, freq))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right

        heapq.heappush(heap, parent)

    return heap[0]


# Generate Huffman Codes
def generate_codes(root, code="", codes=None):
    if codes is None:
        codes = {}

    if root.char is not None:
        codes[root.char] = code if code else "0"
        return codes

    generate_codes(root.left, code + "0", codes)
    generate_codes(root.right, code + "1", codes)

    return codes


# Encode Text
def encode(text, codes):
    return "".join(codes[char] for char in text)


# Decode Text
def decode(encoded, root):
    result = []
    current = root

    # Special case: text contains only one unique character
    if root.char is not None:
        return root.char * len(encoded)

    for bit in encoded:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.char is not None:
            result.append(current.char)
            current = root

    return "".join(result)


# Main Program
text = input("Enter text to compress: ")

if not text:
    print("Please enter some text.")
else:
    root = build_tree(text)
    codes = generate_codes(root)

    encoded_text = encode(text, codes)
    decoded_text = decode(encoded_text, root)

    print("\nCharacter Frequencies:")
    for char, freq in Counter(text).items():
        print(repr(char), ":", freq)

    print("\nHuffman Codes:")
    for char, code in codes.items():
        print(repr(char), ":", code)

    print("\nOriginal Text:", text)
    print("Encoded Binary Data:", encoded_text)
    print("Decoded Text:", decoded_text)

    original_bits = len(text) * 8
    compressed_bits = len(encoded_text)

    print("\nOriginal Size:", original_bits, "bits")
    print("Encoded Size:", compressed_bits, "bits")

    if decoded_text == text:
        print("Compression and decompression successful!")
