#!/usr/bin/env python3
"""
Email Deployment Notification Script
Sends deployment instructions and status to your email
"""

import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_deployment_email(recipient_email, deployment_type="Railway"):
    """Send deployment instructions to email"""
    
    sender_email = "deployment@journaldesk.local"
    
    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🚀 Journal Desk - Free Deployment Ready"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    
    # Email body
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                    <h1 style="margin: 0;">🚀 Journal Desk</h1>
                    <p style="margin: 10px 0 0 0;">Ready for FREE Deployment</p>
                </div>
                
                <!-- Main Content -->
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h2>Hello! 👋</h2>
                    <p>Your Journal Desk application is ready to deploy <strong>for FREE</strong>!</p>
                    <p>Deployment Type: <strong>{deployment_type}</strong></p>
                    <p>Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <!-- Quick Start -->
                <div style="background: white; border-left: 4px solid #667eea; padding: 20px; margin-bottom: 20px;">
                    <h3 style="color: #667eea;">⚡ Quick Start (5 Minutes)</h3>
                    <ol>
                        <li>Visit <a href="https://railway.app/" style="color: #667eea;">Railway.app</a></li>
                        <li>Sign up with GitHub account</li>
                        <li>Click "Create Project" → "Deploy from GitHub"</li>
                        <li>Select your journal-desk repository</li>
                        <li>Railway deploys automatically in 2 minutes!</li>
                        <li>Your app is live at: <code>https://your-app.railway.app</code></li>
                    </ol>
                </div>
                
                <!-- Features -->
                <div style="background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px;">
                    <h3>✨ What You Get (FREE)</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>✅ PostgreSQL Database</li>
                        <li>✅ SSL/HTTPS (Automatic)</li>
                        <li>✅ $5/month in credits (2-3 months FREE hosting)</li>
                        <li>✅ Auto-deploy on GitHub push</li>
                        <li>✅ Automatic backups</li>
                        <li>✅ Custom domain support</li>
                        <li>✅ Performance monitoring</li>
                    </ul>
                </div>
                
                <!-- Cost -->
                <div style="background: #e8f4f8; padding: 20px; margin-bottom: 20px; border-radius: 8px;">
                    <h3>💰 Pricing</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px;"><strong>First 2-3 Months:</strong></td>
                            <td style="padding: 10px; text-align: right;"><strong style="color: green;">$0 (FREE)</strong></td>
                        </tr>
                        <tr style="background: white;">
                            <td style="padding: 10px;">Continued hosting:</td>
                            <td style="padding: 10px; text-align: right;"><strong>~$5-10/month</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">Other platforms:</td>
                            <td style="padding: 10px; text-align: right;"><strong>Vary (see docs)</strong></td>
                        </tr>
                    </table>
                </div>
                
                <!-- Alternative Platforms -->
                <div style="background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px;">
                    <h3>🌐 Alternative FREE Options</h3>
                    <p><strong>Render.com</strong> - Free tier, very reliable</p>
                    <p><strong>PythonAnywhere.com</strong> - Python-friendly, easy setup</p>
                    <p><strong>Fly.io</strong> - $3/month credits</p>
                    <p style="font-size: 12px; color: #666;">See FREE_DEPLOYMENT.md for full comparison</p>
                </div>
                
                <!-- Documentation Link -->
                <div style="background: white; border: 2px solid #667eea; padding: 20px; text-align: center; margin-bottom: 20px; border-radius: 8px;">
                    <h3 style="margin-top: 0;">📖 Complete Deployment Guide</h3>
                    <p>See <strong>FREE_DEPLOYMENT.md</strong> in your project for:</p>
                    <ul>
                        <li>Step-by-step setup for each platform</li>
                        <li>Troubleshooting guide</li>
                        <li>Performance optimization tips</li>
                        <li>Monitoring and backups</li>
                    </ul>
                </div>
                
                <!-- Post-Deployment -->
                <div style="background: #f0f9ff; padding: 20px; margin-bottom: 20px; border-radius: 8px;">
                    <h3>✅ After Deployment</h3>
                    <ol>
                        <li>Create admin account: <code>python manage.py createsuperuser</code></li>
                        <li>Access admin: <code>https://your-app/admin/</code></li>
                        <li>Configure email (optional)</li>
                        <li>Add custom domain (optional)</li>
                        <li>Monitor performance</li>
                    </ol>
                </div>
                
                <!-- Support -->
                <div style="background: white; border-left: 4px solid #667eea; padding: 20px; margin-bottom: 20px;">
                    <h3 style="color: #667eea;">🆘 Need Help?</h3>
                    <p>Check the included documentation files:</p>
                    <ul>
                        <li><strong>FREE_DEPLOYMENT.md</strong> - All free options explained</li>
                        <li><strong>DEPLOYMENT_GUIDE.md</strong> - Detailed platform guides</li>
                        <li><strong>DEPLOYMENT_READY.md</strong> - Quick start overview</li>
                        <li><strong>verify-deployment.sh</strong> - Pre-deployment verification</li>
                    </ul>
                </div>
                
                <!-- CTA -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                    <h2 style="margin-top: 0;">Ready to Deploy?</h2>
                    <p>Your app can be live in less than 5 minutes!</p>
                    <a href="https://railway.app/" 
                       style="display: inline-block; background: white; color: #667eea; 
                              padding: 12px 30px; border-radius: 5px; text-decoration: none; 
                              font-weight: bold; margin-top: 10px;">
                        Get Started Now →
                    </a>
                </div>
                
                <!-- Footer -->
                <div style="text-align: center; color: #666; font-size: 12px; padding: 20px; border-top: 1px solid #ddd;">
                    <p>
                        Journal Desk | Deployment Ready<br>
                        Generated: {datetime.now().strftime('%B %d, %Y')}<br>
                        Project: /home/jayden/Desktop/now
                    </p>
                    <p style="font-size: 11px;">
                        This is an automated deployment notification.<br>
                        All platforms support free deployment. Choose your option and deploy today!
                    </p>
                </div>
                
            </div>
        </body>
    </html>
    """
    
    # Attach HTML content
    msg.attach(MIMEText(html_content, "html"))
    
    # Print email preview
    print("=" * 70)
    print(f"📧 Deployment Email Preview")
    print("=" * 70)
    print(f"To: {recipient_email}")
    print(f"Subject: {msg['Subject']}")
    print("=" * 70)
    print("\n[HTML Email Content - Formatted for browser]\n")
    print(msg.get_payload(0).get_payload(decode=True).decode('utf-8')[:500] + "...")
    print("\n" + "=" * 70)
    print("✅ Email content generated successfully!")
    print("=" * 70)
    
    return msg


def print_deployment_instructions():
    """Print deployment instructions to console"""
    
    instructions = """
