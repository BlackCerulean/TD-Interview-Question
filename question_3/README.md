# Question 3 SQL & Data Contract

Problems: Please write SQL to extract the product names and product classes for the top 2 sales for each product class in our product universe, ordered by 
class and then by sales. If there are any tie breakers, use the lower quantity to break the tie.

Description: This query is used for mocking this problem situation. I started by joining the table together and group them to find a total sales value of each product, then rank them base on their sales with tie breaker condition being the lower quantity will ranked higher.