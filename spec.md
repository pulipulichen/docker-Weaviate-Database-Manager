Weaviate 查詢功能規格文件
=================

1\. 簡介
------

本文件旨在定義一個基於 Weaviate 向量資料庫的查詢應用程式。此應用程式將提供一個直觀的網頁介面，允許使用者連接到 Weaviate 實例，選擇資料類別（Class），執行不同類型的查詢（向量相似性、關鍵字、混合式），並自訂顯示的屬性欄位。後端將使用 Python 處理與 Weaviate 的互動，前端則採用 Vue.js 框架和 Semantic UI 進行介面開發。

2\. 系統架構
--------

本應用程式將採用客戶端-伺服器（Client-Server）架構，分為前端（Frontend）和後端（Backend）兩個主要部分。

    +-----------------+       +-----------------+       +-----------------+
    |   前端 (Vue.js)   |       |   後端 (Python)   |       |    Weaviate     |
    | (瀏覽器運行)      | <-----> | (伺服器運行)      | <-----> |   (向量資料庫)    |
    +-----------------+       +-----------------+       +-----------------+
        - 網頁介面                - API 接口                - 資料儲存與檢索
        - 使用者互動              - Weaviate Client
        - 資料呈現                - 查詢邏輯處理
    
    
    
    
    
    
    
    

3\. 前端功能 (Vue.js + Semantic UI)
-------------------------------

前端負責提供使用者介面、處理使用者輸入，並透過 API 與後端進行通訊。

### 3.1 介面設計

*   **整體佈局**：採用簡潔、響應式的設計，確保在不同螢幕尺寸（桌面、平板、手機）上都能良好顯示。
    
*   **元件化**：使用 Vue.js 的組件化特性，將各功能模組（如連線設定、查詢表單、結果顯示）封裝為獨立組件，提高可維護性和可重用性。
    
*   **樣式**：全面使用 **Semantic UI** 框架進行樣式設計，實現快速開發和一致的視覺風格。
    

### 3.2 核心功能模組

#### 3.2.1 Weaviate 連線設定

*   **Weaviate 實例 URL 輸入**：提供一個文字輸入框，讓使用者輸入 Weaviate 實例的 URL (例如：`http://localhost:8080` 或雲端實例地址)。
    
*   **環境變數支援**：前端啟動時，應檢查是否存在名為 `WEAVIATE_URL` 的環境變數。如果存在，則自動將其值填充到 URL 輸入框中，並嘗試自動連線。
    
*   **連線按鈕**：點擊後觸發後端 API 請求，嘗試連接 Weaviate 並載入其 Schema。
    
*   **載入指示器**：在連線過程中顯示載入動畫。
    
*   **錯誤訊息顯示**：連線失敗時，顯示清晰的錯誤訊息。
    

#### 3.2.2 查詢設定表單

*   **Class 選擇下拉選單**：成功連線後，動態載入並顯示 Weaviate 實例中的所有 Class 名稱供使用者選擇。**此外，應用程式應檢查 URL 參數中是否存在 `class` 參數（例如：`?class=MyClass`），如果存在且該 Class 有效，則自動選擇該 Class 並觸發 Class 屬性載入。**
    
*   **屬性欄位選擇**：根據所選 Class 的 Schema，動態生成該 Class 的所有屬性列表，並以核取方塊（checkbox）形式呈現。使用者可以自由勾選或取消勾選，以決定查詢結果中要顯示哪些欄位。
    
    *   **持久化儲存**：當使用者選擇或取消選擇屬性時，應將當前 Class 的選定屬性列表保存到瀏覽器的 `localStorage` 中。
        
    *   **載入時恢復**：當 Class 被選中時，應嘗試從 `localStorage` 載入該 Class 之前保存的屬性選擇狀態。如果沒有保存的狀態，則預設所有屬性為勾選狀態。
        
*   **查詢類型選擇**：
    
    *   **單選按鈕**：提供「向量相似性查詢 (Vector Search)」、「關鍵字查詢 (Keyword Search)」、「混合式查詢 (Hybrid Search)」三種選項。
        
    *   **條件顯示**：當選擇「混合式查詢」時，顯示 Alpha 參數的滑桿。
        
