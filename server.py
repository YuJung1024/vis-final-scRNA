# #!/usr/bin/env python3
# import os
# import subprocess

# from flask import Flask, request, send_from_directory

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CODES_DIR = os.path.join(BASE_DIR, "codes")
# RSCRIPTS_DIR = os.path.join(CODES_DIR, "rscripts")

# app = Flask(__name__, static_folder=CODES_DIR, static_url_path="/codes")


# # ---------- 靜態檔案 ----------
# # 讓你可以用 http://localhost:8000/codes/analysis.html 之類的方式開網頁
# @app.route("/")
# def root():
#     # 直接跳到 analysis.html
#     return send_from_directory(CODES_DIR, "analysis.html")


# @app.route("/codes/<path:filename>")
# def serve_codes(filename):
#     return send_from_directory(CODES_DIR, filename)


# # ---------- 呼叫 dims_cells.R ----------
# @app.route("/rscripts/dims_cells.r", methods=["POST"])
# def call_dims_cells():
#     """
#     前端 AJAX 會送出一個純文字字串，例如：
#     "2_30_GSE161340.rds_Slc17a7_Gad1"

#     我們把這個 body 原封不動丟到 Rscript 的 stdin，
#     就跟你在終端機打：
#     echo "2_30_GSE161340.rds_Slc17a7_Gad1" | Rscript dims_cells.R
#     一樣。
#     """
#     # 1. 拿到原始 request body（bytes）
#     body = request.get_data()  # 等同於你 echo 那串的內容

#     # 2. 呼叫 Rscript，cwd 設在 rscripts 目錄
#     proc = subprocess.run(
#         ["Rscript", "dims_cells.R"],
#         input=body,
#         cwd=RSCRIPTS_DIR,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )

#     # 3. 如果 R 執行失敗，回傳 500 並印出錯誤方便你 debug
#     if proc.returncode != 0:
#         err = proc.stderr.decode("utf-8", errors="ignore")
#         print("=== R ERROR (dims_cells.R) ===")
#         print(err)
#         print("=== END R ERROR ===")
#         return ("R error:\n" + err, 500, {"Content-Type": "text/plain; charset=utf-8"})

#     # 4. 成功的話，把 R 的輸出原樣丟回前端
#     out = proc.stdout.decode("utf-8", errors="ignore")
#     # dims_cells.R 的設計是輸出一段純文字而不是 JSON
#     return (out, 200, {"Content-Type": "text/plain; charset=utf-8"})

# @app.route("/rscripts/rds_check.r", methods=["POST"])
# def rds_check():
#     """
#     模擬原本的 rds_check.r：
#     - 前端丟一個 rds 檔名（例如 "GSE161340" 或 "GSE161340.rds"）
#     - 回傳 "true" 或 "false"
#     """
#     name = request.get_data(as_text=True).strip()
#     # 跟 R 一樣，如果沒寫 .rds 就自己補上
#     if not name.endswith(".rds"):
#         name = name + ".rds"

#     path = os.path.join(RSCRIPTS_DIR, "rds", name)
#     exists = os.path.exists(path)
#     body = "true" if exists else "false"
#     return (body, 200, {"Content-Type": "text/plain; charset=utf-8"})



# # ---------- 呼叫 density_cluster.py（CPU 版） ----------
# @app.route("/codes/density_cluster.py", methods=["POST"])
# @app.route("/density_cluster.py", methods=["POST"])
# def call_density_cluster():
#     """
#     前端現在用的是：
#         data: {'fd_ld': cluster_str}
#     原本的 density_cluster.py / density.py 也是用 CGI 讀 form 裡的 fd_ld。
#     我們在這裡把 fd_ld 取出來，原封不動丟給 density_cluster.py 的 stdin。
#     """
#     # 1. 先從 form 取 fd_ld，如果沒有再退而求其次用 raw body
#     fd_ld = request.form.get("fd_ld")
#     if fd_ld is None:
#         fd_ld = request.get_data(as_text=True)

#     if fd_ld is None:
#         return ("missing fd_ld", 400, {"Content-Type": "text/plain; charset=utf-8"})

#     # 2. 呼叫 density_cluster.py
#     proc = subprocess.run(
#         ["python3", "density_cluster.py"],
#         input=fd_ld.encode("utf-8"),
#         cwd=CODES_DIR,  # DESC/codes
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
    

