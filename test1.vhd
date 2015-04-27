-------------------------------------------------------------------------------
-- Title      : test1
-- Project    : 
-------------------------------------------------------------------------------
-- File       : test1.vhd
-- Author     :   <kristoffer.nordstrom@HELVNB0100>
-- Company    : 
-- Created    : 2015-04-27
-- Last update: 2015-04-27
-- Platform   : 
-- Standard   : VHDL'93/02
-------------------------------------------------------------------------------
-- Description: 
-------------------------------------------------------------------------------
-- Copyright (c) 2015 
-------------------------------------------------------------------------------
-- Revisions  :
-- Date        Version  Author  Description
-- 2015-04-27  1.0      kn	Created
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------

entity test1 is
  port (
    Clk : in std_logic;
    Clr : in std_logic;

    Test1_A : in std_logic_vector(3 downto 0);
    Test1_B : in std_logic_vector(3 downto 0);

    Test1_AB : out std_logic_vector(4 downto 0)
    );
end entity test1;

-------------------------------------------------------------------------------

architecture str of test1 is

  -----------------------------------------------------------------------------
  -- Internal signal declarations
  -----------------------------------------------------------------------------
  signal AB : unsigned(Test1_AB'range);
    
begin  -- architecture str

  -----------------------------------------------------------------------------
  -- Output assignments
  -----------------------------------------------------------------------------
  Test1_AB <= std_logic_vector(AB);
  
  -----------------------------------------------------------------------------
  -- Component instantiations
  -----------------------------------------------------------------------------
  p_addAandB: process (Clk) is
  begin  -- process p_addAandB
    if Clk'event and Clk = '1' then     -- rising clock edge
      if Clr = '1' then
        AB <= to_unsigned(0, AB'length);
      else
        AB <= unsigned(Test1_A) + unsigned(Test1_B);
      end if;
    end if;
  end process p_addAandB;
  
end architecture str;

-------------------------------------------------------------------------------
