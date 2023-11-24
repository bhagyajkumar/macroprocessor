import re


def split_instruction(instruction):
    # Define a regular expression pattern for matching assembly instructions
    pattern = re.compile(r'^\s*([a-zA-Z_]\w*)?\s*([a-zA-Z]+)\s*(.*)$')
    # Use the pattern to match the input instruction
    match = pattern.match(instruction)

    if match:
        # Extract label, opcode, and operands from the matched groups
        label = match.group(1)
        opcode = match.group(2)
        operands = [operand.strip() for operand in match.group(3).split(',') if operand.strip()]

        # Create a dictionary to represent the structure
        result = {
            "label": label,
            "opcode": opcode,
            "operands": operands
        }

        return result
    else:
        return None
