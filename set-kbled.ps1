function SET-KBLED
{
  <#
  .SYNOPSIS
  This powershell cmdlet was written by Mark Baggett twitter:@markbaggett.  It can be used to control the keyboard backlight colors on Clevo compatible laptops. (Sager, etc)  
  .DESCRIPTION
   This will control the colors and patterns on your keyboard backlights.  This powershell script must run as an ADMINISTRATOR to function properly.  - You can trust me ;)
  .EXAMPLE
  Assuming this script is saved in c:\powershell\ and is named set-kbled.ps1
  PS C:\Windows\system32> Import-Module C:\powershell\set-kbled.ps1
  PS C:\Windows\system32> SET-KBLED -LeftColor RED -CenterColor RED -RightColor RED  
  Sets the keyboard backlights so that they are all red.  (Metasploit mode)
  .EXAMPLE
  SET-KBLED -LeftColor RED -RightColor BLUE -CenterColor WHITE
  Set the left right and center portions of the keyboard to Red, Blue, and White respectively.  (God Bless America Mode)
  .EXAMPLE
  SET-KBLED -Pattern BLINK
  Put the keyboard in blinking color mode
  .EXAMPLE
  SET-KBLED -Off
  Turns in off
  .EXAMPLE
  SET-KBLED -On
  Turns it on
  #>
  param(
    [ValidateSet("RED","WHITE","BLUE","CYAN","PURPLE","YELLOW","GREEN")][string]$LeftColor,
    [ValidateSet("RED","WHITE","BLUE","CYAN","PURPLE","YELLOW","GREEN")][string]$CenterColor,
    [ValidateSet("RED","WHITE","BLUE","CYAN","PURPLE","YELLOW","GREEN")][string]$RightColor,
    [ValidateSet("RED","WHITE","BLUE","CYAN","PURPLE","YELLOW","GREEN")][string]$AllColor,
    [switch]$Off,
    [switch]$On,
    [ValidateSet("DANCE","BREATH","BLINK","RANDOM","SWEEP")][string]$Pattern
    )

    $colors = @{  }
    $colors['RED']= "00FF00"
    $colors['WHITE'] = "FFFFFF"
    $colors['BLUE'] = "FF0000"
    $colors['CYAN'] = "FF00FF"
    $colors['PURPLE'] = "FFFF00"
    $colors['YELLOW'] = "00FFFF"
    $colors['GREEN'] = "0000FF"
    
    $clevo = get-wmiobject -query "select * from CLEVO_GET" -namespace "root\WMI"
  
    if ($LeftColor -NE "" ) {
        $col = [Convert]::ToUInt32("F0" +$colors[$LeftColor], 16)
        write-host $col
        $clevo.SetKBLED( $col  )
    }
    if ($CenterColor -NE "" ) {
        $col = [Convert]::ToUInt32("F1" +$colors[$CenterColor], 16)
        $clevo.SetKBLED( $col  )
    }
    if ($RightColor -NE "" ) {
        $col = [Convert]::ToUInt32("F2" +$colors[$RightColor], 16)
        $clevo.SetKBLED( $col  )
    }
    if ($AllColor -NE "" ) {
        $col0 = [Convert]::ToUInt32("F0" +$colors[$AllColor], 16)
        $col1 = [Convert]::ToUInt32("F1" +$colors[$AllColor], 16)
        $col2 = [Convert]::ToUInt32("F2" +$colors[$AllColor], 16)
        $clevo.SetKBLED( $col0  )
        $clevo.SetKBLED( $col1  )
        $clevo.SetKBLED( $col2  )
    }
    
    if ($Off.IsPresent) {
        $clevo.SetKBLED( [Convert]::ToUInt32("0000a000", 16)  ) 
    }
    if ($On.IsPresent) {
        $clevo.SetKBLED( [Convert]::ToUInt32("00001000", 16)  ) 
    }
    if ($Pattern -EQ "Blink" ) {
        $clevo.SetKBLED( [Convert]::ToUInt32("a0000000", 16)  )  
    }
    if ($Pattern -EQ "Breath" ) {
        $clevo.SetKBLED( [Convert]::ToUInt32("30000000", 16)  )  
    }
    if ($Pattern -EQ "Dance" ) {
        $clevo.SetKBLED( [Convert]::ToUInt32("80000000", 16)  )   
    }
    if ($Pattern -EQ "Random" ) {
        $clevo.SetKBLED( [Convert]::ToUInt32("90000000", 16)  )  
    }
    if ($Pattern -EQ "Sweep" ) {
        $clevo.SetKBLED( [Convert]::ToUInt32("b0000000", 16)  )  
    } 
} 