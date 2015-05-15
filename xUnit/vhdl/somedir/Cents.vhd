-------------------------------------------------------------------------------
-- Title      : Cents
-- Project    : 
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------

entity Cents is
  port (
    Clk : in std_logic;
    Clr : in std_logic;

    Cents_A : in std_logic_vector(3 downto 0);
    Cents_B : in std_logic_vector(3 downto 0);

    Cents_AB : out std_logic_vector(4 downto 0)
    );
end entity Cents;

-------------------------------------------------------------------------------

architecture str of Cents is

  -----------------------------------------------------------------------------
  -- Internal signal declarations
  -----------------------------------------------------------------------------
  signal AB : unsigned(Cents_AB'range);
    
begin  -- architecture str

  -----------------------------------------------------------------------------
  -- Output assignments
  -----------------------------------------------------------------------------
  Cents_AB <= std_logic_vector(AB);
  
  -----------------------------------------------------------------------------
  -- Component instantiations
  -----------------------------------------------------------------------------
  p_addAandB: process (Clk) is
  begin  -- process p_addAandB
    if Clk'event and Clk = '1' then     -- rising clock edge
      if Clr = '1' then
        AB <= to_unsigned(0, AB'length);
      else
        AB <= resize(unsigned(Cents_A), AB'length) + resize(unsigned(Cents_B), AB'length);
      end if;
    end if;
  end process p_addAandB;
  
end architecture str;

-------------------------------------------------------------------------------
