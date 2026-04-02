
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn
import csv
import io
from datetime import datetime

app = FastAPI()

# ---------------- DATA ----------------

DATA = [
    ["Date", "Symbol", "Open", "High", "Low", "Close", "Volume", "Sector", "Daily % Change", "Day Range"],
    ["2026-02-10", "TCS", 3980, 4025, 3960, 4010, 210000, "IT", "", ""],
    ["2026-02-10", "INFY", 1520, 1538, 1505, 1522, 185000, "IT", "", ""],
    ["2026-02-10", "HDFCB", 1420, 1435, 1410, 1415, 250000, "Banking", "", ""],
    ["2026-02-10", "SBIN", 630, 640, 625, 635, 300000, "Banking", "", ""],
    ["2026-02-10", "ONGC", 265, 270, 262, 268, 280000, "Energy", "", ""],
    ["2026-02-10", "RELI", 2480, 2510, 2475, 2505, 320000, "Energy", "", ""],
    ["2026-02-11", "TCS", 4010, 4050, 3995, 4035, 215000, "IT", "", ""],
    ["2026-02-11", "INFY", 1522, 1540, 1518, 1535, 190000, "IT", "", ""],
    ["2026-02-11", "HDFCB", 1415, 1440, 1412, 1438, 260000, "Banking", "", ""],
    ["2026-02-11", "SBIN", 635, 645, 630, 642, 310000, "Banking", "", ""],
    ["2026-02-11", "ONGC", 268, 272, 266, 270, 285000, "Energy", "", ""],
    ["2026-02-11", "RELI", 2505, 2525, 2498, 2512, 330000, "Energy", "", ""],
]

def excel_col(idx):
    s = ""
    while idx >= 0:
        s = chr(idx % 26 + 65) + s
        idx = idx // 26 - 1
    return s

from fastapi import Form
from fastapi.responses import RedirectResponse

users = {}

@app.get("/", response_class=HTMLResponse)
async def registration_form():
    return """
    <html>
    <head>
        <title>Register | Trading Assessment Portal</title>
        <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background: #f3f4f6; 
            margin: 0;
        }
        .header-company {
            width: 100%;
            background: linear-gradient(90deg, #2563eb 0%, #059669 100%);
            color: #fff;
            padding: 24px 0 10px 0;
            font-size: 2.0rem;
            text-align: center;
            font-weight: bold;
            letter-spacing: .02em;
            box-shadow: 0 2px 12px rgba(37,99,235,0.08);
        }
        .header-divider {
            width: 80px;
            height: 3px;
            background: #fff;
            border-radius: 1.5px;
            margin: 10px auto 0 auto;
        }
        .center { 
            max-width: 390px; 
            margin: 60px auto 0 auto; 
            background: #fff; 
            border-radius: 12px; 
            padding: 33px 20px 30px 20px; 
            text-align: center; 
            box-shadow: 0 1px 10px rgba(15,23,42,0.12);
        }
        h1 {
            color: #2563eb;
            margin-bottom: 10px;
            font-size: 1.9rem;
            letter-spacing: .02em;
        }
        h2 {
            margin-bottom: 2px;
            color: #232323;
            font-weight: 600;
            letter-spacing: .01em;
            font-size: 1.07rem;
        }
        .exam-instructions {
            background: #e4ecfd;
            color: #173463;
            padding: 14px 10px 8px 13px;
            border-radius: 7px;
            margin-bottom: 13px;
            text-align: left;
            font-size: 1rem;
            border-left: 4px solid #2563eb;
            line-height: 1.5;
        }
        .exam-instructions ul {
            margin-top:6px; 
            padding-left:20px;
            margin-bottom:0;
        }
        .exam-instructions li {
            margin-bottom: 1px;
            font-size: 0.99em;
        }
        .field-label {
            font-weight: 500;
            color: #193766;
            text-align: left;
            display: block;
            margin-bottom: 2px;
            margin-left:5px;
            letter-spacing: .01em;
            font-size: 1rem;
        }
        input[type="text"], input[type="password"]  {
            width: 97%;
            margin-top: 8px;
            margin-bottom: 14px;
            padding: 9px 13px;
            border-radius: 6px;
            border: 1px solid #bfc9db;
            font-size: 1.03rem;
            box-sizing: border-box;
            background: #f7fafc;
            transition: border 0.2s, background 0.2s;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            outline: 2px solid #2563eb;
            border-color:#2563eb;
            background: #eef4fb;
        }
        button { 
            margin-top: 18px; 
            padding: 10px 0; 
            border-radius: 6px; 
            border: none; 
            font-size: 1.04rem; 
            background: linear-gradient(90deg, #2563eb 0%, #059669 100%);
            color: #fff; 
            cursor: pointer; 
            font-weight: 600;
            width: 100%;
            box-shadow: 0 1px 3px rgba(37, 99, 235, 0.12);
            transition: filter 0.2s, background 0.2s;
            letter-spacing: .01em;
        }
        button:disabled { 
            opacity: 0.6; 
            cursor: not-allowed;
            filter: grayscale(0.14);
        }
        button:hover:enabled { 
            background: linear-gradient(90deg, #1d4ed8 0%, #047857 100%);
            filter: brightness(1.05);
        }
        .checkbox-label {
            margin-top: 6px;
            margin-bottom: 2px;
            font-size: 0.99rem;
            color: #2563eb;
            display: flex;
            align-items: center;
            cursor: pointer;
            user-select: none;
        }
        .checkbox-label input[type="checkbox"] {
            margin-right: 8px;
            accent-color: #2563eb;
            transform: scale(1.18);
        }
        .footer-company {
            width: 100%;
            background: #242f3e;
            color: #e7e7ec;
            text-align: center;
            padding: 14px 0 8px 0;
            font-size: 1.02rem;
            position: fixed;
            bottom: 0;
            left: 0;
            letter-spacing: .01em;
            box-shadow: 0 -1.5px 9px rgba(30,30,50,0.08);
        }
        .footer-company span {
            color: #46c181;
            font-weight: 600;
        }
        .footer-divider {
            width: 50px;
            height: 2.5px;
            background: #217346;
            border-radius: 1.5px;
            margin: 7px auto 1px auto;
        }
        @media (max-width: 600px) {
            .center { max-width: 99vw; padding: 12px 3vw 14px 3vw;}
            .header-company { font-size: 1.12rem;}
            .footer-company { font-size: 0.86rem;}
        }
        </style>
        <script>
        function toggleRegisterBtn() {
            var cb = document.getElementById('read-instructions');
            var btn = document.getElementById('register-btn');
            btn.disabled = !cb.checked;
        }
        </script>
    </head>
    <body>
      <div class="header-company">
        Time Line Investments Pvt Ltd
        <div class="header-divider"></div>
      </div>
      <div class="center">
        <h1>Trading Assessment Portal</h1>
        <div class="exam-instructions">
            <strong>Instructions:</strong>
            <ul>
                <li>Register with your username and password to start the assessment.</li>
                <li>After registration you will access DAX &amp; Excel, Python, and Chart sections.</li>
                <li>Use a unique username and remember your credentials for reviewing results or retaking exams.</li>
                <li>All information is confidential and strictly for assessment use.</li>
            </ul>
        </div>
        <h2>Register</h2>
        <form method="post" action="/login" autocomplete="off" style="margin-bottom:0;">
            <label class="field-label" for="username">Username</label>
            <input type="text" name="username" id="username" placeholder="Enter your username" maxlength="32" required autocomplete="new-username"/>

            <label class="field-label" for="password">Password</label>
            <input type="password" name="password" id="password" placeholder="Enter your password" maxlength="32" required autocomplete="new-password"/>

            <label class="checkbox-label" for="read-instructions">
              <input type="checkbox" id="read-instructions" onclick="toggleRegisterBtn()" />
              <span style="padding-top:1.5px;">I have read and understood the instructions</span>
            </label>

            <button type="submit" id="register-btn" disabled>Register & Start Exam</button>
        </form>
      </div>
      <div class="footer-company">
        <div class="footer-divider"></div>
        &copy; {year} <span>Time Line Investments Pvt Ltd</span> &mdash; All rights reserved. | Designed by Analytics Team
      </div>
      <script>
        // Set dynamic year in footer safely
        document.querySelectorAll('.footer-company').forEach(function(el){
          el.innerHTML = el.innerHTML.replace("{year}", new Date().getFullYear());
        });
        // Enter to submit support for form
        document.getElementById("username").addEventListener("keydown", function(e){
          if(e.key === "Enter") e.preventDefault();
        });
        document.getElementById("password").addEventListener("keydown", function(e){
          if(e.key === "Enter"){
            if(!document.getElementById('register-btn').disabled){
              document.getElementById('register-btn').click();
            }
            e.preventDefault();
          }
        });
      </script>
    </body>
    </html>
    """

