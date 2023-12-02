from utils import InvalidMacroException, split_instruction
from tabulate import tabulate

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
        self.output_table = []
        self.current_address = 0


    def get_line(self):
        if len(self.processed_content) == 0:
            return None
        self.current_address += 1
        
        content =  self.processed_content.pop(0)
        self.output_table.append(content)
        return content

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
                self.def_tab.append(current_line)
            print(current_line)
            current_line = self.get_line()


    def fill_deftab(self, macro_name:str):
        print("processing macro")
        name_tab_content = {
            "name" : macro_name,
            "start": self.current_address + 1,
            "end" : None
        }
        processing = True
        while processing:
            current_line = self.get_line()
            if current_line is None:
                raise InvalidMacroException
            elif current_line["opcode"].lower() == "endmacro":
                name_tab_content["end"] = self.current_address - 1
                processing = False
            else:
                current_line["index"] = self.current_address
                self.def_tab.append(current_line)
                print(current_line)
        self.name_tab.append(name_tab_content)
        print("Macro Processing Finished")


    def display_deftab(self):
        tabular_data = []
        for i in self.def_tab:
            tabular_data.append(
                (i["index"], i["label"], i["opcode"], ",".join(x for x in i["operands"] ))
            )
        table = tabulate(
            headers=["address", "label", "opcode", "operands"],
            tabular_data=tabular_data,
            tablefmt="fancy_grid"
        )
        print(table)


    def display_nametab(self):
        tabular_data = []
        for i in self.name_tab:
            tabular_data.append(
                (i["name"], i["start"], i["end"])
            )
        table = tabulate(
            headers = ["name", "start", "end"],
            tabular_data = tabular_data,
            tablefmt="fancy_grid"
        )
        print(table)

    def display_output_tab(self):
        tabular_data = []
        for i in self.output_table:
            tabular_data.append(
                (i["label"], i["opcode"], ",".join(x for x in i["operands"]))
            )

        table = tabulate(
            headers = ("label", "opcode", "operands"),
            tabular_data=tabular_data,
            tablefmt="fancy_grid"
        )
        print(table)



def main():
    macroprocessor = MacroProcessor("PGM.ASM")
    macroprocessor.process_macro()
    print("Deftab")
    macroprocessor.display_deftab()
    print("NameTab")
    macroprocessor.display_nametab()
    print("OutputTab")
    macroprocessor.display_output_tab()

if __name__ == "__main__":
    main()

    

