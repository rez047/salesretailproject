fetch("/products")
  .then(res => res.json())
  .then(data => {
    let container = document.getElementById("products");

    data.forEach(p => {
      let div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <h3>${p.name}</h3>
        <p>Price: $${p.price}</p>
        <p>Stock: ${p.stock}</p>
        <button onclick="addToCart(${p.id})">Add to Cart</button>
      `;

      container.appendChild(div);
    });
  });

function addToCart(id) {
  fetch("/cart/add", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({product_id: id, quantity: 1})
  })
  .then(res => res.json())
  .then(alert);
}