@app.post("/login", response_class=HTMLResponse)
async def register_then_landing(username: str = Form(...), password: str = Form(...)):
    if username in users:
        # More professional, concise error page with improved wording and accessibility
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Registration Error | Trading Assessment Portal</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #f3f4f6; margin: 0; }
                .header-company {
                    width: 100%;
                    background: linear-gradient(90deg, #2563eb 0%, #059669 100%);
                    color: #fff;
                    padding: 22px 0 10px 0;
                    font-size: 2.1rem;
                    text-align: center;
                    font-weight: 700;
                    letter-spacing: .012em;
                    box-shadow: 0 2px 12px rgba(37,99,235,0.08);
                }
                .header-divider {
                    width: 74px;
                    height: 3px;
                    background: #fff;
                    border-radius: 2px;
                    margin: 10px auto 0 auto;
                }
                .error-message {
                    color: #b91c1c;
                    text-align: center;
                    max-width: 470px;
                    background: #fef2f2;
                    border-radius: 12px;
                    margin: 85px auto 0 auto;
                    box-shadow: 0 2px 18px #b91c1c15;
                    padding: 30px 25px;
                    font-size: 1.13rem;
                    font-weight: 500;
                    border: 1.3px solid #fca5a5;
                }
                .footer-company {
                    text-align: center;
                    padding: 30px 0 20px 0;
                    margin-top: 78px;
                    font-size: 1.08rem;
                    color: #596075;
                    background: #f8fafb;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                .footer-divider {
                    width: 62px;
                    height: 2px;
                    background: #e0e7ef;
                    border-radius: 1.5px;
                    margin: 0 auto 13px auto;
                }
            </style>
        </head>
        <body>
            <div class="header-company">
                Trading Assessment Portal
                <div class="header-divider"></div>
            </div>
            <main>
              <section class="error-message" role="alert" aria-live="assertive">
                <h2 style="margin-top:0;color:#c53030;font-size:1.14em;">Registration Unsuccessful</h2>
                <p>
                  The username you have chosen is already registered.<br>
                  Please select a different username to proceed with your registration.
                </p>
                <a href="/" style="color:#2563eb;text-decoration:underline;display:inline-block;margin-top:10px;font-weight:600;">Back to Registration</a>
              </section>
            </main>
            <footer class="footer-company">
                <div class="footer-divider"></div>
                &copy; <span id="footerYear"></span> Time Line Investments Pvt Ltd &mdash; All rights reserved. | Designed by Analytics Team
            </footer>
            <script>
                document.getElementById("footerYear").textContent = new Date().getFullYear();
            </script>
        </body>
        </html>
        """
    users[username] = password
    # Professionalized welcome/assessment page with streamlined language
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Welcome | Trading Assessment Portal</title>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; background: #f3f4f6; margin:0;}
            .header-company {
                width: 100%;
                background: linear-gradient(90deg, #2563eb 0%, #059669 100%);
                color: #fff;
                padding: 24px 0 10px 0;
                font-size: 2.0rem;
                text-align: center;
                font-weight: bold;
                letter-spacing: .02em;
                box-shadow: 0 2px 12px rgba(37,99,235,0.08);
            }
            .header-divider {
                width: 80px;
                height: 3px;
                background: #fff;
                border-radius: 1.5px;
                margin: 10px auto 0 auto;
            }
            .center {
                max-width: 500px;
                margin: 85px auto 0 auto;
                background: #fff;
                border-radius: 16px;
                padding: 48px 38px 43px 38px;
                text-align: center;
                box-shadow: 0 2px 14px rgba(0,0,0,0.08);
            }
            h1 { color: #2563eb; font-size:2rem; margin-top:0;}
            p.welcome-message {
                color:#3a4250;font-size:1.14rem;
                margin:22px auto 18px auto;
            }
            .btn-group { margin-top: 24px;}
            .btn {
                display: inline-block;
                margin: 10px 13px 0 0;
                padding: 14px 40px;
                background: #2563eb;
                color: #fff;
                text-decoration: none;
                font-weight: 500;
                border-radius: 8px;
                font-size: 1.11rem;
                box-shadow:0 2px 10px #2563eb18;
                border: none;
                transition: background 0.13s,box-shadow 0.15s;
                cursor:pointer;
            }
            .btn-python { background: #059669; }
            .btn-charts { background: #ea580c; }
            .btn-excel { background: #b68900; }
            .btn:hover, .btn:focus { opacity: 0.93; box-shadow:0 4px 18px #11182722; }
            .footer-company {
                text-align: center;
                padding: 28px 0 18px 0;
                margin-top: 72px;
                font-size: 1.05rem;
                color: #707784;
                background: #f8fafb;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            .footer-divider {
                width: 68px;
                height: 2px;
                background: #e0e7ef;
                border-radius: 1.5px;
                margin: 0 auto 12px auto;
            }
            @media (max-width: 650px){
                .center { padding: 10vw 2vw 10vw 2vw; max-width:96vw;}
                .header-company { font-size: 1.18rem; padding:13px 0 7px 0;}
                .btn { padding:11px 8vw; font-size:1rem;}
            }
        </style>
    </head>
    <body>
        <div class="header-company">
            Trading Assessment Portal
            <div class="header-divider"></div>
        </div>
        <main>
            <section class="center" aria-labelledby="welcomeHeader">
                <h1 id="welcomeHeader">Welcome to the Trading Assessment Portal</h1>
                <p class="welcome-message">
                    Thank you for registering. Please select the section you wish to begin.<br>
                    We wish you the best in your assessment.
                </p>
                <div class="btn-group">
                    <a href="/dax" class="btn" style="background:#2563eb;">DAX &amp; Excel Assessment</a>
                    <a href="/python" class="btn btn-python">Python Assessment</a>
                    <a href="/charts" class="btn btn-charts">Chart Section</a>
                    <a href="/exam" class="btn btn-excel">Excel Exam</a>
                </div>
            </section>
        </main>
        <footer class="footer-company">
            <div class="footer-divider"></div>
            &copy; <span id="footerYear"></span> Time Line Investments Pvt Ltd &mdash; All rights reserved. | Designed by Analytics Team
        </footer>
        <script>
            document.getElementById("footerYear").textContent = new Date().getFullYear();
        </script>
    </body>
    </html>
    """


@app.get("/login2", response_class=HTMLResponse)
def login2():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Trading Assessment Portal</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                background: #f3f4f6; 
                margin: 0;
            }
            .header-company {
                width: 100%;
                background: linear-gradient(90deg, #2563eb 0%, #059669 100%);
                color: #fff;
                padding: 28px 0 12px 0;
                font-size: 2.0rem;
                text-align: center;
                font-weight: bold;
                letter-spacing: .02em;
                box-shadow: 0 2px 12px rgba(37,99,235,0.08);
            }
            .header-divider {
                width: 80px;
                height: 3px;
                background: #fff;
                border-radius: 1.5px;
                margin: 12px auto 0 auto;
            }
            .center { 
                max-width: 520px; 
                margin: 70px auto 0 auto; 
                background: #fff; 
                border-radius: 14px; 
                padding: 48px 34px 46px 34px; 
                text-align: center; 
                box-shadow: 0 1px 18px rgba(15,23,42,0.14);
            }
            h1 {
                color: #2563eb;
                margin-bottom: 12px;
                font-size: 1.7rem;
                letter-spacing: .02em;
                font-weight: 700;
            }
            p.welcome-message {
                color: #43466c;
                font-size: 1.06rem;
                margin-bottom: 22px;
            }
            .btn-group {
                margin-top: 18px;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 13px;
            }
            .btn {
                display: inline-block;
                background: #2563eb;
                color: #fff;
                padding: 13px 34px;
                border-radius: 8px;
                margin: 2px 7px;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.07rem;
                transition: background 0.15s, opacity 0.15s;
            }
            .btn-python { background: #059669; }
            .btn-charts { background: #ea580c; }
            .btn-excel { background: #b68900; }
            .btn:hover { opacity: 0.92; box-shadow: 0 1px 7px #2563eb2d; }
            .footer-company {
                width: 100%;
                background: #242f3e;
                color: #e7e7ec;
                text-align: center;
                padding: 16px 0 9px 0;
                font-size: 1.03rem;
                position: fixed;
                bottom: 0;
                left: 0;
                letter-spacing: .01em;
                box-shadow: 0 -1.5px 9px rgba(30,30,50,0.08);
                z-index: 9;
            }
            .footer-company span {
                color: #46c181;
                font-weight: 600;
            }
            .footer-divider {
                width: 54px;
                height: 2.5px;
                background: #217346;
                border-radius: 1.5px;
                margin: 8px auto 1px auto;
            }
            @media (max-width: 600px) {
                .center { max-width: 99vw; padding: 18px 4vw 20px 4vw;}
                .header-company { font-size: 1.11rem;}
                .footer-company { font-size: 0.89rem;}
                .btn { padding:13px 8vw; font-size:0.99rem; }
            }
        </style>
    </head>
    <body>
        <div class="header-company">
            Time Line Investments Pvt Ltd
            <div class="header-divider"></div>
        </div>
        <main>
            <section class="center" aria-labelledby="welcomeHeader">
                <h1 id="welcomeHeader">Welcome to the Trading Assessment Portal</h1>
                <p class="welcome-message">
                    Thank you for registering. Please select the assessment section to begin.<br>
                    Wishing you success in your journey!
                </p>
                <div class="btn-group">
                    <a href="/dax" class="btn" style="background:#2563eb;">DAX &amp; Excel Assessment</a>
                    <a href="/python" class="btn btn-python">Python Assessment</a>
                    <a href="/charts" class="btn btn-charts">Chart Section</a>
                    <a href="/exam" class="btn btn-excel">Excel Exam</a>
                </div>
            </section>
        </main>
        <footer class="footer-company">
            <div class="footer-divider"></div>
            &copy; <span id="footerYear"></span> Time Line Investments Pvt Ltd &mdash; All rights reserved. | Designed by Analytics Team
        </footer>
        <script>
            document.getElementById("footerYear").textContent = new Date().getFullYear();
        </script>
    </body>
    </html>
    """

@app.get("/download", response_class=HTMLResponse)
def download():
    output = io.StringIO()
    writer = csv.writer(output)
    for row in DATA:
        writer.writerow(row)
    csv_content = output.getvalue()
    filename = f"excel_exam_export_{datetime.now().strftime('%Y%m%d')}.csv"
    return HTMLResponse(
        content=csv_content,
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-type": "text/csv"
        }
    )
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse

def exam_already_completed(request: Request) -> bool:
    """
    Returns True if the client already completed the exam:
    - Either: the exam timer expired (exam_timer_end cookie <= now)
    - Or: the exam was submitted (exam_done cookie exists and is '1')
    """
    timer_cookie = request.cookies.get("exam_timer_end")
    exam_done = request.cookies.get("exam_done")
    import time

    # Check if exam_done cookie is set to "1"
    if exam_done == "1":
        return True

    # If timer_cookie exists and is <= current time, means exam time over
    try:
        if timer_cookie and (int(timer_cookie) <= int(time.time())):
            return True
    except Exception:
        pass
    return False


@app.get("/exam", response_class=HTMLResponse)
async def exam(
    request: Request,
    q: int = Query(1),
    sort: str = Query(None),
    top3: str = Query(None),
    goto: int = Query(None)
):
    # Block access if time is over or exam is already submitted
    if exam_already_completed(request):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Excel Exam (Completed)</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <style>
          body { background:#f3f3f3;font-family:Calibri,Arial,sans-serif;margin:0;}
          .msgbox {
            max-width:550px;background:#fffbe7;
            border: 2.2px solid #eacd6a;
            margin:70px auto 0 auto;padding:44px 28px 26px 28px;
            border-radius:11px;box-shadow:0 4px 24px #f7cc361b;
            text-align:center;
          }
          .msgbox h1{color:#b68900;font-size:2rem;}
          .msgbox p{color:#8b7003;font-size:1.2rem;margin-top:14px;}
          .msgbox a {display:inline-block;margin-top:20px;font-size:1rem;background:#2563eb;color:#fff;padding:10px 24px;text-decoration:none;border-radius:7px;}
        </style>
        </head>
        <body>
        <div class="msgbox">
          <h1>📝 Exam Already Completed</h1>
          <p>Your access to the Excel Exam is now closed.<br>
          It was either submitted or the allowed time has expired.<br>
          <span style='color:#476a22;font-size:0.97rem;'>For any queries, please contact your instructor.</span>
          </p>
          <a href="/dax">Continue to DAX Section &rarr;</a>
        </div>
        <script>
        document.cookie = "exam_done=1;path=/;expires=Fri, 31 Dec 2100 23:59:59 GMT";
        </script>
        </body>
        </html>
        """
        response = HTMLResponse(content=html)
        response.set_cookie("exam_done", "1", path="/", samesite="lax")
        return response

    header = DATA[0]
    nav_html = """
    <div class="top-nav" style="margin-bottom:24px;text-align:center;">
        <a href="/login2" class="btn" style="background:#2563eb;color:#fff;margin-right:9px;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">🏠 Dashboard</a>
        <a href="/dax" class="btn" style="background:#2563eb;color:#fff;margin-right:9px;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">📈 DAX Assessment</a>
        <a href="/python" class="btn" style="background:#059669;color:#fff;margin-right:9px;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">🐍 Python Assessment</a>
        <a href="/charts" class="btn" style="background:#ea580c;color:#fff;margin-right:9px;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">📊 Chart Section</a>
        <a href="/exam" class="btn btn-excel" style="background:#b68900;color:#fff;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">📝 Excel Exam</a>
    </div>
    """

    timer_html = """
    <div id="exam-timer" style="text-align:center;font-size:16pt;font-weight:bold;background:#f7f7e8;color:#b16200;padding:10px 0;margin:20px 0 8px 0;border-radius:7px;
        border:1.5px solid #f4ce42;max-width:400px;margin-left:auto;margin-right:auto;" aria-live="polite">
      ⏰ <span id="timer-label">Time Left:</span> <span id="timer-minutes">30</span>:<span id="timer-seconds">00</span>
    </div>
    <script>
      var g_exam_time_over = false;
      (function(){
        function getEndTime() {
          var name = 'exam_timer_end=';
          var ca = document.cookie.split(';');
          for(var i=0;i<ca.length;i++) {
            var c = ca[i];
            while(c.charAt(0)==' ')c=c.substring(1,c.length);
            if(c.indexOf(name)==0) return parseInt(c.substring(name.length,c.length));
          }
          return null;
        }
        function setEndTime(secs) {
          var d = new Date();
          d.setTime(d.getTime()+(secs*1000));
          document.cookie = "exam_timer_end="+(Math.floor(Date.now()/1000) + secs)+";expires="+d.toUTCString()+";path=/";
        }
        var end = getEndTime();
        var now = Math.floor(Date.now()/1000);
        if(!end || isNaN(end) || end-now > 1800 || end-now < 0) {
          setEndTime(1800);
          end = Math.floor(Date.now()/1000) + 1800;
        }
        function updateTimer() {
          var now = Math.floor(Date.now()/1000);
          var left = end - now;
          if(left < 0) left = 0;
          var min = Math.floor(left/60);
          var sec = left%60;
          document.getElementById("timer-minutes").textContent = ("0"+min).slice(-2);
          document.getElementById("timer-seconds").textContent = ("0"+sec).slice(-2);
          if(left <= 0) {
            document.getElementById("exam-timer").style.background="#ffe1e1";
            document.getElementById("exam-timer").style.color="#c00";
            document.getElementById("timer-label").textContent = "Exam Time is Over!";
            Array.from(document.getElementsByClassName('excel-input-sheet')).forEach(inp=>{
              inp.disabled = true;
              inp.style.background="#fdeaea";
              inp.title = 'Time Over';
            });
            if (!g_exam_time_over) {
              g_exam_time_over = true;
              document.cookie = "exam_done=1;path=/;expires=Fri, 31 Dec 2100 23:59:59 GMT";
              setTimeout(function(){
                window.location.href = "/dax";
              }, 1750);
            }
          }
        }
        updateTimer();
        setInterval(updateTimer,1000);
      })();
    </script>
    """

    # --------- BEGIN: Added SIGNAL question as 5th task ---------
    pages = [
        {
            "name": "Daily % Change",
            "desc": """Enter the Excel formula for <b>% Change</b> using <span style='color:#185'>=ROUND((Close-Open)/Open,4)</span> or <b>=(F3-C3)/C3</b> in highlighted column.<br>
            <span style="color:#555;font-weight:500;">You can apply your formula to all rows by dragging/copy just like Excel!</span><br>
            <span style="color:#b28c0b;font-weight:600;">You can also drag the formula handle to apply to all rows below like Excel (dbl-click).</span>""",
            "column_title": "Daily % Change",
            "col_idx": 8,
            "placeholder": "Enter formula...",
            "excelCheckFunc": "excelCheck",
            "cell_class": "cell-input"
        },
        {
            "name": "Day Range (High−Low)",
            "desc": """Enter Excel formula (e.g. <b>=D3-E3</b>) for Day Range in highlighted column.<br>
            <span style="color:#555;font-weight:500;">You can apply your formula to all rows by dragging/copy just like Excel!</span><br>
            <span style="color:#b28c0b;font-weight:600;">You can also drag the formula handle to apply to all rows below like Excel (dbl-click).</span>""",
            "column_title": "Day Range",
            "col_idx": 9,
            "placeholder": "Enter formula...",
            "excelCheckFunc": "dayRangeCheck",
            "cell_class": "cell-input dayrange"
        },
        {
            "name": "High Volume Check (IF Formula)",
            "desc": """Use an <b>Excel IF formula</b> to mark whether the <b>Volume</b> is "High Volume" or "Normal Volume" for each stock.<br>
            <ul>
                <li><b>High Volume</b>: If <b>Volume</b> is greater than 250,000</li>
                <li><b>Normal Volume</b>: Otherwise</li>
            </ul>
            <span style="color:#555;font-weight:500;">Example formula: <b>=IF(G3&gt;250000,"High Volume","Normal Volume")</b> (replace G3 with the cell for Volume in that row).</span><br>
            <span style="color:#b28c0b;font-weight:600;">Drag the formula handle to fill all rows, like in Excel!</span>""",
            "column_title": "High Volume",
            "col_idx": 11,  # New column for High Volume after last index 10 (Signal)
            "placeholder": 'Enter IF() formula...',
            "excelCheckFunc": "highVolumeCheck",
            "cell_class": "cell-input highvolume-input"
        },
        {
            "name": "Signal (BUY/SELL/NEUTRAL): Excel IF Formula",
            "desc": """
            <b>Classify the <span style="color:#197600">Signal</span> column as <span style="color:green"><b>BUY</b></span>, <span style="color:#b80000"><b>SELL</b></span>, or <b>NEUTRAL</b> based on <b>Open</b> and <b>Close</b> prices:</b> <br>
            <ul>
                <li><b>BUY</b> = When Open &lt; Close</li>
                <li><b>SELL</b> = When Open &gt; Close</li>
                <li><b>NEUTRAL</b> = When Open = Close</li>
            </ul>
            <span style="font-size:11pt">Use an <b>Excel IF formula</b> (e.g. <span style="color:#185;font-weight:600">=IF(C3&lt;F3,"BUY",IF(C3&gt;F3,"SELL","NEUTRAL"))</span>) for each row in the <b>Signal</b> column.<br>
            You can apply your formula to all rows by dragging/copy just like in Excel!
            <br>
            <span style="color:#b28c0b;font-weight:600;">Try to use <b>=IF()</b> and nested IF in Excel style for logic!</span></span>
            """,
            "column_title": "Signal",
            "col_idx": 10,   # New column for Signal (after last index 9)
            "placeholder": 'Enter IF() formula...',
            "excelCheckFunc": "signalCheck",
            "cell_class": "cell-input signal-input"
        }
    ]

    if goto is not None and 1 <= goto <= len(pages):
        q = goto

    q = max(1, min(q, 4))
    page = pages[q - 1]
    standard_bg = "#ffffff"
    standard_grid = "#d4d4d4"
    selected_bg = "#fff2cc"
    header_bg = "#f3f3f3"
    green_highlight = "#c6efce"
    yellow_highlight = "#fff999"
    blue_highlight = "#e3e5ff"
    signal_highlight = "#fff5dc"

    table_html = ""
    if q in (1, 2, 3):
        col_input_index = page["col_idx"]
        for i, row in enumerate(DATA[1:], start=2):
            table_html += "<tr>"
            for col_index, cell in enumerate(row):
                cell_style = (
                    "background:#fffbe5;" if (q == 1 and col_index == 8)
                    or (q == 2 and col_index == 9)
                    or (q == 3 and col_index == 11)
                    else "background:#ffffff;"
                )
                if col_index == col_input_index and q in (1, 2, 3):
                    table_html += f"""
                    <td style="padding:0 1px;vertical-align:middle;{cell_style}position:relative;">
                        <div style="display:flex;align-items:center;position:relative;">
                            <input type='text'
                                class='{pages[q - 1]['cell_class']} excel-input-sheet'
                                id='input_{i}_{col_index}'
                                style="border:none;background:transparent;width:calc(100% - 18px);height:23px;font-size:11pt;padding:0 5px;font-family:'Calibri',Arial,sans-serif;"
                                placeholder='{pages[q - 1]['placeholder']}'
                                autocomplete='off' data-row='{i}' data-col='{col_index}'>
                            <div class="excel-drag-fill" title="Drag/copy formula (dbl-click to fill down)" 
                                 style="width:10px;height:22px;display:inline-block;cursor:crosshair;background:transparent;position:relative;margin-left:2px;"
                                 data-row="{i}" data-col="{col_index}"></div>
                        </div>
                    </td>
                    """
                else:
                    table_html += f"<td style='padding:0 1px;vertical-align:middle;{cell_style}font-family:Calibri,Arial,sans-serif;font-size:11pt;'>{cell}</td>"
            table_html += f"<td id='res_{i}' style='background:{standard_bg};font-family:Calibri,Arial,sans-serif;font-size:11pt;padding:0 5px;'></td></tr>"

    elif q == 4:
        col_input_index = page["col_idx"]
        for i, row in enumerate(DATA[1:], start=2):
            table_html += "<tr>"
            for col_index, cell in enumerate(row):
                cell_style = "background:#ffffff;"
                table_html += f"<td style='padding:0 1px;vertical-align:middle;{cell_style}font-family:Calibri,Arial,sans-serif;font-size:11pt;'>{cell}</td>"
            cell_style = "background:%s;" % signal_highlight
            table_html += f"""
            <td style="padding:0 1px;vertical-align:middle;{cell_style}position:relative;">
                <div style="display:flex;align-items:center;position:relative;">
                    <input type='text'
                        class='{page['cell_class']} excel-input-sheet'
                        id='input_{i}_{col_input_index}'
                        style="border:none;background:transparent;width:calc(100% - 18px);height:23px;font-size:11pt;padding:0 5px;font-family:'Calibri',Arial,sans-serif;"
                        placeholder='{page['placeholder']}'
                        autocomplete='off' data-row='{i}' data-col='{col_input_index}'>
                    <div class="excel-drag-fill" title="Drag/copy formula (dbl-click to fill down)" 
                         style="width:10px;height:22px;display:inline-block;cursor:crosshair;background:transparent;position:relative;margin-left:2px;"
                         data-row="{i}" data-col="{col_input_index}"></div>
                </div>
            </td>
            <td id='res_{i}' style='background:{standard_bg};font-family:Calibri,Arial,sans-serif;font-size:11pt;padding:0 5px;'></td></tr>
            """

        table_html += """
        <tr>
          <td colspan="100" style="text-align:center;padding:30px 0 10px 0;">
            <button id="submit-exam-btn" class="excel-btn-action" style="font-size:15.5px;padding:10px 30px 10px 22px;border-radius:8px;background:#217346;" type='button'>
              Submit Exam &amp; Continue to DAX &rarr;
            </button>
          </td>
        </tr>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            var btn = document.getElementById("submit-exam-btn");
            if(btn) btn.onclick = function() {
                document.cookie = "exam_done=1;path=/;expires=Fri, 31 Dec 2100 23:59:59 GMT";
                setTimeout(function(){
                  window.location.href = "/dax";
                }, 150);
            };
        });
        </script>
        """

    excel_css = f"""
    <style>
        body {{
            background: #f4f8fa;
            font-family: 'Calibri', Arial, sans-serif;
        }}
        .excel-sheet-wrapper {{
            border:1px solid {standard_grid};
            border-radius:8px;
            box-shadow:0 6px 20px #a0aec03c, 0 0px 2px #c9c9c9;
            padding:16px 28px;
            background:#fcfdfe;
            max-width:1120px;
        }}
        .excel-table-x {{
            border-spacing: 0;
            border-collapse: separate;
            margin: 23px auto 18px auto;
            background: {standard_bg};
            min-width: 1000px;
            box-shadow:0 0 0 2px #e7e7e7;
        }}
        .excel-table-x th, .excel-table-x td {{
            border: 1px solid #d4d4d4;
            padding: 0 1px;
            min-width: 95px;
            height: 23px;
            font-size: 11pt;
            font-family: 'Calibri', Arial, sans-serif;
            background: #fff;
            text-align:left;
            vertical-align: middle;
            transition: background 0.10s;
        }}
        .excel-table-x th.excel-top-header {{
            background: {header_bg};
            color: #222;
            border-bottom: 2.5px solid #bababa;
            text-align: center;
            font-size:11.5pt;
            font-family:'Calibri',Arial,sans-serif;
            font-weight: 600;
        }}
        .excel-table-x th.excel-col-letters {{
            background: #e7e7e7;
            color: #222;
            font-family:'Calibri',Arial,sans-serif;
            font-size:10.5pt;
            text-align:center;
            border-bottom: 2px solid #b8b8b8;
        }}
        .excel-table-x tr:hover td, .excel-table-x tr:focus-within td {{
            background: #e9f1fe;
            transition: background 0.07s;
        }}
        .excel-table-x input[type="text"], .excel-input-sheet {{
            border: none;
            outline: none;
            background: transparent;
            width: 98%;
            height:21px;
            font-size: 11pt;
            font-family: 'Calibri', Arial, sans-serif;
            padding: 0 5px;
            margin: 0;
            box-sizing: border-box;
        }}
        .excel-table-x input[type="text"]:focus, .excel-input-sheet:focus {{
            background: {selected_bg};
            box-shadow: 0 0 4px #d2bb68d0;
            border-radius:3px;
            border: 1.4px solid #b99a37;
            outline: none;
        }}
        .excel-result-cell {{
            min-width: 100px;
        }}
        .excel-result-success {{
            color: #38761d;
            font-weight: bold;
        }}
        .excel-result-error {{
            color: #e06666;
            font-weight: bold;
        }}
        .excel-result-warn {{
            color: #e69138;
            font-weight: 500;
        }}
        .yellow-hl-x {{ background: #fff999 !important; }}
        .excel-green-correct {{
            color: #38761d;
            font-weight:bold;
        }}
        .excel-warning-calc {{
            color: #e69138;
            font-weight: 500;
        }}
        .excel-err-msg {{
            color:#e06666;
            font-weight:bold;
        }}
        .excel-user-bar {{
            text-align:right;
            color:#217346;
            font-size:11pt;
            padding-bottom:7px;
            font-family:'Calibri',Arial,sans-serif;
        }}
        .excel-nav-bar {{
            background: #e1ebf5;
            padding: 7px 22px 8px 22px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border-bottom: 2.5px solid #a4b1d1;
            display:flex;
            align-items:center;
            font-size:11.5pt;
            font-family:'Calibri',Arial,sans-serif;
        }}
        .excel-row-green {{
            background: {green_highlight} !important;
        }}
        .excel-btn-action {{
            background: #218c3f;
            color: #fff;
            border: none;
            border-radius: 4px;
            padding: 6px 21px;
            margin: 0 7px 9px 0;
            font-size: 11pt;
            font-family: 'Calibri', Arial, sans-serif;
            cursor: pointer;
            font-weight: 700;
            box-shadow: 0 2px 7px #21734617;
            transition: background .14s;
            text-align:center;
        }}
        .excel-btn-action:hover, .excel-btn-action:focus {{
            background: #14642b;
        }}
        .excel-btn-action.reset {{
            background: #e0e4ec;
            color: #246;
            font-weight: 500;
        }}
        .excel-btn-action.reset:hover, .excel-btn-action.reset:focus {{
            background: #e9edfa;
            color: #217346;
        }}
        .excel-drag-fill {{
            border: none;
            border-radius: 2px;
            background: #8c8c8c26;
            transition: background 0.09s;
        }}
        .excel-drag-fill:hover {{
            background: #c7bf07a2;
        }}
        .excel-drag-fill:active {{
            background: #ffe700b2;
        }}
        @media (max-width:1200px) {{
            .excel-table-x {{ width:97vw;overflow-x:auto;min-width:750px; }}
            .excel-sheet-wrapper {{padding:10px 2vw;}}
        }}
        .goto-page-select {{
            margin-left: 18px;
            font-size: 11pt;
            font-family: 'Calibri',Arial,sans-serif;
            border-radius: 5px;
            padding: 3px 7px;
            border: 1px solid #aed6c4;
            background: #f6fafd;
            outline: none;
        }}
    </style>
    """

    js_formula_eval = """
    document.addEventListener('DOMContentLoaded', function () {
        function cellValue(row, col) {
            const cell = document.querySelector('#input_' + row + '_' + col);
            if (cell && cell.value) return cell.value;
            return null;
        }
        function getCellFromData(row, col) {
            var data = [
                ["Date", "Symbol", "Open", "High", "Low", "Close", "Volume", "Sector", "Daily % Change", "Day Range"],
                ["2026-02-10", "TCS", 3980, 4025, 3960, 4010, 210000, "IT", "", ""],
                ["2026-02-10", "INFY", 1520, 1538, 1505, 1522, 185000, "IT", "", ""],
                ["2026-02-10", "HDFCB", 1420, 1435, 1410, 1415, 250000, "Banking", "", ""],
                ["2026-02-10", "SBIN", 630, 640, 625, 635, 300000, "Banking", "", ""],
                ["2026-02-10", "ONGC", 265, 270, 262, 268, 280000, "Energy", "", ""],
                ["2026-02-10", "RELI", 2480, 2510, 2475, 2505, 320000, "Energy", "", ""],
                ["2026-02-11", "TCS", 4010, 4050, 3995, 4035, 215000, "IT", "", ""],
                ["2026-02-11", "INFY", 1522, 1540, 1518, 1535, 190000, "IT", "", ""],
                ["2026-02-11", "HDFCB", 1415, 1440, 1412, 1438, 260000, "Banking", "", ""],
                ["2026-02-11", "SBIN", 635, 645, 630, 642, 310000, "Banking", "", ""],
                ["2026-02-11", "ONGC", 268, 272, 266, 270, 285000, "Energy", "", ""],
                ["2026-02-11", "RELI", 2505, 2525, 2498, 2512, 330000, "Energy", "", ""]
            ];
            if (typeof row !== "number" || typeof col !== "number") return 0;
            if (row < 0 || row >= data.length) return 0;
            if (col < 0 || col >= data[0].length) return 0;
            return data[row][col];
        }

        function parseCellRef(cellRef) {
            var match = /^([A-L])([0-9]+)$/i.exec(cellRef);
            if (!match) return null;
            var colLetter = match[1].toUpperCase();
            var colLetterToIdx = {C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11};
            var baseColIdx = colLetterToIdx[colLetter];
            var rowIdx = parseInt(match[2], 10);
            if (isNaN(baseColIdx) || isNaN(rowIdx)) return null;
            return { col: baseColIdx, row: rowIdx };
        }

        function convertFormula(f, currRowNum) {
            if (!f || !f.trim().startsWith('=')) return null;
            var v = f.trim();
            v = v.replace(/^=/, "");
            var cellRefs = [];
            var colLetterToIdx = {C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11};
            var regex = /([A-L])([0-9]+)/gi;
            var m;
            while (m = regex.exec(v)) {
                cellRefs.push({colLetter: m[1], row: Number(m[2])});
            }
            var relOffset = null;
            if (cellRefs.length > 0) {
                relOffset = currRowNum - cellRefs[0].row;
            }
            v = v.replace(/([A-L])([0-9]+)/gi, function(m, let, baseRow) {
                let baseIdx = colLetterToIdx[let.toUpperCase()];
                var outRow = parseInt(baseRow, 10);
                if (relOffset !== null) outRow = parseInt(baseRow, 10) + relOffset;
                if (outRow < 2) outRow = 2;
                if (outRow > 13) outRow = 13;
                return getCellFromData(outRow - 1, baseIdx);
            });
            v = v.replace(/ROUND\(([^,]+),([0-9]+)\)/gi, function(m, expr, dec) {
                return "(Math.round((" + expr + ")*Math.pow(10," + dec + "))/Math.pow(10," + dec + "))";
            });
            v = v.replace(/SQRT\(([^)]+)\)/gi, function(m, arg) {
                return "Math.sqrt(" + arg + ")";
            });
            v = v.replace(/IF\(([^,]+),([^,]+),([^)]+)\)/gi, function(m, cond, v1, v2) {
                return '((' + cond + ')?(' + v1 + '):(' + v2 + '))';
            });
            return v;
        }

        function formatResult(val) {
            if (typeof val === "number" && isFinite(val)) {
                if (Math.abs(val) > 10000)
                    return val.toExponential(2);
                if (Math.abs(val) > 1)
                    return val.toLocaleString(undefined, { maximumFractionDigits: 3 });
                return Number(val).toFixed(4);
            }
            if (val === undefined || val === null || val === "") return "";
            return String(val).replace(/^"(.*)"$/, "$1");
        }

        function checkAnswer(row, col, formula, qtype) {
            let correct = null, warn = false, msg = "", result = "";
            try {
                let code = convertFormula(formula, row);
                if (!code) {
                    result = "";
                } else {
                    let val = eval(code);
                    result = formatResult(val);

                    if (qtype === 1) {
                        let open = getCellFromData(row, 2);
                        let close = getCellFromData(row, 5);
                        let correctVal = (Math.round((close-open)/open*10000)/10000);
                        let userVal = parseFloat(result);
                        if (isNaN(userVal)) {
                            msg = "<span class='excel-result-error'>#ERROR</span>";
                        } else if (Math.abs(userVal - correctVal) < 0.001) {
                            msg = "<span class='excel-result-success'>&#10004; {}</span>".replace("{}", result);
                        } else {
                            msg = "<span class='excel-result-warn'>&#9888; {}</span>".replace("{}", result);
                        }
                    } 
                    else if (qtype === 3) {
                        // CORRECTED LOGIC for 'High Volume Check'
                        let volume = getCellFromData(row, 6);
                        let correctVal = volume > 250000 ? "High Volume" : "Normal Volume";
                        let userVal = (result + "").replace(/"/g, "").trim();

                        // Accept case-insensitive, ignore spaces, and partial inputs.
                        function normalize(val) { return (val || "").replace(/\s+/g, "").toLowerCase(); }
                        let userNorm = normalize(userVal);
                        let correctNorm = normalize(correctVal);

                        if (userVal === "") {
                            msg = "";
                        } 
                        else if (userNorm === correctNorm) {
                            msg = "<span class='excel-result-success'>&#10004; {}</span>".replace("{}", userVal);
                        }
                        // Accept partial credit for just "high"/"normal"
                        else if (
                            (userNorm === "high" && correctNorm === "highvolume") ||
                            (userNorm === "normal" && correctNorm === "normalvolume")
                        ) {
                            msg = "<span class='excel-result-warn'>&#9888; {}</span>".replace("{}", userVal);
                        }
                        else if (
                            ["highvolume","normalvolume","volumecheck"].includes(userNorm)
                        ) {
                            msg = "<span class='excel-result-warn'>&#9888; {}</span>".replace("{}", userVal);
                        } else {
                            msg = "<span class='excel-result-error'>#ERROR</span>";
                        }
                    }
                    else if (qtype === 2) {
                        let hi = getCellFromData(row, 3);
                        let lo = getCellFromData(row, 4);
                        let correctVal2 = (Math.round((hi-lo)*100)/100);
                        let userVal2 = parseFloat(result);
                        if (isNaN(userVal2)) {
                            msg = "<span class='excel-result-error'>#ERROR</span>";
                        } else if (Math.abs(userVal2 - correctVal2) < 0.01) {
                            msg = "<span class='excel-result-success'>&#10004; {}</span>".replace("{}", result);
                        } else {
                            msg = "<span class='excel-result-warn'>&#9888; {}</span>".replace("{}", result);
                        }
                    } else if (qtype === 5) {
                        let open = getCellFromData(row, 2);
                        let close = getCellFromData(row, 5);

                        let correctSignal = "NEUTRAL";
                        if (open < close) correctSignal = "BUY";
                        else if (open > close) correctSignal = "SELL";

                        let userSignal = (result + "").toUpperCase().replace(/"/g,"").replace(/\s+/g,"");
                        let correctSignalComp = correctSignal.replace(/\s+/g,"").toUpperCase();
                        if (userSignal === "") {
                            msg = "";
                        } else if (userSignal == correctSignalComp) {
                            msg = "<span class='excel-result-success'>&#10004; "+correctSignal+"</span>";
                        } else if (["BUY","SELL","NEUTRAL"].includes(userSignal)) {
                            msg = "<span class='excel-result-warn'>&#9888; "+userSignal+" (should be "+correctSignal+")</span>";
                        } else {
                            msg = "<span class='excel-result-error'>#ERROR</span>";
                        }
                    } else {
                        msg = result;
                    }
                }
            } catch (e) {
                msg = "<span class='excel-result-error'>#ERROR</span>";
            }
            return msg;
        }

        function setupExcelDragFillToAllRows() {
            document.querySelectorAll('.excel-drag-fill').forEach(function(dragHandle) {
                dragHandle.addEventListener('dblclick', function(e) {
                    var col = dragHandle.getAttribute('data-col');
                    var row = parseInt(dragHandle.getAttribute('data-row'));
                    var field = document.querySelector('#input_' + row + '_' + col);
                    if (!field) return;
                    var value = field.value;
                    if (value.trim().startsWith('=')) {
                        var baseFormula = value.trim();
                        var colLetterToIdx = {C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11};
                        var regex = /([A-L])([0-9]+)/gi;
                        var match = regex.exec(baseFormula.replace(/^=/, ""));
                        var anchorRowNum = null;
                        if (match) {
                            anchorRowNum = parseInt(match[2], 10);
                        }
                        document.querySelectorAll('.excel-input-sheet[data-col="' + col + '"]').forEach(function (el) {
                            var erow = parseInt(el.getAttribute('data-row'));
                            if (erow >= row) {
                                if (anchorRowNum !== null) {
                                    var rowDiff = erow - row;
                                    var newFormula = baseFormula.replace(/^=/, "").replace(/([A-L])([0-9]+)/gi, function(m, let, rnum) {
                                        var newRnum = parseInt(rnum,10) + rowDiff + (row - anchorRowNum);
                                        if (newRnum < 2) newRnum = 2;
                                        if (newRnum > 13) newRnum = 13;
                                        return let.toUpperCase() + newRnum;
                                    });
                                    el.value = "=" + newFormula;
                                } else {
                                    el.value = value;
                                }
                                el.dispatchEvent(new Event("input"));
                            }
                        });
                    } else {
                        document.querySelectorAll('.excel-input-sheet[data-col="' + col + '"]').forEach(function (el) {
                            var erow = parseInt(el.getAttribute('data-row'));
                            if (erow >= row) {
                                el.value = value;
                                el.dispatchEvent(new Event("input"));
                            }
                        });
                    }
                });
                dragHandle.addEventListener('mouseenter', function() { dragHandle.style.background = "#ffe700b2"; });
                dragHandle.addEventListener('mouseleave', function() { dragHandle.style.background = "#8c8c8c26"; });
            });
            document.querySelectorAll('.excel-input-sheet').forEach(function(inp) {
                inp.addEventListener('dblclick', function(e) {
                    var col = inp.getAttribute('data-col');
                    var row = parseInt(inp.getAttribute('data-row'));
                    var value = inp.value;
                    if (value.trim().startsWith('=')) {
                        var baseFormula = value.trim();
                        var colLetterToIdx = {C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11};
                        var regex = /([A-L])([0-9]+)/gi;
                        var match = regex.exec(baseFormula.replace(/^=/, ""));
                        var anchorRowNum = null;
                        if (match) {
                            anchorRowNum = parseInt(match[2], 10);
                        }
                        document.querySelectorAll('.excel-input-sheet[data-col="' + col + '"]').forEach(function (el) {
                            var erow = parseInt(el.getAttribute('data-row'));
                            if (erow >= row) {
                                if (anchorRowNum !== null) {
                                    var rowDiff = erow - row;
                                    var newFormula = baseFormula.replace(/^=/, "").replace(/([A-L])([0-9]+)/gi, function(m, let, rnum) {
                                        var newRnum = parseInt(rnum,10) + rowDiff + (row - anchorRowNum);
                                        if (newRnum < 2) newRnum = 2;
                                        if (newRnum > 13) newRnum = 13;
                                        return let.toUpperCase() + newRnum;
                                    });
                                    el.value = "=" + newFormula;
                                } else {
                                    el.value = value;
                                }
                                el.dispatchEvent(new Event("input"));
                            }
                        });
                    } else {
                        document.querySelectorAll('.excel-input-sheet[data-col="' + col + '"]').forEach(function (el) {
                            var erow = parseInt(el.getAttribute('data-row'));
                            if (erow >= row) {
                                el.value = value;
                                el.dispatchEvent(new Event("input"));
                            }
                        });
                    }
                });
            });
        }

        document.querySelectorAll('.excel-input-sheet').forEach(function(inp) {
            inp.addEventListener('input', function() {
                let row = parseInt(inp.getAttribute('data-row'));
                let col = parseInt(inp.getAttribute('data-col'));
                let formula = inp.value;
                let q = 1;
                try {
                    let u = new URL(window.location);
                    q = parseInt(u.searchParams.get('q') || "1");
                } catch (e) { q=1 }
                let resEl = document.getElementById('res_' + row);
                resEl.classList.remove('excel-result-success','excel-result-error','excel-result-warn');
                if(formula.trim() === "") {
                    resEl.innerHTML = "";
                    return;
                }
                let res = checkAnswer(row, col, formula, q);
                resEl.innerHTML = res;
            });
        });

        function handleInputFormulaPaste(e) {
            let value = e.target.value;
            let col = e.target.getAttribute('data-col');
            let startRow = parseInt(e.target.getAttribute('data-row'));
            if (value && (e.inputType === 'insertFromPaste' || e.inputType === 'insertReplacementText')) {
                if (value.trim().startsWith('=')) {
                    var baseFormula = value.trim();
                    var regex = /([A-L])([0-9]+)/gi;
                    var match = regex.exec(baseFormula.replace(/^=/, ""));
                    var anchorRowNum = null;
                    if (match) {
                        anchorRowNum = parseInt(match[2], 10);
                    }
                    document.querySelectorAll('.excel-input-sheet[data-col="' + col + '"]').forEach(function (inp) {
                        var erow = parseInt(inp.getAttribute('data-row'));
                        if (erow >= startRow) {
                            if (anchorRowNum !== null) {
                                var rowDiff = erow - startRow + (startRow - anchorRowNum);
                                var newFormula = baseFormula.replace(/^=/, "").replace(/([A-L])([0-9]+)/gi, function(m, let, rnum) {
                                    var newRnum = parseInt(rnum,10) + rowDiff;
                                    if (newRnum < 2) newRnum = 2;
                                    if (newRnum > 13) newRnum = 13;
                                    return let.toUpperCase() + newRnum;
                                });
                                inp.value = "=" + newFormula;
                            } else {
                                inp.value = value;
                            }
                            inp.dispatchEvent(new Event("input"));
                        }
                    });
                } else {
                    document.querySelectorAll('.excel-input-sheet[data-col="' + col + '"]').forEach(function (inp) {
                        inp.value = value;
                        inp.dispatchEvent(new Event("input"));
                    });
                }
            }
        }

        document.querySelectorAll('.excel-input-sheet').forEach(function (inp) {
            inp.addEventListener('input', handleInputFormulaPaste);
        });

        function setupFirstRowAutoFill() {
            document.querySelectorAll('.excel-input-sheet[data-row="2"]').forEach(function(firstRowInput) {
                firstRowInput.addEventListener('input', function(e) {
                    var col = firstRowInput.getAttribute('data-col');
                    var val = firstRowInput.value;
                    if (val.trim().startsWith('=')) {
                        var baseFormula = val.trim();
                        var regex = /([A-L])([0-9]+)/gi;
                        var match = regex.exec(baseFormula.replace(/^=/, ""));
                        var anchorRowNum = null;
                        if (match) {
                            anchorRowNum = parseInt(match[2], 10);
                        }
                        document.querySelectorAll('.excel-input-sheet[data-col="'+col+'"]').forEach(function(el) {
                            if (el !== firstRowInput) {
                                var erow = parseInt(el.getAttribute('data-row'));
                                if (anchorRowNum !== null) {
                                    var rowDiff = erow - 2;
                                    var newFormula = baseFormula.replace(/^=/, "").replace(/([A-L])([0-9]+)/gi, function(m, let, rnum) {
                                        var newRnum = parseInt(rnum,10) + rowDiff;
                                        if (newRnum < 2) newRnum = 2;
                                        if (newRnum > 13) newRnum = 13;
                                        return let.toUpperCase() + newRnum;
                                    });
                                    el.value = "=" + newFormula;
                                } else {
                                    el.value = val;
                                }
                                el.dispatchEvent(new Event("input"));
                            }
                        });
                    } else {
                        document.querySelectorAll('.excel-input-sheet[data-col="'+col+'"]').forEach(function(el) {
                            if (el !== firstRowInput) {
                                el.value = val;
                                el.dispatchEvent(new Event("input"));
                            }
                        });
                    }
                });
            });
        }

        setupExcelDragFillToAllRows();
        setupFirstRowAutoFill();

        // Setup goto page select
        var gotoSelect = document.getElementById('goto-page-select');
        if (gotoSelect) {
            gotoSelect.addEventListener('change', function() {
                var val = parseInt(this.value);
                if (!isNaN(val) && val >= 1 && val <= 4) {
                    var url = new URL(window.location);
                    url.searchParams.set('goto', val);
                    window.location = url.toString();
                }
            });
        }
    });
    """

    js_functions = js_formula_eval
    if q == 4:
        js_functions += """
        function excelSortVolume() {
            var url = new URL(window.location);
            url.searchParams.set('sort','volume');
            url.searchParams.delete('top3');
            window.location = url.toString();
        }
        function excelHighlightTop3() {
            var url = new URL(window.location);
            url.searchParams.set('top3','true');
            url.searchParams.delete('sort');
            window.location = url.toString();
        }
        function excelResetView() {
            var url = new URL(window.location);
            url.searchParams.delete('top3');
            url.searchParams.delete('sort');
            window.location = url.pathname + (url.searchParams.toString() ? '?' + url.searchParams.toString() : '');
        }
        """

    column_headers = list(header)
    excel_col_headers = [excel_col(i) for i in range(len(header))]
    if q == 2:
        column_headers.append("Day Range")
        excel_col_headers.append(excel_col(len(header)))
    if q == 3:
        column_headers.append("Volume Check")
        excel_col_headers.append(excel_col(len(header)))
    if q == 4:
        column_headers.append("Signal")
        excel_col_headers.append(excel_col(len(header)))

    # Navigation bar for previous, next, and go to any page
    next_prev_nav = ""
    if q > 1:
        next_prev_nav += f"<a href='/exam?q={q-1}' style='color:#217346;margin-right:22px;font-size:11pt;text-decoration:none;border-radius:4px;padding:3px 12px;background:#e2f6e9;'><b>&larr; Previous</b></a>"
    if q < 4:
        next_prev_nav += f"<a href='/exam?q={q+1}' style='color:#217346;margin-left:22px;font-size:11pt;text-decoration:none;border-radius:4px;padding:3px 12px;background:#e2f6e9;'><b>Next &rarr;</b></a>"
    goto_options = "".join([f'<option value="{i+1}"{" selected" if (i+1)==q else ""}>Page {i+1}: {pages[i]["name"]}</option>' for i in range(len(pages))])
    goto_select_html = f"""
    <select id="goto-page-select" class="goto-page-select" title="Go to any page">
        {goto_options}
    </select>
    """

    if q < 3:
        legend_html = "<b>Legend:</b> <span class='excel-green-correct' style='font-weight:normal;'>&#10004;: Correct</span> &nbsp; <span class='excel-warning-calc'>&#9888;: Calculation off</span> &nbsp; <span class='excel-err-msg'>#ERROR</span>"
    elif q == 3:
        legend_html = "<b>Legend:</b> <span style='background:%s;padding:1px 10px;'>Green row: &vert;High Volume Check (IF Formula) &vert; </span>" % green_highlight
    elif q == 4:
        legend_html = (
            "<b>Legend:</b> <span style='background:%s;padding:0 7px 0 7px;border-radius:3px;'>Green row: Top 3 by Volume</span><br>"
            "<b>Excel Tip:</b> Try both methods for Top 3 rows: <ul style='margin:2px 0 0 18px;'><li><b>Sort Table</b></li><li><b>Conditional Formatting &rarr; Top 3</b></li></ul>"
            % green_highlight
        )
    else:
        legend_html = (
            "<b>Legend:</b> <span style='background:#fff5dc;padding:0 7px 0 7px;border-radius:3px;'>Signal: <b>BUY, SELL, NEUTRAL</b></span> "
            "<span class='excel-green-correct' style='font-weight:normal;'>&#10004;: Correct</span> "
            "<span class='excel-warning-calc'>&#9888;: You've chosen one of the right options, but logic result is not actual for the row.</span> "
            "<span class='excel-err-msg'>#ERROR</span>"
        )

    sr_html = """<div style="position:absolute;left:-99999px;top:auto;width:1px;height:1px;overflow:hidden;">
        Table navigation: use Tab to move through fields. All controls are keyboard accessible.
    </div>"""

    help_btn_html = """
    <a href="mailto:support@example.com?subject=Excel%20Stock%20Practice%20Exam%20Support" title="Contact Support"
       style="position:fixed;bottom:22px;right:27px;background:#217346;color:#fff;font-weight:600;
       box-shadow:0 3px 14px #22953029;padding:12px 18px;border-radius:18px;font-size:15px;
       text-decoration:none;z-index:999;font-family:Calibri,Arial;"><i class="fas fa-question-circle"></i> Help/Feedback</a>
    """

    # Serve the normal exam page (only if exam not complete)
    response = HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Excel Stock Practice Exam</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/css/all.min.css" rel="stylesheet">
    {excel_css}
    <script>{js_functions}</script>
    </head>
    <body>
    {sr_html}
    {timer_html}
    <div class="excel-sheet-wrapper" style="width:fit-content;margin:48px auto 20px auto;">
        <div class="excel-nav-bar" role="navigation">
            <div class="excel-user-bar" style="flex:1 1 auto;">
                <span><b>User:</b> Guest</span>
            </div>
            <div>
                {nav_html}
                {next_prev_nav}
                {goto_select_html}
            </div>
        </div>
        <div style="font-size:15px;font-weight:600;color:#286b21;padding:13px 0 7px 4px;font-family:Calibri,Arial;">
            Excel-stock: {page['name']} <span style="color:#5e5e5e;font-size:12.5px;font-weight:normal;margin-left:7px;">({q}/4)</span>
        </div>
        <div style="color:#555;font-size:12.2px;margin-bottom:18px;font-family:'Calibri',Arial;">{page['desc']}</div>
        
        <table class="excel-table-x" aria-label="Excel Stock Table">
            {'<tr style="height:19px;">' + ''.join(f"<th class='excel-col-letters'>{colh}</th>" for colh in excel_col_headers) + "<th class='excel-col-letters'></th></tr>" if q in (1,2,3,4) else ""}
            {'<tr style="height:26px;">' + ''.join(f"<th class='excel-top-header'>{h}</th>" for h in column_headers) + "<th class='excel-top-header'>Result</th></tr>" if q in (1,2,3,4) else ""}
            {table_html}
        </table>
        <div style="font-size:10.7pt;color:#999;margin-top:21px;font-family:Calibri,Arial;">
         <b style="color:#217346;">Excel Tips:</b> &nbsp; Use <b>=</b> formulas, cell refs (e.g. C3), ROUND(), SQRT(), IF(), etc.<br>
         {legend_html}
         {('<div style="color:#ab870a;margin-top:11px;font-size:10.8pt;">Highlight: Values &gt; 40 are highlighted yellow.</div>' if q==2 else "")}
        </div>
    </div>
    {help_btn_html}
    <div style="margin:32px 0 8px 0;text-align:center;color:#b4bac7;font-size:10pt;font-family:Calibri,Arial;">
      &copy; {datetime.now().year} Excel Stock Practice Exam &bull; Design by <span style="color:#107c41;">Analytics Team</span>
      <br>
      <span style="font-size:9pt;color:#a8acb2;">All exam data is confidential. For help, contact <a href="mailto:support@example.com">support@example.com</a></span>
    </div>
    </body>
    </html>
    """)
    # When user is interacting with exam, make sure exam_done is NOT set (for exam retakes/tests)
    response.set_cookie("exam_done", "0", path="/", samesite="lax")
    return response


#app = FastAPI()

# ----------- DAX and Excel Related Page -----------------

DAX_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DAX & Excel Formula - Trading Dataset</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f3f4f6; margin: 0; }
        .container { margin: 40px auto; max-width: 900px; background: #fff; border-radius: 10px; padding: 35px 40px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
        h1 { color: #2563eb; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 25px; }
        th, td { border: 1px solid #d1d5db; padding: 8px 10px; text-align: center; }
        th { background: #e5e7eb; }
        textarea, input[type="text"], button {
            width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #ccc;
            margin-top: 8px; margin-bottom: 15px; box-sizing: border-box;
        }
        button { background: #2563eb; color: white; cursor: pointer; font-weight: bold; border: none; }
        button:hover { background: #1d4ed8; }
        .feedback { font-size: 13px; font-weight: bold; min-height: 22px; margin-bottom: 8px; }
        .section-header { margin-bottom: 10px; color: #111827; }
        #resultBoxDax { margin-top: 15px; }
        .top-nav {
            margin-bottom: 30px;
        }
        .top-nav-link {
            display: inline-block;
            background: #059669;
            color: #fff;
            padding: 7px 20px;
            border-radius: 8px;
            margin-right: 12px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1rem;
        }
        .top-nav-link.dax { background: #2563eb; }
        .top-nav-link:hover { opacity: 0.94; }
        .formula-block {
            font-size: 13px;
            background: #f1f5f9;
            border-left: 4px solid #2563eb;
            padding: 8px 15px;
            margin: 8px 0 18px 0;
            border-radius: 7px;
            color: #23272f;
            display:none;
        }
        .formula-label {
            color: #0f6848;
            font-weight: bold;
        }
        .formula-format {
            font-family: "Consolas", "Menlo", "Monaco", monospace;
            color: #0c2e6b;
            background: #e4ecfd;
            border-radius: 4px;
            margin-left: 7px;
            padding: 1px 5px;
        }
        #timer { 
            font-size: 20px;
            font-weight: bold;
            margin: 18px 0 18px 0;
            color: #e53935;
            display: block;
            text-align: right;
        }
        .disabled {
            pointer-events: none;
            opacity: 0.5;
        }
    </style>
</head>
<body>
<div class="container" id="exam-container">
    <div id="timer" aria-label="Timer">Time Left: 30:00</div>
    <div class="top-nav">
        <a href="/login2" class="top-nav-link">🏠 Dashboard</a>
        <a href="/python" class="top-nav-link">🐍 Python Assessment</a>
        <a href="/charts" class="top-nav-link">📊 Chart Section</a>
        <a href="/exam" class="top-nav-link python">📝 Excel Exam</a>
    </div>
    <h1>DAX &amp; Excel Formula - Trading Dataset</h1>
    <div>
        <h2 class="section-header">Trading Dataset</h2>
        <table>
            <thead>
            <tr>
                <th>Date</th>
                <th>Symbol</th>
                <th>Sector</th>
                <th>Buy Price</th>
                <th>Sell Price</th>
                <th>Quantity</th>
                <th>P/L</th>
                <th>Trade Type</th>
            </tr>
            </thead>
            <tbody>
            <tr><td>2026-01-10</td><td>RELIANCE</td><td>Oil & Gas</td><td>2450</td><td>2510</td><td>100</td><td>6000</td><td>Intraday</td></tr>
            <tr><td>2026-01-11</td><td>TCS</td><td>IT</td><td>3900</td><td>3850</td><td>50</td><td>-2500</td><td>Swing</td></tr>
            <tr><td>2026-01-12</td><td>INFY</td><td>IT</td><td>1600</td><td>1660</td><td>80</td><td>4800</td><td>Intraday</td></tr>
            <tr><td>2026-01-13</td><td>HDFCBANK</td><td>Banking</td><td>1720</td><td>1700</td><td>60</td><td>-1200</td><td>Positional</td></tr>
            <tr><td>2026-01-14</td><td>ICICIBANK</td><td>Banking</td><td>1180</td><td>1220</td><td>75</td><td>3000</td><td>Intraday</td></tr>
            <tr><td>2026-01-15</td><td>SBIN</td><td>Banking</td><td>810</td><td>845</td><td>150</td><td>5250</td><td>Swing</td></tr>
            </tbody>
        </table>
    </div>
    <div style="margin-top:25px;">
        <h2 class="section-header">DAX & Excel Formula Tester</h2>
        <textarea id="daxFormula" rows="6" placeholder="Enter DAX or Excel formula"></textarea>
        <button onclick="testDaxFormula()" id="formulaBtn">Test Formula</button>
        <div id="daxResult" class="feedback"></div>
        <div style="margin-top:13px;">
            <!-- Formula blocks are hidden as per instructions -->
            <div class="formula-block" style="display:none;">
                <span class="formula-label">Q4: Total Profit/Loss</span><br>
                <span class="formula-label">Excel:</span> <span class="formula-format"></span><br>
                <span class="formula-label">DAX:</span> <span class="formula-format"></span>
            </div>
            <div class="formula-block" style="display:none;">
                <span class="formula-label">Q5: Average Buy Price</span><br>
                <span class="formula-label">Excel:</span> <span class="formula-format"></span><br>
                <span class="formula-label">DAX:</span> <span class="formula-format"></span>
            </div>
            <div class="formula-block" style="display:none;">
                <span class="formula-label">Q6: Banking Sector Total P/L</span><br>
                <span class="formula-label">Excel:</span> <span class="formula-format"></span><br>
                <span class="formula-label">DAX:</span> <span class="formula-format"></span>
            </div>
            <div class="formula-block" style="display:none;">
                <span class="formula-label">Q8: Trade Type with Maximum Trades</span><br>
                <span class="formula-label">Excel:</span> <span class="formula-format"></span><br>
                <span class="formula-label">DAX:</span> <span class="formula-format"></span>
            </div>
            <div class="formula-block" style="display:none;">
                <span class="formula-label">Q10: Total Intraday Trades</span><br>
                <span class="formula-label">Excel:</span> <span class="formula-format"></span><br>
                <span class="formula-label">DAX:</span> <span class="formula-format"></span>
            </div>
        </div>
    </div>
    <div style="margin-top:32px;">
        <h2 class="section-header">Candidate DAX Tasks</h2>
        <label>Q4: Total Profit/Loss Formula</label>
        <input type="text" id="q4">
        <div id="q4_feedback" class="feedback"></div>
        <label>Q5: Average Buy Price</label>
        <input type="text" id="q5">
        <div id="q5_feedback" class="feedback"></div>
        <label>Q6: Banking Sector Total P/L</label>
        <input type="text" id="q6">
        <div id="q6_feedback" class="feedback"></div>
        <label>Q8: Trade Type with Maximum Trades</label>
        <input type="text" id="q8">
        <div id="q8_feedback" class="feedback"></div>
        <label>Q10: Total Intraday Trades</label>
        <input type="text" id="q10">
        <div id="q10_feedback" class="feedback"></div>
        <button onclick="handleSubmitExam()" id="submitBtn">Submit DAX Answers</button>
        <div id="resultBoxDax"></div>
    </div>
</div>
<script>
// ------ RETAKE PREVENTION ------
const EXAM_FLAG_KEY = 'dax_exam_done';
if (localStorage.getItem(EXAM_FLAG_KEY) === "1") {
    document.body.innerHTML = '<div class="container"><div style="font-size:24px;color:red;text-align:center; margin-top:40px;"><b>You have already completed this exam.<br><a href="/login2" style="color:#2563eb;text-decoration:underline;">Go back to Dashboard</a></b></div></div>';
    throw new Error("Exam already attempted");
}

// ----------- TIMER SECTION -----------
let totalSeconds = 30 * 60; // 30 minutes in seconds
let timerInterval = null;
const timerDisplay = document.getElementById('timer');

function updateTimer() {
    const mins = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
    const secs = (totalSeconds % 60).toString().padStart(2, '0');
    timerDisplay.textContent = `Time Left: ${mins}:${secs}`;
    if (totalSeconds <= 0) {
        clearInterval(timerInterval);
        timerDisplay.textContent = "Time Left: 00:00";
        localStorage.setItem(EXAM_FLAG_KEY, '1');
        disableExamInputs();
        // Redirect after slight delay so user can see time out (optional)
        setTimeout(() => { window.location.href = '/login2'; }, 800);
    }
}

function countdown() {
    totalSeconds--;
    updateTimer();
    if (totalSeconds <= 0) {
        clearInterval(timerInterval);
    }
}
updateTimer();
timerInterval = setInterval(countdown, 1000);

function disableExamInputs() {
    // Disable all input elements in exam
    document.querySelectorAll('#exam-container input, #exam-container textarea, #exam-container button').forEach(el => {
        el.classList.add('disabled');
        el.disabled = true;
    });
}

// -- Handler for manual submit or expiry (shared logic) --
function handleSubmitExam() {
    localStorage.setItem(EXAM_FLAG_KEY, '1');
    disableExamInputs();
    window.location.href = '/login2';
}

// ------- DAX Functionality - Feedback --------
function normalizeFormula(s) {
    return String(s).trim().replace(/\s+/g, '').replace(/'/g, '"').toUpperCase();
}
function testDaxFormula() {
    const formula = normalizeFormula(document.getElementById('daxFormula').value);
    const resultDiv = document.getElementById('daxResult');
    if (formula === 'SUM(TRADES[P/L])' || formula === '=SUM(G2:G7)') {
        resultDiv.innerHTML = '<span style="color:green;">✔ Correct Formula - Output: 15350</span>';
    } else if (formula === 'AVERAGE(TRADES[BUYPRICE])' || formula === 'AVERAGE(TRADES[BUY PRICE])' || formula === '=AVERAGE(D2:D7)') {
        resultDiv.innerHTML = '<span style="color:green;">✔ Correct Formula - Output: 1943.33</span>';
    } else if (formula === 'SUMIFS(G2:G7,C2:C7,"BANKING")' || formula === 'CALCULATE(SUM(TRADES[P/L]),TRADES[SECTOR]="BANKING")') {
        resultDiv.innerHTML = '<span style="color:green;">✔ Correct Banking Formula - Output: 7050</span>';
    } else if (formula === 'INDEX(H2:H7,MODE.MULT(MATCH(H2:H7,H2:H7,0)))' || formula === 'TOPN(1,SUMMARIZE(TRADES,TRADES[TRADETYPE],"COUNTROWS",COUNTROWS(TRADES)),[COUNTROWS],DESC)') {
        resultDiv.innerHTML = '<span style="color:green;">✔ Correct Maximum Trades Formula - Output: INTRADAY</span>';
    } else if (formula === '=COUNTIF(H2:H7,"INTRADAY")' || formula === 'CALCULATE(COUNTROWS(TRADES),TRADES[TRADETYPE]="INTRADAY")' || formula.includes('INTRADAY')) {
        resultDiv.innerHTML = '<span style="color:green;">✔ Correct Intraday Formula - Output: 3</span>';
    } else {
        resultDiv.innerHTML = '<span style="color:red;">✘ Formula Not Recognized</span>';
    }
}
function checkAnswersDax() {
    const answers = {
        q4: ['15350', 'SUM(TRADES[P/L])', '=SUM(G2:G7)'],
        q5: ['1943.33', 'AVERAGE(TRADES[BUY PRICE])', 'AVERAGE(TRADES[BUYPRICE])', '=AVERAGE(D2:D7)'],
        q6: ['7050', '=SUMIFS(G2:G7,C2:C7,"BANKING")', 'CALCULATE(SUM(TRADES[P/L]),TRADES[SECTOR]="BANKING")'],
        q8: ['INTRADAY', 'INDEX(H2:H7,MODE.MULT(MATCH(H2:H7,H2:H7,0)))', 'TOPN(1,SUMMARIZE(TRADES,TRADES[TRADETYPE],"COUNTROWS",COUNTROWS(TRADES)),[COUNTROWS],DESC)'],
        q10: ['3', '=COUNTIF(H2:H7,"INTRADAY")', 'CALCULATE(COUNTROWS(TRADES),TRADES[TRADETYPE]="INTRADAY")']
    };
    const expected = {
        q4: '15350',
        q5: '1943.33',
        q6: '7050',
        q8: 'INTRADAY',
        q10: '3'
    };
    let score = 0;
    for (const key in answers) {
        const input = document.getElementById(key).value;
        const normalized = normalizeFormula(input);
        const isCorrect = answers[key].some(ans => normalizeFormula(ans) === normalized);
        const feedback = document.getElementById(key + '_feedback');
        if (isCorrect) {
            feedback.innerHTML = `<span style="color:green;">✔ Correct | Expected: ${expected[key]}</span>`;
            score++;
        } else {
            feedback.innerHTML = `<span style="color:red;">✘ Wrong | Expected: ${expected[key]}</span>`;
        }
    }
    document.getElementById('resultBoxDax').innerHTML = `<h3>Total DAX Score: ${score} / 5</h3>`;
}
['q4','q5','q6','q8','q10'].forEach(id => {
    document.getElementById(id).addEventListener('blur', checkAnswersDax);
});
</script>
</body>
</html>
"""


# ---------- Python Assessment Endpoint/HTML -------------

PYTHON_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Python Assessment - Trading MCQs & Theory</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f3f4f6; margin: 0; }
        .container { margin: 40px auto; max-width: 900px; background: #fff; border-radius: 10px; padding: 35px 40px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); }
        h1 { color: #059669; }
        select, button { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #ccc; margin-bottom: 10px; font-size: 1rem;}
        button { background: #059669; color: white; border: none; font-weight: bold; }
        button:hover { background: #047857; }
        .feedback { font-size: 13px; font-weight: bold; min-height: 22px; margin-bottom: 8px; }
        .section-header { margin-bottom: 12px; color: #2563eb; }
        #mcqResult { margin-top: 20px; }
        ol { margin-top: 15px; }
        pre, code { background: #e5e7eb; color: #0a2239; border-radius: 4px; padding: 2px 6px;}
        .top-nav { margin-bottom: 30px; }
        .top-nav-link {
            display: inline-block;
            background: #2563eb;
            color: #fff;
            padding: 7px 20px;
            border-radius: 8px;
            margin-right: 12px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1rem;
        }
        .top-nav-link.python { background: #059669; }
        .top-nav-link:hover { opacity: 0.94; }
        #timerBox { 
            text-align: right;
            color: #e11d48; 
            font-size: 1.22rem; 
            font-weight: bold;
            margin-bottom: 12px;
            letter-spacing: 1px;
        }
        #submitAllButton[disabled] {
            background: #bbb!important;
            cursor: not-allowed;
        }
        #examEndedMsg {
            color: #991b1b;
            font-weight: bold;
            text-align: center;
            font-size: 1.12rem;
            margin-top: 35px;
        }
    </style>
</head>
<body>
<div class="container" id="mainExamContent" style="display:none;">
    <div class="top-nav">
        <a href="/login2" class="top-nav-link">🏠 Dashboard</a>
        <a href="/dax" class="top-nav-link">📈 DAX Assessment</a>
        <a href="/charts" class="top-nav-link">📊 Chart Section</a>
        <a href="/exam" class="top-nav-link python">📝 Excel Exam</a>
    </div>
    <div id="timerBox">
        Time Left: <span id="timerDisplay">30:00</span>
    </div>
    <h1>Python Assessment - Trading MCQs &amp; Theoretical</h1>
    <form id="pythonAssessmentForm" onsubmit="event.preventDefault(); submitAllPythonAssessment();">
    <div>
        <h2 class="section-header">Python Trading MCQ Test</h2>
        <div>
            <label>1. What is the output of <code>sum([6000, -2500, 4800])</code>?</label>
            <select id="mcq1">
                <option value="">Select Answer</option>
                <option>A. 8300</option>
                <option>B. 8500</option>
                <option>C. 9300</option>
                <option>D. 10300</option>
            </select>
            <div id="mcq1_feedback" class="feedback"></div>
            <label>2. Which Python data type is best for storing trade details?</label>
            <select id="mcq2">
                <option value="">Select Answer</option>
                <option>A. List</option>
                <option>B. Tuple</option>
                <option>C. Dictionary</option>
                <option>D. String</option>
            </select>
            <div id="mcq2_feedback" class="feedback"></div>
            <label>3. Which function is commonly used to calculate an average in Python?</label>
            <select id="mcq3">
                <option value="">Select Answer</option>
                <option>A. total()</option>
                <option>B. avg()</option>
                <option>C. mean()</option>
                <option>D. sum()</option>
            </select>
            <div id="mcq3_feedback" class="feedback"></div>
            <label>4. What will <code>len(dataset)</code> return?</label>
            <select id="mcq4">
                <option value="">Select Answer</option>
                <option>A. 5</option>
                <option>B. 6</option>
                <option>C. 7</option>
                <option>D. 8</option>
            </select>
            <div id="mcq4_feedback" class="feedback"></div>
            <label>5. Which operator compares equality in Python?</label>
            <select id="mcq5">
                <option value="">Select Answer</option>
                <option>A. =</option>
                <option>B. ==</option>
                <option>C. ===</option>
                <option>D. !=</option>
            </select>
            <div id="mcq5_feedback" class="feedback"></div>
            <label>6. Which keyword is used to loop through trades?</label>
            <select id="mcq6">
                <option value="">Select Answer</option>
                <option>A. repeat</option>
                <option>B. foreach</option>
                <option>C. for</option>
                <option>D. whileloop</option>
            </select>
            <div id="mcq6_feedback" class="feedback"></div>
            <label>7. What is the output of <code>max([6000, -2500, 4800, 3000, 5250])</code>?</label>
            <select id="mcq7">
                <option value="">Select Answer</option>
                <option>A. 3000</option>
                <option>B. 4800</option>
                <option>C. 5250</option>
                <option>D. 6000</option>
            </select>
            <div id="mcq7_feedback" class="feedback"></div>
            <label>8. Which library is used for charts in this project?</label>
            <select id="mcq8">
                <option value="">Select Answer</option>
                <option>A. NumPy</option>
                <option>B. Chart.js</option>
                <option>C. Pandas</option>
                <option>D. Matplotlib</option>
            </select>
            <div id="mcq8_feedback" class="feedback"></div>
            <label>9. What is the correct syntax to access the first trade symbol?</label>
            <select id="mcq9">
                <option value="">Select Answer</option>
                <option>A. dataset.symbol[0]</option>
                <option>B. dataset[0].symbol</option>
                <option>C. dataset[0]['symbol']</option>
                <option>D. symbol[0]</option>
            </select>
            <div id="mcq9_feedback" class="feedback"></div>
            <label>10. Which trade type appears most frequently?</label>
            <select id="mcq10">
                <option value="">Select Answer</option>
                <option>A. Swing</option>
                <option>B. Positional</option>
                <option>C. Intraday</option>
                <option>D. Delivery</option>
            </select>
            <div id="mcq10_feedback" class="feedback"></div>
            <div id="mcqResult"></div>
        </div>
    </div>
    <div>
        <h2 class="section-header" style="margin-top:32px;">Basic Python Questions</h2>
        <ol>
            <li>What is the difference between a List and a Tuple in Python?</li>
            <li>How do you create a dictionary in Python?</li>
            <li>What is the output of <code>print(2 ** 3)</code>?</li>
            <li>How do you write a for loop to print numbers from 1 to 5?</li>
            <li>What is the difference between <code>=</code> and <code>==</code> in Python?</li>
            <li>What is the output of <code>len([10, 20, 30])</code>?</li>
            <li>How do you define a function in Python?</li>
            <li>What is the purpose of the <code>import</code> keyword?</li>
            <li>Which data type is returned by <code>input()</code>?</li>
            <li>How do you convert a string like <code>"123"</code> into an integer?</li>
        </ol>
    </div>
    <button id="submitAllButton" style="width:100%;margin-top:20px;font-size:1.14rem;" type="submit">Submit Assessment</button>
    </form>
</div>
<div id="examEndedMsg" style="display:none;">
    Exam finished or already attempted.<br>
    You cannot take this exam again.<br>
    Redirecting to chart section...
</div>
<script>
/* --- Persistent finish flag using localStorage --- */
function isPythonExamFinished() {
    return localStorage.getItem('python_exam_finished') === '1';
}
function markPythonExamFinished() {
    localStorage.setItem('python_exam_finished', '1');
}

function redirectToCharts() {
    window.location.href = "/charts";
}
function showExamEndedAndRedirect() {
    document.getElementById('mainExamContent').style.display = 'none';
    document.getElementById('examEndedMsg').style.display = '';
    setTimeout(redirectToCharts, 2000);
}

/* --- TIMER LOGIC (30 min = 1800 seconds) --- */
let totalSecs = 30 * 60;
let timerInterval = null;
function startTimer() {
    function updateTimerDisplay() {
        let min = Math.floor(totalSecs / 60);
        let sec = totalSecs % 60;
        document.getElementById('timerDisplay').textContent = min.toString().padStart(2, '0') + ':' + sec.toString().padStart(2, '0');
    }
    updateTimerDisplay();
    timerInterval = setInterval(function() {
        totalSecs--;
        updateTimerDisplay();
        if (totalSecs <= 0) {
            clearInterval(timerInterval);
            markPythonExamFinished();
            showExamEndedAndRedirect();
        }
    }, 1000);
}

document.addEventListener('DOMContentLoaded', function() {
    // Deny exam if already submitted before
    if (isPythonExamFinished()) {
        showExamEndedAndRedirect();
        return;
    }
    document.getElementById('mainExamContent').style.display = '';
    startTimer();
});

/* MCQ validation logic */
function checkMcqAnswers() {
    const correctAnswers = {
        mcq1: 'A. 8300',
        mcq2: 'C. Dictionary',
        mcq3: 'C. mean()',
        mcq4: 'B. 6',
        mcq5: 'B. ==',
        mcq6: 'C. for',
        mcq7: 'D. 6000',
        mcq8: 'B. Chart.js',
        mcq9: "C. dataset[0]['symbol']",
        mcq10: 'C. Intraday'
    };
    let mcqScore = 0;
    for (const key in correctAnswers) {
        const selected = document.getElementById(key).value;
        const feedback = document.getElementById(key + '_feedback');
        if (selected === correctAnswers[key]) {
            feedback.innerHTML = `<span style="color:green;">✔ Correct Answer</span>`;
            mcqScore++;
        } else {
            feedback.innerHTML = `<span style="color:red;">✘ Wrong | Correct Answer: ${correctAnswers[key]}</span>`;
        }
    }
    document.getElementById('mcqResult').innerHTML = `<h3>MCQ Score: ${mcqScore} / 10</h3>`;
}

/* MAIN submit for whole assessment */
function submitAllPythonAssessment() {
    if (isPythonExamFinished()) return;
    checkMcqAnswers();
    markPythonExamFinished();
    document.getElementById('submitAllButton').disabled = true;
    showExamEndedAndRedirect();
}

</script>
</body>
</html>
"""


# ---------- Chart Section Endpoint/HTML -------------

CHARTS_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Trading Charts Interactive</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background: #f3f4f6; margin: 0; }
        .container { margin: 40px auto; max-width: 950px; background: #fff; border-radius: 10px; padding: 35px 40px; box-shadow: 0 2px 12px rgba(0,0,0,0.09);}
        h1 { color: #ea580c; }
        .top-nav { margin-bottom: 30px; }
        .top-nav-link {
            display: inline-block;
            background: #2563eb;
            color: #fff;
            padding: 7px 20px;
            border-radius: 8px;
            margin-right: 12px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1rem;
        }
        .top-nav-link.charts { background: #ea580c; }
        .top-nav-link:hover { opacity: 0.94; }
        .section-header { margin-bottom: 12px; color: #059669; }
        .question { margin-bottom: 25px; }
        pre, code { background: #e5e7eb; color: #0a2239; border-radius: 4px; padding: 2px 7px;}
        table { width: 100%; border-collapse: collapse; margin-bottom: 18px;}
        th, td { border: 1px solid #d1d5db; padding: 7px 9px; text-align: center; }
        th { background: #e5e7eb; }
        .controls-row { margin-bottom: 14px;}
        #myChart { background: #fafafa; }
        .timer-section { font-size: 1.23em; color:#f43f5e; background:#fff7ed; padding:10px 22px; margin:18px 0 26px 0; border-radius:7px; display: flex; align-items: center; justify-content: space-between;}
        .submit-btn { background:#16a34a;color:#fff;padding:8px 24px;font-size:1.14em;border-radius:6px;border:none;font-weight:bold;margin-left:14px;}
        .submit-btn[disabled] { opacity: 0.4; cursor:not-allowed;}
        .already-submitted-message {
            color: #fff;
            background: #ef4444;
            padding: 15px 22px;
            border-radius: 7px;
            font-size: 1.18em;
            margin: 22px 0 28px 0;
            text-align: center;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="top-nav">
        <a href="/login2" class="top-nav-link">🏠 Dashboard</a>
        <a href="/dax" class="top-nav-link">📈 DAX Assessment</a>
        <a href="/python" class="top-nav-link">🐍 Python Assessment</a>
        <a href="/exam" class="top-nav-link">📝 Excel Exam</a>
    </div>
    <!-- Timer & Submit Section -->
    <div class="timer-section" id="charts-timer-section">
        <div><b>Time Remaining:</b> <span id="charts-timer">30:00</span></div>
        <button class="submit-btn" id="charts-submit-btn" onclick="submitChartsAssessment()">Submit</button>
    </div>
    <div id="already-submitted-message" class="already-submitted-message" style="display:none;">
      You have already submitted your Charts assessment.
    </div>
    <h1>Trading Charts - Interactive Analysis</h1>
    <div>
        <h2 class="section-header">Trading Dataset</h2>
        <table id="charts-dataset-table">
            <thead>
            <tr>
                <th>Date</th>
                <th>Symbol</th>
                <th>Sector</th>
                <th>Buy Price</th>
                <th>Sell Price</th>
                <th>Quantity</th>
                <th>P/L</th>
                <th>Trade Type</th>
            </tr>
            </thead>
            <tbody>
            <tr><td>2026-01-10</td><td>RELIANCE</td><td>Oil & Gas</td><td>2450</td><td>2510</td><td>100</td><td>6000</td><td>Intraday</td></tr>
            <tr><td>2026-01-11</td><td>TCS</td><td>IT</td><td>3900</td><td>3850</td><td>50</td><td>-2500</td><td>Swing</td></tr>
            <tr><td>2026-01-12</td><td>INFY</td><td>IT</td><td>1600</td><td>1660</td><td>80</td><td>4800</td><td>Intraday</td></tr>
            <tr><td>2026-01-13</td><td>HDFCBANK</td><td>Banking</td><td>1720</td><td>1700</td><td>60</td><td>-1200</td><td>Positional</td></tr>
            <tr><td>2026-01-14</td><td>ICICIBANK</td><td>Banking</td><td>1180</td><td>1220</td><td>75</td><td>3000</td><td>Intraday</td></tr>
            <tr><td>2026-01-15</td><td>SBIN</td><td>Banking</td><td>810</td><td>845</td><td>150</td><td>5250</td><td>Swing</td></tr>
            </tbody>
        </table>
    </div>
    <div>
        <h2 class="section-header">Interactive Chart Controls</h2>
        <div class="controls-row">
            <label for="xAxis">X Axis:</label>
            <select id="xAxis">
                <option value="Symbol">Symbol</option>
                <option value="Sector">Sector</option>
                <option value="Date">Date</option>
                <option value="Buy Price">Buy Price</option>
                <option value="Sell Price">Sell Price</option>
                <option value="Quantity">Quantity</option>
                <option value="P/L">P/L</option>
                <option value="Trade Type">Trade Type</option>
            </select>
            &nbsp;&nbsp;
            <label for="yAxis">Y Axis:</label>
            <select id="yAxis">
                <option value="Buy Price">Buy Price</option>
                <option value="Sell Price">Sell Price</option>
                <option value="Quantity">Quantity</option>
                <option value="P/L">P/L</option>
            </select>
            &nbsp;&nbsp;
            <label for="chartType">Chart Type:</label>
            <select id="chartType">
                <option value="bar">Bar</option>
                <option value="line">Line</option>
                <option value="pie">Pie</option>
                <option value="doughnut">Doughnut</option>
            </select>
            &nbsp;
            <button onclick="renderChart()">Apply</button>
        </div>
        <canvas id="myChart" height="78"></canvas>
    </div>
    <div>
        <h2 class="section-header" style="margin-top:30px;">Your Own Chart Application Tasks</h2>
        <div class="question">
            <b>1. Write your own analysis question (Example: "Which sector had the highest total P/L?"):</b><br>
            <input type="text" id="customChartQuestion" style="width:90%;" placeholder="Enter your chart analysis question here">
        </div>
        <div class="question">
            <b>2. Based on your question, select the appropriate X Axis, Y Axis, and Chart Type above and click 'Apply' to create the chart.</b>
        </div>
        <div class="question">
            <b>3. After viewing the chart, describe your observations and answer your question:</b><br>
            <textarea id="customChartObservation" style="width:95%;" rows="3" placeholder="Write your answer or insights from the chart"></textarea>
        </div>
        <div class="question">
            <b>4. Try creating at least two different charts with different combinations of X Axis, Y Axis and chart types. For each, provide the question and your answer or observation below:</b>
            <div>
                <input type="text" id="chartTask2Question" style="width:75%;" placeholder="Enter your second chart analysis question">
                <textarea id="chartTask2Observation" style="width:75%;margin-top:5px;" rows="2" placeholder="Your answer or observation about this chart"></textarea>
            </div>
            <div>
                <input type="text" id="chartTask3Question" style="width:75%;" placeholder="Enter your third chart analysis question">
                <textarea id="chartTask3Observation" style="width:75%;margin-top:5px;" rows="2" placeholder="Your answer or observation about this chart"></textarea>
            </div>
        </div>
    </div>
</div>
<script>
const dataset = [
    { "Date": "2026-01-10", "Symbol": "RELIANCE", "Sector": "Oil & Gas", "Buy Price": 2450, "Sell Price": 2510, "Quantity": 100,  "P/L": 6000,  "Trade Type": "Intraday"},
    { "Date": "2026-01-11", "Symbol": "TCS",      "Sector": "IT",        "Buy Price": 3900, "Sell Price": 3850, "Quantity": 50,   "P/L": -2500, "Trade Type": "Swing"},
    { "Date": "2026-01-12", "Symbol": "INFY",     "Sector": "IT",        "Buy Price": 1600, "Sell Price": 1660, "Quantity": 80,   "P/L": 4800,  "Trade Type": "Intraday"},
    { "Date": "2026-01-13", "Symbol": "HDFCBANK", "Sector": "Banking",   "Buy Price": 1720, "Sell Price": 1700, "Quantity": 60,   "P/L": -1200, "Trade Type": "Positional"},
    { "Date": "2026-01-14", "Symbol": "ICICIBANK","Sector": "Banking",   "Buy Price": 1180, "Sell Price": 1220, "Quantity": 75,   "P/L": 3000,  "Trade Type": "Intraday"},
    { "Date": "2026-01-15", "Symbol": "SBIN",     "Sector": "Banking",   "Buy Price": 810,  "Sell Price": 845,  "Quantity": 150,  "P/L": 5250,  "Trade Type": "Swing"}
];

let chart;

// Exam submission/finish: block if already completed
function isChartsExamFinished() {
    return localStorage.getItem("chartsExamFinished") === "1";
}
function markChartsExamFinished() {
    localStorage.setItem("chartsExamFinished", "1");
}

function showAlreadySubmittedMessage() {
    document.getElementById('already-submitted-message').style.display = '';
    document.getElementById('charts-timer-section').style.display = 'none';

    // Optionally, also disable all form/question elements so user cannot edit.
    // For simplicity, just disable textareas and inputs (excluding hidden, button)
    var inputs = document.querySelectorAll('input, textarea, select, button');
    inputs.forEach(function(el) {
        if (el.id !== "charts-submit-btn") el.disabled = true;
    });
    document.getElementById('charts-submit-btn').disabled = true;
}

// Wrap page redirect to show a message instead of immediately redirecting.
function submitChartsAssessment() {
    if(isChartsExamFinished()) {
        // Already finished, just show message.
        showAlreadySubmittedMessage();
        return;
    }
    markChartsExamFinished();
    document.getElementById('charts-submit-btn').disabled = true;
    // Optional: show alert
    // alert("Your assessment is submitted!");
    window.location.href = "/login2";
}

// TIMER LOGIC
let timeLeftSec = 30*60; // 30 minutes in seconds
let chartsTimerInterval = null;

function updateChartsTimerDisplay() {
    let mins = Math.floor(timeLeftSec / 60);
    let secs = timeLeftSec % 60;
    document.getElementById('charts-timer').textContent = 
        (mins < 10 ? "0":"") + mins + ":" + (secs < 10 ? "0":"") + secs;
}

function chartsTickTimer() {
    if(isChartsExamFinished()) {
        // In case finished while running, show already submitted message instead of redirecting.
        showAlreadySubmittedMessage();
        return;
    }
    timeLeftSec -= 1;
    if(timeLeftSec < 0) timeLeftSec = 0;
    updateChartsTimerDisplay();
    if(timeLeftSec <= 0) {
        submitChartsAssessment();
        return;
    }
}

function setupChartsTimer() {
    updateChartsTimerDisplay();
    chartsTimerInterval = setInterval(chartsTickTimer, 1000);
}

window.onload = function() {
    // Check if already submitted (do this at any entry!)
    if(isChartsExamFinished()) {
        showAlreadySubmittedMessage();
        // No timer, no chart
        return;
    }
    renderChart();
    setupChartsTimer();
};


function groupBy(arr, key, yKey, agg) {
    // Returns { key1: value1, ... } based on agg function (sum or count)
    const result = {};
    arr.forEach(row => {
        let k = row[key];
        if (agg === "count") {
            result[k] = (result[k] || 0) + 1;
        } else if (agg === "sum") {
            result[k] = (result[k] || 0) + (+row[yKey]);
        }
    });
    return result;
}

function renderChart() {
    const xField = document.getElementById('xAxis').value;
    const yField = document.getElementById('yAxis').value;
    const chartType = document.getElementById('chartType').value;

    let labels = [];
    let data = [];
    if (chartType === "pie" || chartType === "doughnut") {
        // If x is a category and y is numeric: group and sum by x
        if (["Symbol", "Sector", "Trade Type"].includes(xField)) {
            const grouped = groupBy(dataset, xField, yField, "sum");
            labels = Object.keys(grouped);
            data = Object.values(grouped);
        } else {
            // make slices for each row
            labels = dataset.map(row => row[xField]);
            data = dataset.map(row => +row[yField]);
        }
    } else {
        // For bar/line default: row-wise plot
        labels = dataset.map(row => row[xField]);
        data = dataset.map(row => +row[yField]);
    }

    if (chart) {
        chart.destroy();
    }

    const bgColors = [
        '#2563eb','#ea580c','#059669','#444','#f59e42','#fbbf24','#111827'
    ];

    chart = new Chart(document.getElementById('myChart').getContext('2d'), {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: yField + " by " + xField,
                data: data,
                backgroundColor: chartType==="pie" || chartType==="doughnut" 
                                ? bgColors.slice(0, labels.length)
                                : bgColors[0],
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: chartType==="pie" || chartType==="doughnut" }
            },
            scales: chartType==="pie"||chartType==="doughnut"? {} : {
                y: { beginAtZero: true }
            }
        }
    });
}
</script>
</body>
</html>
"""



@app.get("/dax", response_class=HTMLResponse)
async def dax_formula_page():
    """
    DAX & Excel related assessment page
    """
    return DAX_PAGE_HTML

@app.get("/python", response_class=HTMLResponse)
async def python_assessment_page():
    """
    Python assessment page (MCQ + Theoretical)
    """
    return PYTHON_PAGE_HTML

@app.get("/charts", response_class=HTMLResponse)
async def charts_section():
    """
    Chart related questions and interactive charting assessment
    """
    return CHARTS_PAGE_HTML



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

