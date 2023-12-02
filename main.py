from utils import InvalidMacroException, split_instruction
import pprint


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
        self.output_tab = []
        self.current_address = 0


    def get_line(self):
        if len(self.processed_content) == 0:
            return None
        self.current_address += 1
        return self.processed_content.pop(0)

    def process_macro(self):
        current_line = self.get_line()
        while (True):
            if current_line is None:
                break
            elif current_line["opcode"].lower() == "end":
                break

            if(current_line["opcode"].lower() == "macro"):
                self.fill_deftab(current_line["label"])
            else:
                current_line["index"] = self.current_address
                self.output_tab.append(current_line)
            print(current_line)
            current_line = self.get_line()


    def fill_deftab(self, macro_name:str):
        print("processing macro")
        name_tab_content = {
            "name" : macro_name,
            "start": self.current_address,
            "end" : None
        }
        processing = True
        while processing:
            current_line = self.get_line()
            if current_line is None:
                raise InvalidMacroException
            elif current_line["opcode"].lower() == "endmacro":
                name_tab_content["end"] = self.current_address
                processing = False
            else:
                current_line["index"] = self.current_address
                self.def_tab.append(current_line)
                print(current_line)
        self.name_tab.append(name_tab_content)
        print("Macro Processing Finished")




def main():
    macroprocessor = MacroProcessor("PGM.ASM")
    macroprocessor.process_macro()
    print("Deftab")
    pprint.pprint(
        macroprocessor.def_tab
    )
    print()

if __name__ == "__main__":
    main()

    