*   **嵌入模型名稱 (Embedding Model Name) 輸入**：
    
    *   提供一個文字輸入框，讓使用者指定用於向量化查詢文字的嵌入模型名稱。
        
    *   此輸入框應在選擇「向量相似性查詢」或「混合式查詢」時顯示。
        
    *   這是選填欄位，如果留空，Weaviate 將使用其預設的向量化配置。
        
*   **查詢文字 / 關鍵字輸入**：多行文字輸入框，用於輸入查詢的文字或關鍵字。
    
*   **混合式查詢 Alpha 參數**：
    
    *   滑桿（Range Input）：允許使用者調整 Alpha 值，範圍從 0.0 到 1.0，步長為 0.1。
        
    *   數值顯示：實時顯示當前 Alpha 值。
        
*   **篩選條件輸入**：多行文字輸入框，供使用者以 JSON 格式輸入 Weaviate 的 `where` 語法篩選條件。提供範例提示。
    
    *   **支援運算子**：`Equal`, `NotEqual`, `LessThan`, `LessThanEqual`, `GreaterThan`, `GreaterThanEqual`, `ContainsAny`, `ContainsAll`, `And`, `Or`。
        
*   **限制數量 (Limit) 輸入**：數字輸入框，用於設定查詢返回結果的最大數量。
    
*   **偏移量 (Offset) 輸入**：數字輸入框，用於設定查詢結果的起始偏移量（用於分頁）。
    
*   **執行查詢按鈕**：點擊後觸發後端 API 請求，執行查詢。
    
*   **載入指示器**：在查詢過程中顯示載入動畫。
    
*   **錯誤訊息顯示**：查詢失敗時，顯示清晰的錯誤訊息。
    

#### 3.2.3 查詢結果顯示

*   **表格呈現**：以響應式表格形式顯示查詢結果。
    
*   **動態表頭**：表頭應包含使用者選擇的屬性欄位，以及 `_additional` 屬性（如 `id`, `distance`, `score`）。
    
*   **資料顯示**：每一行代表一個 Weaviate 物件，顯示其對應屬性的值。對於物件或陣列類型的屬性，應轉換為可讀的字串（例如 JSON 字串）。
    
*   **無結果提示**：當查詢沒有返回任何結果時，顯示「沒有找到符合條件的結果。」訊息。
    

#### 3.2.4 修改單一物件屬性 (Modify Single Object Property)

*   **輸入欄位**：
    
    *   **物件 ID (Object ID)**：文字輸入框，用於輸入要修改的 Weaviate 物件的 UUID。
        
    *   **屬性名稱 (Property Name)**：文字輸入框，用於輸入要修改的屬性名稱。
        
    *   **新值 (New Value)**：文字輸入框或多行文字輸入框，用於輸入屬性的新值。應考慮不同資料類型（字串、數字、布林、JSON 物件/陣列）的輸入。
        
*   **修改按鈕**：點擊後觸發後端 API 請求，執行物件屬性更新。
    
*   **載入指示器**：在修改過程中顯示載入動畫。
    
*   **成功/錯誤訊息顯示**：顯示操作成功或失敗的提示訊息。
    

4\. 後端功能 (Python)
-----------------

後端負責接收前端請求，使用 Weaviate Python Client 庫與 Weaviate 資料庫進行通訊，並將結果返回給前端。

### 4.1 技術棧

*   **語言**：Python
    
*   **Web 框架**：建議使用 **FastAPI** 或 **Flask**，提供輕量級且高效的 API 服務。
    
*   **Weaviate 客戶端**：`weaviate-client` Python 庫。
    

### 4.2 API 定義

後端將提供以下 RESTful API 端點：

#### 4.2.1 `GET /api/schema`

*   **功能**：獲取 Weaviate 實例的 Schema (包含所有 Class 及屬性)。
    
*   **請求參數**：
    
    *   `weaviate_url` (查詢參數, 必填)：Weaviate 實例的 URL。
        
*   **響應**：
    
    *   成功：JSON 格式的 Weaviate Schema 物件。
        
    *   失敗：包含錯誤訊息的 JSON 物件和適當的 HTTP 狀態碼 (例如 400, 500)。
        

#### 4.2.2 `POST /api/query`

*   **功能**：執行 Weaviate 查詢。
    
