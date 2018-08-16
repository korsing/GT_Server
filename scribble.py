
#  문제 다 풀었으면 다 풀었다는 링크 보내주기
flag = True # 다 풀었다고 가정
if(variable == 'intro'): # 처음 설문조사에 해당
    query = "SELECT Q10 FROM intro WHERE userid = '" + userid + "';"
    c.execute(query)
    check = c.fetchone()
    if(not check): # 10번 문항에 답이 없다면 다 완성한게 아님
        flag = False
elif(variable == 'thinking'): # 사고력 문제에 해당
    query = "SELECT Q30 FROM intro WHERE userid = '" + userid + "';"
    c.execute(query)
    check = c.fetchone()
    if(not check): # 30번 문항에 답이 없다면 다 완성한게 아님
        flag = False
else: # 엔트리, 파이썬, C언어에 해당
    query = "SELECT Q50 FROM " + variable + " WHERE userid = '" + userid + "';"
    c.execute(query)
    check = c.fetchone()
    if(not check): # 50번 문항에 답이 없다면 다 완성한게 아님
        flag = False
if(flag == True): # 위 3가지 경우 모두 안결렸다면 -> 다 푼거임
    return render_template("/assessments/finished.html")