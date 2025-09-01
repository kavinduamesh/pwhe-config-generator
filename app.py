from flask import Flask, render_template, request, jsonify
import re
import os

app = Flask(__name__)

def parse_interface_config(config_text):
    """Parse the old Cisco interface configuration and extract interface blocks"""
    interfaces = []
    current_interface = None
    current_lines = []
    
    for line in config_text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a new interface definition
        if line.startswith('interface '):
            # Save previous interface if exists
            if current_interface:
                interfaces.append({
                    'name': current_interface,
                    'config': '\n'.join(current_lines)
                })
            
            # Start new interface
            current_interface = line
            current_lines = [line]
        elif current_interface:
            current_lines.append(line)
    
    # Add the last interface
    if current_interface:
        interfaces.append({
            'name': current_interface,
            'config': '\n'.join(current_lines)
        })
    
    return interfaces

def convert_interface_config(interface_config, pw_ether_id):
    """Convert a single interface configuration from old to new format"""
    lines = interface_config['config'].split('\n')
    new_lines = []
    
    # Extract ctag from encapsulation command, not from interface name
    ctag = None
    for line in lines:
        if 'encapsulation dot1q' in line and 'second-dot1q' in line:
            # Extract the ctag (second dot1q value)
            match = re.search(r'encapsulation dot1q \d+ second-dot1q (\d+)', line.strip())
            if match:
                ctag = match.group(1)
                break
    
    for line in lines:
        original_line = line
        line = line.strip()
        if not line:
            continue
            
        # Handle interface name conversion
        if line.startswith('interface '):
            # Extract the original interface name and subinterface number
            # Also check for l2transport keyword
            match = re.match(r'interface\s+(GigabitEthernet|TenGigE|Tengig)\d+/\d+/\d+/\d+\.(\d+)(\s+l2transport)?', line)
            if match:
                interface_type, subinterface_num, l2transport = match.groups()
                # Use the ctag from encapsulation command for the new interface name
                # If no ctag found, fall back to subinterface number
                interface_suffix = ctag if ctag else subinterface_num
                # Create new PW-Ether interface name
                new_interface_name = f"interface PW-Ether {pw_ether_id}.{interface_suffix}"
                # Add l2transport if it was present in the original
                if l2transport:
                    new_interface_name += l2transport
                new_lines.append(new_interface_name)
            else:
                # If pattern doesn't match, keep original
                new_lines.append(original_line)
        
        # Handle encapsulation conversion
        elif 'encapsulation dot1q' in line and 'second-dot1q' in line:
            # Extract the ctag (second dot1q value)
            match = re.search(r'encapsulation dot1q \d+ second-dot1q (\d+)', line)
            if match:
                ctag = match.group(1)
                # Preserve original indentation
                indent = original_line[:len(original_line) - len(original_line.lstrip())]
                new_line = f"{indent}encapsulation dot1q {ctag}"
                new_lines.append(new_line)
            else:
                new_lines.append(original_line)
        
        # Handle service-policy output conversion
        elif line.startswith('service-policy output '):
            # Keep service-policy output commands as is (don't add 'no' prefix)
            new_lines.append(original_line)
        
        # Handle rewrite ingress tag pop conversion
        elif 'rewrite ingress tag pop 2 symmetric' in line:
            # If ctag is 502 or 504, remove the rewrite command entirely
            if ctag in ['502', '504']:
                continue  # Skip this line
            else:
                # Change pop 2 to pop 1 for other ctags
                # Preserve original indentation
                indent = original_line[:len(original_line) - len(original_line.lstrip())]
                new_line = original_line.replace('pop 2', 'pop 1')
                new_lines.append(new_line)
        
        # Handle shutdown command
        elif line == 'shutdown':
            # Already has shutdown, keep as is
            new_lines.append(original_line)
        
        # All other lines remain unchanged
        else:
            new_lines.append(original_line)
    
    # Add shutdown command if not already present (before the closing '!')
    if 'shutdown' not in [line.strip() for line in new_lines]:
        # Find the position of the closing '!' and insert shutdown before it
        for i, line in enumerate(new_lines):
            if line.strip() == '!':
                # Use the same indentation as other commands
                indent = ''  # No indentation for shutdown command
                new_lines.insert(i, f"{indent}shutdown")
                break
        else:
            # If no '!' found, add shutdown at the end
            new_lines.append('shutdown')
    
    # Ensure there's a closing '!' at the end
    if new_lines and new_lines[-1].strip() != '!':
        new_lines.append('!')
    
    return '\n'.join(new_lines)

def convert_configuration(old_config, pw_ether_id):
    """Convert the entire configuration from old to new format"""
    interfaces = parse_interface_config(old_config)
    converted_interfaces = []
    
    for interface in interfaces:
        converted_config = convert_interface_config(interface, pw_ether_id)
        converted_interfaces.append(converted_config)
    
    # Add migration section
    migration_section = generate_migration_section(interfaces, pw_ether_id)
    
    # Combine converted interfaces with migration section
    result = '\n\n'.join(converted_interfaces)
    if migration_section:
        result += '\n\n' + migration_section
    
    return result

