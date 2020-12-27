# Leepomelo

## 前言
近年來隨著科技的發展，藉由網路行銷開始越來越盛行，而且也可以減省需多人力成本，再加上由於父親最近要退休回去接阿公家的農田，而阿公家主要販售的農作物是柚子，所以便想建立一個屬於柚心園的官方Linebot，藉此減少父母親在處理客戶問題以及訂單的負擔。

## 構想
主選單包含有商品資訊，訂購，問答以及菜單的選項，進入商品資訊頁之後，裡面分別有1.商品優惠資訊:內含有即時的優惠資訊2.商品介紹:則是介紹商品來源和口感3.健康資訊:內含有對身體的益處以及飲食禁忌，這部分提供了網路連結供消費者參考。而主選單上另外的訂購選項則是放有柚心園的訂購表單，而問答則是供消費這詢問有關柚心園的問題，而菜單內則有商品介紹以及菜單圖示的選項。

## 環境
- ubuntu 16.04
- python 3.7.4

## 技術
- NLP
    - 具有NLP的簡易聊天機器人

## 使用教學
1. install `pipenv`
```shell
pip3 install pipenv
```
2. install 所需套件
```shell
pipenv install --three
// 若遇到pygraphviz安裝失敗，則嘗試下面這行
sudo apt-get install graphviz graphviz-dev
```
3. 從`.env.sample`產生出一個`.env`，並填入以下四個資訊

- Line

    - LINE_CHANNEL_SECRET
    
    - LINE_CHANNEL_ACCESS_TOKEN

4. Conncet to Heroku

- Register Heroku: https://signup.heroku.com

- Create Heroku project from website

- CLI Login
    
    `heroku login`

5. Upload project to Heroku    

- Add local project to Heroku project
    
    `heroku git:remote -a {HEROKU_APP_NAME}(記得把{}拿掉)`

- Upload project
    
    ```
    git add .
    git commit -m "Add code
    git push -f heroku master
    ```
- Set Environment - Line Messaging API Secret Keys  
    
    `heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret`
    
    `heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token`

6. Your Project is now running on Heroku!
    
    url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

7. If fail with `pygraphviz` install errors run commands below can solve the problems
    
    `heroku buildpacks:set heroku/python`
    
    `heroku buildpacks:add --index 1 heroku-community/apt`
    
    ```
    refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz
                https://github.com/NCKU-CCS/TOC-Project-2020
    ```

## state說明
- input_menu: 選擇要看商品優惠資訊或是商品介紹或是健康資訊或是回首頁
- question: 提供Q&A給使用者
- answer: 提供Q&A給使用者 
- menu: 選擇要看商品介紹或是柚心園的菜單
- menu_pic: 顯示柚心園菜單
- show_pomelo_introduction: 介紹柚心園的產品
- input_health_information: 選擇要看吃柚子對身體的好處或是吃柚子的飲食禁忌
- show_pomelo_discount: 公告優惠商品活動
- show_pomelo_benefit: 顯示有關吃柚子對身體的好處的有關網頁
- show_pomelo_taboo: 顯示有關吃柚子的飲食禁忌的網頁

## FSM
![](https://i.imgur.com/j75C7Jo.png?1)

## 使用說明
- 基本操作
    - 隨時輸入任何字若沒觸發到都會有提示
    - 可隨時輸入
        - `回首頁`
            - 回到主選單
        - `fsm`
            - 傳回fsm圖片
- 架構圖
    輸入`柚心園`開始
    - 選擇 `商品資訊`
        - 選擇 `商品優惠資訊`
            - 顯示柚心園商品優惠資訊
        - 選擇 `商品介紹`
            - 顯示柚心園商品的資訊
        - 選擇 `健康資訊`
            - 選擇 `對身體的益處`
                - 顯示吃柚子對身體的益處的網頁連結 
            - 選擇 `飲食禁忌`
                - 顯示吃柚子的飲食禁忌的網頁連結 
        - 選擇 `回首頁`
            - 回到主選單
    - 選擇 `訂購`
        - 顯示購買連結，供顧客使用
    - 選擇 `問答`
        - 顧客可輸入有關柚心園的問題，linebot會依照題庫做分類並回答
    - 選擇 `菜單`
        - 選擇 `商品介紹`
             - 顯示柚心園商品的資訊
        - 選擇 `菜單圖示` 
             - 顯示柚心園菜單圖片
        - 選擇 `回首頁`
             - 回到主選單


## 使用示範
### 主選單
![](https://i.imgur.com/Jxd7Spk.jpg)
#### 商品資訊主選單
![](https://i.imgur.com/t6Wudif.jpg?2)
##### 商品優惠資訊
![](https://i.imgur.com/CM85zrp.jpg?1) 商品優惠資訊
![](https://i.imgur.com/CB171TI.jpg?1) 商品介紹
![](https://i.imgur.com/obkUkHA.jpg?1) 健康資訊
###### 健康資訊
![](https://i.imgur.com/1AjUVV8.jpg?1) 益處
![](https://i.imgur.com/nQLQWzU.jpg?1) 禁忌
#### 訂購
![](https://i.imgur.com/T2uhU5C.jpg?1)
#### 菜單
![](https://i.imgur.com/qSnLGec.jpg?1) 菜單
![](https://i.imgur.com/fFDG9vE.jpg?1) 菜單圖示
![](https://i.imgur.com/CgA2Or8.jpg?1)
#### 問答
![](https://i.imgur.com/MEKoACx.jpg?1) 問
![](https://i.imgur.com/LPS53GG.jpg?1) 答
![](https://i.imgur.com/MTL6T5E.jpg?1) 離開
### 畫FSM
![](https://i.imgur.com/cDU7HbU.jpg?1) 