*   **請求體 (Request Body)**：JSON 格式，包含以下欄位：
    
    *   `weaviate_url` (字串, 必填)：Weaviate 實例的 URL。
        
    *   `className` (字串, 必填)：要查詢的 Class 名稱。
        
    *   `queryText` (字串, 必填)：查詢文字或關鍵字。
        
    *   `queryType` (字串, 必填)：查詢類型 (`"vector"`, `"keyword"`, `"hybrid"`)。
        
    *   `alpha` (浮點數, 選填)：僅當 `queryType` 為 `"hybrid"` 時有效，範圍 0.0-1.0。
        
    *   `embeddingModel` (字串, 選填)：指定用於向量化查詢文字的嵌入模型名稱。後端會根據此參數調整 Weaviate 查詢。
        
    *   `filter` (物件, 選填)：Weaviate `where` 語法的 JSON 物件。
        
    *   `limit` (整數, 選填)：返回結果數量限制，預設 10。
        
    *   `offset` (整數, 選填)：結果偏移量，預設 0。
        
    *   `properties` (字串陣列, 選填)：要返回的屬性名稱列表。
        
*   **響應**：
    
    *   成功：JSON 格式的查詢結果列表，每個元素是一個 Weaviate 物件，包含所選屬性及 `_additional` 資訊。
        
    *   失敗：包含錯誤訊息的 JSON 物件和適當的 HTTP 狀態碼 (例如 400, 500)。
        

#### 4.2.3 `PATCH /api/object`

*   **功能**：修改 Weaviate 中單一物件的指定屬性。
    
*   **請求體 (Request Body)**：JSON 格式，包含以下欄位：
    
    *   `weaviate_url` (字串, 必填)：Weaviate 實例的 URL。
        
    *   `className` (字串, 必填)：物件所屬的 Class 名稱。
        
    *   `id` (字串, 必填)：要修改的物件的 UUID。
        
    *   `propertyName` (字串, 必填)：要修改的屬性名稱。
        
    *   `value` (任意類型, 必填)：屬性的新值。後端應根據 Weaviate Schema 處理值的類型轉換。
        
*   **響應**：
    
    *   成功：JSON 物件，表示操作成功（例如 `{"status": "success"}`），HTTP 狀態碼 200。
        
    *   失敗：包含錯誤訊息的 JSON 物件和適當的 HTTP 狀態碼 (例如 400, 404, 500)。
        

### 4.3 查詢邏輯

後端將根據前端傳遞的參數構建 Weaviate GraphQL 查詢：

*   **Weaviate 客戶端初始化**：根據 `weaviate_url` 初始化 `weaviate-client`。
    
*   **查詢構建**：
    
    *   根據 `queryType` 調用 `withNearText()`, `withBm25()`, 或 `withHybrid()` 方法。
        
    *   如果提供了 `embeddingModel` 參數，後端應嘗試將其應用於 `nearText` 的向量化過程，這可能需要根據 Weaviate 模組的具體配置來實現（例如，透過 `targetVector` 或特定模組參數）。
        
    *   如果提供了 `filter`，則調用 `withWhere()`。
        
    *   設定 `withLimit()` 和 `withOffset()`。
        
    *   設定 `withFields()`，包含使用者選擇的屬性以及 `_additional { id distance score }`。
        
*   **物件更新邏輯**：
    
    *   對於 `PATCH /api/object` 請求，後端將使用 Weaviate 客戶端的 `data.updater()` 方法來更新指定物件的屬性。
        
    *   應構建一個包含單一屬性及其新值的字典，然後傳遞給 `withProperties()` 方法。
        
    *   執行 `do()` 操作。
        
*   **錯誤處理**：捕獲 Weaviate 客戶端可能拋出的異常，並返回友善的錯誤訊息給前端。
    

5\. 部署與容器化
----------

本應用程式將透過 Docker 進行容器化部署，以確保環境一致性和易於管理。整個應用程式將由多個 Docker 服務組成，並透過 `docker-compose` 進行協調。

### 5.1 Dockerfile.backend

