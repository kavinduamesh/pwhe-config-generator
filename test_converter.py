#!/usr/bin/env python3
"""
Test script for the Cisco Interface Configuration Converter
"""

import sys
import os

# Add the current directory to Python path to import app functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import convert_configuration

def test_conversion():
    """Test the conversion with the provided examples"""
    
    # Test input configuration
    old_config = """interface GigabitEthernet0/0/0/14.1176049
 description 994614384:FIB:10.24.128.255:Gi0/2/6::SANASA_DEVELOPMENT_BANK_LIMITED:COLOMBO_01
 mtu 1600
 service-policy input 512K_POLICE_DATA_IN
 service-policy output 512K_SHAPE_PARENT
 vrf SDB_DATA
 ipv4 address 10.229.225.1 255.255.255.252
 encapsulation dot1q 3513 second-dot1q 49
!
interface GigabitEthernet0/0/0/14.1176156
 description 994602392:FIB:10.24.128.255:Gi0/2/6::COM BANK:COL 01
 mtu 1600
 service-policy input 20M_POLICE_BE_IN
 service-policy output 20M_SHAPE_PARENT
 vrf ENT_INTERNET
 ipv4 address 122.255.63.33 255.255.255.240
 encapsulation dot1q 3513 second-dot1q 156
 ipv4 access-group TRC_VOIP_BLOCK ingress
 ipv4 access-group TRC_VOIP_BLOCK egress
!
interface GigabitEthernet0/0/0/14.1176350
 description SYS:MGT:POE_SW:COMMERCIAL_BANK:COLOMBO_01
 mtu 1600
 service-policy input 2M_POLICE_DATA_IN
 service-policy output 2M_SHAPE_PARENT
 vrf DIALOG_FIXED_VOICE
 ipv4 address 10.24.189.85 255.255.255.252
 encapsulation dot1q 3513 second-dot1q 350
!"""

    # Expected output configuration
    expected_config = """interface PW-Ether 10239.049
 description 994614384:FIB:10.24.128.255:Gi0/2/6::SANASA_DEVELOPMENT_BANK_LIMITED:COLOMBO_01
 mtu 1600
 service-policy input 512K_POLICE_DATA_IN
 no service-policy output 512K_SHAPE_PARENT
 vrf SDB_DATA
 ipv4 address 10.229.225.1 255.255.255.252
 encapsulation dot1q 49
 shutdown
!
interface PW-Ether 10239.156
 description 994602392:FIB:10.24.128.255:Gi0/2/6::COM BANK:COL 01
 mtu 1600
 service-policy input 20M_POLICE_BE_IN
 no service-policy output 20M_SHAPE_PARENT
 vrf ENT_INTERNET
 ipv4 address 122.255.63.33 255.255.255.240
 encapsulation dot1q 156
 ipv4 access-group TRC_VOIP_BLOCK ingress
 ipv4 access-group TRC_VOIP_BLOCK egress
 shutdown
!
interface PW-Ether 10239.350
 description SYS:MGT:POE_SW:COMMERCIAL_BANK:COLOMBO_01
 mtu 1600
 service-policy input 2M_POLICE_DATA_IN
 no service-policy output 2M_SHAPE_PARENT
 vrf DIALOG_FIXED_VOICE
 ipv4 address 10.24.189.85 255.255.255.252
 encapsulation dot1q 350
 shutdown
!"""

    print("Testing Cisco Interface Configuration Converter...")
    print("=" * 60)
    
    # Convert the configuration
    pw_ether_id = "10239"
    converted_config = convert_configuration(old_config, pw_ether_id)
    
    print("Input Configuration:")
    print("-" * 30)
    print(old_config)
    print("\n" + "=" * 60)
    
    print("Converted Configuration:")
    print("-" * 30)
    print(converted_config)
    print("\n" + "=" * 60)
    
    print("Expected Configuration:")
    print("-" * 30)
    print(expected_config)
    print("\n" + "=" * 60)
    
    # Compare results
    if converted_config.strip() == expected_config.strip():
        print("✅ TEST PASSED: Conversion matches expected output!")
    else:
        print("❌ TEST FAILED: Conversion does not match expected output!")
        print("\nDifferences:")
        print("-" * 20)
        converted_lines = converted_config.strip().split('\n')
        expected_lines = expected_config.strip().split('\n')
        
        for i, (conv_line, exp_line) in enumerate(zip(converted_lines, expected_lines)):
            if conv_line != exp_line:
                print(f"Line {i+1}:")
                print(f"  Expected: {exp_line}")
                print(f"  Got:      {conv_line}")
                print()

if __name__ == "__main__":
    test_conversion() 