#     if proc.returncode != 0:
#         err = proc.stderr.decode("utf-8", errors="ignore")
#         print("=== PY ERROR (density_cluster.py) ===")
#         print(err)
#         print("=== END PY ERROR ===")
#         return ("Python error:\n" + err, 500, {"Content-Type": "text/plain; charset=utf-8"})

#     out = proc.stdout.decode("utf-8", errors="ignore")
#     # density_cluster.py 原本設計是輸出 JSON
#     return (out, 200, {"Content-Type": "application/json; charset=utf-8"})



# if __name__ == "__main__":
#     # host="0.0.0.0" 讓你可以從同一台機器的瀏覽器用 localhost 連進來
#     app.run(host="0.0.0.0", port=8000, debug=True)

#!/usr/bin/env python3
import os
import subprocess
from flask import Flask, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODES_DIR = os.path.join(BASE_DIR, "codes")
RSCRIPTS_DIR = os.path.join(CODES_DIR, "rscripts")

app = Flask(__name__, static_folder=CODES_DIR, static_url_path="/codes")

# ========== 靜態檔案 ==========
@app.route("/")
def root():
    return send_from_directory(CODES_DIR, "analysis.html")

@app.route("/codes/<path:filename>")
def serve_codes(filename):
    return send_from_directory(CODES_DIR, filename)

# ========== dims_cells.R ==========
@app.route("/rscripts/dims_cells.r", methods=["POST"])
def call_dims_cells():
    body = request.get_data()
    
    print(f"[DEBUG] dims_cells.R input: {body.decode('utf-8')}")
    
    proc = subprocess.run(
        ["Rscript", "dims_cells.R"],
        input=body,
        cwd=RSCRIPTS_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="ignore")
        print("=== R ERROR (dims_cells.R) ===")
        print(err)
        print("=== END R ERROR ===")
        return ("R error:\n" + err, 500, {"Content-Type": "text/plain; charset=utf-8"})
    
    out = proc.stdout.decode("utf-8", errors="ignore")
    print(f"[DEBUG] dims_cells.R output: {out[:500]}")
    
    return (out, 200, {"Content-Type": "text/plain; charset=utf-8"})

# ========== rds_check.r ==========
@app.route("/rscripts/rds_check.r", methods=["POST"])
def rds_check():
    name = request.get_data(as_text=True).strip()
    if not name.endswith(".rds"):
        name = name + ".rds"
    
    path = os.path.join(RSCRIPTS_DIR, "rds", name)
    exists = os.path.exists(path)
    body = "true" if exists else "false"
    return (body, 200, {"Content-Type": "text/plain; charset=utf-8"})

# ========== density_cluster.py ==========
# ✅ 重點：支援三種 URL 路徑
@app.route("/codes/density_cluster.py", methods=["POST"])
@app.route("/codes/density_cluster", methods=["POST"])  # ← 加這個
@app.route("/density_cluster.py", methods=["POST"])
@app.route("/density_cluster", methods=["POST"])
def call_density_cluster():
    """
    處理 density clustering 請求
    """
    # 1. 從 form 拿 fd_ld
    fd_ld = request.form.get("fd_ld")
    
    # 2. 如果沒有，試試 raw body
    if not fd_ld:
        fd_ld = request.get_data(as_text=True).strip()
    
    if not fd_ld:
        print("[ERROR] Missing fd_ld parameter")
        return ("missing fd_ld", 400, {"Content-Type": "text/plain; charset=utf-8"})
    
    print(f"[DEBUG] density_cluster input: {fd_ld[:200]}...")
    
    # 3. 呼叫 density_cluster.py
    proc = subprocess.run(
        ["python3", "density_cluster.py"],
        input=fd_ld.encode("utf-8"),
        cwd=CODES_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="ignore")
        print("=== PY ERROR (density_cluster.py) ===")
        print(err)
        print("=== END PY ERROR ===")
        return ("Python error:\n" + err, 500, {"Content-Type": "text/plain; charset=utf-8"})
    
    out = proc.stdout.decode("utf-8", errors="ignore")
    print(f"[DEBUG] density_cluster output: {out[:200]}...")
    
    return (out, 200, {"Content-Type": "application/json; charset=utf-8"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
