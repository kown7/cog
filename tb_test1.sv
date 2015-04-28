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

   test1 i_DUT (Clock, Clear, Ain, Bin, ABout);
   
program test_test1;

   default clocking cb @(posedge Clock);
      default input #1 output #4;
      input Ain, Bin;
      output ABout;
   endclocking // cb
   
   initial begin
      #10 Clear = 1;
      #10 Clear = 0;

      @(cb) Ain = 2;
      
      //@(cb) assert (ABout == 5'h2);
      assert (ABout == 5'h2);

      // Wait three clock cycles
      ##3;
      
      @(cb) Bin = 2;

      
      #100;
   end
   
endprogram // test_test1

endmodule // TB_test1
