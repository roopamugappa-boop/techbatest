
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn


# --- BEGIN COPY OF pbi2.py MAIN CONTENT INTO HERE (lines 1-633) ---

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

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>Trading Assessment Portal</title>
        <style>
        body { font-family: Arial, sans-serif; background: #f3f4f6; }
        .center { max-width: 500px; margin: 120px auto; background: #fff; border-radius: 12px; padding: 40px 30px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.07);}
        h1 { color: #2563eb;}
        .btn { display: inline-block; margin: 12px 12px 0 0; padding: 12px 36px; background: #2563eb; color: #fff; text-decoration: none; font-weight: bold; border-radius: 8px;}
        .btn-python { background: #059669;}
        .btn-charts { background: #ea580c;}
        .btn-excel { background: #b68900;}
        .btn:hover { opacity: 0.94; }
        </style>
    </head>
    <body>
      <div class="center">
        <h1>Welcome to Trading Assessment Portal</h1>
        <p>Select your assessment below:</p>
        <a href="/dax" class="btn">DAX &amp; Excel Assessment</a>
        <a href="/python" class="btn btn-python">Python Assessment</a>
        <a href="/charts" class="btn btn-charts">Chart Section</a>
        <a href="/exam" class="btn btn-excel">Excel Exam</a>
      </div>
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

@app.get("/exam", response_class=HTMLResponse)
def exam(q: int = Query(1), sort: str = Query(None), top3: str = Query(None), goto: int = Query(None)):
    header = DATA[0]
    # Add top navigation buttons for other assessment sections (Dashboard, DAX, Python, Charts)
    nav_html = """
    <div class="top-nav" style="margin-bottom:24px;text-align:center;">
        <a href="/" class="btn" style="background:#2563eb;color:#fff;margin-right:9px;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">🏠 Dashboard</a>
        <a href="/dax" class="btn" style="background:#2563eb;color:#fff;margin-right:9px;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">📈 DAX Assessment</a>
        <a href="/python" class="btn" style="background:#059669;color:#fff;margin-right:9px;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">🐍 Python Assessment</a>
        <a href="/charts" class="btn" style="background:#ea580c;color:#fff;text-decoration:none;padding:8px 22px;border-radius:6px;font-weight:bold;">📊 Chart Section</a>
    </div>
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
            "name": "Daily % Change (Your Formula)",
            "desc": """Enter Excel formula for "Daily % Change" in each highlighted cell below. <br>
            <span style="color:#555;font-weight:500;">Rows where |Daily % Change| &gt; 1% (>|0.01|) using your formula are <b>highlighted green</b>. 
            You can apply your formula to all rows by dragging/copy just like Excel!</span><br>
            <span style="color:#b28c0b;font-weight:600;">You can also drag the formula handle to apply to all rows below like Excel (dbl-click).</span>""",
            "column_title": "Daily % Change",
            "col_idx": 8,
            "placeholder": "Enter formula...",
            "excelCheckFunc": "excelCheck",
            "cell_class": "cell-input"
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

    # Add support for traversing to any page
    if goto is not None and 1 <= goto <= len(pages):
        q = goto  # If 'goto' is specified and valid, override q

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
                    or (q == 3 and col_index == 8)
                    else "background:#ffffff;"
                )
                if col_index == col_input_index and q in (1, 2, 3):
                    # Each input gets its own formula value
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
            // IF Excel logic (simple): =IF(cond, val1, val2)
            v = v.replace(/IF\(([^,]+),([^,]+),([^)]+)\)/gi, function(m, cond, v1, v2) {
                // Try crude JS conversion:
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
            return String(val).replace(/^"(.*)"$/, "$1"); // Remove quoted string results
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
                    if ((qtype === 1 || qtype === 3)) {
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
                    } else if (qtype === 2) {
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
    if q == 5:
        column_headers.append("Signal")
        excel_col_headers.append(excel_col(len(header)))

    # Navigation bar for previous, next, and go to any page
    next_prev_nav = ""
    if q > 1:
        next_prev_nav += f"<a href='/exam?q={q-1}' style='color:#217346;margin-right:22px;font-size:11pt;text-decoration:none;border-radius:4px;padding:3px 12px;background:#e2f6e9;'><b>&larr; Previous</b></a>"
    if q < 4:
        next_prev_nav += f"<a href='/exam?q={q+1}' style='color:#217346;margin-left:22px;font-size:11pt;text-decoration:none;border-radius:4px;padding:3px 12px;background:#e2f6e9;'><b>Next &rarr;</b></a>"
    # Add Go-To page dropdown
    goto_options = "".join([f'<option value="{i+1}"{" selected" if (i+1)==q else ""}>Page {i+1}: {pages[i]["name"]}</option>' for i in range(len(pages))])
    goto_select_html = f"""
    <select id="goto-page-select" class="goto-page-select" title="Go to any page">
        {goto_options}
    </select>
    """

    if q < 3:
        legend_html = "<b>Legend:</b> <span class='excel-green-correct' style='font-weight:normal;'>&#10004;: Correct</span> &nbsp; <span class='excel-warning-calc'>&#9888;: Calculation off</span> &nbsp; <span class='excel-err-msg'>#ERROR</span>"
    elif q == 3:
        legend_html = "<b>Legend:</b> <span style='background:%s;padding:1px 10px;'>Green row: &vert;Daily %% Change (your formula)&vert; &gt; 1%%</span>" % green_highlight
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

    return f"""
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
    """



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
    </style>
</head>
<body>
<div class="container">
    <div class="top-nav">
        <a href="/" class="top-nav-link">🏠 Dashboard</a>
        <a href="/python" class="top-nav-link">🐍 Python Assessment</a>
        <a href="/charts" class="top-nav-link">📊 Chart Section</a>
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
        <button onclick="testDaxFormula()">Test Formula</button>
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
        <button onclick="checkAnswersDax()">Submit DAX Answers</button>
        <div id="resultBoxDax"></div>
    </div>
</div>
<script>
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
    </style>
</head>
<body>
<div class="container">
    <div class="top-nav">
        <a href="/" class="top-nav-link">🏠 Dashboard</a>
        <a href="/dax" class="top-nav-link">📈 DAX Assessment</a>
        <a href="/python" class="top-nav-link">🐍 Python Assessment</a>
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

window.onload = function() {
    renderChart();
};

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
    </style>
</head>
<body>
<div class="container">
    <div class="top-nav">
        <a href="/" class="top-nav-link">🏠 Dashboard</a>
        <a href="/dax" class="top-nav-link">📈 DAX Assessment</a>
        <a href="/charts" class="top-nav-link">📊 Chart Section</a>
    </div>
    <h1>Python Assessment - Trading MCQs &amp; Theoretical</h1>
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
            <button onclick="checkMcqAnswers()">Submit MCQ Test</button>
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
</div>
<script>
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

# Optionally home could be a HTML landing with links, or redirect to /dax
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>Trading Assessment Portal</title>
        <style>
        body { font-family: Arial, sans-serif; background: #f3f4f6; }
        .center { max-width: 500px; margin: 120px auto; background: #fff; border-radius: 12px; padding: 40px 30px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.07);}
        h1 { color: #2563eb;}
        .btn { display: inline-block; margin: 12px 12px 0 0; padding: 12px 36px; background: #2563eb; color: #fff; text-decoration: none; font-weight: bold; border-radius: 8px;}
        .btn-python { background: #059669;}
        .btn-charts { background: #ea580c;}
        .btn:hover { opacity: 0.94; }
        </style>
    </head>
    <body>
      <div class="center">
        <h1>Welcome to Trading Assessment Portal</h1>
        <p>Select your assessment below:</p>
        <a href="/dax" class="btn">DAX &amp; Excel Assessment</a>
        <a href="/python" class="btn btn-python">Python Assessment</a>
        <a href="/charts" class="btn btn-charts">Chart Section</a>
      </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