def generate_migration_section(interfaces, pw_ether_id):
    """Generate migration section with shutdown commands for old interfaces and no shutdown for new ones"""
    migration_lines = []
    
    # Section 1: New PW-Ether interfaces with no shutdown
    migration_lines.append('### no shutdown (from config) ###')
    for interface in interfaces:
        # Extract the original interface name and subinterface number
        match = re.match(r'interface\s+(GigabitEthernet|TenGigE|Tengig)\d+/\d+/\d+/\d+\.(\d+)(\s+l2transport)?', interface['name'].strip())
        if match:
            interface_type, subinterface_num, l2transport = match.groups()
            
            # Extract ctag from encapsulation command in the interface config
            ctag = None
            config_lines = interface['config'].split('\n')
            for config_line in config_lines:
                if 'encapsulation dot1q' in config_line and 'second-dot1q' in config_line:
                    ctag_match = re.search(r'encapsulation dot1q \d+ second-dot1q (\d+)', config_line.strip())
                    if ctag_match:
                        ctag = ctag_match.group(1)
                        break
            
            # Use ctag if found, otherwise fall back to subinterface number
            interface_suffix = ctag if ctag else subinterface_num
            
            # Add no shutdown command for new PW-Ether interface
            new_interface_name = f"interface PW-Ether {pw_ether_id}.{interface_suffix}"
            if l2transport:
                new_interface_name += l2transport
            migration_lines.append(new_interface_name)
            migration_lines.append(' no shutdown')
    
    migration_lines.append('')
    
    # Section 2: Old interfaces with shutdown
    migration_lines.append('### shutdown (from list) ###')
    for interface in interfaces:
        # Use the complete original interface name for shutdown commands
        original_interface_name = interface['name'].strip()
        migration_lines.append(original_interface_name)
        migration_lines.append(' shutdown')
    
    return '\n'.join(migration_lines)

def generate_bridge_config(interfaces, pw_ether_id):
    """Generate L2VPN bridge configuration for ctags 502/504"""
    special_ctags = []
    
    # Check for interfaces with ctags 502 or 504
    for interface in interfaces:
        match = re.match(r'interface\s+(GigabitEthernet|TenGigE|Tengig)\d+/\d+/\d+/\d+\.(\d+)(\s+l2transport)?', interface['name'].strip())
        if match:
            subinterface_num = match.group(2)
            
            # Extract ctag from encapsulation command in the interface config
            ctag = None
            config_lines = interface['config'].split('\n')
            for config_line in config_lines:
                if 'encapsulation dot1q' in config_line and 'second-dot1q' in config_line:
                    ctag_match = re.search(r'encapsulation dot1q \d+ second-dot1q (\d+)', config_line.strip())
                    if ctag_match:
                        ctag = ctag_match.group(1)
                        break
            
            # Use ctag if found, otherwise fall back to subinterface number
            interface_suffix = ctag if ctag else subinterface_num
            
            # Check if the ctag ends with 502 or 504 (for 4+ digit ctags)
            if interface_suffix.endswith('502') or interface_suffix.endswith('504'):
                # Extract the last 3 digits for the bridge domain name
                ctag_suffix = interface_suffix[-3:]
                special_ctags.append({
                    'ctag': ctag_suffix,
                    'original_interface': interface['name'].strip(),
                    'new_interface': f"PW-Ether {pw_ether_id}.{interface_suffix}"
                })
    
    if not special_ctags:
        return None
    
    # Generate bridge configuration
    bridge_lines = []
    bridge_lines.append('l2vpn')
    bridge_lines.append(' bridge group D_NET')
    
    for ctag_info in special_ctags:
        bridge_lines.append(f'  bridge-domain ME_DNET_{ctag_info["ctag"]}')
        bridge_lines.append(f'   interface {ctag_info["new_interface"]}')
        bridge_lines.append('    storm-control multicast kbps 50000')
        bridge_lines.append('    storm-control broadcast kbps 50000')
        bridge_lines.append('    split-horizon group')
        bridge_lines.append('   !')
        bridge_lines.append('  !')
    
    bridge_lines.append(' !')
    bridge_lines.append('!')
    
    return '\n'.join(bridge_lines)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'PW-HE Config Generator'})

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        old_config = data.get('old_config', '')
        pw_ether_id = data.get('pw_ether_id', '')
        
        if not old_config.strip():
            return jsonify({'error': 'Please provide the old configuration'}), 400
        
        if not pw_ether_id.strip():
            return jsonify({'error': 'Please provide the PW-Ether ID'}), 400
        
        # Convert the configuration
        new_config = convert_configuration(old_config, pw_ether_id)
        
        return jsonify({
            'success': True,
            'new_config': new_config
        })
    
    except Exception as e:
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Get port from environment variable (for production) or use 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 