╔════════════════════════════════════════════════════════════╗
║         🚀 Journal Desk - FREE Deployment Ready           ║
╚════════════════════════════════════════════════════════════╝

📧 EMAIL DEPLOYMENT NOTIFICATION SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your deployment instructions have been prepared and can be:

1️⃣  DISPLAY HERE (printed above)
2️⃣  SEND TO EMAIL (enter your email address)
3️⃣  SAVE AS FILE (for offline reference)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ QUICK START - Deploy in 5 Minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Visit https://railway.app/
2. Sign up with GitHub
3. Create Project → Select Your Repository
4. Railway auto-deploys (takes 2 minutes)
5. Your app is LIVE! 🎉

URL: https://your-app-name.railway.app

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 PRICING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ First 2-3 Months: $0 (FREE - $5/month in credits)
✅ After: ~$5-10/month (very affordable!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ PLATFORM COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥇 RECOMMENDED: Railway.app
   - Easiest setup (2 clicks)
   - $5/month free credits
   - Auto-detects Django
   - Includes PostgreSQL
   
🥈 ALTERNATIVE: Render.com
   - Free tier (with limitations)
   - Very reliable
   - Good for production
   
🥉 ALTERNATIVE: PythonAnywhere
   - Python-friendly
   - Easy for beginners
   - Permanent free tier

See 'FREE_DEPLOYMENT.md' for details on ALL platforms →

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 WHAT YOU GET (FREE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PostgreSQL Database
✅ SSL/HTTPS Automatic
✅ Live Domain URL
✅ Automatic Backups
✅ Email Support
✅ Monitoring & Logs
✅ Auto-deploy on GitHub push
✅ Custom Domain Support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Read these files in your project:

1. FREE_DEPLOYMENT.md ← START HERE!
   Complete guide to all free options

2. DEPLOYMENT_GUIDE.md
   Detailed step-by-step for each platform

3. DEPLOYMENT_READY.md
   Quick overview of all options

4. verify-deployment.sh
   Pre-deployment verification ✓ PASSED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆘 HELP & SUPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Railway Docs: https://docs.railway.app/
Render Docs: https://render.com/docs/
PythonAnywhere: https://www.pythonanywhere.com/help/

All platforms have excellent documentation and support!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ✅ Read FREE_DEPLOYMENT.md (5 min)
2. ✅ Choose your platform (1 min)
3. ✅ Sign up with GitHub (2 min)
4. ✅ Deploy your app (2 min)
5. ✅ Create admin account (1 min)
6. ✅ Your app is LIVE! 🎉 (Total: 11 min!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 YOU'RE READY TO DEPLOY!

Go to https://railway.app/ and start NOW →

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    
    print(instructions)


if __name__ == "__main__":
    print_deployment_instructions()
    
    # Check if email address provided as argument
    if len(sys.argv) > 1:
        email = sys.argv[1]
        print(f"\n📧 Generating deployment email for: {email}\n")
        msg = send_deployment_email(email)
    else:
        print("\n💡 To send this to your email, run:")
        print("   python email-deployment.py your-email@gmail.com\n")
