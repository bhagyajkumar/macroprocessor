from utils import InvalidMacroException, MacroNotFound, split_instruction, CommandType
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
        
        self.original_processed = processed.copy()
        self.processed_content = processed.copy()
        self.def_tab = []
        self.name_tab = []
        self.inter_table = []
        self.current_address = 0
        self.is_processing_macro = False
        self.arguments = {}
        self.invocation_count = {}


    def get_line(self):
        if len(self.processed_content) == 0:
            return None
        #self.current_address += 1
        
        content =  self.processed_content.pop(0)
        self.inter_table.append(content)
        return content

    def process_macro(self):
        current_line = self.get_line()
        while (True):
            if current_line is None:
                break
            elif current_line["opcode"].lower() == "end":
                break

            if(current_line["opcode"].lower() == "macro"):
                self.fill_deftab(current_line["label"], arguments = [i for i in current_line["operands"]])
            else:
                current_line["index"] = self.current_address
            print(current_line)
            current_line = self.get_line()


    def fill_deftab(self, macro_name:str, arguments:list):
        self.arguments[macro_name] = arguments
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
            elif current_line["opcode"].lower() == "mend":
                name_tab_content["end"] = self.current_address - 1
                processing = False
            else:
                current_line["index"] = self.current_address
                self.def_tab.append(current_line)
                self.current_address += 1
        self.name_tab.append(name_tab_content)
        print("Macro Processing Finished")
    

    def is_macro(self, macro_name):
        for i in self.name_tab:
            if i["name"] == macro_name:
                return True
        return False


    def display_deftab(self):
        tabular_data = []
        for i in self.def_tab:
            tabular_data.append(
                ( i["index"], i["label"], i["opcode"], ",".join(x for x in i["operands"] ))
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
            headers = ["name", "start", "end", "arguments"],
            tabular_data = tabular_data,
            tablefmt="fancy_grid"
        )
        print(table)

    def display_output_tab(self):
        tabular_data = []
        for i in self.inter_table:
            tabular_data.append(
                (i["label"], i["opcode"], ",".join(x for x in i["operands"]))
            )

        table = tabulate(
            headers = ("label", "opcode", "operands"),
            tabular_data=tabular_data,
            tablefmt="fancy_grid"
        )
        print(table)

    def get_command_type(self, command):
        if command["opcode"] == "macro" and not self.is_processing_macro:
            self.is_processing_macro = True
            return CommandType.MACRO_LITERALS
        elif self.is_processing_macro and command["opcode"].lower() != "mend":
            return CommandType.DEFINITION
        elif self.is_processing_macro and command["opcode"].lower() == "mend":
            self.is_processing_macro = False
            return CommandType.MACRO_LITERALS
        elif self.is_macro(command["opcode"].lower()):
            return CommandType.INVOCATION
        return CommandType.NORMAL
    

    def get_macro_expansion(self,macro_name:str,params:list):
        try:
            inv_frequency = self.invocation_count[macro_name]
        except:
            inv_frequency, self.invocation_count[macro_name] = 0,0

        self.invocation_count[macro_name] = inv_frequency+1
        macro_info = None
        for i in self.name_tab:
            if i["name"] == macro_name:
                macro_info = i

        if macro_info is None:
            raise MacroNotFound

        expansion = []
        for i in range(macro_info["start"], macro_info["end"]):
            command = self.def_tab[i].copy()
            command["label"] = command.get("label", "").replace("$", str(inv_frequency))
            expansion.append(command)

        for i in range(len(expansion)):
            for j in range(len(expansion[i]["operands"])):
                expansion[i]["operands"][j] = params[j]
        
        return expansion


    def generate_processed_assembly(self):
        # __imrort__('pprint').pprint(self.original_processed)
        for i in self.original_processed:
            command_type = self.get_command_type(i)
            if command_type == CommandType.NORMAL:
                print(self.detokenize(i))
            elif command_type == CommandType.INVOCATION:
                invocation = self.get_macro_expansion(i["opcode"], i["operands"])
                for i in invocation:
                    print(self.detokenize(i))
            else:
                # print(self.detokenize(i))
                pass
    
    def detokenize(self, command:dict):
        detokenized = "{}\t{}\t{}".format(command["label"], command["opcode"], ",".join(i for i in command["operands"]))
        return detokenized

def main():
    macroprocessor = MacroProcessor("PGM.ASM")
    macroprocessor.process_macro()
    print("Deftab")
    macroprocessor.display_deftab()
    print("NameTab")
    macroprocessor.display_nametab()
    print("OutputTab")
    macroprocessor.display_output_tab()
    print("test op")
    macroprocessor.generate_processed_assembly()

if __name__ == "__main__":
    main()

    

