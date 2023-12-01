from utils import split_instruction
import pprint



# The output after processing the command will be the following
# [{'label': 'copy', 'opcode': 'start', 'operands': ['1000']},
#  {'label': 'mov', 'opcode': 'alpha', 'operands': ['gamma']},
#  {'label': 'mov', 'opcode': 'alpha', 'operands': ['beta']},
#  {'label': 'mov', 'opcode': 'beta', 'operands': ['gamma']},
#  {'label': 'alpha', 'opcode': 'resw', 'operands': ['1']},
#  {'label': 'beta', 'opcode': 'resw', 'operands': ['1']},
#  {'label': 'gamma', 'opcode': 'resw', 'operands': ['1']}]
#

class MacroProcessor():

    def __init__(self, file_name):
        with open(file_name) as f:
            content = f.read()
            content = content.strip()
        lines = content.split("\n")
        processed = []
        for i in lines:
            processed.append(split_instruction(i))
        
        self.processed_content = processed
        self.def_tab = []
        self.name_tab = []


    def get_line(self):
        return self.processed_content.pop(0)

    def get_macro_output(self):
        current_line = self.get_line()
        while (current_line["opcode"].lower() != "end"):
            pass
        return current_line
        # while(current_line[])



def main():
    macroprocessor = MacroProcessor("PGM.ASM")
    pprint.pprint(macroprocessor.get_macro_output())


if __name__ == "__main__":
    main()

    

