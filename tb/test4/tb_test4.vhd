library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_test4 is
  
end entity tb_test4;

architecture rtl of tb_test4 is

  constant END_SIM_TIME : time := 1 us;
  
  signal Clk      : std_logic := '0';
  signal Clr      : std_logic;
  
  signal Test1_A  : std_logic_vector(3 downto 0);
  signal Test1_B  : std_logic_vector(3 downto 0);
  signal Test1_AB : std_logic_vector(4 downto 0);

begin  -- architecture rtl

  Clk <= not Clk after 5 ns when now < END_SIM_TIME else
         '0';
  Clr <= '0', '1' after 10 ns, '0' after 100 ns;
  
  
  test1_1: entity work.test1
    port map (
      Clk      => Clk,
      Clr      => Clr,
      Test1_A  => Test1_A,
      Test1_B  => Test1_B,
      Test1_AB => Test1_AB);
  Test1_A <= (others => '0');
  Test1_B <= (2 => '0', others => '1');
  
  assert unsigned(Test1_A) + unsigned(Test1_B) = unsigned(Test1_AB) + 2 report "Test failed intentionally" severity error;

end architecture rtl;
