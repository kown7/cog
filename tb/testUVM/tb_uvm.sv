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
endclass // DataPointsTransaction

class ResultTransaction extends uvm_sequence_item;
   int ab;

   `uvm_object_utils_begin(ResultTransaction)
      `uvm_field_int(ab, UVM_ALL_ON)
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
   uvm_analysis_port #(DataPointsTransaction) stim_aport;

   function new (string name = "", uvm_component parent);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      //assert(uvm_resource_db#(virtual dutif)::read_by_name(get_full_name(), "dutif", d_if));
      assert(uvm_config_db#(virtual dutif)::get(this, "", "dutif", d_if));
      stim_aport = new("stim_aport", this);
   endfunction // assert
      
   task run_phase(uvm_phase phase);
      forever
	begin
	   DataPointsTransaction tx;
	   @(posedge d_if.cb);
	   seq_item_port.get_next_item(tx);
	   stim_aport.write(tx);
	   d_if.Ain = tx.a;
	   d_if.Bin = tx.b;
	   d_if.AinVld = 1;
	   d_if.BinVld = 1;
	   @(posedge d_if.cb);
	   seq_item_port.item_done();
	   d_if.AinVld = 0;
	   d_if.BinVld = 0;
	end
   endtask // run_phase
   
endclass // DataDriver


class DataMonitor extends uvm_monitor;
   `uvm_component_utils(DataMonitor);
   uvm_analysis_port #(ResultTransaction) aport;
   virtual dutif d_if;

   function new (string name = "", uvm_component parent);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      aport = new("aport", this);
      assert(uvm_config_db#(virtual dutif)::get(this, "", "dutif", d_if));
   endfunction // assert

   task run_phase(uvm_phase phase);
      forever begin
	 ResultTransaction tx;
	 @(posedge d_if.cb);
	 if (d_if.cb.ABvld == 1) begin
	    tx = ResultTransaction::type_id::create("tx");
	    tx.ab = d_if.cb.ABout;
	    aport.write(tx); 
	 end
      end
   endtask // run_phase
endclass


class DataAgent extends uvm_agent;
   `uvm_component_utils(DataAgent)
   
   DataDriver d_drive;
   DataSequencer d_seqr;
   DataMonitor d_mon;
   uvm_analysis_port #(ResultTransaction) aport;
   uvm_analysis_port #(DataPointsTransaction) stim_aport;
   
   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      d_drive = DataDriver::type_id::create("d_drive", this);
      d_seqr = DataSequencer::type_id::create("d_seqr", this);
      d_mon = DataMonitor::type_id::create("d_mon", this);
      aport = new("aport", this);
      stim_aport = new("stim_aport", this);
   endfunction // build_phase

   function void connect_phase(uvm_phase phase);
      d_drive.seq_item_port.connect(d_seqr.seq_item_export);
      d_drive.stim_aport.connect(stim_aport);
      d_mon.aport.connect(aport);
   endfunction // connect_phase
   
endclass // DataAgent


class Predictor extends uvm_subscriber #(DataPointsTransaction);
   `uvm_component_utils(Predictor)
   uvm_analysis_port #(ResultTransaction) exp_aport;

   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      exp_aport = new("exp_aport", this);
   endfunction // build_phase

   function void write(DataPointsTransaction t);
      ResultTransaction res_tx;
      res_tx = ResultTransaction::type_id::create("res_tx");
      res_tx.ab = t.a + t.b;
      exp_aport.write(res_tx);
   endfunction // write
endclass // Predictor


class Comparator extends uvm_component;
   `uvm_component_utils(Comparator)

   uvm_analysis_export #(ResultTransaction) exp_export;
   uvm_analysis_export #(ResultTransaction) act_export;

   uvm_tlm_analysis_fifo #(ResultTransaction) exp_fifo;
   uvm_tlm_analysis_fifo #(ResultTransaction) act_fifo;
      
   int m_matches, m_mismatches;
   
   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new
   
   function void build_phase(uvm_phase phase);
      exp_export = new("exp_export", this);
      act_export = new("act_export", this);
      exp_fifo = new("exp_fifo", this);
      act_fifo = new("act_fifo", this);
   endfunction // build_phase

   function void connect_phase(uvm_phase phase);
      exp_export.connect(exp_fifo.analysis_export);
      act_export.connect(act_fifo.analysis_export);
   endfunction // connect_phase

   task run_phase(uvm_phase phase);
      string s; 
      ResultTransaction exp_txn, act_txn; 
      forever begin
	 exp_fifo.get(exp_txn);
	 act_fifo.get(act_txn);
	 if (!exp_txn.compare(act_txn)) begin
	    `uvm_error("Comparator Mismatch", $sformatf("%s does not match %s", 
						       exp_txn.convert2string(), 
						       act_txn.convert2string()));
	    m_mismatches++;
	 end
	 else begin
	    m_matches++;
	 end
      end
   endtask // run_phase
   
   function void report_phase(uvm_phase phase);
      `uvm_info("InorderComparator",$sformatf("Matches:    %0d", m_matches), UVM_LOW)
      `uvm_info("InorderComparator", $sformatf("Mismatches: %0d", m_mismatches), UVM_LOW)
  endfunction // report_phase
endclass // ComparatorInorder
   

class Scoreboard extends uvm_component;
  `uvm_component_utils(Scoreboard)

   uvm_analysis_port #(DataPointsTransaction) exp_in_aport;
   uvm_analysis_port #(ResultTransaction) act_aport;

   Predictor pred;
   Comparator comp;
   
   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      exp_in_aport = new("exp_in_aport", this);
      act_aport = new("act_aport", this);
      pred = Predictor::type_id::create("pred", this);
      comp = Comparator::type_id::create("comp", this);
   endfunction // build_phase
   
   function void connect_phase(uvm_phase phase);
      act_aport.connect(comp.act_export);
      pred.exp_aport.connect(comp.exp_export);
      exp_in_aport.connect(pred.analysis_export);
   endfunction // connect_phase

   function bit passfail();
      return 0;
   endfunction // passfail

   function void summarize();
      $display("pipapo");
   endfunction // summarize
   
endclass // Scoreboard


class DataSubscriber extends uvm_subscriber #(ResultTransaction);
   `uvm_component_utils(DataSubscriber);
   
   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new

   function void write(ResultTransaction t);
      $display(t.ab);
   endfunction // write
endclass // DataSubscriber

   
class Env extends uvm_env;
   `uvm_component_utils(Env)
   DataAgent d_agent;
   //DataSubscriber d_sub;
   Scoreboard d_score;
      
   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction // new

   function void build_phase(uvm_phase phase);
      d_agent = DataAgent::type_id::create("d_agent", this);
      //d_sub = DataSubscriber::type_id::create("d_sub", this);
      d_score = Scoreboard::type_id::create("d_score", this);
   endfunction // run_phase

   function void connect_phase(uvm_phase phase);
      //d_agent.aport.connect(d_sub.analysis_export);
      d_agent.aport.connect(d_score.act_aport);
      d_agent.stim_aport.connect(d_score.exp_in_aport);
   endfunction // connect_phase
   
   task run_phase(uvm_phase phase);
      begin
	 phase.raise_objection(this);
	 `uvm_info("LABEL", "Started run phase.", UVM_HIGH);
	 
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
   logic       AinVld = 0, BinVld = 0;
   logic [4:0] ABout;
   logic       ABvld;

   wire [4:0] ABL;
   assign ABL = ABout;

   default clocking cb @(posedge Clock);
      default input #1ns output #1ns;
      output Ain, Bin, AinVld, BinVld, Clear;
      input ABout, ABvld;
   endclocking // cb

   modport tb (input Clock, clocking cb);
endinterface // dutif


module DUTSV(dutif iface);
   test1vld i_DUT (.Clk(iface.Clock), .Clr(iface.Clear), .Test1_A(iface.Ain), .Test1_B(iface.Bin),
		   .Test1_A_vld(iface.AinVld), .Test1_B_vld(iface.BinVld),
		   .Test1_AB(iface.ABout), .Test1_AB_vld(iface.ABvld));
endmodule // DUTSV
