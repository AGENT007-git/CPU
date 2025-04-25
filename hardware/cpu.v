module cpu (
    input clk,
    input rst
);

    // Program Counter
    reg [7:0] pc;

    // Instruction Memory
    reg [18:0] imem [0:255];

    // Data Memory (First 256 addresses = registers)
    reg [7:0] dmem [0:511];

    // Support Registers
    reg [7:0] sreg [0:3];
    reg cflag; // Carry / compare flag

    // Instruction Register (IF stage)
    reg [18:0] ireg;

    // Decoded Fields
    wire [2:0] opcode = ireg[18:16];
    wire [7:0] op1 = ireg[15:8];
    wire [7:0] op2 = ireg[7:0];

    // Control Signals (1-hot)
    wire is_mov = (opcode == 3'b000);
    wire is_add = (opcode == 3'b001);
    wire is_sub = (opcode == 3'b010);
    wire is_cmp = (opcode == 3'b011);
    wire is_jmp = (opcode == 3'b100);
    wire is_hlt = (opcode == 3'b101);

    // Cycle Counter (2-bit upcounter)
    reg [1:0] cycle;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            pc <= 8'd0;
            cycle <= 2'd0;
            cflag <= 1'b0;
        end else begin
            case (cycle)
                2'd0: begin // IF (Instruction Fetch)
                    ireg <= imem[pc];
                    cycle <= 2'd1;
                end

                2'd1: begin // DECODE / EXECUTE
                    if (is_mov)  
                        sreg[0] <= dmem[op2]; // MOV R1, R2
                    if (is_add)  
                        sreg[0] <= dmem[op1] + dmem[op2]; // ADD R1, R2
                    if (is_sub)  
                        sreg[0] <= dmem[op1] - dmem[op2]; // SUB R1, R2
                    if (is_cmp)  
                        cflag <= (dmem[op1] == dmem[op2]); // CMP R1, R2 (set cflag on equal)
                    cycle <= 2'd2;
                end

                2'd2: begin // WRITEBACK (Update Memory)
                    if (is_mov || is_add || is_sub)
                        dmem[op1] <= sreg[0]; // Write result back to data memory
                    cycle <= 2'd3;
                end

                2'd3: begin // PC UPDATE (Update the Program Counter)
                    if (is_jmp && cflag)
                        pc <= op1; // Jump if cflag is set
                    else if (is_hlt)
                        pc <= 8'd0; // Halt and reset PC
                    else
                        pc <= pc + 1; // Increment PC
                    cycle <= 2'd0;
                end
            endcase
        end
    end

endmodule
