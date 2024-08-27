from queue import Queue

def create_queue(bit_string):
    # Ensure the bit string length is a multiple of 6
    if len(bit_string) % 6 != 0:
        bit_string = bit_string.ljust(len(bit_string) + (6 - len(bit_string) % 6), '0')
    
    # Group the bit string into 6-bit segments
    groups = [bit_string[i:i+6] for i in range(0, len(bit_string), 6)]
    
    # Create queues
    queue_big = Queue()
    queue_sml = Queue()
    queue_map = Queue()
    
    # Scan the first 3 bits of each 6-bit group and place them into the appropriate queue
    for group in groups:
        first_three_bits = group[:3]
        if '000' <= first_three_bits <= '011':
            decimal_value = int(group, 2)
            queue_sml.put(decimal_value)
            queue_map.put(0)
        else:
            decimal_value = int(group, 2)
            queue_big.put(decimal_value)
            queue_map.put(1)
    
    return  queue_big, queue_sml, queue_map


"""
# Example usage
bit_string = "100001010111010111110010001011010101111000111011100011001000010101100101111110111001110101110011001101110100000110000011000000010010111011010010011100100101001011001100000100101101010110010100000011000000101001111101111001011101111100000011100010100011010110011000110011100000"
queue_big, queue_sml, queue_map = create_queue(bit_string)

# Print the contents of each queue

print("\nQueue 1:")
while not queue_big.empty():
    print(queue_big.get())

print("\nQueue Mid:")
while not queue_sml.empty():
    print(queue_sml.get())

print("\nQueue Map:")
while not queue_map.empty():
    print(queue_map.get())
"""
