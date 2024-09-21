from queue import Queue

def create_queue(bit_string):
    # Clean the bit_string to remove any non-binary characters (like tabs, spaces, etc.)
    bit_string = ''.join(filter(lambda x: x in '01', bit_string))

    # Ensure the bit string length is a multiple of 8
    if len(bit_string) % 8 != 0:
        bit_string = bit_string.ljust(len(bit_string) + (8 - len(bit_string) % 8), '0')
    
    # Group the bit string into 8-bit segments
    groups = [bit_string[i:i+8] for i in range(0, len(bit_string), 8)]
    
    # Create queues
    queue_vbig = Queue()  # Values between 192 and 255
    queue_big = Queue()   # Values between 128 and 191
    queue_sml = Queue()   # Values between 64 and 127
    queue_vsml = Queue()  # Values between 0 and 63
    queue_map = Queue()   # To store the queue identification

    # Scan the 8-bit groups and assign them to queues based on their decimal value
    for group in groups:
        decimal_value = int(group, 2)

        # Assign the decimal value to the appropriate queue and map queue
        if 0 <= decimal_value <= 63:  # Range for vsml
            queue_vsml.put(decimal_value)
            queue_map.put('vsml')  # Map queue indicating the queue source
        elif 64 <= decimal_value <= 127:  # Range for sml
            queue_sml.put(decimal_value)
            queue_map.put('sml')
        elif 128 <= decimal_value <= 191:  # Range for big
            queue_big.put(decimal_value)
            queue_map.put('big')
        elif 192 <= decimal_value <= 255:  # Range for vbig
            queue_vbig.put(decimal_value)
            queue_map.put('vbig')

    return queue_vbig, queue_big, queue_sml, queue_vsml, queue_map

# Example usage for testing
"""
bit_string = "100001010111010111110010001011010101111000111011100011001000010101100101111110111001110101110011001101110100000110000011000000010010111011010010011100100101001011001100000100101101010110010100000011000000101001111101111001011101111100000011100010100011010110011000110011100000"
queue_vbig, queue_big, queue_sml, queue_vsml, queue_map = create_queue(bit_string)

# Print the contents of each queue for debugging

print("\nQueue vbig:")
while not queue_vbig.empty():
    print(queue_vbig.get())

print("\nQueue big:")
while not queue_big.empty():
    print(queue_big.get())

print("\nQueue sml:")
while not queue_sml.empty():
    print(queue_sml.get())

print("\nQueue vsml:")
while not queue_vsml.empty():
    print(queue_vsml.get())

print("\nQueue map:")
while not queue_map.empty():
    print(queue_map.get())
"""
