<!DOCTYPE html>
<html>
<head>
    <title>My Orders</title>
</head>

<body>

<h2>My Order History</h2>

<a href="/buyer">← Back to Shop</a>

<table border="1">
    <tr>
        <th>Order ID</th>
        <th>Product</th>
        <th>Price</th>
        <th>Quantity</th>
        <th>Total</th>
        <th>Status</th>
    </tr>

    {% for order in orders %}
    <tr>
        <td>{{ order.id }}</td>
        <td>{{ order.product.name }}</td>
        <td>{{ order.product.price }}</td>
        <td>{{ order.quantity }}</td>
        <td>{{ order.total_price }}</td>
        <td>{{ order.status }}</td>
    </tr>
    {% endfor %}

</table>

</body>
</html>
