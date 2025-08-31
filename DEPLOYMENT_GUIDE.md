# 🚀 PW-HE Config Generator - Deployment Guide

## 📋 **Prerequisites**
- GitHub account
- Python 3.11+ installed locally
- Git installed locally

## 🌐 **Option 1: Render (Recommended - Free)**

### **Step 1: Prepare Your Repository**
1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/pwhe-config-generator.git
   git push -u origin main
   ```

2. **Required Files** (already created):
   - `app.py` - Flask application
   - `requirements.txt` - Python dependencies
   - `Procfile` - Process definition
   - `runtime.txt` - Python version
   - `templates/` - HTML templates

### **Step 2: Deploy to Render**
1. **Go to [render.com](https://render.com)** and sign up
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `pwhe-config-generator`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. **Click "Create Web Service"**
6. **Wait for deployment** (5-10 minutes)

### **Step 3: Access Your Tool**
- **URL**: `https://your-app-name.onrender.com`
- **Login**: `/login`
- **Main Tool**: `/`

---

## 🐳 **Option 2: Docker Deployment**

### **Step 1: Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### **Step 2: Build and Run**
```bash
docker build -t pwhe-config-generator .
docker run -p 5000:5000 pwhe-config-generator
```

---

## ☁️ **Option 3: Vercel (Advanced)**

### **Step 1: Install Vercel CLI**
```bash
npm i -g vercel
```

### **Step 2: Deploy**
```bash
vercel
```

---

## 🖥️ **Option 4: Self-Hosted Server**

### **Step 1: Server Setup**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nginx

# Install dependencies
pip3 install -r requirements.txt
```

### **Step 2: Run with Systemd**
```bash
# Create service file
sudo nano /etc/systemd/system/pwhe-config.service

[Unit]
Description=PW-HE Config Generator
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/app/venv/bin"
ExecStart=/path/to/your/app/venv/bin/gunicorn app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### **Step 3: Start Service**
```bash
sudo systemctl enable pwhe-config
sudo systemctl start pwhe-config
```

---

## 🔧 **Environment Variables**

### **Production Settings**
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export PORT=5000
```

### **Security Settings**
```bash
export SECRET_KEY=your-secret-key-here
export SESSION_COOKIE_SECURE=true
export SESSION_COOKIE_HTTPONLY=true
```

---

## 🌍 **Custom Domain Setup**

### **DNS Configuration**
1. **Add CNAME record** pointing to your hosting URL
2. **Wait for DNS propagation** (24-48 hours)

### **SSL Certificate**
- **Render**: Automatic SSL
- **Vercel**: Automatic SSL
- **Self-hosted**: Use Let's Encrypt

---

## 📊 **Monitoring & Maintenance**

### **Health Checks**
- **URL**: `/health` (add this endpoint)
- **Monitoring**: UptimeRobot, Pingdom

### **Logs**
- **Render**: Built-in logging
- **Vercel**: Built-in logging
- **Self-hosted**: Check systemd logs

---

## 💰 **Cost Comparison**

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| **Render** | ✅ Yes | $7/month | Small teams, testing |
| **Vercel** | ✅ Yes | $20/month | Production, high traffic |
| **Railway** | ✅ Yes | Pay-per-use | Development, testing |
| **Heroku** | ❌ No | $5/month | Easy deployment |
| **AWS** | ❌ No | $10-50/month | Enterprise, control |
| **Self-hosted** | ✅ Yes | Server costs | Full control, security |

---

## 🎯 **Recommendations**

### **For Testing/Development**
- **Render** (Free tier)

### **For Small Teams (5-20 users)**
- **Render** ($7/month) or **Vercel** ($20/month)

### **For Enterprise/High Traffic**
- **AWS EC2** or **Google Cloud**

### **For Maximum Control**
- **Self-hosted** on your own server

---

## 🚨 **Security Considerations**

### **Production Checklist**
- [ ] Debug mode disabled
- [ ] Strong secret key
- [ ] HTTPS enabled
- [ ] Session security configured
- [ ] Rate limiting (optional)
- [ ] Input validation
- [ ] Regular updates

### **Access Control**
- [ ] Multiple passcodes configured
- [ ] Session timeout set
- [ ] Logout functionality working
- [ ] Access level tracking

---

## 📞 **Support & Troubleshooting**

### **Common Issues**
1. **Port binding errors**: Check PORT environment variable
2. **Template not found**: Verify templates folder structure
3. **Static files**: Ensure proper file paths
4. **Database errors**: Check connection strings

### **Getting Help**
- Check deployment platform logs
- Verify all required files are present
- Test locally before deploying
- Check Python version compatibility

---

## 🎉 **Success!**

Once deployed, your tool will be accessible at:
- **Local**: `http://localhost:5000`
- **Production**: `https://your-domain.com`

**Share access with your team using the passcodes:**
- `PWHE2024` → Admin Access
- `TEAM001` → Team 1 Access
- `TEAM002` → Team 2 Access
- `GUEST01` → Guest Access
- `DEV001` → Developer Access

---

*Happy deploying! 🚀*
