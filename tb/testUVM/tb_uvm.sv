import uvm_pkg::*;
`include "uvm_macros.svh"


module tb_uvm;
   bit clk;
   Env environment;
   dutif iface(clk);
   DUTSV dut(iface);

   initial begin
      clk = 0;
      //uvm_config_db#(virtual dutif)::set(null, "uvm_test_top", "dutif", iface);
      ////                                        ^^ Always top level
      uvm_config_db#(virtual dutif)::set(null, "*", "dutif", iface);
      run_test("DataTest1");
   end

   initial begin
      forever begin
	 #(50) clk = ~clk;
      end
   end
endmodule // tb_uvm


class DataPointsTransaction extends uvm_sequence_item;
   rand int a, b;

   constraint a_inp { a >= 0; a < 2**4-1; }
   constraint b_inp { b >= 0; b < 2**4-1; }
   
   `uvm_object_utils_begin(DataPointsTransaction)
      `uvm_field_int(a, UVM_ALL_ON)
      `uvm_field_int(b, UVM_ALL_ON)
   `uvm_object_utils_end

   function new (string name = "");
      super.new(name);
   endfunction : new // new
endclass


typedef uvm_sequencer #(DataPointsTransaction) DataSequencer;


class DataSequence extends uvm_sequence #(DataPointsTransaction);
   `uvm_object_utils(DataSequence)

   function new (string name = "");
      super.new(name);
   endfunction // new

   task body;
      int a = 0;
      
      do begin
	 DataPointsTransaction my_tx;
	 my_tx = DataPointsTransaction::type_id::create("my_tx");

	 start_item(my_tx);
	 assert(my_tx.randomize());
	 a++;
	 finish_item(my_tx);
      end while (a < 100);
   endtask: body
endclass // DataSequence


class DataDriver extends uvm_driver #(DataPointsTransaction);
   `uvm_component_utils(DataDriver)
   virtual dutif d_if;

   function new (string name = "", uvm_component parent);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      //assert(uvm_resource_db#(virtual dutif)::read_by_name(get_full_name(), "dutif", d_if));
      assert(uvm_config_db#(virtual dutif)::get(this, "", "dutif", d_if));
   endfunction // assert
      
   task run_phase(uvm_phase phase);
      forever
	begin
	   DataPointsTransaction tx;
	   @(posedge d_if.cb);
	   seq_item_port.get_next_item(tx);
	   d_if.Ain = tx.a;
	   d_if.Bin = tx.b;
	   @(posedge d_if.cb);
	   seq_item_port.item_done();
	end
   endtask // run_phase
   
endclass // DataDriver


class DataAgent extends uvm_agent;
   `uvm_component_utils(DataAgent)

   DataDriver d_drive;
   DataSequencer d_seqr;

   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      d_drive = DataDriver::type_id::create("d_drive", this);
      d_seqr = DataSequencer::type_id::create("d_seqr", this);
   endfunction // build_phase

   function void connect_phase(uvm_phase phase);
      d_drive.seq_item_port.connect(d_seqr.seq_item_export);
   endfunction // connect_phase
   
endclass // DataAgent

   
class Env extends uvm_env;
   `uvm_component_utils(Env)
   DataAgent d_agent;
   
   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      d_agent = DataAgent::type_id::create("d_agent", this);
   endfunction // run_phase

   task run_phase(uvm_phase phase);
      begin
	 phase.raise_objection(this);
	 `uvm_info("LABEL", "Started run phase.", UVM_HIGH);
	 
	 //if (d_if.cb.ABout == a+b) begin
         //  `uvm_info("RESULT", $sformatf("%0d + %0d = %0d", a, b, d_if.cb.ABout), UVM_LOW);
	 //end else begin
	 //  `uvm_error("RESULT", $sformatf("%0d + %0d != %0d", a, b, d_if.cb.ABout));
	 //end
	 
	 //if (d_if.cb.ABout == a+b+1) begin
         //  `uvm_info("RESULT", $sformatf("%0d + %0d + 1 = %0d", a, b, d_if.cb.ABout), UVM_LOW);
	 //end else begin
	 //  `uvm_error("RESULT", $sformatf("%0d + %0d + 1 != %0d", a, b, d_if.cb.ABout));
	 //end
	 
	 #200ns;
	 `uvm_info("LABEL", "Finished run phase.", UVM_HIGH);
	 phase.drop_objection(this);
      end
  endtask: run_phase
endclass // env


class DataTest1 extends uvm_test;
   `uvm_component_utils(DataTest1)
   Env e;

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      e = Env::type_id::create("e", this);
   endfunction // build_phase
   
   task run_phase(uvm_phase phase);
      DataSequence seq;
      seq = DataSequence::type_id::create("seq");
      phase.raise_objection(this);
      seq.start(e.d_agent.d_seqr);
      phase.drop_objection(this);
   endtask; // run_phase

endclass // DataTest1



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
