import sys

def parse(command, mem, pc):
    args = command.split(" ")
    if args[0] == "MOV":
        handle_mov(args, mem)
    elif args[0] == "ADD":
        handle_add(args, mem)
    elif args[0] == "SUB":
        handle_sub(args, mem)
    elif args[0] == "JMP":
        return handle_jmp(args, pc)
    elif args[0] == "HLT":
        disp_mem(mem)
    else:
        print(f"Invalid command: {args[0]} at line {pc + 1}")
        return pc + 1  # Skip to the next command

def handle_mov(args, mem):
    i = 1
    add1 = add2 = None
    val = None
    for arg in args[1:]:
        if arg.startswith("[") and arg.endswith("]"):
            if i == 1:
                add1 = arg.strip("[]")
            elif i == 2:
                add2 = arg.strip("[]")
                val = mem_acc(mem, add2)
        elif arg.isdigit():
            if i == 1:
                add1 = arg
            elif i == 2:
                val = int(arg)
        elif arg in ["reg1", "reg2", "reg3"]:
            if i == 1:
                add1 = arg
            elif i == 2:
                add2 = arg
                val = mem_acc(mem, add2)
        else:
            print(f"Invalid MOV syntax at line {i}")
            return mem
        i += 1
    mem_update(mem, add1, val)
    return mem

def handle_add(args, mem):
    val1, val2, add1 = ret_val(args, mem)
    val1 = val1 + val2
    mem_update(mem, add1, val1)
    return val1, mem

def handle_sub(args, mem):
    val1, val2, add1 = ret_val(args, mem)
    val1 = val1 - val2
    mem_update(mem, add1, val1)
    return val1, mem

def handle_jmp(args, pc):
    try:
        return int(args[1])
    except ValueError:
        print(f"Invalid JMP address at line {pc + 1}")
        return pc + 1

def ret_val(args, mem):
    val1 = val2 = None
    add1 = None
    for i in range(1, 3):
        arg = args[i]
        if arg.startswith("[") and arg.endswith("]"):
            if i == 1:
                add1 = arg.strip("[]")
                val1 = mem_acc(mem, add1)
            elif i == 2:
                add2 = arg.strip("[]")
                val2 = mem_acc(mem, add2)
        elif arg.isdigit():
            if i == 1:
                val1 = int(arg)
            elif i == 2:
                val2 = int(arg)
        elif arg in ["reg1", "reg2", "reg3"]:
            if i == 1:
                val1 = mem_acc(mem, arg)
            elif i == 2:
                val2 = mem_acc(mem, arg)
    return val1, val2, add1

def mem_acc(mem, arg):
    for m in mem:
        if m.get("add") == arg:
            return m.get("val", 0)
    print(f"Address '{arg}' not found in memory.")
    return 0

def mem_update(mem, add, val):
    for entry in mem:
        if entry["add"] == add:
            entry["val"] = val
            return
    mem.append({"add": add, "val": val})

def disp_mem(mem):
    for entry in mem:
        print(f"address: {entry['add']}, value: {entry['val']}")
    sys.exit()

def load_commands_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

def main():
    print("Enter the program. Type '.' in a new line to stop, init pc=0")
    print("Caution: Error handling is not present in earlier versions!")
    
    lines = []
    file_path = input("Enter file path (leave empty for CLI input): ").strip()
    
    if file_path:
        lines = load_commands_from_file(file_path)
    else:
        while True:
            line = input()
            if line.strip() == ".":
                break
            lines.append(line)
    
    commands = [line.strip() for line in lines if line.strip()]
    pc = 0
    mem = [{"add": "reg1", "val": 0}, {"add": "reg2", "val": 0}, {"add": "reg3", "val": 0}]
    
    while pc < len(commands):
        result = parse(commands[pc], mem, pc)
        if result is not None:
            pc = result
        else:
            pc += 1

if __name__ == "__main__":
    main()
