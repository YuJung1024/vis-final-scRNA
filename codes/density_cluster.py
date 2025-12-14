
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import sys
# import json
# import numpy as np
# import traceback


# def parse_fd_ld(cluster_str):
#     """
#     解析 cluster_str，容忍前面有非數字 token。
    
#     格式：
#         fd_ld=2_30_GSE161340.rds_30500_29_1_0.1_12833 0 2 4 12 15...
        
#     解析為：
#         fd=2, ld=30, rds_name=GSE161340.rds, nrow=30500, n_dims=29, 
#         n_markers=1, density_th=0.1
#         然後是 cell_ids
#     """
    
#     # 先處理可能的 "fd_ld=..." 這種情況
#     if "fd_ld=" in cluster_str:
#         cluster_str = cluster_str.split("fd_ld=", 1)[1]
    
#     # 分成兩部分：底線分隔的 header 和空格分隔的 cell_ids
#     parts = cluster_str.strip().split()
    
#     # 第一個 part 是用底線分隔的 header
#     header = parts[0].split("_")
    
#     # 解析 header
#     if len(header) < 7:
#         raise ValueError(f"Header too short: {header}")
    
#     fd = int(header[0])
#     ld = int(header[1])
#     rds_name = header[2]
#     nrow = int(header[3])
#     n_dims = int(header[4])
#     n_markers = int(header[5])
#     density_th = float(header[6])  # 注意這裡是 float
    
#     # 剩下的 parts 是 cell_ids（空格分隔的整數）
#     cell_ids_parts = parts[1:]  # 跳過 header
    
#     # 解析 cell_ids
#     max_num_clusters = n_markers
#     ids = np.full(n_dims * max_num_clusters * nrow, -1, dtype=np.int32)
#     num_clusters_arr = np.zeros(n_dims, dtype=np.int32)
#     num_points_arr = np.zeros(n_dims * max_num_clusters, dtype=np.int32)
    
#     # 對每個 marker 解析其 cell_ids
#     pos = 0
#     for marker_idx in range(n_markers):
#         if pos >= len(cell_ids_parts):
#             break
            
#         # 讀取這個 marker 有多少個 cells
#         num_cells = int(cell_ids_parts[pos])
#         pos += 1
        
#         # 這個 marker 在所有維度中只有一個 cluster
#         for dim_idx in range(n_dims):
#             num_clusters_arr[dim_idx] = n_markers
#             num_points_arr[dim_idx * max_num_clusters + marker_idx] = num_cells
            
#             base = dim_idx * max_num_clusters * nrow + marker_idx * nrow
            
#             # 讀取 cell_ids
#             for k in range(num_cells):
#                 if pos >= len(cell_ids_parts):
#                     raise ValueError(f"Unexpected end while reading cell_ids")
                
#                 cell_id = int(cell_ids_parts[pos])
#                 pos += 1
#                 ids[base + k] = cell_id
    
#     return (
#         fd,
#         ld,
#         rds_name,
#         nrow,
#         n_dims,
#         density_th,
#         max_num_clusters,
#         ids,
#         num_clusters_arr,
#         num_points_arr,
#     )


# def main():
#     # 從 stdin 讀取整個 fd_ld 字串
#     raw = sys.stdin.read()
#     fd_ld_str = raw.strip()
    
#     if not fd_ld_str:
#         json.dump({"error": "empty fd_ld"}, sys.stdout)
#         return
    
#     try:
#         (
#             fd,
#             ld,
#             rds_name,
#             nrow,
#             n_dims,
#             density_th,
#             max_num_clusters,
#             ids,
#             num_clusters_arr,
#             num_points_arr,
#         ) = parse_fd_ld(fd_ld_str)
        
#         # ⭐ 現在策略：**全部保留**
#         # filtered_ids = ids（不做任何過濾）
#         filtered_ids = ids.astype(int).tolist()
        
#         result = {"filtered_ids": filtered_ids}
#         json.dump(result, sys.stdout)
        
#     except Exception as e:
#         # 若還是有錯，把錯訊 + 前 200 chars 的原始字串一併丟回去
#         err_msg = f"{e} | raw='{fd_ld_str[:200]}'"
#         json.dump({"error": err_msg}, sys.stdout)
#         # 完整 traceback 印到 stderr（你在跑 server 的 terminal 會看到）
#         traceback.print_exc(file=sys.stderr)


# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import traceback
import os
import csv
from urllib.parse import unquote_plus

import numpy as np


# ---------- 2D Convex Hull + Area（Monotone Chain） ----------

def _cross(o, a, b):
    """向量叉積 (OA x OB)，用來判斷轉彎方向。"""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    """
    points: list of (x, y)
    回傳 hull 的點序列（逆時鐘），至少 3 個點；如果點數 < 3，直接回傳原 points。
    """
    pts = sorted(set(points))  # 去重 + 依 x,y 排序
    if len(pts) <= 2:
        return pts

    # 下半部
    lower = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # 上半部
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # 最後一個點會跟第一個點重複，因此各去掉最後一個
    return lower[:-1] + upper[:-1]


def polygon_area(poly):
    """
    poly: list of (x, y)，已經是凸多邊形的點序列
    回傳多邊形面積（絕對值）。
    """
    n = len(poly)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) * 0.5


# ---------- fd_ld 解析 + CSV 讀取 ----------

def parse_fd_ld(fd_ld_str: str):
    """
    解析 fd_ld_str

    格式：
        fd_ld_str = "2_30_GSE161340.rds_30500_29_2_0.1_1427 67 185 ..."

    header（底線分隔前 7 個）：
        fd, ld, rds_name, nrow, n_dims, n_markers, density_th

    tail（空白分隔）：
        每個 marker：
            cell_count cell_id1 cell_id2 ... cell_idN
    """
    s = fd_ld_str.strip()
    if not s:
        raise ValueError("empty fd_ld")

    # URL decode
    s = unquote_plus(s)

    # 移除 "fd_ld=" 前綴（如果有）
    if s.startswith("fd_ld="):
        s = s[len("fd_ld="):]

    # 先切出 header 的 7 個 token，其餘當成 tail 字串
    parts = s.split("_", 7)
    if len(parts) < 8:
        raise ValueError(f"fd_ld header too short: '{s[:100]}'")

    header = parts[:7]
    tail_str = parts[7].strip()

    try:
        fd = int(header[0])
        ld = int(header[1])
        rds_name = header[2]
        nrow = int(header[3])
        n_dims = int(header[4])
        n_markers = int(header[5])
        density_th = float(header[6])
    except Exception as e:
        raise ValueError(f"header parse error: {e} | header={header}")

    if not tail_str:
        raise ValueError("no tail (cell ids) in fd_ld")

    # tail：空白分隔的整數
    try:
        int_tokens = [int(x) for x in tail_str.split()]
    except Exception as e:
        raise ValueError(f"tail int parse error: {e} | tail='{tail_str[:200]}'")

    # 解析每個 marker 的 cell_ids
    marker_cells = []
    pos = 0
    for m in range(n_markers):
        if pos >= len(int_tokens):
            raise ValueError(f"int_tokens too short for marker {m}")

        cell_count = int_tokens[pos]
        pos += 1

        if pos + cell_count > len(int_tokens):
            raise ValueError(
                f"marker {m}: expect {cell_count} cell_ids, "
                f"but only {len(int_tokens) - pos} left"
            )

        cell_ids = int_tokens[pos:pos + cell_count]
        pos += cell_count
        marker_cells.append(cell_ids)

    return fd, ld, rds_name, nrow, n_dims, n_markers, density_th, marker_cells


