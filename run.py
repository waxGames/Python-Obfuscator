from pyobfuscator import inflate, deflate, unicode_compress, unicode_decompress

# It is recommended to Obfuscate with UniCode.

#Example:
code = """
print("hello world!")
"""

def preprocess_code(input_code: str) -> str:
    return ''.join(c for c in input_code if ord(c) < 128)

code = preprocess_code(code)

inflated_code = inflate(code)
original_code = deflate(inflated_code)

compressed_code = unicode_compress(code)
original_uni_code = unicode_decompress(code)

print(f"obfuscated code: {inflated_code}\n")
print(f"obfuscated unicode: {compressed_code}\n")
print(f"obfuscated decode: {original_code}\n")
print(f"obfuscated deunicode: {original_uni_code}\n")

with open("output/obfuscated.py", "w", encoding="UTF-8") as f:
    f.write(inflated_code)

with open("output/obfuscated_uni.py", "w", encoding="UTF-8") as f:
    f.write(compressed_code)
