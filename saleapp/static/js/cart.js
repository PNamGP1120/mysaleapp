function addToCart(id, name, price) {
    event.preventDefault();

    fetch(`/api/add-cart`, {
        method: 'POST',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector('.badge').textContent = data.count;
            alert('Product added to cart successfully!');
        } else {
            alert('Failed to add product to cart.');
        }
    })
    .catch(error => console.error('Error:', error));
}