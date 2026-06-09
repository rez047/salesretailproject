fetch("/cart")
  .then(res => res.json())
  .then(data => {
    let c = document.getElementById("cart");

    if (data.length === 0) {
      c.innerHTML = "<p>Cart is empty</p>";
      return;
    }

    data.forEach(item => {
      let div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <p>Product ID: ${item.product_id}</p>
        <p>Quantity: ${item.quantity}</p>
      `;

      c.appendChild(div);
    });
  });