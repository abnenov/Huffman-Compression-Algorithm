# Import necessary libraries
import heapq  # For creating priority queue (min-heap)
from collections import Counter  # For easy frequency counting
import pickle  # For storing and loading the Huffman tree

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    # Calculate frequency of each character
    frequency = Counter(text)
    
    # Create a priority queue of all characters
    priority_queue = []
    for char, freq in frequency.items():
        heapq.heappush(priority_queue, HuffmanNode(char, freq))
    
    # Special case - only one unique character
    if len(priority_queue) == 1:
        node = heapq.heappop(priority_queue)
        new_node = HuffmanNode(None, node.freq)
        new_node.left = node
        heapq.heappush(priority_queue, new_node)
    
    # Build the tree until only one node remains in the queue
    while len(priority_queue) > 1:
        # Get the two nodes with lowest frequency
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        
        # Create a new internal node with the sum of frequencies
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        # Add the new node back to the queue
        heapq.heappush(priority_queue, merged)
    
    # The last remaining node is the root of the tree
    return priority_queue[0]

def build_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}
        
    # If we find a leaf (character), save the current code
    if node.char is not None:
        codes[node.char] = current_code or "0"  # To have a code even for a single character
        return codes
        
    # Recursively traverse the left and right subtree
    if node.left:
        build_huffman_codes(node.left, current_code + "0", codes)
    if node.right:
        build_huffman_codes(node.right, current_code + "1", codes)
        
    return codes

def huffman_encoding(text):
    if not text:
        return "", None
        
    # Build Huffman tree and generate codes
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    
    # Encode the text
    encoded_text = "".join(codes[char] for char in text)
    
    return encoded_text, root

def huffman_decoding(encoded_text, huffman_tree):
    if not encoded_text:
        return ""
        
    # Special case - only one unique character
    if huffman_tree.char is not None:
        return huffman_tree.char * len(encoded_text)
    
    decoded_text = []
    current_node = huffman_tree
    
    for bit in encoded_text:
        # Navigate the tree according to the bits
        if bit == '0':
            current_node = current_node.left
        else:  # bit == '1'
            current_node = current_node.right
            
        # If we reach a leaf, add the character and go back to the start
        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = huffman_tree
            
    return ''.join(decoded_text)

def calculate_compression_ratio(original_text, encoded_text):
    # Size of original text in bits (1 character = 8 bits)
    original_size = len(original_text) * 8
    
    # Size of compressed text in bits
    compressed_size = len(encoded_text)
    
    # Calculate compression ratio
    ratio = (compressed_size / original_size) * 100
    
    return ratio

def save_huffman_tree(huffman_tree, filename):
    with open(filename, 'wb') as file:
        pickle.dump(huffman_tree, file)

def load_huffman_tree(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# Examples
# Main program
if __name__ == "__main__":
    # Test the algorithm with a basic example
    text = "this is an example for huffman encoding"
    
    # Encode the text
    encoded_text, huffman_tree = huffman_encoding(text)
    print(f"Original text: {text}")
    print(f"Compressed text: {encoded_text}")
    
    # Decode the text
    decoded_text = huffman_decoding(encoded_text, huffman_tree)
    print(f"Decoded text: {decoded_text}")
    
    # Calculate compression ratio
    ratio = calculate_compression_ratio(text, encoded_text)
    print(f"Compression ratio: {ratio:.2f}%")
    
    # Demonstration of storing and loading the tree
    save_huffman_tree(huffman_tree, "huffman_tree.pkl")
    loaded_tree = load_huffman_tree("huffman_tree.pkl")
    
    # Check if the loaded tree works correctly
    decoded_from_loaded = huffman_decoding(encoded_text, loaded_tree)
    print(f"Decoded with loaded model: {decoded_from_loaded}")
    
    # Test with different types of input data
    test_texts = [
        "aaaaa",  # Text with a single unique character
        "abcdefghijklmnopqrstuvwxyz",  # Text with uniform distribution
        "the quick brown fox jumps over the lazy dog"  # Standard test text
    ]
    
    # Output results for each test case
    for test in test_texts:
        print("\n" + "="*50)
        print(f"Test: {test}")
        encoded, tree = huffman_encoding(test)
        compression = calculate_compression_ratio(test, encoded)
        decoded = huffman_decoding(encoded, tree)
        print(f"Compression ratio: {compression:.2f}%")
        print(f"Successfully decoded: {decoded == test}")