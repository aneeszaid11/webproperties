import pandas as pd
import urllib3
import subprocess
import json
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

input_file = "urls.txt"
output_file = "redirect_results.xlsx"

results = []

# Get today's date
today_date = datetime.now().strftime("%Y-%m-%d")

with open(input_file, "r") as f:
    urls = f.read().splitlines()

for original_url in urls:
    try:
        url = original_url.strip()

        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        # PowerShell script using Invoke-WebRequest
        ps_script = f"""
        try {{
            $resp = Invoke-WebRequest -Uri '{url}' -UseBasicParsing -MaximumRedirection 20

            [PSCustomObject]@{{
                FinalUrl = $resp.BaseResponse.ResponseUri.AbsoluteUri
                StatusCode = $resp.StatusCode
            }} | ConvertTo-Json -Compress
        }}
        catch {{
            if ($_.Exception.Response) {{
                [PSCustomObject]@{{
                    FinalUrl = $_.Exception.Response.ResponseUri.AbsoluteUri
                    StatusCode = [int]$_.Exception.Response.StatusCode
                }} | ConvertTo-Json -Compress
            }}
            else {{
                throw
            }}
        }}
        """

        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        data = json.loads(result.stdout)

        final_url = data.get("FinalUrl", "")
        final_code = data.get("StatusCode", "N/A")

        status = "PASS" if str(final_code) == "200" else "FAIL"
        status_color = "Green" if str(final_code) == "200" else "Red"

        chain_str = f"{url} -> {final_url} [{final_code}]"

        review_comment = (
            f"Reviewed on {today_date}: "
            f"Link is redirected to {final_url}"
        )

        results.append({
            "Source URL": original_url,
            "Final URL": final_url,
            "Final Status Code": final_code,
            "Redirect Count": "N/A",
            "Redirect Chain": chain_str,
            "Loop Detected": "UNKNOWN",
            "Result": status,
            "Status Color": status_color,
            "Review Comment": review_comment
        })

        print(f"{original_url} -> {final_url} [{final_code}]")

    except Exception as e:

        results.append({
            "Source URL": original_url,
            "Final URL": "ERROR",
            "Final Status Code": "N/A",
            "Redirect Count": 0,
            "Redirect Chain": "ERROR",
            "Loop Detected": "UNKNOWN",
            "Result": "FAIL",
            "Status Color": "Red",
            "Review Comment": f"Reviewed on {today_date}: Link check failed"
        })

        print(f"{original_url} -> ERROR: {e}")

# Export to Excel
df = pd.DataFrame(results)
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"\nReport saved to {output_file}")