def load_dimensions(rds_name: str, fd: int, ld: int, nrow: int, n_dims: int):
    """
    讀取 data2/<rds_name_without_rds>_<fd>_<ld>/dimensions.csv

    CSV 結構：
        row_col, x_fd, y_fd, x_fd+1, y_fd+1, ...

    回傳：
        x: shape = (n_dims, nrow)
        y: shape = (n_dims, nrow)
        其中 dim_index = 0 對應 fd，dim_index = 1 對應 fd+1，以此類推
    """
    if rds_name.endswith(".rds"):
        rds_base = rds_name[:-4]
    else:
        rds_base = rds_name

    folder = os.path.join("GSE161340", "processed", "gene_expression", f"{rds_base}_{fd}_{ld}")
    dim_path = os.path.join(folder, "dimensions.csv")

    if not os.path.exists(dim_path):
        raise FileNotFoundError(f"dimensions.csv not found at {dim_path}")

    x = np.empty((n_dims, nrow), dtype=np.float32)
    y = np.empty((n_dims, nrow), dtype=np.float32)

    with open(dim_path, "r", newline="", encoding="utf-8") as f:
        rdr = csv.reader(f)
        header = next(rdr, None)  # skip header
        row_idx = 0
        for row in rdr:
            # row: [row_col, x_fd, y_fd, x_fd+1, y_fd+1, ...]
            for d in range(n_dims):
                x_val = float(row[1 + 2 * d])
                y_val = float(row[1 + 2 * d + 1])
                x[d, row_idx] = x_val
                y[d, row_idx] = y_val
            row_idx += 1

    if row_idx != nrow:
        raise ValueError(f"dimensions.csv rows ({row_idx}) != nrow ({nrow})")

    return x, y


# ---------- 主邏輯：convex hull + row-wise normalize ----------

def run_density_cluster(fd_ld_str: str):
    (
        fd,
        ld,
        rds_name,
        nrow,
        n_dims,
        n_markers,
        density_th,
        marker_cells,
    ) = parse_fd_ld(fd_ld_str)

    # 讀取所有維度的座標
    x_all, y_all = load_dimensions(rds_name, fd, ld, nrow, n_dims)

    # filtered_ids & density
    # index = m * (n_dims * nrow) + d * nrow + local_idx
    total_len = n_markers * n_dims * nrow
    filtered_ids = np.full(total_len, -1, dtype=np.int32)
    density = np.zeros(total_len, dtype=np.float32)

    # 先計算每個 marker / dim 的 convex hull 面積
    areas = np.zeros((n_markers, n_dims), dtype=np.float64)

    for m, cell_ids in enumerate(marker_cells):
        if len(cell_ids) == 0:
            continue

        cell_ids_arr = np.array(cell_ids, dtype=np.int64)

        for d in range(n_dims):
            xs = x_all[d, cell_ids_arr]
            ys = y_all[d, cell_ids_arr]
            pts = list(zip(xs.tolist(), ys.tolist()))
            if len(pts) < 3:
                area_md = 0.0
            else:
                hull = convex_hull(pts)
                area_md = polygon_area(hull)
            areas[m, d] = area_md

    # 對每個 marker row 做 normalize（依據數值佔總值的比例）
    # value_md = areas[m, d] / sum_d areas[m, d]
    for m in range(n_markers):
        row = areas[m, :]
        total = row.sum()
        if total <= 0:
            # 整 row 都沒有面積，就全部 0
            norm_row = np.zeros_like(row)
        else:
            norm_row = row / total

        # 把 normalized 值寫入 density array，對同一 marker/dim 的每個 cell 都是同一個值
        cell_ids = marker_cells[m]
        cell_count = len(cell_ids)
        for d in range(n_dims):
            value_md = float(norm_row[d])
            base = m * n_dims * nrow + d * nrow
            # 前 cell_count 個位置對應這個 marker 的 cell
            density[base: base + cell_count] = value_md

    # 再把 filtered_ids 填進去（全部保留）
    for m, cell_ids in enumerate(marker_cells):
        cell_count = len(cell_ids)
        if cell_count == 0:
            continue
        for d in range(n_dims):
            base = m * n_dims * nrow + d * nrow
            for local_idx, cell_id in enumerate(cell_ids):
                if 0 <= cell_id < nrow:
                    filtered_ids[base + local_idx] = cell_id

    return {
        "filtered_ids": filtered_ids.astype(int).tolist(),
        "density": density.astype(float).tolist(),
    }


def main():
    raw = sys.stdin.read()
    fd_ld_str = raw.strip()

    if not fd_ld_str:
        json.dump({"error": "empty fd_ld"}, sys.stdout)
        return

    try:
        result = run_density_cluster(fd_ld_str)
        json.dump(result, sys.stdout)
    except Exception as e:
        err_msg = f"{e} | raw='{fd_ld_str[:200]}'"
        json.dump({"error": err_msg}, sys.stdout)
        traceback.print_exc(file=sys.stderr)


if __name__ == "__main__":
    main()
