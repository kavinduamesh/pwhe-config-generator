#!/usr/bin/env python3
"""
Demonstration script for the Cisco Interface Configuration Converter
"""

from app import convert_configuration

def demo_conversion():
    """Demonstrate the conversion functionality"""
    
    print("🚀 Cisco Interface Configuration Converter Demo")
    print("=" * 60)
    
    # Example old configuration with l2transport and rewrite command
    old_config = """interface GigabitEthernet0/0/0/13.1001200 l2transport
description 994635457:FIB:10.24.32.74:Gi0/13::INDUSTRIAL_CLOTHING:MALWANA
encapsulation dot1q 1001 second-dot1q 200
rewrite ingress tag pop 2 symmetric
mtu 1600
service-policy input 2M_POLICE_DATA_IN
service-policy output 2M_SHAPE_PARENT
!
interface GigabitEthernet0/0/0/14.1176049
description 994614384:FIB:10.24.128.255:Gi0/2/6::SANASA_DEVELOPMENT_BANK_LIMITED:COLOMBO_01
mtu 1600
service-policy input 512K_POLICE_DATA_IN
service-policy output 512K_SHAPE_PARENT
vrf SDB_DATA
ipv4 address 10.229.225.1 255.255.255.252
encapsulation dot1q 3513 second-dot1q 49
!"""
    
    pw_ether_id = "10239"
    
    print("📥 Input Configuration (Old Format):")
    print("-" * 40)
    print(old_config)
    print("\n" + "=" * 60)
    
    # Convert the configuration
    converted_config = convert_configuration(old_config, pw_ether_id)
    
    print("📤 Output Configuration (New Format):")
    print("-" * 40)
    print(converted_config)
    print("\n" + "=" * 60)
    
    print("✅ Conversion completed successfully!")
    print("\n🔧 Key Changes Applied:")
    print("  • GigabitEthernet → PW-Ether")
    print("  • Interface numbering: 1001200 → 200, 1176049 → 049")
    print("  • Preserved: l2transport keyword")
    print("  • Encapsulation: dot1q 1001 second-dot1q 200 → dot1q 200")
    print("  • Rewrite command: pop 2 → pop 1")
    print("  • Service policy: kept as-is (no 'no' prefix added)")
    print("  • Added: shutdown command")
    
    print("\n🌐 Web Interface:")
    print("  Start the web application with: python app.py")
    print("  Then open: http://localhost:5000")

if __name__ == "__main__":
    demo_conversion() 