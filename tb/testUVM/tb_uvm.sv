import uvm_pkg::*;
`include "uvm_macros.svh"

class env extends uvm_env;

   virtual dutif d_if;

   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new

   function void connect_phase(uvm_phase phase);
      `uvm_info("LABEL", "Started connect phase.", UVM_HIGH);
      // Get the interface from the resource database.
      assert(uvm_resource_db#(virtual dutif)::read_by_name(get_full_name(), "dutif", d_if));
      `uvm_info("LABEL", "Finished connect phase.", UVM_HIGH);
   endfunction: connect_phase

   task run_phase(uvm_phase phase);
      phase.raise_objection(this);
      `uvm_info("LABEL", "Started run phase.", UVM_HIGH);
      begin
         int a = 4'h2, b = 4'h3;
         @(d_if.cb);
         d_if.cb.Ain <= a;
         d_if.cb.Bin <= b;
         repeat(2) @(d_if.cb);
	 if (d_if.cb.ABout == a+b) begin
           `uvm_info("RESULT", $sformatf("%0d + %0d = %0d", a, b, d_if.cb.ABout), UVM_LOW);
	 end else begin
	   `uvm_error("RESULT", $sformatf("%0d + %0d != %0d", a, b, d_if.cb.ABout));
	 end
	 if (d_if.cb.ABout == a+b+1) begin
           `uvm_info("RESULT", $sformatf("%0d + %0d + 1 = %0d", a, b, d_if.cb.ABout), UVM_LOW);
	 end else begin
	   `uvm_error("RESULT", $sformatf("%0d + %0d + 1 != %0d", a, b, d_if.cb.ABout));
	 end	 
	 
	 #200ns;
      end


      `uvm_info("LABEL", "Finished run phase.", UVM_HIGH);
      phase.drop_objection(this);
  endtask: run_phase

endclass // env


module tb_uvm;
   bit clk;
   env environment;
   dutif iface(clk);
   DUTSV dut(iface);

   initial begin
      clk = 0;
      environment = new("env");
      // Put the interface into the resource database.
      uvm_resource_db#(virtual dutif)::set("env", "dutif", iface);
      run_test();
   end

   initial begin
      forever begin
	 #(50) clk = ~clk;
      end
   end


endmodule // tb_uvm




interface dutif (input Clock);
   logic Clear = 0;
   logic [3:0] Ain = 0, Bin = 0;
   logic [4:0] ABout;

   wire [4:0] ABL;
   assign ABL = ABout;

   default clocking cb @(posedge Clock);
      default input #1ns output #1ns;
      output Ain, Bin, Clear;
      input ABout;
   endclocking // cb

   modport tb (input Clock, clocking cb);
endinterface // dutif


module DUTSV(dutif iface);
   test1 i_DUT (.Clk(iface.Clock), .Clr(iface.Clear), .Test1_A(iface.Ain), .Test1_B(iface.Bin), .Test1_AB(iface.ABout));
endmodule // DUTSV
