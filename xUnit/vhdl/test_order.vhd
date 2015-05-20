-------------------------------------------------------------------------------
-- Title      : test_order
-- Project    : 
-------------------------------------------------------------------------------
-- File       : test_order.vhd
-- Author     :   <kristoffer.nordstrom@HELVNB0100>
-- Company    : 
-- Created    : 2015-04-27
-- Last update: 2015-05-20
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

library work;
use work.test_order_pkg.all;

-------------------------------------------------------------------------------

entity test_order is
  port (
    Clk : in std_logic;
    Clr : in std_logic;

    Order_A : in std_logic_vector(3 downto 0);
    Order_B : in std_logic_vector(3 downto 0);

    Order_AB : out std_logic_vector(4 downto 0)
    );
end entity test_order;

-------------------------------------------------------------------------------

architecture str of test_order is

  -----------------------------------------------------------------------------
  -- Internal signal declarations
  -----------------------------------------------------------------------------
  signal AB : unsigned(Order_AB'range);
    
begin  -- architecture str

  -----------------------------------------------------------------------------
  -- Output assignments
  -----------------------------------------------------------------------------
  Order_AB <= std_logic_vector(AB);
  
  -----------------------------------------------------------------------------
  -- Component instantiations
  -----------------------------------------------------------------------------
  p_addAandB: process (Clk) is
  begin  -- process p_addAandB
    if Clk'event and Clk = '1' then     -- rising clock edge
      if Clr = '1' then
        AB <= to_unsigned(0, AB'length);
      else
        AB <= resize(unsigned(Order_A), AB'length) + resize(unsigned(Order_B), AB'length);
      end if;
    end if;
  end process p_addAandB;

  assert THE_TRUTH = 42 report "No answer to the question." severity error;
  
end architecture str;

-------------------------------------------------------------------------------
