--товары из определенного списка
SELECT p."name", stp.amount, p.unit  FROM product p 
JOIN sl_temptale_product stp ON p.id = stp.product_id 
JOIN sl_template st ON st.id = stp.sl_template_id
WHERE st."name" = 'гости'

--все продукты за определенную дату, которые не попали ни в один список покупок
-- все продукты со пн по пт вне списка покупок(изменения только в условии)

SELECT pp.id, pp.date, p.name, pp.amount  FROM product p 
JOIN purchased_products pp ON p.id = pp.product_id 
WHERE '2023-08-02'<= pp."date" AND pp.date < '2023-08-04' AND pp.shopping_list_id is NULL
ORDER BY p.name

-- в какой магазин пойти чтобы купить все из списка покупок
SELECT sq.count, s.name FROM shop s
JOIN 
(SELECT count(*),ps.shop_id  FROM shopping_list_product slp
FULL JOIN product_shop ps ON slp.product_id = ps.product_id
WHERE slp.shopping_list_id ='5'
GROUP BY ps.shop_id 
HAVING count(*)=
(SELECT count(*) FROM shopping_list_product 
WHERE shopping_list_id = '5'))
AS sq ON s.id = sq.shop_id