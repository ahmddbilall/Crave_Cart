function openSearchPage() {
    window.location.href = '/search';
}

function logout() {
    window.location.href = '/logout'; 
}

setTimeout(function() {
    var flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        flashMessage.style.display = 'none';
    }
}, 2000);

























var addToCartButtonsPromotion = document.querySelectorAll('.add-to-cart-btn-promortion');

addToCartButtonsPromotion.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var PromotionName = button.getAttribute('data-PromotionName');
        var discount = button.getAttribute('data-discount');
        addToCartPromotionHome(PromotionName, discount);
    });
});

function addToCartPromotionHome(PromotionName, discount) {
    window.location.href = '/handle-Add-to-cart-Promotion-from-home?PromotionName=' + encodeURIComponent(PromotionName) + '&discount=' + encodeURIComponent(discount);
}




var addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

addToCartButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addToCart(itemName, description, price);
    });
});

function addToCart(itemName, description, price) {
    // Implement your logic to add item to cart
    // Here you can make an AJAX request or redirect to a specific URL with item details
    // Example:
    window.location.href = '/handle-Add-to-cart-from-home?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}