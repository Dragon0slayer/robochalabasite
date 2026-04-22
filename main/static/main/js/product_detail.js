document.addEventListener('DOMContentLoaded', function() {
    const quantityInput = document.getElementById('quantity');
    const btnMinus = document.getElementById('btn-minus');
    const btnPlus = document.getElementById('btn-plus');
    const totalPriceElement = document.getElementById('total-price');
    const basePriceElement = document.getElementById('base-price');

    if (!quantityInput || !totalPriceElement || !basePriceElement) return;

    const basePrice = parseFloat(basePriceElement.dataset.price);

    function updatePrice() {
        let quantity = parseInt(quantityInput.value);
        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
            quantityInput.value = 1;
        }
        const total = (basePrice * quantity).toFixed(2);
        totalPriceElement.textContent = total + ' грн';
    }

    if (btnMinus) {
        btnMinus.addEventListener('click', function() {
            let val = parseInt(quantityInput.value);
            if (val > 1) {
                quantityInput.value = val - 1;
                updatePrice();
            }
        });
    }

    if (btnPlus) {
        btnPlus.addEventListener('click', function() {
            let val = parseInt(quantityInput.value);
            quantityInput.value = val + 1;
            updatePrice();
        });
    }

    quantityInput.addEventListener('input', updatePrice);
});
