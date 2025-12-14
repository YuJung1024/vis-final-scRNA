# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, send_from_directory
import pandas as pd
import os
from analysis.dataloader import load_dataset

# 設定路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_ROOT = os.path.join(BASE_DIR, "GSE161340", "raw")
app = Flask(__name__)
# app = Flask(__name__, static_folder=BASE_DIR, static_url_path="/static")

# 資料集配置
datasets = {
    "natural_old_rep1": {
        "name": "年老小鼠 (自然衰老) - 重複1",
        "group": "自然衰老",
        "condition": "年老",
        "replicate": 1,
        "folder_path": "GSM4905059_sn_OBrain1_mm10_pre_mRNA",
        "gsm_id": "GSM4905059",
        "data_type": "sn"
    },
    "natural_old_rep2": {
        "name": "年老小鼠 (自然衰老) - 重複2",
        "group": "自然衰老",
        "condition": "年老",
        "replicate": 2,
        "folder_path": "GSM4905060_sn_OBrain3_mm10_pre_mRNA",
        "gsm_id": "GSM4905060",
        "data_type": "sn"
    },
    "natural_young_rep1": {
        "name": "年輕小鼠 (自然衰老) - 重複1",
        "group": "自然衰老",
        "condition": "年輕",
        "replicate": 1,
        "folder_path": "GSM4905061_sn_YBrain1_mm10_pre_mRNA",
        "gsm_id": "GSM4905061",
        "data_type": "sn"
    },
    "natural_young_rep2": {
        "name": "年輕小鼠 (自然衰老) - 重複2",
        "group": "自然衰老",
        "condition": "年輕",
        "replicate": 2,
        "folder_path": "GSM4905061_sn_YBrain3_mm10_pre_mRNA",
        "gsm_id": "GSM4905061",
        "data_type": "sn"
    },
    "treatment_old_rep1": {
        "name": "年老小鼠 (治療) - 重複1",
        "group": "清除衰老細胞",
        "condition": "年老",
        "replicate": 1,
        "folder_path": "GSM4905055_sc_OBrain1_mm10",
        "gsm_id": "GSM4905055",
        "data_type": "sc"
    },
    "treatment_old_rep2": {
        "name": "年老小鼠 (治療) - 重複2",
        "group": "清除衰老細胞",
        "condition": "年老",
        "replicate": 2,
        "folder_path": "GSM4905055_sc_OBrain3_mm10",
        "gsm_id": "GSM4905055",
        "data_type": "sc"
    },
    "treatment_young_rep1": {
        "name": "年輕小鼠 (治療) - 重複1",
        "group": "清除衰老細胞",
        "condition": "年輕",
        "replicate": 1,
        "folder_path": "GSM4905057_sc_YBrain1_mm10",
        "gsm_id": "GSM4905057",
        "data_type": "sc"
    },
    "treatment_young_rep2": {
        "name": "年輕小鼠 (治療) - 重複2",
        "group": "清除衰老細胞",
        "condition": "年輕",
        "replicate": 2,
        "folder_path": "GSM4905057_sc_YBrain3_mm10",
        "gsm_id": "GSM4905057",
        "data_type": "sc"
    }
}


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

# 提供 pages 目錄中的 HTML 檔案
@app.route('/pages/<path:filename>')
def serve_pages(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'pages'), filename)

# 提供 downsampling 目錄中的檔案
@app.route('/downsampling/<path:filename>')
def serve_downsampling(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'downsampling'), filename)

# 提供 gene expression 資料
@app.route('/data2/<path:filename>')
def serve_data2(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'GSE161340', 'processed', 'gene_expression'), filename)

# API - 獲取資料集列表
@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    return jsonify(datasets)

# API - 載入資料集
@app.route('/api/load_dataset', methods=['POST'])
def api_load_dataset():
    try:
        data = request.json
        dataset_key = data.get('dataset_key')
        
        if dataset_key not in datasets:
            return jsonify({"error": "資料集不存在"}), 404
        
        # 使用你的 load_dataset 函數
        dataset_info = datasets[dataset_key]
        full_path = os.path.join(DATASET_ROOT, dataset_info['folder_path'])
        
        adata = load_dataset(full_path)  # 假設你的函數接受路徑參數
        
        # 返回基本資訊
        result = {
            "status": "success",
            "dataset_key": dataset_key,
            "name": dataset_info['name'],
            "n_cells": int(adata.n_obs),
            "n_genes": int(adata.n_vars)
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - 預留給未來功能
@app.route('/api/analyze', methods=['POST'])
def analyze():
    # 這裡之後會放分析邏輯
    return jsonify({"status": "success", "message": "準備就緒"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)

