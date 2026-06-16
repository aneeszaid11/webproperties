import requests
import pandas as pd
import urllib3
from datetime import datetime  # ✅ NEW
 
# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
input_file = "urls.txt"
output_file = "redirect_results.xlsx"
 
headers = {
    "User-Agent": "Mozilla/5.0"
}
 
results = []
 
# ✅ Get today's date
today_date = datetime.now().strftime("%Y-%m-%d")
 
with open(input_file, "r") as f:
    urls = f.read().splitlines()
 
for original_url in urls:
    try:
        url = original_url.strip()
 
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
 
        try:
            response = requests.get(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=10,
                verify=False
            )
        except:
            url = url.replace("https://", "http://")
            response = requests.get(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=10,
                verify=False
            )
 
        # ✅ Build redirect chain
        chain = []
        visited = set()
 
        for resp in response.history:
            step_url = resp.url
            step_code = resp.status_code
 
            if step_url in visited:
                chain.append(f"{step_url} [{step_code}] (LOOP)")
                break
 
            visited.add(step_url)
            chain.append(f"{step_url} [{step_code}]")
 
        # Final destination
        final_url = response.url
        final_code = response.status_code
 
        loop_flag = "YES" if final_url in visited else "NO"
 
        chain.append(f"{final_url} [{final_code}]")
        chain_str = " → ".join(chain)
 
        status = "PASS" if final_code == 200 else "FAIL"
 
        # ✅ NEW: Status Color
        status_color = "Green" if final_code == 200 else "Red"
 
        # ✅ NEW: Review Comment
        review_comment = f"Reviewed on {today_date}: Link is redirected to {final_url}"
 
        results.append({
            "Source URL": original_url,
            "Final URL": final_url,
            "Final Status Code": final_code,
            "Redirect Count": len(response.history),
            "Redirect Chain": chain_str,
            "Loop Detected": loop_flag,
            "Result": status,
            "Status Color": status_color,          # ✅ NEW COLUMN
            "Review Comment": review_comment       # ✅ NEW COLUMN
        })
 
        print(f"{original_url} -> {final_url} [{final_code}]")
 
    except Exception as e:
        # ✅ even for errors, add new columns
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
 
# ✅ Export to Excel
df = pd.DataFrame(results)
df.to_excel(output_file, index=False, engine="openpyxl")
 
print(f"\n✅ Report saved to {output_file}")
