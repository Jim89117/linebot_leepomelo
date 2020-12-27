
def nlp_ans(question):
    flag1 = ['產地','地方','販賣','商店','店面','地址','種植地','在哪裡','賣','買']
    flag1_sale = ['賣','買','販賣','商店','店面','地址']
    flag2 = ['口感','水分','酸','肉質','多汁','甜','好吃']
    flag3 = ['放多久','保存多久','有效期限','保存期限','期限']
    flag4 = ['益處','好處','幫助','功效','健康']
    flag5 = ['宅配','貨運','運送','寄','運費']
    flag6 = ['付款','付','付錢','怎麼付費','轉帳','匯款','貨到付款','刷卡','分期付款']
    flag7 = ['農藥']
    ans = ''
    flag = 0
    if flag != 1:
        for text1 in flag1:
            if question.find(text1) >= 0:
                for text1_1 in flag1_sale:
                    if question.find(text1_1) > 0:
                        ans = '歡迎光臨~~柚心園\n我們的店面位於『台南市仁德區 義林六街 119號』\n連絡電話『06-2490341』\n歡迎您前來購賣，也可以採用線上訂購歐，要使用線上訂購，請輸入『訂購』即可前往訂購表單'
                        flag = 1
                if flag != 1:
                    ans = '我們的產地位於台南市的文旦盛產地『麻豆』,是正宗的麻豆老欉文旦'
                    flag = 1
    if flag != 1:
        for text2 in flag2:
            if question.find(text2) >= 0:
                ans = '我說的不準啦!!哪有老闆會不誇讚自己的產品，來~您買一次吃過就知道，保證是肉質鮮嫩多汁，甜而不膩，果粒晶瑩，飽滿的果肉裡滿滿的都是水分，獨特清新的果香絕對讓您難以忘懷的，不甜包退'
                flag = 1
    if flag != 1:
        for text3 in flag3:
            if question.find(text3) >= 0:
                ans = '1.收到後請先將保裝盒打開，置放陰涼處，切勿碰水，待放置7-10天讓文旦消水，果肉變軟變甜會更好吃\n2.文旦本身熟度越高越不易存放，建議存放溫度為20-25度，因糖分越高越容易自然發酵(產生酒味、影響口感)外表略黃，觸摸起來消水，口感甜度較佳，如食用上果肉仍脆甜帶微酸，建議請再存放3-7天。'
                flag = 1
    if flag != 1:
        for text4 in flag4:
            if question.find(text4) >= 0:
                ans = '柚子的好處絕不僅是清熱去火。柚子含有非常豐富的蛋白質、有機酸及鈣、磷、鎂、鈉等人體必需的元素，能夠增強體質\n柚子中的維生素C的含量是檸檬和橙子的3倍。鈣的含量更是比蘋果、梨，香蕉等水果多10倍。長吃有助於防止腸癌和胃癌的發生\n柚子裡面含有一定的柚皮苷，它是一種活性物質，不但可以對血液的粘稠度起到降低的作用，而且還可以減少身體中血栓的可能。經常食用可以預防敗血症和腦血栓，所以老年人應該多吃柚子\n\nhttps://superfit.com.tw/all/eat-grapefruit-to-lose-weight/\nhttps://yesser99.pixnet.net/blog/post/371682337\nhttps://kknews.cc/culture/'
                flag = 1
    if flag != 1:
        for text5 in flag5:
            if question.find(text5) >= 0:
                ans = '您好\n我們可以全島配送哦!!\n一箱宅配費用統一$100/箱'
                flag = 1
    if flag != 1:
        for text6 in flag6:
            if question.find(text6) >= 0:
                ans = '您好\n付款方式可以\n1.直接面交\n轉帳的方式:帳號:XXOOXXOOXXOOXXOO'
                flag = 1 
    if flag != 1:
        for text7 in flag7:
            if question.find(text7) >= 0:
                ans = '您好\n由於為了防範蚊蟲叮咬，導致整顆柚子毀損，所以我們有噴灑農藥，但我們都會依據政府規定在採收前的規定時間內不噴灑農藥，所以不用擔心農藥殘留的問題。'
                flag = 1               
    if flag == 0:
        ans = '很抱歉，我不知道要怎麼回答您，因為我的設計者太笨，請您再換個問法~ 拜託'
    return ans
    
