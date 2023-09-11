examples = """
# 我有肺炎。
MATCH (u:User {id: $userId})
MERGE (u)-[:has_disease]->(:Disease {name: "肺炎"})
RETURN distinct {answer: '已註冊'} AS result
# 肺炎的症狀是什麼？
MATCH (d:Disease {name:"肺炎"})-[:has_symptom]->(s:Symptom)
RETURN {symptom: s.name} AS result
# 我最近感到呼吸困難，這可能是由什麼疾病引起的呢？
MATCH (u:User {id: $userId})-[:has_symptom]->(s:Symptom {name: "呼吸困難"})
MATCH (d:Disease)-[:has_symptom]->(s)
WHERE NOT (u)-[:has_disease]->(d)
RETURN {disease: d.name} AS result
# 最近一直流鼻涕怎麼辦？
MATCH (s:Symptom {name: "流鼻涕"})<-[:has_symptom]-(d:Disease)
RETURN {disease: d.name} AS result
# 肝病要吃甚麼藥？
MATCH (d:Disease {name: "肝病"})-[:recommand_drug]->(d2:Drug)
RETURN {Drug: d2.name} AS result
# 為什麼有的人會失眠？
MATCH (d:Disease {name: "失眠"})
RETURN {cause:d.cause} AS result
# 失眠有哪些併發症？
MATCH (d:Disease {name: "失眠"})-[:acompany_with]->(d2:Disease)
RETURN {comorbidity: d2.name} AS result
# 失眠的人不要吃啥？
MATCH (d:Disease {name: "失眠"})-[:no_eat]->(food:Food)
RETURN {avoid_food: food.name} AS result
# 耳鳴的話吃甚麼可以改善？
MATCH (s:Disease {name: "耳鳴"})-[:do_eat]->(f1:Food)
MATCH (s:Disease {name: "耳鳴"})-[:recommand_eat]->(f2:Food)
RETURN {do_eat: f1.name, recommand_eat: f2.name} AS result
# 板藍根顆粒能治甚麼病？
MATCH (drug:Drug {name: "板藍根顆粒"})<-[:recommand_drug]-(d:Disease)
RETURN {cures_disease: d.name} AS result
# 腦膜炎怎麼才能查出來？
MATCH (d:Disease {name: "腦膜炎"})-[:need_check]->(check:Check)
RETURN {diagnostic_test: check.name} AS result
# 全血細胞計數能查出啥來？
MATCH (check:Check {name: "全血細胞計數"})<-[:need_check]-(d:Disease)
RETURN {detects_disease: d.name} AS result
# 如何預防腎虛？
MATCH (d:Disease {name: "腎虛"})
RETURN {prevention: d.prevent} AS result
# 感冒要多久才能好？
MATCH (d:Disease {name: "感冒"})
RETURN {recovery_time: d.cure_lasttime} AS result
# 高血壓要怎麼治？
MATCH (d:Disease {name: "高血壓"})
RETURN {treatment: d.cure_way} AS result
# 白血病能治好嗎？
MATCH (d:Disease {name: "白血病"})
RETURN {cure_probability: d.cured_prob} AS result
# 什麼人容易得高血壓？
MATCH (d:Disease {name: "高血壓"})
RETURN {risk_factors: d.easy_get} AS result
"""
