import resend
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

resend.api_key= os.getenv("MAIL_API_KEY")
EMAIL_SENDER= os.getenv("SENDER_EMAIL")


def send_welcome_message(email: str, name: str):
    subject="Welcome to the Hustle Waitlist."
    content=f'''
               <html>
    <body style="font-family: Arial, sans-serif; background-color:#f4f6fb; margin:0; padding:0;">

        <table align="center" width="600" style="background:white; border-radius:8px; overflow:hidden; box-shadow:0 4px 10px rgba(0,0,0,0.05);">

            <!-- Header -->
            <tr>
                <td style="background:#2563eb; padding:25px; text-align:center; color:white;">
                    <h1 style="margin:0;">HustleApp</h1>
                    <p style="margin:5px 0 0 0;"> Quick Jobs, Reliable Hands.</p>
                </td>
            </tr>

            <!-- Body -->
            <tr>
                <td style="padding:30px; color:#333;">

                    <h2 style="color:#2563eb;">Welcome {name} 👋</h2>

                    <p>
                    Thank you for joining the <strong> HustleApp Waitlist </strong>.
                    </p>

                    <p>
                    We're excited to have you among the first group of users who will experience
                    a smarter way to grow and manage your hustle.
                    </p>

                    <p>
                    While you wait, stay connected with us for updates, new features,
                    and exclusive early access opportunities.
                    </p>

                    <!-- CTA Button -->
                    <div style="text-align:center; margin:30px 0;">
                        <a href="https://usehustleapp.com/"
                        target="_blank"
                        rel="noopener noreferrer"
                        style="background:#2563eb;
                        color:white;
                        padding:12px 25px;
                        text-decoration:none;
                        border-radius:6px;
                        font-weight:bold;">
                        Follow Our Updates
                        </a>
                    </div>

                    <p>
                    We're building something amazing, and we're glad you're part of the journey.
                    </p>
                    
                    <br>
                    <p> <strong>Follow our socials:</strong></p>
                         
                    <div>
                        <a href="https://www.tiktok.com/@usehustleapp" 
                        target="_blank" 
                        rel="noopener noreferrer "> 
                        Tiktok
                        </a>

                         <a href="https://x.com/usehustleapp"
                         target="_blank" rel="noopener noreferrer"> 
                       Twitter/X 
                        </a>  
                    </div>

                    <p>
                    Best regards,<br>
                    <strong>The HustleApp Team</strong>
                    </p>

                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td style="background:#f1f5f9; padding:15px; text-align:center; font-size:12px; color:#666;">
                    © 2026 HustleApp. All rights reserved.
                </td>
            </tr>
        </table>
    </body>
    </html>
    '''
    client = email
    resend.Emails.send(
    {
      "from":EMAIL_SENDER,
      "to":[client],
      "subject":subject,
      "html": content
    }
    )