此 Dockerfile 用於構建 Python 後端服務的 Docker 映像。

    # 使用官方 Python 基礎映像
    FROM python:3.9-slim-buster
    
    # 設定工作目錄
    WORKDIR /app
    
    # 將 requirements.txt 複製到容器中並安裝依賴
    COPY backend/requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # 將後端應用程式程式碼複製到容器中
    COPY backend/ .
    
    # 暴露後端服務的埠號（假設你的 FastAPI/Flask 運行在 8000 埠）
    EXPOSE 8000
    
    # 定義啟動後端服務的命令
    # 這裡假設你的 FastAPI 應用程式在 app.py 中，並使用 uvicorn 運行
    # 如果是 Flask，你需要調整為 Flask 的啟動命令
    CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
    
    # 範例 requirements.txt 內容:
    # fastapi
    # uvicorn
    # weaviate-client
    # python-dotenv # 如果後端也需要讀取 .env 檔案
    

### 5.2 Dockerfile.frontend

此 Dockerfile 用於構建 Vue.js 前端應用程式的 Docker 映像，並使用 Nginx 提供靜態檔案。

    # 第一階段：構建 Vue.js 應用程式
    FROM node:18-alpine AS build-stage
    
    # 設定工作目錄
    WORKDIR /app/frontend
    
    # 複製 package.json 和 package-lock.json (或 yarn.lock)
    COPY frontend/package*.json ./
    
    # 安裝前端依賴
    RUN npm install
    
    # 複製前端應用程式程式碼
    COPY frontend/ .
    
    # 構建 Vue.js 應用程式
    # 這裡假設你的 build 命令是 'npm run build'，會將靜態檔案輸出到 'dist' 目錄
    RUN npm run build
    
    # 第二階段：使用 Nginx 提供靜態檔案
    FROM nginx:alpine
    
    # 移除 Nginx 預設配置
    RUN rm /etc/nginx/conf.d/default.conf
    
    # 複製自定義的 Nginx 配置檔
    COPY nginx.conf /etc/nginx/conf.d/nginx.conf
    
    # 從構建階段複製靜態檔案到 Nginx 的服務目錄
    COPY --from=build-stage /app/frontend/dist /usr/share/nginx/html
    
    # 暴露 Nginx 服務的埠號
    EXPOSE 80
    
    # 啟動 Nginx 服務
    CMD ["nginx", "-g", "daemon off;"]
    

### 5.3 nginx.conf

