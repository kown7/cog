-------------------------------------------------------------------------------
-- Title      : test1
-- Project    : 
-------------------------------------------------------------------------------
-- File       : test1.vhd
-- Author     :   <kristoffer.nordstrom@HELVNB0100>
-- Company    : 
-- Created    : 2015-04-27
-- Last update: 2015-05-12
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

entity A is
  port (
    Clk : in std_logic;
    Clr : in std_logic;

    A_A : in std_logic_vector(3 downto 0);
    A_B : in std_logic_vector(3 downto 0);

    A_AB : out std_logic_vector(4 downto 0)
    );
end entity A;

-------------------------------------------------------------------------------

architecture str of A is

  signal Cents_A  : std_logic_vector(3 downto 0);
  signal Cents_B  : std_logic_vector(3 downto 0);
  signal Cents_AB : std_logic_vector(4 downto 0);
  
  signal B_A  : std_logic_vector(3 downto 0);
  signal B_B  : std_logic_vector(3 downto 0);
  signal B_AB : std_logic_vector(4 downto 0);
  -----------------------------------------------------------------------------
  -- Internal signal declarations
  -----------------------------------------------------------------------------
  signal AB : unsigned(A_AB'range);
    
begin  -- architecture str

  -----------------------------------------------------------------------------
  -- Output assignments
  -----------------------------------------------------------------------------
  A_AB <= std_logic_vector(AB);
  
  -----------------------------------------------------------------------------
  -- Component instantiations
  -----------------------------------------------------------------------------
  p_addAandB: process (Clk) is
  begin  -- process p_addAandB
    if Clk'event and Clk = '1' then     -- rising clock edge
      if Clr = '1' then
        AB <= to_unsigned(0, AB'length);
      else
        AB <= resize(unsigned(A_A), AB'length) + resize(unsigned(A_B), AB'length);
      end if;
    end if;
  end process p_addAandB;


  i_B_1: entity work.B
    port map (
      Clk  => Clk,
      Clr  => Clr,
      B_A  => B_A,
      B_B  => B_B,
      B_AB => B_AB);

  i_Cents_1: entity work.Cents
    port map (
      Clk      => Clk,
      Clr      => Clr,
      Cents_A  => Cents_A,
      Cents_B  => Cents_B,
      Cents_AB => Cents_AB);
  
end architecture str;

-------------------------------------------------------------------------------
