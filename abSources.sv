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