此 Nginx 配置檔用於前端服務，負責處理靜態檔案的提供和 API 請求的代理。

    # Nginx 配置檔
    server {
        listen 80;
        server_name localhost;
    
        # 設定根目錄為 Vue.js 應用程式的靜態檔案目錄
        root /usr/share/nginx/html;
        index index.html index.htm;
    
        location / {
            # 如果檔案不存在，則嘗試提供 index.html，這對於 Vue.js 的 history 模式很重要
            try_files $uri $uri/ /index.html;
        }
    
        # 將 /api/ 的請求代理到後端服務
        # 這裡假設後端服務在 docker-compose 中被命名為 'backend'
        location /api/ {
            proxy_pass http://backend:8000; # 注意：這裡的 backend:8000 是 Docker 內部網路名稱和埠號
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    

### 5.4 docker-compose.yml

此檔案用於定義和運行整個多服務 Docker 應用程式，協調 Weaviate、後端和前端服務。

    version: '3.8'
    
    services:
      # Weaviate 服務 (可選，如果你已經有外部 Weaviate 實例，可以移除此服務)
      weaviate:
        image: semitechnologies/weaviate:1.24.2 # 使用你需要的 Weaviate 版本
        ports:
          - "8080:8080" # Weaviate RESTful API
          - "50051:50051" # Weaviate gRPC API
        restart: on-failure
        environment:
          QUERY_DEFAULTS_LIMIT: 25
          AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true' # 允許匿名訪問，生產環境請配置認證
          PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
          DEFAULT_VECTORIZER_MODULE: 'none' # 如果你不使用內建的向量化模組，可以設定為 'none'
          ENABLE_MODULES: '' # 啟用你需要的模組，例如 'text2vec-openai' 等
          # 如果需要啟用特定模組，例如 OpenAI，需提供 API 金鑰
          # OPENAI_APIKEY: 'YOUR_OPENAI_API_KEY'
        volumes:
          - weaviate_data:/var/lib/weaviate # 持久化 Weaviate 資料
    
      # 後端服務
      backend:
        build:
          context: .
          dockerfile: Dockerfile.backend
        ports:
          - "8000:8000" # 將容器的 8000 埠映射到主機的 8000 埠
        volumes:
          - ./backend:/app # 將主機的 backend 目錄映射到容器的 /app，方便開發時修改程式碼
        depends_on:
          - weaviate # 確保後端在 Weaviate 啟動後才啟動 (非硬性依賴，僅啟動順序)
        environment:
          # 後端不需要直接的 WEAVIATE_URL 環境變數，因為前端會透過請求傳遞
          # 但如果後端有其他需要連接 Weaviate 的邏輯，可以設定
          WEAVIATE_URL: http://weaviate:8080 # Docker 內部網路名稱和埠號
    
      # 前端服務
      frontend:
        build:
          context: .
          dockerfile: Dockerfile.frontend
        ports:
          - "80:80" # 將容器的 80 埠映射到主機的 80 埠
        volumes:
          - ./frontend:/app/frontend # 映射前端程式碼，方便開發時修改
          - ./nginx.conf:/etc/nginx/conf.d/nginx.conf # 映射 Nginx 配置
        depends_on:
          - backend # 確保前端在後端啟動後才啟動
        environment:
          # 將 Weaviate URL 傳遞給前端，供前端在啟動時自動連線
          # 注意：這裡的 WEAVIATE_URL 是給前端 Vue.js 應用程式使用的
          # 它的值應該是前端可以直接訪問的 Weaviate URL
          # 如果 Weaviate 服務也在 docker-compose 內，則為 http://localhost:8080
          # 如果是外部 Weaviate，則為其外部可訪問的 URL
          WEAVIATE_URL: http://localhost:8080 # 這裡設置為 localhost:8080，因為 Weaviate 服務被映射到主機的 8080 埠
    
    # 定義 Docker 卷，用於持久化 Weaviate 資料
    volumes:
      weaviate_data:
    

6\. 技術棧總結
---------

*   **前端**：
    
    *   框架：Vue.js (推薦 Vue 3)
        
    *   樣式：**Semantic UI**
        
    *   HTTP 客戶端：Axios 或 Fetch API
        
*   **後端**：
    
    *   語言：Python
        
    *   Web 框架：FastAPI 或 Flask
        
    *   Weaviate 客戶端：`weaviate-client`
        
*   **資料庫**：Weaviate
    

7\. 實作考量
--------

*   **安全性**：
    
    *   **CORS**：後端需要配置 CORS (Cross-Origin Resource Sharing) 以允許前端應用程式的請求。
        
    *   **API 金鑰/認證**：如果 Weaviate 實例需要 API 金鑰或認證，後端應提供安全的方式來處理這些憑證，不應直接暴露給前端。
        
*   **效能**：
    
    *   **後端響應時間**：確保後端 API 響應時間在可接受範圍內，尤其是在處理大量資料或複雜查詢時。
        
    *   **前端渲染效能**：對於大量查詢結果，考慮虛擬滾動（Virtual Scrolling）或其他優化技術，避免瀏覽器卡頓。
        
*   **錯誤處理**：
    
    *   前後端都應實作健壯的錯誤處理機制，捕獲並顯示有意義的錯誤訊息給使用者。
        
    *   後端應記錄詳細的錯誤日誌，便於問題追蹤。
        
*   **可擴展性**：
    
    *   後端應設計為無狀態服務，便於水平擴展。
        
    *   Weaviate 本身支援高可用性和水平擴展。
        

8\. 測試計畫
--------

*   **單元測試**：
    
    *   **前端**：測試 Vue.js 組件的渲染、狀態管理和使用者互動邏輯。
        
    *   **後端**：測試 API 端點的請求處理、Weaviate 查詢構建邏輯、錯誤處理。
        
*   **整合測試**：
    
    *   測試前端與後端 API 的通訊是否正常。
        
    *   測試後端與 Weaviate 資料庫的整合是否無誤。
        
*   **端到端測試 (E2E Test)**：
    
    *   模擬使用者操作流程，從連線到查詢並顯示結果，驗證整個應用程式的功能。
        
*   **效能測試**：
    
    *   在不同資料量級別和併發使用者情況下，測試前後端的響應時間和資源消耗。