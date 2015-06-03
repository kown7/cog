-------------------------------------------------------------------------------
-- Title      : test1vld
-- Author     :   <kristoffer.nordstrom@HELVNB0100>
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------

entity test1vld is
  port (
    Clk : in std_logic;
    Clr : in std_logic;

    Test1_A     : in std_logic_vector(3 downto 0);
    Test1_A_vld : in std_logic;
    Test1_B     : in std_logic_vector(3 downto 0);
    Test1_B_vld : in std_logic;

    Test1_AB     : out std_logic_vector(4 downto 0);
    Test1_AB_vld : out std_logic
    );
end entity test1vld;

-------------------------------------------------------------------------------

architecture str of test1vld is

  -----------------------------------------------------------------------------
  -- Internal signal declarations
  -----------------------------------------------------------------------------
  signal AB     : unsigned(Test1_AB'range);
  signal AB_vld : std_logic := '0';

begin  -- architecture str

  -----------------------------------------------------------------------------
  -- Output assignments
  -----------------------------------------------------------------------------
  Test1_AB     <= std_logic_vector(AB);
  Test1_AB_vld <= AB_vld;

  -----------------------------------------------------------------------------
  -- Component instantiations
  -----------------------------------------------------------------------------
  p_addAandB : process (Clk) is
  begin  -- process p_addAandB
    if Clk'event and Clk = '1' then     -- rising clock edge
      AB <= resize(unsigned(Test1_A), AB'length) + resize(unsigned(Test1_B), AB'length);
    end if;
  end process p_addAandB;

  p_generateValidSignal : process (Clk) is
  begin  -- process p_generateValidSignal
    if Clk'event and Clk = '1' then     -- rising clock edge
      if Clr = '1' then
        AB_vld <= '0';
      else
        AB_vld <= Test1_A_vld and Test1_B_vld;
      end if;
    end if;
  end process p_generateValidSignal;

end architecture str;

-------------------------------------------------------------------------------
