# stego_lsb.py
from PIL import Image

# -------------------------
# Helper functions
# -------------------------
def _int_to_bits(n, length):
    return [(n >> i) & 1 for i in reversed(range(length))]

def _text_to_bits(text):
    data = text.encode('utf-8')
    bits = []
    for byte in data:
        bits.extend(_int_to_bits(byte, 8))
    return bits

def _bits_to_text(bits):
    bytes_out = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            break
        val = 0
        for b in byte_bits:
            val = (val << 1) | b
        bytes_out.append(val)
    return bytes(bytes_out).decode('utf-8', errors='replace')

# -------------------------
# Encode / Decode functions
# -------------------------
def encode_text_into_image(input_image_path, output_image_path, message):
    img = Image.open(input_image_path).convert('RGB')
    width, height = img.size
    capacity = width * height * 3          # total available LSBs (1 per channel)
    
    message_bits = _text_to_bits(message)
    message_length = len(message_bits)     # number of bits in the message
    total_bits = 32 + message_length       # 32 bits reserved to store message length
    
    if total_bits > capacity:
        raise ValueError(f"Image too small. Capacity={capacity} bits, required={total_bits} bits.")
    
    length_bits = _int_to_bits(message_length, 32)    # store length first (32 bits)
    bitstream = length_bits + message_bits
    
    pixels = list(img.getdata())
    new_pixels = []
    bit_idx = 0
    for (r,g,b) in pixels:
        if bit_idx < total_bits:
            r = (r & ~1) | bitstream[bit_idx]; bit_idx += 1
        if bit_idx < total_bits:
            g = (g & ~1) | bitstream[bit_idx]; bit_idx += 1
        if bit_idx < total_bits:
            b = (b & ~1) | bitstream[bit_idx]; bit_idx += 1
        new_pixels.append((r,g,b))
    new_img = Image.new('RGB', (width, height))
    new_img.putdata(new_pixels)
    new_img.save(output_image_path, 'PNG')
    return output_image_path

def decode_text_from_image(stego_image_path):
    img = Image.open(stego_image_path).convert('RGB')
    pixels = list(img.getdata())
    bits = []
    for (r,g,b) in pixels:
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)
    # first 32 bits = length
    length_bits = bits[:32]
    message_length = 0
    for b in length_bits:
        message_length = (message_length << 1) | b
    message_bits = bits[32:32+message_length]
    return _bits_to_text(message_bits)

# -------------------------
# Example usage (easy to change)
# -------------------------
if __name__ == "__main__":
    # Use the sample image created here OR replace with your own image path
    sample_image = "sample_image.png"
    # If you have your own image, put it in this project folder and set sample_image = "your_image.png"
    
    # Create a simple sample image (optional)
    width, height = 300, 300
    img = Image.new('RGB', (width, height))
    pixels = []
    for y in range(height):
        for x in range(width):
            r = (x * 255) // (width - 1)
            g = (y * 255) // (height - 1)
            b = ((x + y) * 255) // (width + height - 2)
            pixels.append((r,g,b))
    img.putdata(pixels)
    img.save(sample_image, 'PNG')
    
    # Change the message here to whatever you want to hide
    secret_message = "Hello Priyanshu — LSB stego test!"
    stego_output = "stego.png"
    
    encode_text_into_image(sample_image, stego_output, secret_message)
    print("Stego image saved to:", stego_output)
    decoded = decode_text_from_image(stego_output)
    print("Decoded message:\n", decoded)
