module TB_test1;
   timeunit 1ns;

   reg Clock = 0, Clear = 0;
   reg [3:0] Ain = 0, Bin = 0;
   wire [4:0] ABout;

   always
     begin
	#5 Clock = 1;
	#5 Clock = 0;
     end

   test1 i_DUT (.Clk(Clock), .Clr(Clear), .Test1_A(Ain), .Test1_B(Bin), .Test1_AB(ABout)); 

   class abSources;
     rand int Ain, Bin;
     int seed = $time;
     
     constraint common { Ain <= 10; Ain > 0; }
     
     task inc();
        begin
     	 Ain = ABS($random(seed) % 2**4);
     	 Bin = ABS($random(seed) % 2**4);
        end;
     endtask; // inc
     
     task print();
        begin
     	 $write("A: %2d; B: %2d\n", Ain, Bin);
        end;
     endtask; // print
     
     function int ABS (int num);
        ABS = (num <0) ? -num : num;
     endfunction // ABS
   endclass; // abSources

program test_test1;

   abSources absrc;
   
   default clocking cb @(posedge Clock);
      default input #1 output #4;
      input Ain, Bin;
      output ABout;
   endclocking // cb

   initial begin
      absrc = new;

      ##10 Clear = 1;
      ##100 Clear = 0;

      @(cb) Ain = 2;
      @(cb) assert (ABout == 5'h2);

      // Wait three clock cycles
      ##3;

      for (int i = 0; i < 3; i++) begin
	 // Missing licence for randomize()
	 //absrc.randomize();
	 @(cb) absrc.inc();
	 absrc.print();
	 Ain = absrc.Ain;
	 Bin = absrc.Bin;
	 fork
	    assertABio(absrc.Ain, absrc.Bin);
	 join_none;
      end;

      #100;
   end // initial begin
   
   
   task assertABio;
      input a, b;
      integer a, b;
      begin
	 ##2 assert (ABout == (a + b)) $display("Good A: %2d; B: %2d\n", a, b);
	     else $error("Bad A: %2d; B: %2d\n", a, b);
      end;
   endtask; // assertABio

endprogram // test_test1

endmodule // TB_test1
