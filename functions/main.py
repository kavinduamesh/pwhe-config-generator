import functions_framework
from flask import Flask, request, jsonify, render_template_string
import re
import os

# Import your existing conversion functions
def parse_interface_config(config_text):
    """Parse interface blocks from configuration text."""
    interfaces = []
    current_interface = None
    
    for line in config_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check if this is an interface line
        if line.startswith('interface '):
            if current_interface:
                interfaces.append(current_interface)
            current_interface = {'config': line, 'lines': [line]}
        elif current_interface:
            current_interface['lines'].append(line)
            if line == '!':
                interfaces.append(current_interface)
                current_interface = None
    
    # Add the last interface if exists
    if current_interface:
        interfaces.append(current_interface)
    
    return interfaces

def convert_interface_config(interface_config, pw_ether_id):
    """Convert a single interface configuration."""
    lines = interface_config['lines']
    converted_lines = []
    
    for line in lines:
        # Convert interface line
        if line.startswith('interface '):
            # Extract interface name and check for l2transport
            match = re.match(r'interface\s+(\S+)(?:\s+(l2transport))?', line)
            if match:
                interface_name = match.group(1)
                l2transport = match.group(2)
                
                # Extract ctag (last 3 digits)
                ctag_match = re.search(r'\.(\d{3})$', interface_name)
                if ctag_match:
                    ctag = ctag_match.group(1)
                    new_interface = f"interface PW-Ether {pw_ether_id}.{ctag}"
                    if l2transport:
                        new_interface += f" {l2transport}"
                    converted_lines.append(new_interface)
                else:
                    converted_lines.append(line)
            else:
                converted_lines.append(line)
        
        # Convert encapsulation line
        elif 'encapsulation dot1q' in line and 'second-dot1q' in line:
            # Extract ctag from second-dot1q
            match = re.search(r'second-dot1q\s+(\d+)', line)
            if match:
                ctag = match.group(1)
                # Check if ctag is 502 or 504
                if ctag in ['502', '504']:
                    # Remove rewrite ingress tag pop commands for these ctags
                    pass
                else:
                    # Convert to simple dot1q
                    new_line = re.sub(r'encapsulation dot1q \d+ second-dot1q \d+', f'encapsulation dot1q {ctag}', line)
                    converted_lines.append(new_line)
                    continue
            converted_lines.append(line)
        
        # Handle rewrite ingress tag pop commands
        elif 'rewrite ingress tag pop 2 symmetric' in line:
            # Check if we should remove this command (ctag 502 or 504)
            # We'll need to check the ctag from the interface name
            interface_name = None
            for prev_line in reversed(converted_lines):
                if prev_line.startswith('interface PW-Ether'):
                    ctag_match = re.search(r'\.(\d+)$', prev_line)
                    if ctag_match and ctag_match.group(1) in ['502', '504']:
                        # Skip this line for ctags 502/504
                        break
                    else:
                        # Convert to pop 1 for other ctags
                        converted_lines.append(line.replace('pop 2', 'pop 1'))
                        break
            else:
                converted_lines.append(line.replace('pop 2', 'pop 1'))
            continue
        
        # Add shutdown command before the closing '!'
        elif line == '!':
            # Check if shutdown already exists
            has_shutdown = any('shutdown' in prev_line for prev_line in converted_lines)
            if not has_shutdown:
                # Add shutdown command before the '!'
                converted_lines.append('shutdown')
            converted_lines.append(line)
        
        # Keep other lines as-is
        else:
            converted_lines.append(line)
    
    return '\n'.join(converted_lines)

def convert_configuration(old_config, pw_ether_id):
    """Convert the entire configuration."""
    interfaces = parse_interface_config(old_config)
    converted_configs = []
    
    for interface in interfaces:
        converted = convert_interface_config(interface, pw_ether_id)
        converted_configs.append(converted)
    
    return '\n\n'.join(converted_configs)

# Firebase Functions entry point
@functions_framework.http
def app(request):
    """HTTP Cloud Function."""
    # Set CORS headers
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            old_config = data.get('old_config', '')
            pw_ether_id = data.get('pw_ether_id', '')
            
            if not old_config or not pw_ether_id:
                return (jsonify({'error': 'Missing required parameters'}), 400, headers)
            
            converted_config = convert_configuration(old_config, pw_ether_id)
            
            return (jsonify({
                'converted_config': converted_config,
                'status': 'success'
            }), 200, headers)
            
        except Exception as e:
            return (jsonify({'error': str(e)}), 500, headers)
    
    elif request.method == 'GET':
        # Serve the main page
        return (render_template_string(INDEX_HTML), 200, headers)
    
    return (jsonify({'error': 'Method not allowed'}), 405, headers)

# HTML template for the main page
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PW-HE Config Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .main-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .card { margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn-primary { background-color: #007bff; border-color: #007bff; }
        .btn-success { background-color: #28a745; border-color: #28a745; }
        .btn-info { background-color: #17a2b8; border-color: #17a2b8; }
        .form-control:focus { border-color: #007bff; box-shadow: 0 0 0 0.2rem rgba(0,123,255,0.25); }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="text-center mb-4">
            <h1><i class="fas fa-network-wired me-2"></i>PW-HE Config Generator</h1>
            <p class="lead">Convert Metro interfaces to PW-Ether format</p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-cog me-2"></i>Configuration Settings</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="pwEtherId" class="form-label">PW-Ether ID</label>
                            <input type="text" class="form-control" id="pwEtherId" placeholder="e.g., 10239">
                        </div>
                        <button type="button" class="btn btn-primary" onclick="convertConfiguration()">
                            <i class="fas fa-sync-alt me-2"></i>Convert Configuration
                        </button>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-file-code me-2"></i>Old Configuration</h5>
                    </div>
                    <div class="card-body">
                        <textarea class="form-control" id="oldConfig" rows="15" placeholder="Paste your old Cisco interface configuration here..."></textarea>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-check-circle me-2"></i>New Configuration</h5>
                    </div>
                    <div class="card-body">
                        <textarea class="form-control" id="newConfig" rows="15" readonly placeholder="Converted configuration will appear here..."></textarea>
                        <div class="mt-2">
                            <button type="button" class="btn btn-success" onclick="copyToClipboard('newConfig')">
                                <i class="fas fa-copy me-2"></i>Copy
                            </button>
                            <button type="button" class="btn btn-info" onclick="downloadConfiguration()">
                                <i class="fas fa-download me-2"></i>Download
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        async function convertConfiguration() {
            const oldConfig = document.getElementById('oldConfig').value;
            const pwEtherId = document.getElementById('pwEtherId').value;
            
            if (!oldConfig || !pwEtherId) {
                alert('Please enter both the old configuration and PW-Ether ID');
                return;
            }
            
            try {
                const response = await fetch('/api/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        old_config: oldConfig,
                        pw_ether_id: pwEtherId
                    })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    document.getElementById('newConfig').value = data.converted_config;
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                alert('Error converting configuration: ' + error.message);
            }
        }
        
        function copyToClipboard(elementId) {
            const element = document.getElementById(elementId);
            element.select();
            document.execCommand('copy');
            alert('Configuration copied to clipboard!');
        }
        
        function downloadConfiguration() {
            const config = document.getElementById('newConfig').value;
            if (!config) {
                alert('No configuration to download');
                return;
            }
            
            const blob = new Blob([config], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'pwhe-config.txt';
            a.click();
            window.URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>
'''
