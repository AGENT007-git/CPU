itCustom 8-bit CPU System (Interpreter + Verilog Core)
This project is a full-stack experiment in processor design — from a Python-based virtual CPU interpreter to a Verilog implementation of a pipelined RISC-like CPU. It's built from scratch with minimal abstraction, focusing on how instruction sets, registers, memory, and control logic really work.

Project Structure
.
├── interpreter/     # Python-based CPU simulation
│   └── cpu.py       # Executes MOV, ADD, SUB, JMP, CMP, HLT on virtualmemory
├── hardware/        # Verilog-based CPU module
│   └── cpu.v        # 4-stage pipeline with 19-bit custom instruction format
├── README.md        # This file
Features
Interpreter
Assembly-like instruction parser and executor

Memory modeled as 256 8-bit registers

Supports:

MOV, ADD, SUB, JMP, HLT

Verilog CPU
4-stage pipeline: Fetch → Decode/Exec → Writeback → PC Update

19-bit instruction format: [OPCODE (3)] [OP1 (8)] [OP2 (8)]

256-byte instruction memory and 512-byte data memory

Carry flag (CFLAG) for CMP/JMP flow control

Cycle-managed using a 2-bit state counter

Goals
Understand instruction encoding and CPU internals deeply.

Simulate and test architectures without relying on toolchain abstractions.

Build a base to expand into:

I/O-mapped devices

Assembler integration

Real FPGA deployment

Future Plans
Add assembler to convert human-readable instructions into binary

Expand instruction set (e.g., AND, OR, SHL)

Implement I/O peripherals via memory mapping

License
MIT License — use freely, credit appreciated.

Author
Built by a self-taught developer focused on embedded systems, digital design, and low-level tools.

just code.
Reach out for collaborations, contributions, or project help.
