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

program test_test1;
   initial begin
      #10 Clear = 1;
      #10 Clear = 0;

      #10 Ain = 2;
   end
   
endprogram // test_test1

endmodule // TB_test1
