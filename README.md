# 🔧 PW-HE Config Generator

A professional web-based tool for converting Cisco interface configurations to PW-Ether format with multi-user access control.

## ✨ **Features**

- 🔐 **Multi-user Authentication** - Secure access with passcodes
- 🔄 **Interface Conversion** - Convert GigabitEthernet to PW-Ether
- 🎯 **Smart Processing** - Intelligent ctag extraction and MTU detection
- 📱 **Responsive Design** - Works on all devices
- 🎨 **Modern UI** - Material 3 design principles
- 🔒 **Access Control** - Different access levels for teams
- 📤 **Export Options** - Download complete configurations

## 🚀 **Quick Start**

### **Local Development**
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/pwhe-config-generator.git
cd pwhe-config-generator

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Access at http://localhost:5000
```

### **Production Deployment**
1. **Push to GitHub**
2. **Connect to Render/Vercel**
3. **Automatic deployment**
4. **Share with your team**

## 🔑 **Access Codes**

| Passcode | Access Level | Description |
|----------|--------------|-------------|
| `PWHE2024` | Admin | Full access to all features |
| `TEAM001` | Team 1 | Team-specific access |
| `TEAM002` | Team 2 | Team-specific access |
| `GUEST01` | Guest | Limited access |
| `DEV001` | Developer | Development access |

## 🏗️ **Architecture**

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Session-based with passcodes
- **Styling**: Material 3 design system
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Roboto)

## 📁 **Project Structure**

```
pwhe-config-generator/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Procfile             # Deployment configuration
├── runtime.txt          # Python version
├── templates/           # HTML templates
│   ├── index.html      # Main application
│   └── login.html      # Authentication page
├── .github/            # GitHub Actions
│   └── workflows/      # Deployment automation
├── README.md           # This file
├── DEPLOYMENT_GUIDE.md # Hosting instructions
└── GITHUB_HOSTING_GUIDE.md # GitHub integration
```

## 🌐 **Hosting Options**

### **Free Tier**
- **Render** - Recommended for small teams
- **Railway** - Good for development
- **Vercel** - Excellent performance

### **Paid Plans**
- **Vercel Pro** - $20/month for production
- **Render** - $7/month for scaling
- **AWS/GCP** - Enterprise solutions

## 🔒 **Security Features**

- ✅ **Multi-factor authentication** via passcodes
- ✅ **Session management** with timeout
- ✅ **Access level tracking**
- ✅ **Secure logout**
- ✅ **HTTPS enforcement**
- ✅ **Input validation**

## 📱 **Browser Support**

- ✅ **Chrome** 90+
- ✅ **Firefox** 88+
- ✅ **Safari** 14+
- ✅ **Edge** 90+
- ✅ **Mobile browsers**

## 🛠️ **Development**

### **Adding New Features**
1. **Create feature branch**
2. **Implement changes**
3. **Test locally**
4. **Create pull request**
5. **Review and merge**

### **Testing**
```bash
# Run basic tests
python -m pytest tests/

# Check code quality
flake8 app.py
black app.py
```

## 📊 **Usage Examples**

### **Interface Conversion**
```
Input:  interface GigabitEthernet0/0/0/14.1176350
Output: interface PW-Ether 20280.350
```

### **Configuration Generation**
- Complete PW-Ether configurations
- Traffic policies and MPLS settings
- Verification commands
- Export to file

## 🤝 **Contributing**

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes**
4. **Test thoroughly**
5. **Submit pull request**

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/pwhe-config-generator/issues)
- **Documentation**: Check the guides in this repository
- **Community**: Stack Overflow, GitHub Discussions

## 🙏 **Acknowledgments**

- **Material Design** for UI inspiration
- **Font Awesome** for icons
- **Google Fonts** for typography
- **Bootstrap** for responsive components

---

**Built with ❤️ for network engineers**

*Happy configuring! 🚀* 